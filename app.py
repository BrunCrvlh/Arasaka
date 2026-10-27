from flask import Flask, render_template, request, redirect, url_for, flash, session
from cliente import clientes, criar_cliente, buscar_cliente_por_cpf
from agencia import agencias, criar_agencia, buscar_agencia_por_codigo, montante_total_agencia
from conta import contas, criacao_de_conta, buscar_conta_por_numero, depositar, sacar, transferir, montante_total_banco
from dados_no_json import salvar_dados_gerais_do_banco

app = Flask(__name__) #cria o site
app.secret_key = "bolas"   #qualquer coisa pro session e pro flash funcionarem
ADMIN_SENHA = "arasaka"    #senha da gerencia


#salva tudo. sempre q algo é criado ou operado, ela chama salvar(), senão perde tudo quando fecha
def salvar():
    salvar_dados_gerais_do_banco(clientes, agencias, contas)


#deixa o valor bonito: 1234.5 vai pra R$ 1.234,50 (usado nos templates como filtro "brl")
def brl(valor):
    texto = "{:,.2f}".format(valor)
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ " + texto

app.add_template_filter(brl, "brl")


#confere o texto antes de converter pra float
def ler_valor(texto):
    texto = texto.strip().replace(",", ".")
    partes = texto.split(".")
    if len(partes) > 2:
        return None
    for p in partes:
        if not p.isdigit():
            return None
    return float(texto)

#tira . e - do cpf
def limpar_cpf(texto):
    return texto.replace(".", "").replace("-", "").strip()

#confere se o cpf é valido (11 numeros, 2 verificadores)
def cpf_valido(cpf):
    if not cpf.isdigit() or len(cpf) != 11:
        return False

    # 1111111111, 2222222 e por ai vai, nao existem
    if cpf == cpf[0] * 11:
        return False

    #primeiro verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = (soma * 10) % 11
    if resto == 10:
        resto = 0
    if resto != int(cpf[9]):
        return False

    # segundo verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = (soma * 10) % 11
    if resto == 10:
        resto = 0
    return resto == int(cpf[10])


#devolve a conta de quem esta logado (ou None se ninguem ta logado)
def conta_logada():
    numero = session.get("numero")
    if numero is None:
        return None
    return buscar_conta_por_numero(numero)


#renderiza o html
@app.route("/")
def index():
    return render_template("index.html")

#percorre as info das contas criadas procurando login e senha iguais. se achar, session["numero"] = número da conta e entra
@app.route("/entrar", methods=["GET", "POST"])
def entrar():
    if request.method == "POST":
        login = request.form["login"].strip()
        senha = request.form["senha"]
        for conta in contas:
            if conta["login"] == login and conta["senha"] == senha:
                session.clear()
                session["numero"] = conta["numero"]
                return redirect(url_for("painel"))
        flash("Credenciais inválidas. Acesso negado.", "erro")
    return render_template("entrar.html")

#volta pro início
@app.route("/sair")
def sair():
    session.clear()
    flash("Sessão encerrada.", "ok")
    return redirect(url_for("index"))

#valida tudo na ordem (campos vazios, cpf, agência, login repetido e tals), se passar, cria o cliente e a conta, salva e manda pro login. 
@app.route("/abrir-conta", methods=["GET", "POST"])
def abrir_conta():
    if request.method == "POST":
        nome = request.form["nome"].strip()
        cpf = limpar_cpf(request.form["cpf"])
        codigo = request.form["codigo_agencia"]
        login = request.form["login"].strip()
        senha = request.form["senha"]
        tipo = request.form["tipo"]

        login_em_uso = False
        for conta in contas:
            if conta["login"] == login:
                login_em_uso = True

        if nome == "" or login == "" or senha == "":
            flash("Preencha todos os campos.", "erro")
        elif not cpf_valido(cpf):
            flash("CPF inválido. Confira os números digitados.", "erro")
        elif buscar_agencia_por_codigo(codigo) is None:
            flash("Escolha uma agência válida.", "erro")
        elif login_em_uso:
            flash("Esse login já está em uso.", "erro")
        else:
            if buscar_cliente_por_cpf(cpf) is None:
                criar_cliente(nome, cpf)
            criadas = criacao_de_conta([cpf], codigo, login, senha, tipo)
            if criadas is None:
                flash("Tipo de conta inválido.", "erro")
            else:
                salvar()
                flash("Conta aberta! Número da sua conta: %d. Faça login para acessar." % criadas[0]["numero"], "ok")
                return redirect(url_for("entrar"))
    return render_template("abrir_conta.html", agencias=agencias)


#manda pro painel.html a conta, o cliente, a agência e as 5 últimas movimentações
def painel():
    conta = conta_logada()
    if conta is None:
        flash("Identifique-se para acessar o terminal.", "erro")
        return redirect(url_for("entrar"))

    return render_template("painel.html", conta=conta,
                           cliente=buscar_cliente_por_cpf(conta["cpf"]),
                           agencia=buscar_agencia_por_codigo(conta["codigo_agencia"]),
                           ultimos=conta.get("extrato", [])[-5:][::-1])

