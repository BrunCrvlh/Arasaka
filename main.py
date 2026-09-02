from cliente import criar_cliente
from conta import criacao_de_conta, consultar_saldo, depositar, sacar

# cliente
nome, cpf = criar_cliente('Bruno', '12345678900')

# conta
numero, cliente, saldo = criacao_de_conta(

# consultar saldo
saldo = consultar_saldo(saldo)

# depósito
saldo = depositar(500)

# consultando saldo após depósito 
saldo = consultar_saldo(saldo)

# saque
saldo = sacar(saldo, 200)

# consultando saldo após saque 
saldo = consultar_saldo(saldo)
