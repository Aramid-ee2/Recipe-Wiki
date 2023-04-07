#Creating a settings class to store users settings
from dataclasses import dataclass


@dataclass
class Settings:
    night_mode: bool = False
    language: str = "English"
