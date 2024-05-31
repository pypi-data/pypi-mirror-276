import json

from jsonschema import validate
from pydantic import BaseModel
from pathlib import Path

from doipy.input_schema import input_schema_create_fdo, input_schema_create


class DoInput(BaseModel):
    file: Path = None
    md: dict = None

    @classmethod
    def parse(cls, input_json: dict) -> 'DoInput':
        # validate the input against the JSON input schema
        validate(instance=input_json, schema=input_schema_create)

        file = None
        if 'file' in input_json:
            file = Path(input_json['file'])

        metadata = None
        if 'md-file' in input_json:
            with open(input_json['md-file']) as f:
                metadata = json.load(f)

        return cls(file=file, md=metadata)


class FdoInput(BaseModel):
    data_bit_sequences: list[DoInput] = None
    metadata_bit_sequence: DoInput = None

    @classmethod
    def parse(cls, input_json: dict) -> 'FdoInput':
        # validate the input against the JSON input schema
        validate(instance=input_json, schema=input_schema_create_fdo)

        fdo_input = cls()
        if input_json['data-bit-sequences']:
            fdo_input.data_bit_sequences = []
            for item in input_json['data-bit-sequences']:
                data_do = DoInput.parse(item)
                fdo_input.data_bit_sequences.append(data_do)

        if input_json['metadata-bit-sequence']:
            metadata_do = DoInput.parse(input_json['metadata-bit-sequence'])
            fdo_input.metadata_bit_sequence = metadata_do

        return fdo_input
