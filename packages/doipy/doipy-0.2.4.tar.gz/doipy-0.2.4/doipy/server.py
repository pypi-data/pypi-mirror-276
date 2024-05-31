import json
import socket
import ssl

from rich import print

from doipy.socket_utils import send_server_message


def server(hostname: str, port: int, privkey: str, cert: str):
    context = ssl.create_default_context()

    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            print(ssock.version())

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(cert, privkey)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind(('127.0.0.1', port))
        sock.listen(5)
        with context.wrap_socket(sock, server_side=True) as ssock:
            print('Wait for connection')
            while True:
                conn, addr = ssock.accept()
                print('Connected by', addr)
                request = json.loads(conn.recv(8192))
                print(request)
                # data2 = conn.recv(8192)
                if request['operationId'] == '0.DOIP/Op.Hello':
                    doip_hello(conn, port)
                elif request['operationId'] == '0.DOIP/Op.ListOperations':
                    doip_list_operations(conn)
                else:
                    not_implemented(conn, request['operationId'])
                conn.close()


def doip_list_operations(conn: object):
    message = {
        'status': '0.DOIP/Status.001',
        'output': [
            '0.DOIP/Op.Hello',
            '0.DOIP/Op.ListOperations',
        ]
    }
    send_server_message(message, conn)


def doip_hello(conn: object, port: int):
    message = {'status': '0.DOIP/Status.001',
               'output': {
                   'id': 'doip-server-1',
                   'type': '0.TYPE/DOIPServiceInfo',
                   'attributes': {
                       'ipAddress': '0.0.0.0',
                       'port': port,
                       'protocol': 'TCP',
                       'protocolVersion': '2.0'
                   }
               }
               }
    print('send reply')
    send_server_message(message, conn)


def doip_create():
    print('dummy')


def doip_update():
    print('dummy')


def doip_delete():
    print('dummy')


def doip_search():
    print('dummy')


def not_implemented(conn: object, operation_id: str):
    message = {operation_id: 'not supported'}
    send_server_message(message, conn)
