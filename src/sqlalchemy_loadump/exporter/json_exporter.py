import datetime
import json
from pathlib import Path
from typing import Dict, List

from _decimal import Decimal

from sqlalchemy_loadump.exporter.exporter import Exporter


class SQLAlchemyTypesJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


class JSONExporter(Exporter):
    def export_to_file(
        self,
        dump_data: Dict[str, List[Dict[str, any]]],
        to: Path,
        human_readable: bool = False,
    ):
        with to.open("w", encoding="utf-8") as f:
            dump_data_json = json.dumps(
                dump_data,
                cls=SQLAlchemyTypesJSONEncoder,
                indent=4 if human_readable else None,
                ensure_ascii=False,
            )
            f.write(dump_data_json)
