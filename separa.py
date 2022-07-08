# pylint: disable=E1101
from os import mkdir, listdir
from sys import argv
from pathlib import Path
from shutil import copy
from dataclasses import dataclass

from PyPDF2 import PdfReader


# Tamanhos de papel ----------------------------------------------------------
@dataclass
class Papel:
    """Classe para representar os tamanhos de papel."""

    nome: str
    largura: int
    altura: int


FOLHA_A4 = Papel("A4", 595, 842)
FOLHA_A3 = Papel("A3", 842, 1191)
ROLO = Papel("ROLO", 2520, 91440)

TAMANHOS_PAPEL = [FOLHA_A4, FOLHA_A3, ROLO]
# -----------------------------------------------------------------------------

DESKTOP = Path.home().joinpath("Desktop")
ARGUMENTOS = argv[1:]


def move_para_pasta(arquivo: Path, tamanho: str) -> None:
    """Move o arquivo recebito para a pasta do tamanho correspondente no
    Desktop do usuário."""

    pasta_tamanho = Path().joinpath(DESKTOP, tamanho)

    if not pasta_tamanho.exists():
        mkdir(pasta_tamanho)

    copy(arquivo, pasta_tamanho.joinpath(arquivo.name))


def separa_por_tamanho(lista_prints: list[Path]) -> None:
    """Recebe uma lista de objetos Path apontando para arquivos PDF e retorna uma
    lista de objetos Tuple com os arquivos separados por tamanho."""

    for printout in lista_prints:
        for tamanho in TAMANHOS_PAPEL:
            with open(printout, "rb") as arquivo:
                reader = PdfReader(arquivo)
                pagina = reader.pages[0]
                largura = pagina.mediabox.width
                altura = pagina.mediabox.height
                if (largura <= tamanho.largura and altura <= tamanho.altura) or (
                    largura <= tamanho.altura and altura <= tamanho.largura
                ):
                    move_para_pasta(printout, tamanho.nome)
                    break


def main() -> None:
    """Executa o programa."""

    arquivos = [Path(arg) for arg in ARGUMENTOS if Path(arg).is_file()]
    pastas = [Path(arg) for arg in ARGUMENTOS if Path(arg).is_dir()]

    if arquivos:
        arquivos = [arquivo for arquivo in arquivos if arquivo.suffix == ".pdf"]
        separa_por_tamanho(arquivos)

    if pastas:
        for pasta in pastas:
            arquivos_pasta = [
                Path(pasta, a) for a in listdir(pasta) if Path(a).suffix == ".pdf"
            ]
            separa_por_tamanho(arquivos_pasta)


if __name__ == "__main__":
    main()
