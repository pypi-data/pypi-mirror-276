from enum import Enum


class CordraOperation(Enum):
    GET_DESIGN = '20.DOIP/Op.GetDesign'
    GET_INIT_DATA = '20.DOIP/Op.GetInitData'


class DOIPOperation(Enum):
    HELLO = '0.DOIP/Op.Hello'
    CREATE = '0.DOIP/Op.Create'
    RETRIEVE = '0.DOIP/Op.Retrieve'
    UPDATE = '0.DOIP/Op.Update'
    DELETE = '0.DOIP/Op.Delete'
    SEARCH = '0.DOIP/Op.Search'
    LIST_OPERATION = '0.DOIP/Op.ListOperations'


class ResponseStatus(Enum):
    SUCCESS = '0.DOIP/Status.001'
    INVALID = '0.DOIP/Status.101'
    UNAUTHENTICATED = '0.DOIP/Status.102'
    UNAUTHORIZED = '0.DOIP/Status.103'
    UNKNOWN_DO = '0.DOIP/Status.104'
    DUPLICATED_PID = '0.DOIP/Status.105'
    UNKNOWN_OPERATION = '0.DOIP/Status.200'
    UNKNOWN_ERROR = '0.DOIP/Status.500'


class TypeIdentifier(Enum):
    FDO_PROFILE_REF = '21.T11969/bcc54a2a9ab5bf2a8f2c'
    FDO_TYPE_REF = '21.T11969/2bb5fec05c00bb89793e'
    FDO_DATA_REFS = '21.T11969/867134e94b3ec5afc6fe'
    FDO_MD_REFS = '21.T11969/a02253b264a9f2f1cf9a'


class TypeInstance(Enum):
    FDO_PROFILE_REF_VAL = '21.T11969/141bf451b18a79d0fe66'
    FDO_TYPE_REF_VAL = '21.1/fdo_type_ref'


class DOType(Enum):
    DO = 'Document'
    FDO = 'FDO'
