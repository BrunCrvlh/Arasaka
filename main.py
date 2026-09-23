from cliente import (criar_cliente, buscar_cliente_por_cpf, listar_clientes, definir_clientes, clientes)

from conta import (criacao_de_conta, consultar_saldo, depositar, sacar, transferir, listar_contas, montante_total_banco, definir_contas, contas)

from agencia import (criar_agencia, listar_agencias, buscar_agencia_por_codigo, montante_total_agencia, definir_agencias, agencias)

from dados_no_json import (salvar_dados_gerais_do_banco, carrega_dados_gerais_do_banco)

clientes_salvos, agencias_salvas, contas_salvas = carrega_dados_gerais_do_banco()
definir_clientes(clientes_salvos)
definir_agencias(agencias_salvas)
definir_contas(contas_salvas)

def menu():
    opcao = ""
    while opcao != "0": 
        print("\n========== MENU DO BANCO ==========")
        print("1 - Cadastrar clientes")
        print("2 - Cadastrar contas")
        print("3 - Cadastrar agências")
        print("4 - Listar Contas")
        print("5 - Listar Agências")
        print("6 - Listar Clientes")
        print("7 - Sacar")
        print("8 - Transferir")
        print("9 - Depositar")
        print("10 - Consultar Saldo")
        print("11 - Relatório do banco")
        print("12 - Montante Total da Agência")
        print("13 - Montante Total do Banco")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")
        
        # Cadastrar cliente
        if opcao == "2":
            nome = input("Nome do cliente: ")
            cpf = input("CPF: ")
            cliente = criar_cliente(nome, cpf)

            if cliente != ():
                print("Cliente cadastrado com sucesso!")

        # Cadastrar conta
        elif opcao == "3":
            cpf = input("CPF do cliente: ")
            codigo_agencia = input("Código da agência: ")

            cliente = buscar_cliente_por_cpf(cpf)

            if cliente == ():
                print("Cliente não encontrado!")

            agencia = buscar_agencia_por_codigo(codigo_agencia)

            elif agencia ():
                print("Agência não encontrada!")
            login = input("Login: ")
            senha = input("Senha: ")

            conta = criacao_de_conta(cpf, codigo_agencia, login, senha)
            print("Conta criada com sucesso!")
            print("Número da conta:", conta[0])

        # Cadastrar agência
        elif opcao == "4":

            codigo = input("Código da agência: ")
            nome = input("Nome da agência: ")
            cidade = input("Cidade: ")

            agencia = criar_agencia(codigo, nome, cidade)

            if agencia != ():
                print("Agência cadastrada com sucesso!")

        # Listar contas
        elif opcao == "5":
            listar_contas()

        # Lista agências
        elif opcao == "6":
            listar_agencias()

        # Listar clientes
        elif opcao == "7":
            listar_clientes()

        # Sacar
        elif opcao == "8":
            numero = int(input("Número da conta: "))
            valor = float(input("Valor do saque: "))

            if sacar(numero, valor):
                print("Saque realizado com sucesso!")

        # Transferir
        elif opcao == "9":
            origem = int(input("Conta de origem: "))
            destino = int(input("Conta de destino: "))
            valor = float(input("Valor da transferência: "))

            if transferir(origem, destino, valor):
                print("Transferência realizada com sucesso!")

        # Depositar
        elif opcao == "10":
            numero = int(input("Número da conta: "))
            valor = float(input("Valor do depósito: "))

            if depositar(numero, valor):
                print("Depósito realizado com sucesso!")

        # Consultar saldo
        elif opcao == "11":
            numero = int(input("Número da conta: "))
            saldo = consultar_saldo(numero)

            if saldo is not None:
                print("Saldo: R$", saldo)

        # Relatório do banco
        elif opcao == "12":
            print("\n========== RELATÓRIO DO BANCO ==========")
            print("Quantidade de clientes:", len(clientes))
            print("Quantidade de agências:", len(agencias))
            print("Quantidade de contas:", len(contas))
            print("Montante total do banco: R$", montante_total_banco())

        # Montante total da agência
        elif opcao == "13":
            codigo = input("Código da agência: ")
            agencia = buscar_agencia_por_codigo(codigo)

            if agencia == ():
                print("Agência não encontrada!")
            else:
                total = montante_total_agencia(codigo, contas)
                print("Montante total da agência: R$",total)

        # Montante total do banco
        elif opcao == "14":
            print("Montante total do banco: R$", montante_total_banco())
            
        else:
            print("Opção inválida!")
            
print("Sessão encerrada.")            
salvar_dados_gerais_do_banco(clientes, agencias, contas)
menu()
