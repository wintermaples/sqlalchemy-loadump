import datetime
from decimal import Decimal
import json
from pathlib import Path
from typing import Any, Dict, List
import uuid
from sqlalchemy_loadump.importer.importer import Importer
from base64 import b64decode


class JSONImporter(Importer):
    @staticmethod
    def _decoder(obj: Dict[Any, Any]) -> Any:
        if not ("type" in obj and "value" in obj):
            return obj

        # type-specified value
        type_name = obj["type"]
        value = obj["value"]

        if type_name == "decimal":
            return Decimal(value)
        elif type_name == "datetime":
            return datetime.datetime.fromisoformat(value)
        elif type_name == "date":
            return datetime.date.fromisoformat(value)
        elif type_name == "time":
            return datetime.time.fromisoformat(value)
        elif type_name == "timedelta":
            return datetime.timedelta(**value)
        elif type_name == "bytes":
            return b64decode(value)
        elif type_name == "uuid":
            return uuid.UUID(value)
        else:
            raise ValueError(f"Unknown type: {type_name}")

    def import_from_file(self, from_path: Path) -> Dict[str, List[Dict[str, Any]]]:
        with from_path.open("r", encoding="utf-8") as f:
            return json.loads(f.read(), object_hook=self._decoder)
