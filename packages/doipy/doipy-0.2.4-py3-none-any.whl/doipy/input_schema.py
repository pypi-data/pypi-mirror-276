input_schema_create_fdo = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "",
    "title": "Input to create_fdo",
    "description": "Input to the create_fdo operation for FDOs complying to configuration type 4.",
    "type": "object",
    "properties": {
        "data-bit-sequences": {
            "type": "array",
            "description": "Array of data bit-sequences and corresponding metadata for an FDO. Each item forms a DO.",
            "minItems": 1,
            "items": {
                "type": "object",
                "description": "Data bit-sequence and corresponding metadata for a data DO.",
                "properties": {
                    "file": {
                        "type": "string",
                        "description": "Data bit-sequence of a DO."
                    },
                    "md-file": {
                        "type": "string",
                        "description": "Metadata of a DO, written into the PID record."
                    }
                },
                "minProperties": 1,
                "additionalProperties": False
            }
        },
        "metadata-bit-sequence": {
            "type": "object",
            "description": "Metadata bit-sequence and corresponding metadata for an FDO. This object forms a metadata "
                           "DO.",
            "properties": {
                "file": {
                    "type": "string",
                    "description": "Metadata bit-sequence of a DO."
                },
                "md-file": {
                    "type": "string",
                    "description": "Metadata of a DO, written into the PID record."
                }
            },
            "minProperties": 1,
            "additionalProperties": False
        }
    },
    "minProperties": 1,
    "additionalProperties": False
}


input_schema_create = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "",
    "title": "Input to create",
    "description": "Input to the create operation to generate a DO.",
    "type": "object",
    "properties": {
        "file": {
            "type": "string",
            "description": "Bit-sequence of a DO."
        },
        "md-file": {
            "type": "string",
            "description": "Metadata of a DO, written into the PID record."
        }
    },
    "minProperties": 1,
    "additionalProperties": False
}
