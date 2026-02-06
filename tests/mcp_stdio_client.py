#!/usr/bin/env python3
"""Simple MCP stdio test client.

Run from project root after activating venv:

    python tests/mcp_stdio_client.py

It launches your server subprocess and sends an `initialize` message then a `call_tool`
request for the `calculate` tool. It prints responses from the server.

Adjust `PYTHON_BIN` and `CWD` if needed.
"""
import subprocess
import json
import os
import sys
import threading
import select

PYTHON_BIN = os.path.expanduser("/Users/asadvp/My-MCP-Server/venv/bin/python")
CWD = os.path.expanduser("/Users/asadvp/My-MCP-Server")

def send_message(proc, message_obj):
    body = json.dumps(message_obj, separators=(',', ':')).encode('utf-8')
    # LSP framing: Content-Length header + empty line + body
    header = f"Content-Length: {len(body)}\r\n\r\n".encode('ascii')
    full_message = header + body
    proc.stdin.write(full_message)
    proc.stdin.flush()
    print(f"[debug] sent {len(full_message)} bytes")

def read_response(proc):
    # Read headers
    headers = b""
    while True:
        line = proc.stdout.readline()
        if not line:
            return None
        headers += line
        if headers.endswith(b"\r\n\r\n") or headers.endswith(b"\n\n"):
            break
    # Parse Content-Length
    header_text = headers.decode('ascii', errors='ignore')
    length = 0
    for h in header_text.splitlines():
        if h.lower().startswith('content-length:'):
            length = int(h.split(':',1)[1].strip())
            break
    if length <= 0:
        return None
    # wait for data with timeout to avoid hanging indefinitely
    ready, _, _ = select.select([proc.stdout], [], [], 10)
    if not ready:
        return None
    body = proc.stdout.read(length)
    try:
        return json.loads(body)
    except Exception:
        return body.decode('utf-8', errors='ignore')

def main():
    cmd = [PYTHON_BIN, '-m', 'src.main']
    proc = subprocess.Popen(
        cmd,
        cwd=CWD,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    def _read_stderr(p):
        for line in iter(p.stderr.readline, b''):
            try:
                sys.stderr.write('[server-stderr] ' + line.decode('utf-8', errors='ignore'))
                sys.stderr.flush()
            except Exception:
                pass

    t = threading.Thread(target=_read_stderr, args=(proc,), daemon=True)
    t.start()

    try:
        # send initialize
        init = {
            'jsonrpc': '2.0',
            'id': 0,
            'method': 'initialize',
            'params': {
                'protocolVersion': '2025-06-18',
                'capabilities': {},
                'clientInfo': {'name': 'mcp-test-client', 'version': '0.1.0'}
            }
        }
        print('-> sending initialize')
        send_message(proc, init)
        resp = read_response(proc)
        print('<- response:', resp)

        # send a tool call for the calculate tool
        call = {
            'jsonrpc': '2.0',
            'id': 2,
            'method': 'call_tool',
            'params': {
                'name': 'calculate',
                'arguments': {'operation': 'add', 'a': 10, 'b': 5}
            }
        }
        print('-> sending call_tool (calculate 10 + 5)')
        send_message(proc, call)
        resp = read_response(proc)
        print('<- response:', json.dumps(resp, indent=2))

    finally:
        try:
            proc.kill()
        except Exception:
            pass

if __name__ == '__main__':
    main()
