import json
import os
from conta import Banco, Movimentacao


# essa classe cuida de salvar e carregar, pra não misturar isso com as operações
class RepositorioJSON:
    def __init__(self, caminho):
        self.caminho = caminho

    # transforma os objetos em dicionários e salva tudo no mesmo arquivo
    def salvar(self, banco):
        clientes, agencias, contas = [], [], []
        for cliente in banco.listar_clientes():
            clientes.append(cliente.para_dicionario())
        for agencia in banco.listar_agencias():
            agencias.append(agencia.para_dicionario())
        for conta in banco.listar_contas():
            contas.append(conta.para_dicionario())
        # esse 2 só avisa que os valores já estão em centavos, diferente do json antigo
        dados = {'versao': 2, 'clientes': clientes, 'agencias': agencias, 'contas': contas}
        with open(self.caminho, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)

    # abre o arquivo e reconstrói o banco; se ainda não tem arquivo, começa vazio
    def carregar(self):
        banco = Banco('Arasaka Bank')
        if not os.path.exists(self.caminho) or os.path.getsize(self.caminho) == 0:
            return banco
        with open(self.caminho, 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)
        # o json antigo era uma lista com três listas dentro, isso aqui então é pra ainda aceitar ele
        antigo = type(dados) == list
        if antigo:
            clientes, agencias, contas = dados
        else:
            clientes, agencias, contas = dados['clientes'], dados['agencias'], dados['contas']
        for cliente in clientes:
            banco.cadastrar_cliente(cliente['Nome'], cliente['CPF'])
        for agencia in agencias:
            banco.cadastrar_agencia(agencia['Codigo da agencia'],
                                    agencia['Nome da agencia'], agencia['Cidade'])
        for dados_conta in contas:
            conta = banco.restaurar_conta(dados_conta)
            if conta is None:
                # se a conta tá com algum problema no arquivo, avisa em vez de sumir com ela
                raise ValueError('Conta inválida no arquivo: ' + str(dados_conta['numero']))
            saldo = dados_conta['saldo']
            if antigo:
                saldo = round(saldo * 100)
            movimentos = []
            for linha in dados_conta.get('extrato', []):
                valor = linha['valor']
                saldo_apos = linha.get('saldo_apos')
                if antigo:
                    valor = round(valor * 100)
                    if saldo_apos is not None:
                        saldo_apos = round(saldo_apos * 100)
                movimentos.append(Movimentacao(linha['tipo'], valor, linha['descricao'],
                                              linha['data'], saldo_apos))
            conta.restaurar_historico(saldo, movimentos)
        return banco
