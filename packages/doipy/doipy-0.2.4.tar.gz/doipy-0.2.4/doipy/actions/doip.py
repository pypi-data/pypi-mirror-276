import uuid
from pathlib import Path
import json

from doipy.exceptions import InvalidRequestException
from doipy.config import settings
from doipy.constants import DOIPOperation, ResponseStatus
from doipy.socket_utils import create_socket, send_message, finalize_socket, finalize_segment, read_response


def hello():
    # create request message
    message = {
        'targetId': f'{settings.target_id}',
        'operationId': DOIPOperation.HELLO.value
    }
    # send request and read response
    with create_socket() as ssl_sock:
        send_message(message, ssl_sock)
        finalize_segment(ssl_sock)
        finalize_socket(ssl_sock)
        response = read_response(ssl_sock)
        return response


def list_operations():
    # create request message
    message = {
        'targetId': f'{settings.target_id}',
        'operationId': DOIPOperation.LIST_OPERATION.value
    }

    # send request and read response
    with create_socket() as ssl_sock:
        send_message(message, ssl_sock)
        finalize_segment(ssl_sock)
        finalize_socket(ssl_sock)
        response = read_response(ssl_sock)
        return response


def create(do_type: str, bitsq: Path, metadata: dict, password: str, client_id: str = None, username: str = None):
    with create_socket() as ssl_sock:

        # target id and operation id
        message_1 = {
            'targetId': f'{settings.target_id}',
            'operationId': DOIPOperation.CREATE.value,
            'authentication': {
                'password': password
            }
        }

        # authentication
        # if both username and client_id are provided, authentication is successful if and only if the clientId is
        # correct
        # TODO: provide authentication via token
        if username is not None:
            message_1['authentication']['username'] = username
        if client_id is not None:
            message_1['clientId'] = client_id

        send_message(message_1, ssl_sock)
        finalize_segment(ssl_sock)

        # create a DO of type document in Cordra for the file which is added
        message_2 = {
            'type': do_type,
            'attributes': {
                'content': {
                    'id': '',
                    'name': 'digital object'
                }
            }
        }
        # add metadata to DO
        if metadata:
            message_2['attributes']['content'] = message_2['attributes']['content'] | metadata

        # add information on files to DO
        if bitsq:
            filename = bitsq.name
            my_uuid = str(uuid.uuid4())
            message_2['elements'] = [
                {
                    'id': my_uuid,
                    'type': 'text/plain',
                    'attributes': {
                        'filename': filename
                    }
                }
            ]

        send_message(message_2, ssl_sock)
        finalize_segment(ssl_sock)

        if bitsq:
            # send id
            message_3 = {
                'id': my_uuid
            }
            send_message(message_3, ssl_sock)
            finalize_segment(ssl_sock)

            # send content of files
            buffer_size = 1024
            with open(bitsq, 'rb') as f:
                while bytes_read := f.read(buffer_size):
                    ssl_sock.sendall(bytes_read)
                finalize_segment(ssl_sock)

        finalize_socket(ssl_sock)

        reply = read_response(ssl_sock)
        if reply[0]['status'] == ResponseStatus.SUCCESS.value:
            do_ref = reply[0]['output']['id']
            return do_ref
        else:
            raise InvalidRequestException(json.dumps(reply, indent=2) + '\n' + 'request was invalid in some way')
        # Next step: update the DO to put the correct metadata
        # update(reply['output']['id'], client_id, password, do_type)


def update(target_id: str, client_id: str, password: str, do_type: str):
    # TODO fix message

    with create_socket() as ssl_sock:
        message = {
            'clientId': client_id,
            'targetId': target_id,
            'operationId': DOIPOperation.UPDATE.value,
            'authentication': {
                'password': password
            }
        }
        send_message(message, ssl_sock)
        string1 = f'https://cordra.testbed.pid.gwdg.de/objects/{target_id}?payload=file'
        string2 = f'https://cordra.testbed.pid.gwdg.de/objects/{target_id}'
        message = {
            'type': do_type,
            'attributes': {
                'content': {
                    'id': '',
                    'Payload': string1,
                    'Metadata': string2
                }
            }
        }
        send_message(message, ssl_sock)
        finalize_socket(ssl_sock)
        response = read_response(ssl_sock)
        return response


def search(query: str = 'type:Document', username: str = None, password: str = None):
    # TODO fix message
    message = {
        'targetId': f'{settings.target_id}',
        'operationId': DOIPOperation.SEARCH.value,
        'attributes': {
            'query': query
        }
    }
    if username and password:
        message['authentication'] = {
            'username': username,
            'password': password
        }

    with create_socket() as ssl_sock:
        send_message(message, ssl_sock)
        finalize_socket(ssl_sock)
        response = read_response(ssl_sock)
        return response

# delete
# retrieve
