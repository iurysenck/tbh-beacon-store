"""Junta mods/*.json num docs/catalog.json unico, para a pagina publica consumir.

Por que existe: a pagina do GitHub Pages e estatica, sem backend, e uma pagina estatica nao
consegue listar um diretorio. Ela precisa de um indice pronto. Este script gera esse indice a
partir dos MESMOS manifestos que o app le, que e a decisao da spec 011: uma fonte de verdade, zero
duplicacao de dado entre a pagina web e a loja de dentro do app.

Roda no CI a cada mudanca em mods/, entao o indice nunca fica atras dos manifestos.

Uso:
    python scripts/build_catalog.py
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODS_DIR = os.path.join(ROOT, "mods")
OUT = os.path.join(ROOT, "docs", "catalog.json")


def main():
    if not os.path.isdir(MODS_DIR):
        print(f"mods/ nao encontrado em {MODS_DIR}")
        return 1

    mods = []
    for name in sorted(os.listdir(MODS_DIR)):
        if not name.endswith(".json"):
            continue
        with open(os.path.join(MODS_DIR, name), encoding="utf-8") as f:
            mods.append(json.load(f))

    # Sem carimbo de data de proposito: o conteudo e derivado inteiramente de mods/, entao gravar a
    # hora da geracao faria este arquivo mudar em toda execucao do CI mesmo sem nenhum manifesto ter
    # mudado, enchendo o historico de diffs vazios.
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"mods": mods}, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")

    print(f"{len(mods)} manifesto(s) -> {OUT} ({os.path.getsize(OUT) / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
