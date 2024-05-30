import asyncio
import functools
import json
from pathlib import Path
from threading import Thread
import time
import websockets

from pw_console.console_log_server import (
    ConsoleLogHTTPRequestHandler,
    pw_console_http_server,
)

_PW_CONSOLE_MODULE = 'pw_console'

html_files = {
    '/{}'.format(t.name): t.read_text()
    for t in Path(__file__).parent.iterdir()
    if t.suffix in ['.css', '.html', '.js', '.json']
}


def _http_server_entry() -> None:
    handler = functools.partial(ConsoleLogHTTPRequestHandler, html_files)
    pw_console_http_server(3000, handler)


sample_logfiles = sorted(list(Path(__file__).parent.glob('*logs.json')))

websocket_server = None
websocket_port = None
websocket_loop = asyncio.new_event_loop()


async def _send_logs_over_websockets(websocket, _path) -> None:
    log_file = sample_logfiles[0].read_text()

    log_lines = list(log_file.splitlines())

    start_time = time.time()
    index = 0

    beginning_log_time = float(json.loads(log_lines[index])['time'])
    current_log_line = json.loads(log_lines[index])
    current_log_time = float(current_log_line['time'])

    while True:
        # if index >= 50:
        #     return
        delta_time = (time.time() - start_time) * 0.5
        if delta_time > (current_log_time - beginning_log_time):
            await websocket.send(log_lines[index])
            index += 1
            if index >= len(log_lines):
                # Restart from the beginning
                index = 0
                beginning_log_time = float(json.loads(log_lines[index])['time'])
            current_log_line = json.loads(log_lines[index])
            current_log_time = float(current_log_line['time'])
        else:
            await asyncio.sleep(0.1)


def _websocket_thread_entry():
    asyncio.set_event_loop(websocket_loop)
    websocket_server = websockets.serve(  # type: ignore # pylint: disable=no-member
        _send_logs_over_websockets, '127.0.0.1'
    )
    websocket_loop.run_until_complete(websocket_server)
    websocket_port = websocket_server.ws_server.sockets[0].getsockname()[1]
    websocket_running = True
    print(f'Serving on:\nhttp://127.0.0.1:3000/#ws={websocket_port}')

    websocket_loop.run_forever()


def main() -> None:
    if not sample_logfiles:
        print('ERROR: No files exist named *logs.json')

    print(f'Replaying: {sample_logfiles[0]}')

    server_thread = Thread(target=_http_server_entry, args=(), daemon=True)
    server_thread.start()

    websocket_thread = Thread(
        target=_websocket_thread_entry, args=(), daemon=True
    )
    websocket_thread.start()
    s = input('Press enter to quit.\n')


if __name__ == '__main__':
    main()
