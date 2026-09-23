from menu import menu

clientes_salvos, agencias_salvas, contas_salvas = carrega_dados_gerais_do_banco()
definir_clientes(clientes_salvos)
definir_agencias(agencias_salvas)
definir_contas(contas_salvas)
            
menu()

print("Sessão encerrada.")            
salvar_dados_gerais_do_banco(clientes, agencias, contas)
