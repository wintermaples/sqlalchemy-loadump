import importlib.metadata


def get_version() -> str:
    try:
        return importlib.metadata.version('sqlalchemy-loadump')
    except importlib.metadata.PackageNotFoundError:
        return 'NoVersion'
