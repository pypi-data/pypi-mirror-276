import json
import os

from jw_don_confirm.services import Persistable
from dataclasses import is_dataclass
from typing import Any, TypeVar, Generic, Type
import dataclass_wizard

T = TypeVar('T')


class DataclassEncoder:

    @staticmethod
    def encode_dataclass(obj: Any):
        if is_dataclass(obj):
            return dataclass_wizard.asdict(obj)
        raise TypeError(f'Objekt vom Typ {type(obj).__name__} is not a dataclass or a date and cannot be serialized')

    @staticmethod
    def decode_dataclass(dct: dict, dataclass_type: type):
        return dataclass_wizard.fromdict(dataclass_type, dct)


class JsonDataRepo(Persistable, Generic[T]):
    data: T

    @staticmethod
    def _write(file: str, md: T):
        # Check existence of directory
        directory = os.path.dirname(file)

        # Create directory, if it does not exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(file, 'w') as f:
            json.dump(md, f, default=DataclassEncoder.encode_dataclass, indent=2)

    def _read(self, file: str, dataclass_type: Type[T]) -> T:
        with open(file, 'r') as f:
            data = json.load(f)
            return DataclassEncoder.decode_dataclass(data, dataclass_type)

    def __init__(self, filename: str, dataclass_type: Type[T]):
        self.filename: str = filename
        if os.path.isfile(filename):
            self.data = self._read(filename, dataclass_type)
        else:
            self.data = dataclass_type()

    def persist(self):
        self._write(self.filename, self.data)
