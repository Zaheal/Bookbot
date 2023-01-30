from dataclasses import dataclass
from environs import Env

@dataclass
class Config:
    token: str


def load_config(path: str | None) -> Config:
    env: Env = Env()
    env.read_env(path)
    
    return Config(token=env('BOT_TOKEN'))
