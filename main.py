from cliente import criar_cliente
from conta import criacao_de_conta, consultar_saldo, depositar, sacar

# cliente
cliente, cpf = criar_cliente('Bruno', '12345678900')

# conta
numero_da_conta, cpf, usuario, saldo_atual = criacao_de_conta(cliente, cpf)
print("     Sua conta foi criada com sucesso!    ")
print("Número da conta:", numero_da_conta)
print("Usuário:", cliente)
print("Saldo:", saldo_atual)

# consultar saldo
saldo_atual = consultar_saldo(saldo_atual)
print("Seu saldo:", saldo_atual)

# depósito
saldo_atual = depositar(saldo_atual, 500)
print("Depósito realizado com sucesso!")

# consultando saldo após depósito 
saldo_atual = consultar_saldo(saldo_atual)
print("Seu saldo:", saldo_atual)

# saque
saldo_atual = sacar(saldo_atual, 200)
print("Saque realizado com sucesso!")

# consultando saldo após saque 
saldo_atual = consultar_saldo(saldo_atual)
print("Seu saldo:", saldo_atual)
