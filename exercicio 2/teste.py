import funcoes

def executar(nome_funcao, var1, var2=None):
    funcao = getattr(funcoes, nome_funcao, None)

    if not funcao:
        raise Exception(f"Função '{nome_funcao}' não existe")

    return funcao(var1, var2)


if __name__ == "__main__":
    try:
        nome = input('entre com o nome da função:')
        var1 = input('entre com o valor da primeira variavel:')
        var2 = input('entre com o valor da segunda variavel caso houver: ')
        print(executar(nome, var1, var2))
    except Exception as e:
        print(f"Erro: {e}")