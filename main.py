from cliente import criar_cliente
from conta import criacao_de_conta, depositar, sacar

# cliente
nome, cpf = criar_cliente('Bruno', '12345678900')

# conta
numero, cliente, saldo = criacao_de_contaUpdate 

# deposito
saldo = depositar(saldo, 500)

# saque
saldo= sacar(saldo, 200)
