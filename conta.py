def criacao_de_conta(cliente):
    numero_da_conta = 260078955
    nome = cliente
    saldo = float(0)
    conta = (numero_da_conta, nome, saldo)
    
    return conta

cliente = "XXXXX"
conta = criacao_de_conta(cliente)

print("         Sua conta foi criada com sucesso!          ")
print("Número da conta: ", conta[0])
print("Cliente: ", conta[1])
print("Saldo: ", conta[2])
