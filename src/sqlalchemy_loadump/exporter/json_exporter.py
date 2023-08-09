import datetime
import json
from base64 import b64encode
from pathlib import Path
from typing import Any, Dict, List

from _decimal import Decimal

from sqlalchemy_loadump.exporter.exporter import Exporter


class JSONExporter(Exporter):
    class SQLAlchemyTypesJSONEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Decimal):
                return {"type": "decimal", "value": str(obj)}
            elif isinstance(obj, datetime.datetime):
                return {"type": "datetime", "value": obj.isoformat()}
            elif isinstance(obj, bytes):
                return {"type": "bytes", "value": b64encode(obj).decode("utf-8")}
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
