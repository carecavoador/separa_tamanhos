from pathlib import Path
from os import mkdir
from shutil import copy

from PyPDF2 import PdfReader

from separa_tamanhos.papel import Papel


def move_para_pasta(arquivo: Path, tamanho: str, destino: Path) -> None:
    """Move o arquivo recebito para a pasta do tamanho correspondente no
    Desktop do usuário."""

    pasta_tamanho = Path().joinpath(destino, tamanho)

    if not pasta_tamanho.exists():
        mkdir(pasta_tamanho)

    copy(arquivo, pasta_tamanho.joinpath(arquivo.name))


def separa_por_tamanho(lista_prints: list[Path], tamanhos: list[Papel], saida: Path) -> None:
    """Recebe uma lista de objetos Path apontando para arquivos PDF e retorna uma
    lista de objetos Tuple com os arquivos separados por tamanho."""

    for printout in lista_prints:
        print(f"Processando {printout.name}..")
        for tamanho in tamanhos:
            with open(printout, "rb") as arquivo:
                reader = PdfReader(arquivo)
                pagina = reader.pages[0]
                largura = pagina.mediabox.width
                altura = pagina.mediabox.height
                if (largura <= tamanho.largura and altura <= tamanho.altura) or (
                    largura <= tamanho.altura and altura <= tamanho.largura
                ):
                    move_para_pasta(printout, tamanho.nome, saida)
                    break
