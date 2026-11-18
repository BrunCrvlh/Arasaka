from datetime import datetime
from cliente import Cliente, limpar_cpf, cpf_valido
from agencia import Agencia
from abc import ABC, abstractmethod

# mexi em coisa pra carai aqui
# essas funções ajeitam o valor que vem do formulário e como ele aparece no site
def ler_valor(texto):
    # transforma 10,50 em 1050 centavos, pra não dar aquelas diferenças de float
    partes = texto.strip().replace(',', '.').split('.')
    if len(partes) > 2:
        return None
    for parte in partes:
        if not parte.isascii() or not parte.isdigit():
            return None
    centavos = 0
    if len(partes) == 2:
        if len(partes[1]) > 2:
            return None
        centavos = int(partes[1])
        if len(partes[1]) == 1:
            centavos *= 10
    return int(partes[0]) * 100 + centavos


# o valor precisa ser um número inteiro de centavos e maior que zero
def valor_valido(valor):
    return type(valor) == int and valor > 0


# aqui faz o caminho contrário: pega os centavos e mostra em reais
def brl(valor):
    sinal = ''
    if valor < 0:
        sinal = '-'
        valor = -valor
    inteiro = str(valor // 100)
    grupos = []
    while len(inteiro) > 3:
        grupos.insert(0, inteiro[-3:])
        inteiro = inteiro[:-3]
    grupos.insert(0, inteiro)
    return sinal + 'R$ ' + '.'.join(grupos) + ',' + str(valor % 100).zfill(2)


# cada depósito, saque ou transferência vira uma movimentação no extrato
class Movimentacao:
    def __init__(self, tipo, valor, descricao, data=None, saldo_apos=None):
        self.tipo = tipo
        self.valor = valor
        self.descricao = descricao
        self.saldo_apos = saldo_apos
        if data is None:
            data = datetime.now().strftime('%d/%m/%Y %H:%M')
        self.data = data

    # positivo entrou dinheiro e negativo saiu
    def entrada(self):
        return self.valor > 0

    def para_dicionario(self):
        return {'tipo': self.tipo, 'valor': self.valor,
                'descricao': self.descricao, 'data': self.data,
                'saldo_apos': self.saldo_apos}


# essa é a base dos dois tipos de conta, com as operações que eles têm em comum e conta herda ABC por ser uma classe abstrata.
class Conta(ABC):
    def __init__(self, numero, cliente, agencia, login, senha):
        self.numero = numero
        # aqui ficam o cliente e a agência da conta, os dois já são objetos
        self.cliente = cliente
        self.agencia = agencia
        self.login = login
        self.tipo = 'conta'
        # os dois __ são pra acessar isso pelos métodos, em vez de mudar por fora
        self.__senha = senha
        self.__saldo = 0
        self.__extrato = []

    # compara com a senha dessa conta
    def autenticar(self, senha):
        return self.__senha == senha

    def consultar_saldo(self):
        return self.__saldo

    def consultar_extrato(self):
        # manda uma cópia da lista, pra não apagarem o extrato com um clear sem querer
        return self.__extrato.copy()

    # monta a movimentação e coloca no extrato com o saldo daquele momento
    def registrar(self, tipo, valor, descricao):
        movimento = Movimentacao(tipo, valor, descricao, saldo_apos = self.__saldo)
        self.__extrato.append(movimento)

    # se o valor for válido, soma no saldo e guarda no extrato
    def depositar(self, valor):
        if not valor_valido(valor):
            return False
        self.__saldo += valor
        self.registrar('Depósito', valor, 'Depósito na conta')
        return True

    # mesma ideia do depósito, mas antes confere se tem saldo suficiente
    def sacar(self, valor):
        if not valor_valido(valor) or valor > self.__saldo:
            return False
        self.__saldo -= valor
        self.registrar('Saque', -valor, 'Saque na conta')
        return True
    
    # percorre o extrato somando separado o que entrou e o que saiu
    def totais_movimentados(self):
        entradas = 0
        saidas = 0
        for movimento in self.__extrato:
            if movimento.entrada():
                entradas += movimento.valor
            else:
                saidas -= movimento.valor
        return entradas, saidas
    
    @abstractmethod
    def descricao_tipo(self):
        return 'Conta para organizar seu dinheiro.'

    def restaurar_historico(self, saldo, movimentos):
        # isso aqui é só pra trazer de volta o que já tava salvo no json
        # não registra depósito de novo, senão ia duplicar o histórico toda vez que abrisse
        self.__saldo = saldo
        self.__extrato = movimentos.copy()

    def para_dicionario(self):
        movimentos = []
        for movimento in self.__extrato:
            movimentos.append(movimento.para_dicionario())
        return {'numero': self.numero, 'cpf': self.cliente.cpf,
                'codigo_agencia': self.agencia.codigo, 'login': self.login,
                'senha': self.__senha, 'tipo': self.tipo, 'saldo': self.__saldo,
                'extrato': movimentos}


# os dois tipos herdam de Conta e cada um muda a própria descrição
# isso é o polimorfismo daqui: chama descricao_tipo igual, mas o texto depende do objeto
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, agencia, login, senha):
        # o super chama o __init__ da Conta, aí não precisa copiar tudo de novo
        super().__init__(numero, cliente, agencia, login, senha)
        self.tipo = 'corrente'

    def descricao_tipo(self):
        return 'Sua conta para depósitos, saques e transferências do dia a dia.'

    # não deixa mandar pra própria conta nem mandar mais do que tem.
    def transferir(self, destino, valor):
            if not isinstance(destino, Conta) or destino is self:
                return False
            if not valor_valido(valor) or valor > self.consultar_saldo():
                return False
            # passou nas verificações, aí tira de uma conta e coloca na outra
            self.sacar(valor)
            destino.depositar(valor)
            return True
    
