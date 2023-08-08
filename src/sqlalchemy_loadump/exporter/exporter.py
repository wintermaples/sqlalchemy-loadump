import abc
from pathlib import Path
from typing import Any, Dict, List


class Exporter(metaclass=abc.ABCMeta):
    def export_to_file(
        self,
        dump_data: Dict[str, List[Dict[str, Any]]],
        to_path: Path,
        human_readable: bool = False,
    ):
        raise NotImplementedError()
