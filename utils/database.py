import json
import os
from typing import Any, List, Dict

def carregar_json(arquivo: str) -> List[Dict[str, Any]]:
    """
    Carrega dados de um arquivo JSON.

    Args:
        arquivo (str): Caminho para o arquivo JSON.

    Returns:
        List[Dict[str, Any]]: Lista de dicionários com os dados.
    """
    if not os.path.exists(arquivo):
        return []
    with open(arquivo, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_json(arquivo: str, dados: Any) -> None:
    """
    Salva dados em um arquivo JSON.

    Args:
        arquivo (str): Caminho para o arquivo JSON.
        dados (Any): Dados a serem salvos.
    """
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
