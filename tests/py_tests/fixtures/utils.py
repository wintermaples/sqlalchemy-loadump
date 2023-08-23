import os
from logging import warning


def get_env_or_default_with_warn(key: str, default: str) -> str:
    """
    Get the specified environment variable if exists, but default value with warning logging.

    :param key: The key of environment variables
    :param default: The default value if not exists.
    """
    val = os.environ.get(key)

    if val is None:
        warning(f"The specified environment variables(key={key}) is not found. Using {default}.")
        return default
    else:
        return val
