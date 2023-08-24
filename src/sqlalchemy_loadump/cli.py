import abc
import argparse
from ast import dump
from pathlib import Path
from ssl import Options
import sys
from typing import Any, Dict, List, Optional, Union

from sqlalchemy import create_engine

from sqlalchemy_loadump.dumper import Dumper
from sqlalchemy_loadump.importer_switcher import default_importer_switcher
from sqlalchemy_loadump.exporter_switcher import default_exporter_switcher
from sqlalchemy_loadump.importer.importer import Importer
from sqlalchemy_loadump.loader import Loader
from sqlalchemy_loadump.version import get_version
from sqlalchemy.orm import sessionmaker


class CliMode(metaclass=abc.ABCMeta):
    def run(self):
        raise NotImplementedError()


class DumpCliMode(CliMode):
    def __init__(
        self,
        dump_file_type: str,
        dump_file_path: Path,
        db_url: str,
        engine_options: Dict[str, Any] = {},
        schema: Optional[str] = None,
        human_readable: bool = False,
    ):
        self.dump_file_type = dump_file_type
        self.dump_file_path = dump_file_path
        self.db_url = db_url
        self.engine_options = engine_options
        self.schema = schema
        self.human_readable = human_readable

    def run(self):
        engine = create_engine(self.db_url, **self.engine_options)
        session_maker = sessionmaker(bind=engine)
        with session_maker() as session:
            dumper: Dumper = Dumper(engine, session, self.schema)
            dump_data = dumper.dump()

        exporter = default_exporter_switcher.get_route(self.dump_file_type)
        if exporter is None:
            raise ValueError(f"Unknown dump file type: {self.dump_file_type}")
        exporter.export_to_file(dump_data, self.dump_file_path, self.human_readable)


class LoadCliMode(CliMode):
    def __init__(
        self,
        dump_file_type: str,
        dump_file_path: Path,
        db_url: str,
        engine_options: Dict[str, str] = {},
        schema: Optional[str] = None,
    ):
        self.dump_file_type = dump_file_type
        self.dump_file_path = dump_file_path
        self.db_url = db_url
        self.engine_options = engine_options
        self.schema = schema

    def run(self):
        importer = default_importer_switcher.get_route(self.dump_file_type)
        if importer is None:
            raise ValueError(f"Unknown dump file type: {self.dump_file_type}")
        dump_data = importer.import_from_file(self.dump_file_path)

        engine = create_engine(self.db_url, **self.engine_options)
        session_maker = sessionmaker(bind=engine)
        with session_maker() as session:
            loader = Loader(dump_data, engine, session, self.schema)
            loader.load()
            session.commit()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sqlalchemy_loadump",
        description="Dump and load data in databases with sqlalchemy.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=get_version(),
    )

    subparsers = parser.add_subparsers(
        title="mode",
        dest="mode",
        required=True,
    )

    # region DumpModeParser
    dump_mode_parser = subparsers.add_parser(
        "dump",
        help="Dump data from a database.",
    )
    dump_mode_parser.add_argument(
        "-t",
        "--dump-file-type",
        required=False,
        help="The type of dump file.",
        default="json",
    )
    dump_mode_parser.add_argument(
        "-f",
        "--dump-file-path",
        required=False,
        help="The path to the dump file.",
        default="dump.json",
    )
    dump_mode_parser.add_argument(
        "-u",
        "--db-url",
        required=True,
        help="The database url.",
    )
    dump_mode_parser.add_argument(
        "--engine-options",
        action="append",
        required=False,
        help="The engine options.",
        default=[],
    )
    dump_mode_parser.add_argument(
        "--schema",
        required=False,
        help="The database schema.",
        default=None,
    )
    dump_mode_parser.add_argument(
        "-r",
        "--human-readable",
        action="store_true",
        required=False,
        help="The human reable dump file will be exported.",
    )
    # endregion

    # region LoadModeParser
    load_mode_parser = subparsers.add_parser(
        "load",
        help="Load data from a file and inserts it into a database.",
    )
    load_mode_parser.add_argument(
        "-t",
        "--dump-file-type",
        required=True,
        help="The type of dump file.",
    )
    load_mode_parser.add_argument(
        "-f",
        "--dump-file-path",
        required=True,
        help="The path to the dump file.",
    )
    load_mode_parser.add_argument(
        "-u",
        "--db-url",
        required=True,
        help="The database url.",
    )
    load_mode_parser.add_argument(
        "--engine-options",
        action="append",
        required=False,
        help="The engine options.",
        default=[],
    )
    load_mode_parser.add_argument(
        "--schema",
        required=False,
        help="The database schema.",
        default=None,
    )
    # endregion

    return parser


def _parse_engine_options(engine_options_str: List[str]) -> Dict[str, Any]:
    options: Dict[str, Any] = {}
    for option_str in engine_options_str:
        k, v = option_str.split("=", 1)
        options[k] = eval(v)
    return options


def main():
    parser = build_parser()
    args = parser.parse_args(sys.argv[1:])
    mode = args.mode

    if mode == "dump":
        DumpCliMode(
            dump_file_type=args.dump_file_type,
            dump_file_path=Path(args.dump_file_path),
            db_url=args.db_url,
            engine_options=_parse_engine_options(args.engine_options),
            schema=args.schema,
            human_readable=args.human_readable,
        ).run()
    elif mode == "load":
        LoadCliMode(
            dump_file_type=args.dump_file_type,
            dump_file_path=Path(args.dump_file_path),
            db_url=args.db_url,
            engine_options=_parse_engine_options(args.engine_options),
            schema=args.schema,
        ).run()
    else:
        raise ValueError(f"Unknown mode: {mode}")
