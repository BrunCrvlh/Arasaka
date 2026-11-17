# guarda as informações da agência, nada demais
class Agencia:
    def __init__(self, codigo, nome, cidade):
        self.codigo = codigo
        self.nome = nome
        self.cidade = cidade

    # junta o código e o nome pra mostrar nas opções do site
    def identificacao(self):
        return self.codigo + ' · ' + self.nome

    # deixa os dados no formato que vai pro json
    def para_dicionario(self):
        return {'Codigo da agencia': self.codigo,
                'Nome da agencia': self.nome, 'Cidade': self.cidade}