#olha o campo operacao (depositar, sacar ou transferir). saque e transferência pedem a senha, e transferência confere o destino. depois 
#chama as suas funções e salva
@app.route("/operacoes", methods=["GET", "POST"])
def operacoes():
    conta = conta_logada()
    if conta is None:
        flash("Identifique-se para acessar o terminal.", "erro")
        return redirect(url_for("entrar"))

    if request.method == "POST":
        operacao = request.form["operacao"]
        valor = ler_valor(request.form.get("valor", ""))

        if valor is None or valor <= 0:
            flash("Valor inválido.", "erro")
        elif operacao == "depositar":
            depositar(conta["numero"], valor)
            salvar()
            flash("Depósito de %s efetuado." % brl(valor), "ok")
        elif request.form.get("senha", "") != conta["senha"]:
            flash("Senha de confirmação incorreta. Operação bloqueada.", "erro")
        elif operacao == "sacar":
            if sacar(conta["numero"], valor):
                salvar()
                flash("Saque de %s efetuado." % brl(valor), "ok")
            else:
                flash("Saldo insuficiente.", "erro")
        elif operacao == "transferir":
            texto = request.form.get("destino", "").strip()
            destino = None
            if texto.isdigit():
                destino = buscar_conta_por_numero(int(texto))
            if destino is None:
                flash("Conta de destino não encontrada.", "erro")
            elif destino["numero"] == conta["numero"]:
                flash("Você não pode transferir para a própria conta.", "erro")
            elif transferir(conta["numero"], destino["numero"], valor):
                salvar()
                titular = buscar_cliente_por_cpf(destino["cpf"])
                flash("Transferência de %s enviada para %s (conta %d)." % (brl(valor), titular["Nome"], destino["numero"]), "ok")
            else:
                flash("Saldo insuficiente.", "erro")
        return redirect(url_for("operacoes"))
    return render_template("operacoes.html", conta=conta)

#só manda a lista de movimentacao
@app.route("/extrato")
def extrato():
    conta = conta_logada()
    if conta is None:
        flash("Identifique-se para acessar o terminal.", "erro")
        return redirect(url_for("entrar"))

    return render_template("extrato.html", conta=conta, linhas=conta.get("extrato", [])[::-1])


#compara a senha do admin com a senha digitada e entra
@app.route("/admin/entrar", methods=["GET", "POST"])
def admin_entrar():
    if request.method == "POST":
        if request.form["senha"] == ADMIN_SENHA:
            session.clear()
            session["admin"] = True
            return redirect(url_for("admin"))
        flash("Código de acesso incorreto.", "erro")
    return render_template("admin_entrar.html")

#monta uma lista com as informacoes e manda pro painelzinho do site
@app.route("/admin")
def admin():
    if not session.get("admin"):
        flash("Acesso restrito à gerência.", "erro")
        return redirect(url_for("admin_entrar"))

    por_agencia = []
    for ag in agencias:
        codigo = ag["Codigo da agencia"]
        qtd = 0
        for conta in contas:
            if conta["codigo_agencia"] == codigo:
                qtd += 1
        por_agencia.append({"agencia": ag, "qtd": qtd, "total": montante_total_agencia(codigo, contas)})
    return render_template("admin.html", qtd_clientes=len(clientes), qtd_agencias=len(agencias),
                           qtd_contas=len(contas), total=montante_total_banco(), por_agencia=por_agencia)

#listagem e cadastramento de agências
@app.route("/admin/agencias", methods=["GET", "POST"])
def admin_agencias():
    if not session.get("admin"):
        flash("Acesso restrito à gerência.", "erro")
        return redirect(url_for("admin_entrar"))

    if request.method == "POST":
        codigo = request.form["codigo"].strip()
        nome = request.form["nome"].strip()
        cidade = request.form["cidade"].strip()
        if codigo == "" or nome == "" or cidade == "":
            flash("Preencha todos os campos.", "erro")
        elif criar_agencia(codigo, nome, cidade) is None:
            flash("Código de agência já cadastrado.", "erro")
        else:
            salvar()
            flash("Agência cadastrada.", "ok")
        return redirect(url_for("admin_agencias"))
    return render_template("admin_agencias.html", agencias=agencias)

#literalmente lista os clientes
@app.route("/admin/clientes")
def admin_clientes():
    if not session.get("admin"):
        flash("Acesso restrito à gerência.", "erro")
        return redirect(url_for("admin_entrar"))

    return render_template("admin_clientes.html", clientes=clientes)

#lista das contas
@app.route("/admin/contas")
def admin_contas():
    if not session.get("admin"):
        flash("Acesso restrito à gerência.", "erro")
        return redirect(url_for("admin_entrar"))

    filtro = request.args.get("cpf", "").strip()
    lista = []
    for conta in contas:
        if filtro == "" or conta["cpf"] == limpar_cpf(filtro):
            lista.append(conta)
    return render_template("admin_contas.html", contas=lista, filtro=filtro)
