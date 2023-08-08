import json
from pathlib import Path
from typing import Any, Dict, List
from sqlalchemy_loadump.importer.importer import Importer


class JSONImporter(Importer):

    def import_from_file(self, from_path: Path) -> Dict[str, List[Dict[str, Any]]]:
        with from_path.open('r', encoding='utf-8') as f:
            return json.loads(f.read())
