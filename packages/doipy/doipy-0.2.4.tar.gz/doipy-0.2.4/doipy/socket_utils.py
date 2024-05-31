from contextlib import contextmanager
import socket
import ssl
import json

from doipy.config import settings


@contextmanager
def create_socket():
    # create context object to configure socket
    # negotiate protocol between client and server
    ssl_settings = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    # do not match peer certificates hostname
    ssl_settings.check_hostname = False
    # do not try to verify other peer's certificates
    ssl_settings.verify_mode = ssl.CERT_NONE

    # create SSL socket
    # create a new socket given address family and socket type
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # wrap sock and return an SSL socket (ssl_sock) that is tied to the context
        with ssl_settings.wrap_socket(sock) as ssl_sock:
            # connect to a remote socket at address
            ssl_sock.connect((settings.ip, settings.port))
            yield ssl_sock


def send_message(message, ssl_sock):
    """Send a message to the server via ssl_sock without segment separator."""
    data = json.dumps(message).encode(encoding='UTF-8', errors='ignore')
    ssl_sock.send(data)


def send_server_message(message, conn):
    data = (json.dumps(message) + '\n').encode(encoding='UTF-8', errors='ignore')
    conn.send(data)
    conn.send(b'\n#\n')
    conn.send(b'#\n')


def finalize_segment(ssl_sock):
    """Finalize the current segment with separator \n#\n"""
    ssl_sock.send(b'\n#\n')


def finalize_socket(ssl_sock):
    """Finalize the current message with separator #/n"""
    ssl_sock.send(b'#\n')


def read_response(ssl_sock):
    """Read and store the response from the server"""
    recv_message = ''
    resp_list = []
    byte_size = 1024

    while True:
        # read from buffer and save message
        received = ssl_sock.recv(byte_size)

        # end of segment
        if received == b'\n#\n':
            recv_message = json.loads(recv_message)
            resp_list.append(recv_message)
            received = ssl_sock.recv(byte_size)
            # end of response
            if received == b'#\n':
                return resp_list
            # read beginning of next segment
            recv_message = ''
            continue

        # concatenate messages
        recv_message += received.decode()
