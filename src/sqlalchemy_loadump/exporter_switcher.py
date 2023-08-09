from typing import Dict, Union

from sqlalchemy_loadump.exporter.exporter import Exporter
from sqlalchemy_loadump.exporter.json_exporter import JSONExporter


class ExporterSwitcher:
    def __init__(self):
        self.routes: Dict[str, Exporter] = {}
    
    def add_route(self, name: str, exporter: Exporter) -> None:
        self.routes[name] = exporter
    
    def get_route(self, name: str) -> Union[Exporter, None]:
        return self.routes[name]
    
    def get_routes(self) -> Dict[str, Exporter]:
        return self.routes


default_exporter_switcher = ExporterSwitcher()
default_exporter_switcher.add_route('json', JSONExporter())
