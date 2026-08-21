from dataclasses import dataclass

@dataclass(frozen=True)
class CustomException(Exception):
    customValue: str