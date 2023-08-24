import datetime
import json
from base64 import b64encode
from pathlib import Path
from typing import Any, Dict, List

from _decimal import Decimal
import uuid

from sqlalchemy_loadump.exporter.exporter import Exporter


class JSONExporter(Exporter):
    class SQLAlchemyTypesJSONEncoder(json.JSONEncoder):
        datetime.timedelta()
        def default(self, obj):
            if isinstance(obj, Decimal):
                return {"type": "decimal", "value": str(obj)}
            elif isinstance(obj, datetime.datetime):
                return {"type": "datetime", "value": obj.isoformat()}
            elif isinstance(obj, datetime.date):
                return {"type": "date", "value": obj.isoformat()}
            elif isinstance(obj, datetime.time):
                return {"type": "time", "value": obj.isoformat()}
            elif isinstance(obj, datetime.timedelta):
                return {"type": "timedelta", "value": {
                    "days": obj.days,
                    "seconds": obj.seconds,
                    "microseconds": obj.microseconds,
                }}
            elif isinstance(obj, bytes):
                return {"type": "bytes", "value": b64encode(obj).decode("utf-8")}
            elif isinstance(obj, uuid.UUID):
                return {"type": "uuid", "value": obj.hex}
            return json.JSONEncoder.default(self, obj)

    def export_to_file(
        self,
        dump_data: Dict[str, List[Dict[str, Any]]],
        to: Path,
        human_readable: bool = False,
    ):
        with to.open("w", encoding="utf-8") as f:
            dump_data_json = json.dumps(
                dump_data,
                cls=self.SQLAlchemyTypesJSONEncoder,
                indent=4 if human_readable else None,
                ensure_ascii=False,
            )
            f.write(dump_data_json)
