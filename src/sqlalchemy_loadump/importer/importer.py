import abc
from pathlib import Path
from typing import Any, Dict, List


class Importer(metaclass=abc.ABCMeta):
    def import_from_file(
        self,
        from_path: Path,
    ) -> Dict[str, List[Dict[str, Any]]]:
        raise NotImplementedError()
