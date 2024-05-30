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
"""Device classes to interact with targets via RPC."""

import logging
from pathlib import Path
from types import ModuleType
from typing import Any, Callable

from pw_thread_protos import thread_pb2
from pw_hdlc import rpc
from pw_log import log_decoder
from pw_log_rpc import rpc_log_stream
from pw_metric import metric_parser
import pw_rpc
from pw_rpc import callback_client, console_tools
from pw_thread import thread_analyzer
from pw_tokenizer import detokenize
from pw_tokenizer.proto import decode_optionally_tokenized
from pw_unit_test.rpc import run_tests as pw_unit_test_run_tests, TestRecord

# Internal log for troubleshooting this tool (the console).
_LOG = logging.getLogger('tools')
DEFAULT_DEVICE_LOGGER = logging.getLogger('rpc_device')


# pylint: disable=too-many-arguments
class Device:
    """Represents an RPC Client for a device running a Pigweed target.

    The target must have and RPC support, RPC logging.
    Note: use this class as a base for specialized device representations.
    """

    def __init__(
        self,
        channel_id: int,
        reader: rpc.CancellableReader,
        write,
        proto_library: list[ModuleType | Path],
        detokenizer: detokenize.Detokenizer | None = None,
        timestamp_decoder: Callable[[int], str] | None = None,
        rpc_timeout_s: float = 5,
        use_rpc_logging: bool = True,
        use_hdlc_encoding: bool = True,
        logger: logging.Logger | logging.LoggerAdapter = DEFAULT_DEVICE_LOGGER,
    ):
        self.channel_id = channel_id
        self.protos = proto_library
        self.detokenizer = detokenizer
        self.rpc_timeout_s = rpc_timeout_s

        self.logger = logger
        self.logger.setLevel(logging.DEBUG)  # Allow all device logs through.

        callback_client_impl = callback_client.Impl(
            default_unary_timeout_s=self.rpc_timeout_s,
            default_stream_timeout_s=None,
        )

        def detokenize_and_log_output(data: bytes, _detokenizer=None):
            log_messages = data.decode(
                encoding='utf-8', errors='surrogateescape'
            )

            if self.detokenizer:
                log_messages = decode_optionally_tokenized(
                    self.detokenizer, data
                )

            for line in log_messages.splitlines():
                self.logger.info(line)

        self.client: rpc.RpcClient
        if use_hdlc_encoding:
            channels = [
                pw_rpc.Channel(self.channel_id, rpc.channel_output(write))
            ]
            self.client = rpc.HdlcRpcClient(
                reader,
                self.protos,
                channels,
                detokenize_and_log_output,
                client_impl=callback_client_impl,
            )
        else:
            channel = pw_rpc.Channel(self.channel_id, write)
            self.client = rpc.NoEncodingSingleChannelRpcClient(
                reader,
                self.protos,
                channel,
                client_impl=callback_client_impl,
            )

        if use_rpc_logging:
            # Create the log decoder used by the LogStreamHandler.

            def decoded_log_handler(log: log_decoder.Log) -> None:
                log_decoder.log_decoded_log(log, self.logger)

            self._log_decoder = log_decoder.LogStreamDecoder(
                decoded_log_handler=decoded_log_handler,
                detokenizer=self.detokenizer,
                source_name='RpcDevice',
                timestamp_parser=(
                    timestamp_decoder
                    if timestamp_decoder
                    else log_decoder.timestamp_parser_ns_since_boot
                ),
            )

            # Start listening to logs as soon as possible.
            self.log_stream_handler = rpc_log_stream.LogStreamHandler(
                self.rpcs, self._log_decoder
            )
            self.log_stream_handler.listen_to_logs()

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()

    def close(self) -> None:
        self.client.close()

    def info(self) -> console_tools.ClientInfo:
        return console_tools.ClientInfo('device', self.rpcs, self.client.client)

    @property
    def rpcs(self) -> Any:
        """Returns an object for accessing services on the specified channel."""
        return next(iter(self.client.client.channels())).rpcs

    def run_tests(self, timeout_s: float | None = 5) -> TestRecord:
        """Runs the unit tests on this device."""
        return pw_unit_test_run_tests(self.rpcs, timeout_s=timeout_s)

    def get_and_log_metrics(self) -> dict:
        """Retrieves the parsed metrics and logs them to the console."""
        metrics = metric_parser.parse_metrics(
            self.rpcs, self.detokenizer, self.rpc_timeout_s
        )

        def print_metrics(metrics, path):
            """Traverses dictionaries, until a non-dict value is reached."""
            for path_name, metric in metrics.items():
                if isinstance(metric, dict):
                    print_metrics(metric, path + '/' + path_name)
                else:
                    _LOG.info('%s/%s: %s', path, path_name, str(metric))

        print_metrics(metrics, '')
        return metrics

    def snapshot_peak_stack_usage(self, thread_name: str | None = None):
        snapshot_service = self.rpcs.pw.thread.proto.ThreadSnapshotService
        _, rsp = snapshot_service.GetPeakStackUsage(name=thread_name)

        thread_info = thread_pb2.SnapshotThreadInfo()
        for thread_info_block in rsp:
            for thread in thread_info_block.threads:
                thread_info.threads.append(thread)
        for line in str(
            thread_analyzer.ThreadSnapshotAnalyzer(thread_info)
        ).splitlines():
            _LOG.info('%s', line)
