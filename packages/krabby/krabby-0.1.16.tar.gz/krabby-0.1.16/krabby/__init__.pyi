from typing import Any


def md5sum(file: str, batch_size: int) -> str:
    ...

class Span:
    def dict(self) -> dict[str, Any]:
        ...
        
    @property
    def start(self) -> int:
        ...
        
    @property
    def end(self) -> int:
        ...
        
    @property
    def value(self) -> str:
        ...


class KeywordProcessor:
    def __init__(self, case_sensitive: bool):
        ...
        
    def put(self, keyword: str):
        ...
        
    def pop(self, keyword: str):
        ...
        
    @property
    def case_sensitive(self) -> bool:
        ...
        
    @property
    def boundary(self) -> str:
        ...
        
    @property
    def keywords(self) -> list[str]:
        ...
        
    def set_boundary(self, boundary: str):
        ...
        
    def add_boundary(self, boundary: str):
        ...
        
    def del_boundary(self, boundary: str):
        ...
        
    def extract(self, text: str) -> list[Span]:
        ...
        
    def replace(self, text: str, repl: dict[str, str], default: str | None) -> str:
        ...
        
    def has(self, keyword: str) -> bool:
        ...
