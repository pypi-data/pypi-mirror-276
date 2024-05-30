# Copyright 2021 The Pigweed Authors
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""Console for interacting with devices using HDLC.

To start the console, provide a serial port as the --device argument and paths
or globs for .proto files that define the RPC services to support:

  python -m pw_system.console --device /dev/ttyUSB0 --proto-globs pw_rpc/echo.proto

This starts an IPython console for communicating with the connected device. A
few variables are predefined in the interactive console. These include:

    rpcs   - used to invoke RPCs
    device - the serial device used for communication
    client - the pw_rpc.Client
    protos - protocol buffer messages indexed by proto package

An example echo RPC command:

  rpcs.pw.rpc.EchoService.Echo(msg="hello!")
"""  # pylint: disable=line-too-long

import argparse
import datetime
import glob
from inspect import cleandoc
import logging
from pathlib import Path
import sys
import time
from types import ModuleType
from typing import (
    Any,
    Collection,
    Iterable,
    Iterator,
)

import serial
import IPython  # type: ignore

from pw_cli import log as pw_cli_log
from pw_console import embed
from pw_console import log_store
from pw_console.plugins import bandwidth_toolbar
from pw_console import pyserial_wrapper
from pw_console import python_logging
from pw_console import socket_client
from pw_hdlc import rpc
from pw_rpc.console_tools.console import flattened_rpc_completions
from pw_system import device as pw_device
from pw_system import device_tracing
from pw_tokenizer import detokenize

# Default proto imports:
from pw_log.proto import log_pb2
from pw_metric_proto import metric_service_pb2
from pw_thread_protos import thread_snapshot_service_pb2
from pw_unit_test_proto import unit_test_pb2
from pw_file import file_pb2
from pw_trace_protos import trace_service_pb2
from pw_transfer import transfer_pb2

_LOG = logging.getLogger('tools')
_DEVICE_LOG = logging.getLogger('rpc_device')
_SERIAL_DEBUG = logging.getLogger('pw_console.serial_debug_logger')
_ROOT_LOG = logging.getLogger()

MKFIFO_MODE = 0o666


def get_parser() -> argparse.ArgumentParser:
    """Gets argument parser with console arguments."""

    parser = argparse.ArgumentParser(
        prog="python -m pw_system.console", description=__doc__
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', '--device', help='the serial port to use')
    parser.add_argument(
        '-b',
        '--baudrate',
        type=int,
        default=115200,
        help='the baud rate to use',
    )
    parser.add_argument(
        '--serial-debug',
        action='store_true',
        help=(
            'Enable debug log tracing of all data passed through'
            'pyserial read and write.'
        ),
    )
    parser.add_argument(
        '-o',
        '--output',
        type=argparse.FileType('wb'),
        default=sys.stdout.buffer,
        help=(
            'The file to which to write device output (HDLC channel 1); '
            'provide - or omit for stdout.'
        ),
    )

    # Log file options
    parser.add_argument(
        '--logfile',
        default='pw_console-logs.txt',
        help=(
            'Default log file. This will contain host side '
            'log messages only unles the '
            '--merge-device-and-host-logs argument is used.'
        ),
    )

    parser.add_argument(
        '--merge-device-and-host-logs',
        action='store_true',
        help=(
            'Include device logs in the default --logfile.'
            'These are normally shown in a separate device '
            'only log file.'
        ),
    )

    parser.add_argument(
        '--host-logfile',
        help=(
            'Additional host only log file. Normally all logs in the '
            'default logfile are host only.'
        ),
    )

    parser.add_argument(
        '--device-logfile',
        default='pw_console-device-logs.txt',
        help='Device only log file.',
    )

    parser.add_argument(
        '--json-logfile', help='Device only JSON formatted log file.'
    )

    group.add_argument(
        '-s',
        '--socket-addr',
        type=str,
        help=(
            'Socket address used to connect to server. Type "default" to use '
            'localhost:33000, pass the server address and port as '
            'address:port, or prefix the path to a forwarded socket with '
            f'"{socket_client.SocketClient.FILE_SOCKET_SERVER}:" as '
            f'{socket_client.SocketClient.FILE_SOCKET_SERVER}:path_to_file.'
        ),
    )
    parser.add_argument(
        "--token-databases",
        metavar='elf_or_token_database',
        nargs="+",
        type=Path,
        help="Path to tokenizer database csv file(s).",
    )
    parser.add_argument(
        '--config-file',
        type=Path,
        help='Path to a pw_console yaml config file.',
    )
    parser.add_argument(
        '--proto-globs',
        nargs='+',
        default=[],
        help='glob pattern for .proto files.',
    )
    parser.add_argument(
        '-f',
        '--ticks_per_second',
        type=int,
        dest='ticks_per_second',
        help=('The clock rate of the trace events.'),
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Enables debug logging when set.',
    )
    parser.add_argument(
        '--ipython',
        action='store_true',
        dest='use_ipython',
        help='Use IPython instead of pw_console.',
    )

    parser.add_argument(
        '--rpc-logging',
        action=argparse.BooleanOptionalAction,
        default=True,
        help='Use pw_rpc based logging.',
    )

    parser.add_argument(
        '--hdlc-encoding',
        action=argparse.BooleanOptionalAction,
        default=True,
        help='Use HDLC encoding on transfer interfaces.',
    )

    parser.add_argument(
        '--channel-id',
        type=int,
        default=rpc.DEFAULT_CHANNEL_ID,
        help="Channel ID used in RPC communications.",
    )

    return parser


def _parse_args(args: argparse.Namespace | None = None):
    """Parses and returns the command line arguments."""
    if args is not None:
        return args

    parser = get_parser()
    return parser.parse_args()


def _expand_globs(globs: Iterable[str]) -> Iterator[Path]:
    for pattern in globs:
        for file in glob.glob(pattern, recursive=True):
            yield Path(file)


def _start_python_terminal(  # pylint: disable=too-many-arguments
    device: pw_device.Device,
    device_log_store: log_store.LogStore,
    root_log_store: log_store.LogStore,
    serial_debug_log_store: log_store.LogStore,
    log_file: str,
    host_logfile: str,
    device_logfile: str,
    json_logfile: str,
    serial_debug: bool = False,
    config_file_path: Path | None = None,
    use_ipython: bool = False,
) -> None:
    """Starts an interactive Python terminal with preset variables."""
    local_variables = dict(
        client=device.client,
        device=device,
        rpcs=device.rpcs,
        protos=device.client.protos.packages,
        # Include the active pane logger for creating logs in the repl.
        DEVICE_LOG=_DEVICE_LOG,
        LOG=logging.getLogger(),
    )

    welcome_message = cleandoc(
        """
        Welcome to the Pigweed Console!

        Help: Press F1 or click the [Help] menu
        To move focus: Press Shift-Tab or click on a window

        Example Python commands:

          device.rpcs.pw.rpc.EchoService.Echo(msg='hello!')
          LOG.warning('Message appears in Host Logs window.')
          DEVICE_LOG.warning('Message appears in Device Logs window.')
    """
    )

    welcome_message += '\n\nLogs are being saved to:\n  ' + log_file
    if host_logfile:
        welcome_message += '\nHost logs are being saved to:\n  ' + host_logfile
    if device_logfile:
        welcome_message += (
            '\nDevice logs are being saved to:\n  ' + device_logfile
        )
    if json_logfile:
        welcome_message += (
            '\nJSON device logs are being saved to:\n  ' + json_logfile
        )

    if use_ipython:
        print(welcome_message)
        IPython.start_ipython(
            argv=[],
            display_banner=False,
            user_ns=local_variables,
        )
        return

    client_info = device.info()
    completions = flattened_rpc_completions([client_info])

    log_windows: dict[str, list[logging.Logger] | log_store.LogStore] = {
        'Device Logs': device_log_store,
        'Host Logs': root_log_store,
    }
    if serial_debug:
        log_windows['Serial Debug'] = serial_debug_log_store

    interactive_console = embed.PwConsoleEmbed(
        global_vars=local_variables,
        local_vars=None,
        loggers=log_windows,
        repl_startup_message=welcome_message,
        help_text=__doc__,
        config_file_path=config_file_path,
    )
    interactive_console.add_sentence_completer(completions)
    if serial_debug:
        interactive_console.add_bottom_toolbar(
            bandwidth_toolbar.BandwidthToolbar()
        )

    # Setup Python logger propagation
    interactive_console.setup_python_logging(
        # Send any unhandled log messages to the external file.
        last_resort_filename=log_file,
        # Don't change propagation for these loggers.
        loggers_with_no_propagation=[_DEVICE_LOG],
    )

    interactive_console.embed()


# pylint: disable=too-many-arguments,too-many-locals
def console(
    device: str,
    baudrate: int,
    proto_globs: Collection[str],
    ticks_per_second: int | None,
    token_databases: Collection[Path],
    socket_addr: str,
    logfile: str,
    host_logfile: str,
    device_logfile: str,
    json_logfile: str,
    output: Any,
    serial_debug: bool = False,
    config_file: Path | None = None,
    verbose: bool = False,
    compiled_protos: list[ModuleType] | None = None,
    merge_device_and_host_logs: bool = False,
    rpc_logging: bool = True,
    use_ipython: bool = False,
    channel_id: int = rpc.DEFAULT_CHANNEL_ID,
    hdlc_encoding: bool = True,
) -> int:
    """Starts an interactive RPC console for HDLC."""
    # argparse.FileType doesn't correctly handle '-' for binary files.
    if output is sys.stdout:
        output = sys.stdout.buffer

    # Don't send device logs to the root logger.
    _DEVICE_LOG.propagate = False
    # Create pw_console log_store.LogStore handlers. These are the data source
    # for log messages to be displayed in the UI.
    device_log_store = log_store.LogStore()
    root_log_store = log_store.LogStore()
    serial_debug_log_store = log_store.LogStore()
    # Attach the log_store.LogStores as handlers for each log window we want to
    # show. This should be done before device initialization to capture early
    # messages.
    _DEVICE_LOG.addHandler(device_log_store)
    _ROOT_LOG.addHandler(root_log_store)
    _SERIAL_DEBUG.addHandler(serial_debug_log_store)

    if not logfile:
        # Create a temp logfile to prevent logs from appearing over stdout. This
        # would corrupt the prompt toolkit UI.
        logfile = python_logging.create_temp_log_file()

    log_level = logging.DEBUG if verbose else logging.INFO

    pw_cli_log.install(
        level=log_level, use_color=False, hide_timestamp=False, log_file=logfile
    )

    if device_logfile:
        pw_cli_log.install(
            level=log_level,
            use_color=False,
            hide_timestamp=False,
            log_file=device_logfile,
            logger=_DEVICE_LOG,
        )
    if host_logfile:
        pw_cli_log.install(
            level=log_level,
            use_color=False,
            hide_timestamp=False,
            log_file=host_logfile,
            logger=_ROOT_LOG,
        )

    if merge_device_and_host_logs:
        # Add device logs to the default logfile.
        pw_cli_log.install(
            level=log_level,
            use_color=False,
            hide_timestamp=False,
            log_file=logfile,
            logger=_DEVICE_LOG,
        )

    _LOG.setLevel(log_level)
    _DEVICE_LOG.setLevel(log_level)
    _ROOT_LOG.setLevel(log_level)
    _SERIAL_DEBUG.setLevel(logging.DEBUG)

    if json_logfile:
        json_filehandler = logging.FileHandler(json_logfile, encoding='utf-8')
        json_filehandler.setLevel(log_level)
        json_filehandler.setFormatter(python_logging.JsonLogFormatter())
        _DEVICE_LOG.addHandler(json_filehandler)

    detokenizer = None
    if token_databases:
        token_databases_with_domains = [] * len(token_databases)
        for token_database in token_databases:
            # Load all domains from token database.
            token_databases_with_domains.append(str(token_database) + "#.*")

        detokenizer = detokenize.AutoUpdatingDetokenizer(
            *token_databases_with_domains
        )
        detokenizer.show_errors = True

    protos: list[ModuleType | Path] = list(_expand_globs(proto_globs))

    if compiled_protos is None:
        compiled_protos = []

    # Append compiled log.proto library to avoid include errors when manually
    # provided, and shadowing errors due to ordering when the default global
    # search path is used.
    if rpc_logging:
        compiled_protos.append(log_pb2)
    compiled_protos.append(unit_test_pb2)
    protos.extend(compiled_protos)
    protos.append(metric_service_pb2)
    protos.append(thread_snapshot_service_pb2)
    protos.append(file_pb2)
    protos.append(trace_service_pb2)
    protos.append(transfer_pb2)

    if not protos:
        _LOG.critical(
            'No .proto files were found with %s', ', '.join(proto_globs)
        )
        _LOG.critical('At least one .proto file is required')
        return 1

    _LOG.debug(
        'Found %d .proto files found with %s',
        len(protos),
        ', '.join(proto_globs),
    )

    timestamp_decoder = None
    if socket_addr is None:
        serial_impl = (
            pyserial_wrapper.SerialWithLogging
            if serial_debug
            else serial.Serial
        )
        serial_device = serial_impl(
            device,
            baudrate,
            # Timeout in seconds. This should be a very small value. Setting to
            # zero makes pyserial read() non-blocking which will cause the host
            # machine to busy loop and 100% CPU usage.
            # https://pythonhosted.org/pyserial/pyserial_api.html#serial.Serial
            timeout=0.1,
        )
        reader = rpc.SerialReader(serial_device, 8192)
        write = serial_device.write

        # Overwrite decoder for serial device.
        def milliseconds_to_string(timestamp):
            """Parses milliseconds since boot to a human-readable string."""
            return str(datetime.timedelta(seconds=timestamp / 1e3))[:-3]

        timestamp_decoder = milliseconds_to_string
    else:
        socket_impl = (
            socket_client.SocketClientWithLogging
            if serial_debug
            else socket_client.SocketClient
        )

        def disconnect_handler(
            socket_device: socket_client.SocketClient,
        ) -> None:
            """Attempts to reconnect on disconnected socket."""
            _LOG.error('Socket disconnected. Will retry to connect.')
            while True:
                try:
                    socket_device.connect()
                    break
                except:  # pylint: disable=bare-except
                    # Ignore errors and retry to reconnect.
                    time.sleep(1)
            _LOG.info('Successfully reconnected')

        try:
            socket_device = socket_impl(
                socket_addr, on_disconnect=disconnect_handler
            )
            reader = rpc.SelectableReader(socket_device)
            write = socket_device.write
        except ValueError:
            _LOG.exception('Failed to initialize socket at %s', socket_addr)
            return 1

    with reader:
        device_client = device_tracing.DeviceWithTracing(
            channel_id,
            reader,
            write,
            proto_library=protos,
            detokenizer=detokenizer,
            timestamp_decoder=timestamp_decoder,
            rpc_timeout_s=5,
            use_rpc_logging=rpc_logging,
            use_hdlc_encoding=hdlc_encoding,
            ticks_per_second=ticks_per_second,
        )
        with device_client:
            _start_python_terminal(
                device=device_client,
                device_log_store=device_log_store,
                root_log_store=root_log_store,
                serial_debug_log_store=serial_debug_log_store,
                log_file=logfile,
                host_logfile=host_logfile,
                device_logfile=device_logfile,
                json_logfile=json_logfile,
                serial_debug=serial_debug,
                config_file_path=config_file,
                use_ipython=use_ipython,
            )
    return 0


def main(args: argparse.Namespace | None = None) -> int:
    return console(**vars(_parse_args(args)))


def main_with_compiled_protos(
    compiled_protos, args: argparse.Namespace | None = None
):
    return console(**vars(_parse_args(args)), compiled_protos=compiled_protos)


if __name__ == '__main__':
    sys.exit(main())
