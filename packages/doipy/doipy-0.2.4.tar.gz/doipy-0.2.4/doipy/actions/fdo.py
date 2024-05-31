from doipy.actions.doip import create
from doipy.config import settings
from doipy.constants import DOIPOperation, DOType, TypeInstance, TypeIdentifier
from doipy.models import FdoInput
from doipy.socket_utils import create_socket, send_message, finalize_segment, finalize_socket, read_response


def create_fdo(fdo_input: FdoInput,
               password: str,
               client_id: str = None,
               username: str = None):

    with create_socket() as ssl_sock:
        message_1 = {
            'targetId': f'{settings.target_id}',
            'operationId': DOIPOperation.CREATE.value,
            'authentication': {
                'password': password
            }
        }
        if client_id is not None:
            message_1['clientId'] = client_id
        if username is not None:
            message_1['authentication']['username'] = username

        message_2 = {
            'type': DOType.FDO.value,
            'attributes': {
                'content': {
                    'id': '',
                    # FDO_Profile_Ref: mandatory
                    TypeIdentifier.FDO_PROFILE_REF.value: TypeInstance.FDO_PROFILE_REF_VAL.value,
                    # FDO_Type_Ref: mandatory
                    TypeIdentifier.FDO_TYPE_REF.value: TypeInstance.FDO_TYPE_REF_VAL.value
                }
            }
        }
        # create the data DOs
        if fdo_input.data_bit_sequences:
            data_refs = []
            for item in fdo_input.data_bit_sequences:
                do_ref = create(DOType.DO.value, item.file, item.md, password, client_id, username)
                data_refs.append(do_ref)
            message_2['attributes']['content'][TypeIdentifier.FDO_DATA_REFS.value] = data_refs

        # create the metadata DO
        if fdo_input.metadata_bit_sequence:
            metadata_ref = create(DOType.DO.value,
                                  fdo_input.metadata_bit_sequence.file,
                                  fdo_input.metadata_bit_sequence.md,
                                  password,
                                  client_id,
                                  username)
            message_2['attributes']['content'][TypeIdentifier.FDO_MD_REFS.value] = metadata_ref

        # create the FDO
        send_message(message_1, ssl_sock)
        finalize_segment(ssl_sock)

        send_message(message_2, ssl_sock)
        finalize_segment(ssl_sock)
        finalize_socket(ssl_sock)

        response = read_response(ssl_sock)
        return response
