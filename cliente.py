# tira os pontos e o traço do cpf antes de conferir os números
def limpar_cpf(texto):
    return texto.strip().replace('.', '').replace('-', '')


# confere o tamanho e os dois últimos dígitos do cpf
def cpf_valido(cpf):
    if len(cpf) != 11 or not cpf.isascii() or not cpf.isdigit():
        return False
    if cpf == cpf[0] * 11:
        return False
    for quantidade in range(9, 11):
        soma = 0
        for i in range(quantidade):
            soma += int(cpf[i]) * (quantidade + 1 - i)
        digito = (soma * 10) % 11
        if digito == 10:
            digito = 0
        if digito != int(cpf[quantidade]):
            return False
    return True



# cada cliente guarda nome e cpf, agora num objeto em vez de dicionário
class Cliente:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf

    # pega só o primeiro nome pra aparecer no olá do painel
    def primeiro_nome(self):
        return self.nome.split()[0]

    # só coloca os pontos e o traço pra mostrar o cpf bonitinho no site
    def cpf_formatado(self):
        return (self.cpf[:3] + '.' + self.cpf[3:6] + '.' +
                self.cpf[6:9] + '-' + self.cpf[9:])

    # o json não salva o objeto direto, então monta um dicionário com os dados
    def para_dicionario(self):
        return {'Nome': self.nome, 'CPF': self.cpf}
