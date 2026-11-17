import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from dados_no_json import RepositorioJSON
from conta import brl, ler_valor


# monta o flask e carrega o banco antes de abrir as páginas
def criar_app(caminho_dados=None):
    app = Flask(__name__)
    app.secret_key = 'arasaka-projeto-academico-local'
    app.config['ADMIN_SENHA'] = 'arasaka'
    if caminho_dados is None:
        caminho_dados = os.path.join(os.path.dirname(__file__), 'dados.json')
    repositorio = RepositorioJSON(caminho_dados)
    banco = repositorio.carregar()
    if len(banco.listar_agencias()) == 0:
        banco.cadastrar_agencia('001', 'Agência Central', 'São Cristóvão')
    # deixa o banco e o arquivo acessíveis nos testes também
    app.banco = banco
    app.repositorio = repositorio
    app.add_template_filter(brl, 'brl')

    # pega o número salvo na sessão e procura a conta dele
    def conta_logada():
        return banco.buscar_conta(session.get('numero'))

    def exigir_login():
        flash('Entre na sua conta para continuar.', 'erro')
        return redirect(url_for('entrar'))

    def exigir_gerencia():
        flash('Entre na gerência para continuar.', 'erro')
        return redirect(url_for('admin_entrar'))

    @app.route('/')
    def index():
        return render_template('index.html', pagina='inicio')

    @app.route('/ajuda')
    def ajuda():
        return render_template('index.html', pagina='ajuda')

    # pega os campos do formulário e pede pro banco abrir a conta
    @app.route('/abrir-conta', methods=['GET', 'POST'])
    def abrir_conta():
        if request.method == 'POST':
            conta, mensagem = banco.abrir_conta(
                request.form.get('nome', ''), request.form.get('cpf', ''),
                request.form.get('codigo_agencia', ''), request.form.get('login', ''),
                request.form.get('senha', ''), request.form.get('tipo', ''))
            if conta is None:
                flash(mensagem, 'erro')
            else:
                repositorio.salvar(banco)
                flash('Conta ' + str(conta.numero) + ' aberta! Entre com seu login e senha.', 'ok')
                return redirect(url_for('entrar'))
        return render_template('abrir_conta.html', agencias=banco.listar_agencias(), pagina='abrir')

    @app.route('/entrar', methods=['GET', 'POST'])
    def entrar():
        if request.method == 'POST':
            conta = banco.autenticar(request.form.get('login', ''), request.form.get('senha', ''))
            if conta is None:
                flash('Login ou senha incorretos. Confira e tente novamente.', 'erro')
            else:
                session.clear()
                session['numero'] = conta.numero
                return redirect(url_for('painel'))
        return render_template('entrar.html', pagina='entrar')

    @app.route('/sair')
    def sair():
        session.clear()
        flash('Você saiu da sua conta.', 'ok')
        return redirect(url_for('index'))

    # manda pra página o saldo, os totais e as cinco últimas movimentações
    @app.route('/painel')
    def painel():
        conta = conta_logada()
        if conta is None:
            return exigir_login()
        entradas, saidas = conta.totais_movimentados()
        return render_template('painel.html', conta=conta, pagina='painel',
            entradas=entradas, saidas=saidas, ultimos=conta.consultar_extrato()[-5:][::-1])

    # olha qual operação veio do formulário, confere os dados e chama o método da conta
    @app.route('/operacoes', methods=['GET', 'POST'])
    def operacoes():
        conta = conta_logada()
        if conta is None:
            return exigir_login()
        if request.method == 'POST':
            operacao = request.form.get('operacao', '')
            valor = ler_valor(request.form.get('valor', ''))
            if operacao not in ['depositar', 'sacar', 'transferir']:
                flash('Escolha uma operação disponível.', 'erro')
            elif valor is None or valor <= 0:
                flash('Digite um valor maior que zero, com até duas casas decimais e sem milhar.', 'erro')
            elif operacao != 'depositar' and not conta.autenticar(request.form.get('senha', '')):
                flash('Senha de confirmação incorreta. Nenhum valor foi movimentado.', 'erro')
            elif operacao == 'depositar':
                if conta.depositar(valor):
                    repositorio.salvar(banco)
                    flash('Depósito de ' + brl(valor) + ' realizado.', 'ok')
                else:
                    flash('Não foi possível realizar o depósito.', 'erro')
            elif operacao == 'sacar':
                if conta.sacar(valor):
                    repositorio.salvar(banco)
                    flash('Saque de ' + brl(valor) + ' realizado.', 'ok')
                else:
                    flash('Saldo insuficiente para este saque.', 'erro')
            else:
                texto = request.form.get('destino', '').strip()
                destino = None
                if texto.isascii() and texto.isdigit():
                    destino = banco.buscar_conta(int(texto))
                if destino is None:
                    flash('Conta de destino não encontrada. Confira o número.', 'erro')
                elif destino is conta:
                    flash('Escolha uma conta diferente da sua para transferir.', 'erro')
                elif banco.transferir(conta.numero, destino.numero, valor):
                    repositorio.salvar(banco)
                    flash(brl(valor) + ' transferidos para ' + destino.cliente.nome +
                          ' · Conta ' + str(destino.numero) + '.', 'ok')
                else:
                    flash('Saldo insuficiente para esta transferência.', 'erro')
            return redirect(url_for('operacoes', acao=operacao if operacao in
                ['depositar', 'sacar', 'transferir'] else 'depositar'))
        return render_template('operacoes.html', conta=conta, pagina='operacoes')

    # filtra pelo que entrou ou saiu, e mostra o mais recente primeiro
    @app.route('/extrato')
    def extrato():
        conta = conta_logada()
        if conta is None:
            return exigir_login()
        filtro = request.args.get('tipo', '')
        linhas = []
        for movimento in conta.consultar_extrato()[::-1]:
            if filtro == '' or (filtro == 'entradas' and movimento.entrada()) or (
                filtro == 'saidas' and not movimento.entrada()):
                linhas.append(movimento)
        return render_template('extrato.html', conta=conta, linhas=linhas,
                               filtro=filtro, pagina='extrato')

    @app.route('/admin/entrar', methods=['GET', 'POST'])
    def admin_entrar():
        if request.method == 'POST':
            if request.form.get('senha', '') == app.config['ADMIN_SENHA']:
                session.clear()
                session['admin'] = True
                return redirect(url_for('admin'))
            flash('Senha da gerência incorreta.', 'erro')
        return render_template('admin_entrar.html', pagina='gerencia')

    # a gerência vê os totais, mas precisa entrar com a senha dela primeiro
    @app.route('/admin')
    def admin():
        if not session.get('admin'):
            return exigir_gerencia()
        return render_template('admin.html', pagina='admin',
            qtd_clientes=len(banco.listar_clientes()), qtd_contas=len(banco.listar_contas()),
            qtd_agencias=len(banco.listar_agencias()), total=banco.montante_total(),
            por_agencia=banco.resumo_agencias())

    @app.route('/admin/agencias', methods=['GET', 'POST'])
    def admin_agencias():
        if not session.get('admin'):
            return exigir_gerencia()
        if request.method == 'POST':
            agencia = banco.cadastrar_agencia(request.form.get('codigo', ''),
                request.form.get('nome', ''), request.form.get('cidade', ''))
            if agencia is None:
                flash('Preencha todos os campos e escolha um código ainda não cadastrado.', 'erro')
            else:
                repositorio.salvar(banco)
                flash('Agência cadastrada com sucesso.', 'ok')
                return redirect(url_for('admin_agencias'))
        return render_template('admin_agencias.html', agencias=banco.listar_agencias(), pagina='agencias')

    @app.route('/admin/clientes')
    def admin_clientes():
        if not session.get('admin'):
            return exigir_gerencia()
        return render_template('admin_clientes.html', clientes=banco.listar_clientes(), pagina='clientes')

    @app.route('/admin/contas')
    def admin_contas():
        if not session.get('admin'):
            return exigir_gerencia()
        filtro = request.args.get('cpf', '').strip()
        return render_template('admin_contas.html', contas=banco.listar_contas(filtro),
                               filtro=filtro, pagina='contas')

    return app


app = criar_app()
