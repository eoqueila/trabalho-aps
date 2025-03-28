from datetime import datetime, timedelta
import random
import string
from typing import List


funcionarios = []
visitantes = {}



class Usuario:
    def __init__(self, id: int, nome: str, documento: str, tipo: str):
        self.id = id
        self.nome = nome
        self.documento = documento
        self.tipo = tipo  

class Funcionario(Usuario):
    def __init__(self, id: int, nome: str, documento: str, cargo: str, departamento: str, senha: str ):
        super().__init__(id, nome, documento, "Funcionário")
        self.cargo = cargo
        self.senha = senha
        self.departamento = departamento

class Visitante(Usuario):
    def __init__(self, id: int, nome: str, documento: str, empresa: str, senha: str):
        super().__init__(id, nome, documento, "Visitante")
        self.empresa = empresa
        self.senha = senha
        self.expiracao = datetime.now() + timedelta(hours=1)  

class Administrador(Funcionario):
    ADMIN_CODIGO = "1234"  

    def __init__(self, id: int, nome: str, documento: str, cargo: str, departamento: str, permissao_total: bool):
        super().__init__(id, nome, documento, cargo, departamento)
        self.permissao_total = permissao_total

    @staticmethod
    def autenticar():
        codigo = input("Digite o código de administrador: ")
        return codigo == Administrador.ADMIN_CODIGO


class PontoDeAcesso:
    def __init__(self, id: int, localizacao: str, tipo: str):
        self.id = id
        self.localizacao = localizacao
        self.tipo = tipo  # "Catraca", "Porta", "Cancela"

class Acesso:
    acessos = []

    def __init__(self, usuario: Usuario, ponto_de_acesso: PontoDeAcesso, status: str):
        self.usuario = usuario
        self.ponto_de_acesso = ponto_de_acesso
        self.data_hora = datetime.now()
        self.status = status  # "Autorizado" ou "Negado"
        Acesso.acessos.append(self)

    @staticmethod
    def registrar_entrada(usuario: Usuario, ponto: PontoDeAcesso):
        senha_digitada = input(f"Digite a senha de acesso para {usuario.nome}: ")
        
        if isinstance(usuario, Visitante):
            if usuario.senha == senha_digitada and usuario.expiracao > datetime.now():
                status = "Autorizado"
            else:
                status = "Negado"
        else:
            status = "Autorizado"  
        
        Acesso(usuario, ponto, status)
        print(f"✅ {usuario.nome} - {status}")


class Relatorio:
    @staticmethod
    def gerar():
        print("\n📄 Relatório de Acessos:")
        for acesso in Acesso.acessos:
            print(f"{acesso.data_hora} - {acesso.usuario.nome} - {acesso.status}")



def gerar_senha():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def cadastrar_usuario():
    tipo = input("Cadastrar (1) Funcionário ou (2) Visitante? ")
    
    nome = input("Nome: ")
    documento = input("Documento: ")

    if tipo == "1":
        cargo = input("Cargo: ")
        senha = gerar_senha()
        departamento = input("Departamento: ")
        funcionario = Funcionario(len(funcionarios) + 1, nome, documento, cargo, departamento, senha)
        funcionarios.append(funcionario)
        print(f"✅ Funcionário {funcionario.nome} cadastrado! senha de acesso: {senha}!")

    elif tipo == "2":
        empresa = input("Empresa: ")
        senha = gerar_senha()
        visitante = Visitante(len(visitantes) + 1, nome, documento, empresa, senha)
        visitantes[documento] = visitante
        print(f"✅ Visitante {visitante.nome} cadastrado! Senha de acesso: {senha}")

def verificar_acesso():
    documento = input("Digite o documento: ")

    usuario = next((u for u in funcionarios if u.documento == documento), visitantes.get(documento, None))

    if usuario:
        local = input("Local de acesso: ")
        ponto = PontoDeAcesso(1, local, "Catraca")
        Acesso.registrar_entrada(usuario, ponto)
    else:
        print("❌ Usuário não encontrado!")


if Administrador.autenticar():
    while True:
        print("\n1️⃣ Cadastrar Usuário")
        print("2️⃣ Verificar Entrada/Saída")
        print("3️⃣ Gerar Relatório")
        print("4️⃣ Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            verificar_acesso()
        elif opcao == "3":
            Relatorio.gerar()
        elif opcao == "4":
            print("🔒 Sistema encerrado.")
            break
        else:
            print("❌ Opção inválida!")
else:
    print("❌ Código de administrador incorreto!")

