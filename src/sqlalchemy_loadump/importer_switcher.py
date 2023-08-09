from typing import Dict, Union

from sqlalchemy_loadump.exporter.exporter import Exporter
from sqlalchemy_loadump.exporter.json_exporter import JSONExporter
from sqlalchemy_loadump.importer.importer import Importer
from sqlalchemy_loadump.importer.json_importer import JSONImporter


class ImporterSwitcher:
    def __init__(self):
        self.routes: Dict[str, Importer] = {}

    def add_route(self, name: str, exporter: Importer) -> None:
        self.routes[name] = exporter

    def get_route(self, name: str) -> Union[Importer, None]:
        return self.routes[name]

    def get_routes(self) -> Dict[str, Importer]:
        return self.routes


default_importer_switcher = ImporterSwitcher()
default_importer_switcher.add_route("json", JSONImporter())
