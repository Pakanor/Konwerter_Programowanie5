from pathlib import Path
from typing import Callable, Dict, Tuple, List
from dataclasses import dataclass

Converter = Callable[[Path, Path], Path]
REGISTRY: Dict[Tuple[str, str], Converter] = {}

def converter(source: str, target: str):
    def register(func: Converter) -> Converter:
        REGISTRY[(source.lower(), target.lower())] = func
        return func
    return register

@dataclass(frozen=True)
class ConversionRequest:
    source: Path
    target_format: str
    output_dir: Path

    def validate(self) -> None:
        if not self.source.is_file():
            raise FileNotFoundError(f"Nie znaleziono pliku wejściowego: {self.source}")
        if not self.output_dir.is_dir():
            raise NotADirectoryError(f"Nie znaleziono katalogu docelowego: {self.output_dir}")
        
        key = (self.source.suffix.lower(), self.target_format.lower())
        if key not in REGISTRY:
            raise ValueError(f"Nieobsługiwana konwersja: {key[0]} -> {key[1]}")

def available_targets(source: Path) -> List[str]:
    return sorted(target for (src, target) in REGISTRY if src == source.suffix.lower())

def execute(request: ConversionRequest) -> Path:
    request.validate()
    key = (request.source.suffix.lower(), request.target_format.lower())
    return REGISTRY[key](request.source, request.output_dir)