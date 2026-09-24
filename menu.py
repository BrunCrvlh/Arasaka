from cliente import (criar_cliente, buscar_cliente_por_cpf, listar_clientes, definir_clientes, clientes)
from conta import (criacao_de_conta, consultar_saldo, depositar, sacar, transferir, listar_contas, montante_total_banco, definir_contas, contas)
from agencia import (criar_agencia, listar_agencias, buscar_agencia_por_codigo, montante_total_agencia, definir_agencias, agencias)

def menu_de_opcoes():
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
 
        if opcao == "0":
            print("Sessão finalizada!")
        
        # Cadastrar cliente
        elif opcao == "1":
            nome = input("Nome do cliente: ")
            cpf = input("CPF: ")
            cliente = criar_cliente(nome, cpf)

            if cliente is not None:
                print("Cliente cadastrado com sucesso!")

        # Cadastrar conta
        elif opcao == "2":
            cpf = input("CPF do cliente: ")
            numero = input("Numero da conta que deseja: ")
            codigo_agencia = input("Código da agência: ")

            cliente = buscar_cliente_por_cpf(cpf)
            agencia = buscar_agencia_por_codigo(codigo_agencia)

            if cliente == None:
                print("Cliente não encontrado!")                
             
            elif agencia is None:
                print("Agência não encontrada!")
                print('Crie sua conta: ')
                login = input("Seu login: ")
                senha = input("Sua senha: ")

                cpfs = [cpf]

                contas_criadas = criacao_de_conta(cpfs, codigo_agencia, login, senha)

                print("Conta criada com sucesso!")
                print("Número da conta:", contas_criadas[0][0])

        # Cadastrar agência
        elif opcao == "3":

            codigo = input("Código da agência: ")
            nome = input("Nome da agência: ")
            cidade = input("Cidade: ")

            agencia = criar_agencia(codigo, nome, cidade)

            if agencia is not None:
                print("Agência cadastrada com sucesso!")

        # Listar contas
        elif opcao == "4":
            listar_contas()

        # Lista agências
        elif opcao == "5":
            listar_agencias()

        # Listar clientes
        elif opcao == "6":
            listar_clientes()

        # Sacar
        elif opcao == "7":
            numero = int(input("Número da conta: "))
            valor = float(input("Valor do saque: "))

            if sacar(numero, valor):
                print("Saque realizado com sucesso!")

        # Transferir
        elif opcao == "8":
            origem = int(input("Conta de origem: "))
            destino = int(input("Conta de destino: "))
            valor = float(input("Valor da transferência: "))

            if transferir(origem, destino, valor):
                print("Transferência realizada com sucesso!")

        # Depositar
        elif opcao == "9":
            numero = int(input("Número da conta: "))
            valor = float(input("Valor do depósito: "))

            if depositar(numero, valor):
                print("Depósito realizado com sucesso!")

        # Consultar saldo
        elif opcao == "10":
            numero = int(input("Número da conta: "))
            saldo = consultar_saldo(numero)

            if saldo is not None:
                print("Saldo: R$", saldo)

        # Relatório do banco
        elif opcao == "11":
            print("\n========== RELATÓRIO DO BANCO ==========")
            print("Quantidade de clientes:", len(clientes))
            print("Quantidade de agências:", len(agencias))
            print("Quantidade de contas:", len(contas))
            print("Montante total do banco: R$", montante_total_banco())

        # Montante total da agência
        elif opcao == "12":
             codigo = input("Código da agência: ")
             agencia = buscar_agencia_por_codigo(codigo)

             if agencia == None:
                 print("Agência não encontrada!")
             else:
                 total = montante_total_agencia(codigo, contas)
                 print("Montante total da agência: R$",total)

        # Montante total do banco
        elif opcao == "13":
            print("Montante total do banco: R$", montante_total_banco())
            
        else:
            if opcao == "0"
                print("Sessão encerrada")
            else:
                print("Opção inválida!")
        
