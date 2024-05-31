from doipy.config import settings
from doipy.constants import CordraOperation
from doipy.socket_utils import create_socket, send_message, finalize_segment, finalize_socket, read_response


def get_design():
    message = {
        'targetId': f'{settings.target_id}',
        'operationId': CordraOperation.GET_DESIGN.value
    }
    with create_socket() as ssl_sock:
        send_message(message, ssl_sock)
        finalize_segment(ssl_sock)
        finalize_socket(ssl_sock)
        response = read_response(ssl_sock)
        return response


def get_init_data():
    message = {
        'targetId': f'{settings.target_id}',
        'operationId': CordraOperation.GET_INIT_DATA.value
    }
    with create_socket() as ssl_sock:
        send_message(message, ssl_sock)
        finalize_segment(ssl_sock)
        finalize_socket(ssl_sock)
        response = read_response(ssl_sock)
        return response
