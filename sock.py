import os
import sys
import json
import socket


HOST = socket.gethostbyname(socket.gethostname())
PORT = int(os.getenv('port') or 5348)
ENCODING = sys.getdefaultencoding()
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CON: socket.socket = None
ADDRESS: tuple = None


def set_port(new_port: int) -> None:
    global PORT
    PORT = new_port


def set_host(new_host: str) -> None:
    global HOST
    HOST = new_host


def init() -> None:
    os.environ['host'] = HOST
    os.environ['port'] = str(PORT)
    print(f'Started at {HOST}:{PORT}.')
    SOCKET.bind((HOST, PORT))
    SOCKET.listen(1)


def wait_for_connection() -> None:
    global CON, ADDRESS
    CON, ADDRESS = SOCKET.accept()


def quit() -> None:
    CON.close()
    SOCKET.close()


def encode_message(msg_: dict) -> bytes:
    return json.dumps(msg_).encode(ENCODING)


def decode_message(msg_: bytes) -> dict:
    return json.loads(msg_.decode(ENCODING))


def get_msg_length(ten_bytes: bytes) -> int:
    return int(ten_bytes.decode(ENCODING).strip())


def send_msg(msg_: dict) -> None:
    CON.send(encode_message(msg_))


def get_msg() -> dict:
    return decode_message(CON.recv(get_msg_length(CON.recv(10))))
