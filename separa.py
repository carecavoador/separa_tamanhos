# pylint: disable=E1101
from os import listdir
from sys import argv
from pathlib import Path

from separa_tamanhos.papel import Papel
from separa_tamanhos.separa_tamanhos import separa_por_tamanho


# Tamanhos de papel ----------------------------------------------------------
FOLHA_A4 = Papel("A4", 595, 842)
FOLHA_A3 = Papel("A3", 842, 1191)
ROLO = Papel("ROLO", 2520, 91440)
TAMANHOS_PAPEL = [FOLHA_A4, FOLHA_A3, ROLO]
# -----------------------------------------------------------------------------

DESKTOP = Path.home().joinpath("Desktop")
ARGUMENTOS = argv[1:]


def main() -> None:
    """Executa o programa."""

    arquivos = [Path(arg) for arg in ARGUMENTOS if Path(arg).is_file()]
    pastas = [Path(arg) for arg in ARGUMENTOS if Path(arg).is_dir()]

    if arquivos:
        arquivos = [arquivo for arquivo in arquivos if arquivo.suffix == ".pdf"]
    
    if pastas:
        for pasta in pastas:
            arquivos_pasta = [
                Path(pasta, a) for a in listdir(pasta) if Path(a).suffix == ".pdf"
            ]
            arquivos.extend(arquivos_pasta)
    
    if not arquivos:
        saida = input("Nenhum arquivo separado. Pressione qualquer tecla para sair.\n>")
        exit()
    
    separa_por_tamanho(arquivos, TAMANHOS_PAPEL, DESKTOP)


if __name__ == "__main__":
    main()
    saida = input("Programa terminado. Pressione qualquer tecla para sair.\n>")
