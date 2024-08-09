import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent
ENV_FILE = os.path.join(BASE_DIR, ".env")


class SettingsMixin(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE, extra="ignore"
    )
