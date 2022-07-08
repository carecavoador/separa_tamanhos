from dataclasses import dataclass


@dataclass
class Papel:
    """Classe para representar os tamanhos de papel."""

    nome: str
    largura: int
    altura: int
