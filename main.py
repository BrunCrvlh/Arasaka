import os
import sys
from app import app, criar_app


def criar_demo(caminho=None):
    if caminho is None:
        caminho = os.path.join(os.path.dirname(__file__), 'dados_demo.json')
    app = criar_app(caminho)
    banco = app.banco
    if len(banco.listar_contas()) == 0:
        ana, mensagem = banco.abrir_conta('Ana Souza', '52998224725', '001',
                                         'ana', '123', 'corrente')
        bruno, mensagem = banco.abrir_conta('Bruno Silva', '11144477735', '001',
                                           'bruno', '123', 'poupança')
        salario, mensagem = banco.abrir_conta('Ana Souza', '52998224725', '001',
                                             'ana_salario', '123', 'salário')
        ana.depositar(248050)
        ana.transferir(bruno, 12000)
        ana.sacar(8000)
        salario.depositar(150000)
        app.repositorio.salvar(banco)
    return app



if __name__ == '__main__':
    # com --demo abre as contas de exemplo, sem mexer nos dados do banco normal
    if '--demo' in sys.argv:
        print('Logins de exemplo: ana, bruno ou ana_salario. A senha é 123.')
        criar_demo().run(debug=True)
    else:
        app.run(debug=True)