class ContaPoupanca(Conta):
    def __init__(self, numero, cliente, agencia, login, senha):
        super().__init__(numero, cliente, agencia, login, senha)
        self.tipo = 'poupanca'

    def descricao_tipo(self):
        return 'Separe uma reserva. Nesta simulação, não há rendimento automático.'


# o banco junta os clientes, agências e contas pra não ficar tudo solto no app
class Banco:
    def __init__(self, nome):
        self.nome = nome
        self.__clientes = []
        self.__agencias = []
        self.__contas = []
        self.__proximo_numero = 1

    def listar_clientes(self):
        return self.__clientes.copy()

    def listar_agencias(self):
        return self.__agencias.copy()

    # sem cpf mostra todas, com cpf deixa só as contas daquele cliente
    def listar_contas(self, cpf=''):
        if cpf == '':
            return self.__contas.copy()
        cpf = limpar_cpf(cpf)
        return [conta for conta in self.__contas if conta.cliente.cpf == cpf]

    def buscar_cliente(self, cpf):
        cpf = limpar_cpf(cpf)
        for cliente in self.__clientes:
            if cliente.cpf == cpf:
                return cliente
        return None

    def buscar_agencia(self, codigo):
        for agencia in self.__agencias:
            if agencia.codigo == codigo:
                return agencia
        return None

    # procura a conta pelo número e devolve None se não achar
    def buscar_conta(self, numero):
        for conta in self.__contas:
            if conta.numero == numero:
                return conta
        return None

    def buscar_login(self, login):
        for conta in self.__contas:
            if conta.login == login:
                return conta
        return None

    def cadastrar_cliente(self, nome, cpf):
        nome = nome.strip()
        cpf = limpar_cpf(cpf)
        if nome == '' or not cpf_valido(cpf) or self.buscar_cliente(cpf) is not None:
            return None
        cliente = Cliente(nome, cpf)
        self.__clientes.append(cliente)
        return cliente

    def cadastrar_agencia(self, codigo, nome, cidade):
        codigo, nome, cidade = codigo.strip(), nome.strip(), cidade.strip()
        if codigo == '' or nome == '' or cidade == '':
            return None
        if self.buscar_agencia(codigo) is not None:
            return None
        agencia = Agencia(codigo, nome, cidade)
        self.__agencias.append(agencia)
        return agencia

    def abrir_conta(self, nome, cpf, codigo, login, senha, tipo):
        # confere tudo primeiro, pra não cadastrar metade das coisas e dar erro depois
        nome, cpf, login = nome.strip(), limpar_cpf(cpf), login.strip()
        if nome == '' or not cpf_valido(cpf):
            return None, 'Informe o nome e um CPF válido.'
        agencia = self.buscar_agencia(codigo)
        if agencia is None:
            return None, 'Escolha uma agência disponível.'
        if login == '' or senha.strip() == '':
            return None, 'Preencha o login e a senha.'
        if self.buscar_login(login) is not None:
            return None, 'Este login já está em uso. Escolha outro.'
        if tipo not in ['corrente', 'poupanca']:
            return None, 'Escolha um tipo de conta válido.'
        cliente = self.buscar_cliente(cpf)
        if cliente is None:
            cliente = self.cadastrar_cliente(nome, cpf)
        if tipo == 'corrente':
            conta = ContaCorrente(self.__proximo_numero, cliente, agencia, login, senha)
        else:
            conta = ContaPoupanca(self.__proximo_numero, cliente, agencia, login, senha)
        self.__contas.append(conta)
        self.__proximo_numero += 1
        return conta, 'Conta aberta com sucesso.'

    def autenticar(self, login, senha):
        conta = self.buscar_login(login.strip())
        if conta is not None and conta.autenticar(senha):
            return conta
        return None

    def transferir(self, numero_origem, numero_destino, valor):
        origem = self.buscar_conta(numero_origem)
        destino = self.buscar_conta(numero_destino)
        if origem is None or destino is None:
            return False
        if not isinstance(origem, ContaCorrente):
            return False
        return origem.transferir(destino, valor)

    # percorre as contas e soma os saldos
    def montante_total(self):
        total = 0
        for conta in self.__contas:
            total += conta.consultar_saldo()
        return total

    # pra cada agência, conta quantas contas ela tem e soma o dinheiro delas
    def resumo_agencias(self):
        resumo = []
        for agencia in self.__agencias:
            quantidade = 0
            total = 0
            for conta in self.__contas:
                if conta.agencia is agencia:
                    quantidade += 1
                    total += conta.consultar_saldo()
            resumo.append({'agencia': agencia, 'quantidade': quantidade, 'total': total})
        return resumo

    def restaurar_conta(self, dados):
        # pega os dados do json e monta a conta de novo como objeto
        cliente = self.buscar_cliente(dados['cpf'])
        if cliente is None or self.buscar_conta(dados['numero']) is not None:
            return None
        conta, mensagem = self.abrir_conta(cliente.nome, cliente.cpf,
            dados['codigo_agencia'], dados['login'], dados['senha'], dados['tipo'])
        if conta is not None:
            conta.numero = dados['numero']
            maior = 0
            for cadastrada in self.__contas:
                if cadastrada.numero > maior:
                    maior = cadastrada.numero
            self.__proximo_numero = maior + 1
        return conta
