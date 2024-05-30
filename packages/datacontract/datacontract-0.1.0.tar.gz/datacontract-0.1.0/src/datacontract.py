from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class DataContract:
    schema: Dict[str, Any]
    name: str
    version: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema": self.schema,
            "name": self.name,
            "version": self.version
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'DataContract':
        return DataContract(
            schema=data["schema"],
            name=data["name"],
            version=data["version"]
        )
