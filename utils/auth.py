import bcrypt
from utils.database import carregar_json, salvar_json
import os

def verificar_credenciais(usuario, senha):
    usuarios = carregar_json('usuarios.json')
    if usuario in usuarios:
        senha_hash = usuarios[usuario]['senha'].encode('utf-8')
        return bcrypt.checkpw(senha.encode('utf-8'), senha_hash), usuarios[usuario].get('admin', False)
    return False, False

def salvar_usuario(usuario, senha, admin=False):
    usuarios = carregar_json('usuarios.json')
    salt = bcrypt.gensalt()
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), salt)
    usuarios[usuario] = {
        'senha': senha_hash.decode('utf-8'),
        'admin': admin
    }
    salvar_json('usuarios.json', usuarios)

def inicializar_admin():
    usuarios = carregar_json('usuarios.json')
    if 'StrongerFX' not in usuarios:
        salvar_usuario('StrongerFX', 'senha_admin', admin=True)
