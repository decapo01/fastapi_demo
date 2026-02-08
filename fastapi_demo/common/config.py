import logging
import os
import re
from pathlib import Path
import yaml
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class DatabaseConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str
    database: str


class Config(BaseModel):
    db: DatabaseConfig


_ENV_VAR_PATTERN = re.compile(r"\$\{([A-Z0-9_]+)\}")


def expand_env_vars(text: str, strict: bool = True) -> str:
    def replacer(match: re.Match[str]) -> str:
        name = match.group(1)
        value = os.environ.get(name)
        if value is None:
            if strict:
                raise ValueError(f"Missing environment variable: {name}")
            return match.group(0)  # keep ${VAR}
        return value

    return _ENV_VAR_PATTERN.sub(replacer, text)


def load_config(optional_path: str | Path = "../configs/local.yml") -> Config:
    path = os.getenv("CONFIG_PATH")
    if path is None:
        logger.warning("CONFIG_PATH environment variable is not set, using default path: %s", optional_path)
        path = optional_path
    raw = Path(path).read_text(encoding="utf-8")
    expanded = expand_env_vars(raw)
    data = yaml.safe_load(expanded)
    return Config.model_validate(data)
