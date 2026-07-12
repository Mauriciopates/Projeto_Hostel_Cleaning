# ============================================================
# utils.py - FUNCOES AUXILIARES
# ============================================================
# Modulo com funcoes reutilizaveis para todo o sistema:
# - Cores no terminal
# - Validacoes de dados
# - Formatacao de valores
# - Inputs com validacao
# ============================================================

import re
from datetime import datetime

# ------------------------------------------------------------
# 1. CORES PARA O TERMINAL
# ------------------------------------------------------------

CORES = {
    "preto": "\033[30m",
    "vermelho": "\033[31m",
    "verde": "\033[32m",
    "amarelo": "\033[33m",
    "azul": "\033[34m",
    "magenta": "\033[35m",
    "ciano": "\033[36m",
    "branco": "\033[37m",
    "fundo_preto": "\033[40m",
    "fundo_vermelho": "\033[41m",
    "fundo_verde": "\033[42m",
    "fundo_amarelo": "\033[43m",
    "fundo_azul": "\033[44m",
    "fundo_magenta": "\033[45m",
    "fundo_ciano": "\033[46m",
    "fundo_branco": "\033[47m",
    "negrito": "\033[1m",
    "italico": "\033[3m",
    "sublinhado": "\033[4m",
    "reset": "\033[0m",
}


def cor(texto, cor_texto=None, cor_fundo=None, estilo=None):
    """
    Aplica cores e estilos ao texto para exibicao no terminal.

    Parametros:
        texto (str): Texto a ser colorido
        cor_texto (str): Cor do texto (ex: "vermelho", "verde")
        cor_fundo (str): Cor do fundo (ex: "fundo_azul")
        estilo (str): Estilo do texto (ex: "negrito", "sublinhado")

    Retorna:
        str: Texto com os codigos ANSI aplicados
    """
    codigos = []

    if cor_texto and cor_texto in CORES:
        codigos.append(CORES[cor_texto])

    if cor_fundo and cor_fundo in CORES:
        codigos.append(CORES[cor_fundo])

    if estilo and estilo in CORES:
        codigos.append(CORES[estilo])

    if not codigos:
        return texto

    return "".join(codigos) + texto + CORES["reset"]


# ------------------------------------------------------------
# 2. CABECALHOS E SEPARADORES
# ------------------------------------------------------------


def cabecalho(titulo, largura=60, caractere="="):
    """
    Cria um cabecalho formatado com titulo centralizado.

    Parametros:
        titulo (str): Titulo do cabecalho
        largura (int): Largura total do cabecalho
        caractere (str): Caractere para a linha

    Retorna:
        str: Cabecalho formatado
    """
    espacos = largura - len(titulo) - 2
    if espacos < 0:
        espacos = 0

    esquerda = espacos // 2
    direita = espacos - esquerda

    return f"{caractere * esquerda} {titulo} {caractere * direita}"


def linha_separadora(largura=60, caractere="-"):
    """
    Cria uma linha separadora.

    Parametros:
        largura (int): Largura da linha
        caractere (str): Caractere para a linha

    Retorna:
        str: Linha formatada
    """
    return caractere * largura


# ------------------------------------------------------------
# 3. VALIDACOES
# ------------------------------------------------------------


def validar_email(email):
    """
    Valida um endereco de email usando expressao regular.

    Parametros:
        email (str): Email a ser validado

    Retorna:
        bool: True se valido, False se invalido
    """
    padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(padrao, email))


def validar_telefone(telefone):
    """
    Valida um numero de telefone (formato Portugues).
    Aceita: 912345678, 912 345 678, +351 912345678

    Parametros:
        telefone (str): Telefone a ser validado

    Retorna:
        bool: True se valido, False se invalido
    """
    telefone_limpo = re.sub(r"[\s\-\(\)]", "", telefone)
    padrao = r"^(\+351)?9[1236]\d{7}$"
    return bool(re.match(padrao, telefone_limpo))


def validar_nif(nif):
    """
    Valida um NIF Portugues (9 digitos).

    Parametros:
        nif (str): NIF a ser validado

    Retorna:
        bool: True se valido, False se invalido
    """
    nif_limpo = re.sub(r"\s", "", nif)
    padrao = r"^[1235689]\d{8}$"
    return bool(re.match(padrao, nif_limpo))


def validar_data(data_str, formato="%Y-%m-%d"):
    """
    Valida se uma string corresponde a uma data valida.

    Parametros:
        data_str (str): Data em formato texto
        formato (str): Formato esperado (default: YYYY-MM-DD)

    Retorna:
        bool: True se valido, False se invalido
    """
    try:
        datetime.strptime(data_str, formato)
        return True
    except ValueError:
        return False


def validar_documento(documento):
    """
    Valida um documento de identificacao (passaporte ou CC).
    Aceita: AA123456 (passaporte) ou 12345678 (CC)

    Parametros:
        documento (str): Documento a ser validado

    Retorna:
        bool: True se valido, False se invalido
    """
    documento_limpo = re.sub(r"\s", "", documento)

    # Passaporte: 2 letras + 6 digitos
    padrao1 = r"^[A-Za-z]{2}\d{6}$"
    # CC: 8 digitos
    padrao2 = r"^\d{8}$"

    return bool(re.match(padrao1, documento_limpo)) or bool(
        re.match(padrao2, documento_limpo)
    )


# ------------------------------------------------------------
# 4. FORMATACAO
# ------------------------------------------------------------


def formatar_preco(valor):
    """
    Formata um valor para exibicao como preco em Euros.

    Parametros:
        valor (float): Valor a ser formatado

    Retorna:
        str: Preco formatado (ex: 250,00 €)
    """
    return f"{valor:.2f} €"


def formatar_data(data_str, formato_entrada="%Y-%m-%d", formato_saida="%d/%m/%Y"):
    """
    Converte uma data de um formato para outro.

    Parametros:
        data_str (str): Data em formato texto
        formato_entrada (str): Formato atual da data
        formato_saida (str): Formato desejado

    Retorna:
        str: Data no novo formato, ou string vazia se invalida
    """
    try:
        data = datetime.strptime(data_str, formato_entrada)
        return data.strftime(formato_saida)
    except ValueError:
        return ""


def formatar_data_hora(
    data_str, formato_entrada="%Y-%m-%d %H:%M:%S", formato_saida="%d/%m/%Y %H:%M"
):
    """
    Converte uma data/hora para exibicao.

    Parametros:
        data_str (str): Data/hora em formato texto
        formato_entrada (str): Formato atual
        formato_saida (str): Formato desejado

    Retorna:
        str: Data/hora no novo formato, ou string vazia se invalida
    """
    try:
        data = datetime.strptime(data_str, formato_entrada)
        return data.strftime(formato_saida)
    except ValueError:
        return ""


def obter_data_atual(formato="%Y-%m-%d %H:%M:%S"):
    """
    Retorna a data e hora atual no formato especificado.

    Parametros:
        formato (str): Formato desejado

    Retorna:
        str: Data/hora atual
    """
    return datetime.now().strftime(formato)


# ------------------------------------------------------------
# 5. INPUTS COM VALIDACAO
# ------------------------------------------------------------


def input_obrigatorio(mensagem, erro="Este campo e obrigatorio."):
    """
    Solicita um input obrigatorio ao utilizador.
    Nao aceita valores vazios.

    Parametros:
        mensagem (str): Mensagem exibida ao utilizador
        erro (str): Mensagem de erro se o campo estiver vazio

    Retorna:
        str: Valor informado pelo utilizador
    """
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print(cor(erro, "vermelho"))


def input_email(mensagem="Email: "):
    """
    Solicita um email e valida o formato.

    Parametros:
        mensagem (str): Mensagem exibida ao utilizador

    Retorna:
        str: Email valido informado pelo utilizador
    """
    while True:
        email = input(mensagem).strip()
        if validar_email(email):
            return email
        print(cor("Email invalido. Tente novamente.", "vermelho"))


def input_telefone(mensagem="Telefone: "):
    """
    Solicita um telefone e valida o formato.

    Parametros:
        mensagem (str): Mensagem exibida ao utilizador

    Retorna:
        str: Telefone valido informado pelo utilizador
    """
    while True:
        telefone = input(mensagem).strip()
        if validar_telefone(telefone):
            return telefone
        print(cor("Telefone invalido. Use: 912345678 ou +351 912345678", "vermelho"))


def input_nif(mensagem="NIF (opcional): ", obrigatorio=False):
    """
    Solicita um NIF e valida o formato (opcional).

    Parametros:
        mensagem (str): Mensagem exibida ao utilizador
        obrigatorio (bool): Se True, o campo e obrigatorio

    Retorna:
        str: NIF valido informado, ou string vazia se opcional e vazio
    """
    while True:
        nif = input(mensagem).strip()

        if not obrigatorio and not nif:
            return ""

        if validar_nif(nif):
            return nif
        print(cor("NIF invalido. Deve ter 9 digitos.", "vermelho"))


def input_data(mensagem="Data (YYYY-MM-DD): ", obrigatorio=True):
    """
    Solicita uma data e valida o formato.

    Parametros:
        mensagem (str): Mensagem exibida ao utilizador
        obrigatorio (bool): Se True, o campo e obrigatorio

    Retorna:
        str: Data valida informada, ou string vazia se opcional e vazio
    """
    while True:
        data = input(mensagem).strip()

        if not obrigatorio and not data:
            return ""

        if validar_data(data):
            return data
        print(cor("Data invalida. Use o formato YYYY-MM-DD", "vermelho"))


def input_documento(mensagem="Documento (Passaporte ou CC): ", obrigatorio=True):
    """
    Solicita um documento e valida o formato.

    Parametros:
        mensagem (str): Mensagem exibida ao utilizador
        obrigatorio (bool): Se True, o campo e obrigatorio

    Retorna:
        str: Documento valido informado, ou string vazia se opcional e vazio
    """
    while True:
        documento = input(mensagem).strip()

        if not obrigatorio and not documento:
            return ""

        if validar_documento(documento):
            return documento
        print(
            cor(
                "Documento invalido. Use: AA123456 (passaporte) ou 12345678 (CC)",
                "vermelho",
            )
        )


def input_float(mensagem="Valor: ", obrigatorio=True, min_valor=None, max_valor=None):
    """
    Solicita um valor numerico (float) com validacao.

    Parametros:
        mensagem (str): Mensagem exibida ao utilizador
        obrigatorio (bool): Se True, o campo e obrigatorio
        min_valor (float): Valor minimo permitido
        max_valor (float): Valor maximo permitido

    Retorna:
        float: Valor informado, ou None se opcional e vazio
    """
    while True:
        valor_str = input(mensagem).strip()

        if not obrigatorio and not valor_str:
            return None

        try:
            valor = float(valor_str.replace(",", "."))

            if min_valor is not None and valor < min_valor:
                print(
                    cor(f"Valor deve ser maior ou igual a {min_valor:.2f}", "vermelho")
                )
                continue

            if max_valor is not None and valor > max_valor:
                print(
                    cor(f"Valor deve ser menor ou igual a {max_valor:.2f}", "vermelho")
                )
                continue

            return valor

        except ValueError:
            print(cor("Valor invalido. Use um numero (ex: 250.50)", "vermelho"))


def input_int(mensagem="Numero: ", obrigatorio=True, min_valor=None, max_valor=None):
    """
    Solicita um valor numerico (inteiro) com validacao.

    Parametros:
        mensagem (str): Mensagem exibida ao utilizador
        obrigatorio (bool): Se True, o campo e obrigatorio
        min_valor (int): Valor minimo permitido
        max_valor (int): Valor maximo permitido

    Retorna:
        int: Valor informado, ou None se opcional e vazio
    """
    while True:
        valor_str = input(mensagem).strip()

        if not obrigatorio and not valor_str:
            return None

        try:
            valor = int(valor_str)

            if min_valor is not None and valor < min_valor:
                print(cor(f"Valor deve ser maior ou igual a {min_valor}", "vermelho"))
                continue

            if max_valor is not None and valor > max_valor:
                print(cor(f"Valor deve ser menor ou igual a {max_valor}", "vermelho"))
                continue

            return valor

        except ValueError:
            print(cor("Valor invalido. Digite um numero inteiro.", "vermelho"))


def input_opcao(mensagem, opcoes, sair=False):
    """
    Solicita uma opcao de uma lista de opcoes validas.

    Parametros:
        mensagem (str): Mensagem exibida ao utilizador
        opcoes (list): Lista de opcoes validas
        sair (bool): Se True, adiciona opcao "0" para sair

    Retorna:
        str: Opcao selecionada
    """
    opcoes_formatadas = ", ".join(opcoes)
    if sair:
        opcoes_formatadas += ", 0 (Sair)"

    while True:
        opcao = input(f"{mensagem} ({opcoes_formatadas}): ").strip()

        if sair and opcao == "0":
            return "0"

        if opcao in opcoes:
            return opcao

        print(cor(f"Opcao invalida. Escolha: {opcoes_formatadas}", "vermelho"))


def input_sim_nao(mensagem="Confirmar? (S/N): "):
    """
    Solicita uma confirmacao SIM/NAO.

    Parametros:
        mensagem (str): Mensagem exibida ao utilizador

    Retorna:
        bool: True se SIM, False se NAO
    """
    while True:
        resposta = input(mensagem).strip().upper()
        if resposta in ["S", "SIM", "Y", "YES"]:
            return True
        if resposta in ["N", "NAO", "NO"]:
            return False
        print(cor("Resposta invalida. Digite S ou N.", "vermelho"))


# ------------------------------------------------------------
# 6. BLOCO DE TESTE
# ------------------------------------------------------------

if __name__ == "__main__":

    print("\nTESTANDO MODULO DE UTILS")
    print("=" * 30)

    # Teste de cores
    print(cor("Texto em vermelho", "vermelho"))
    print(cor("Texto em verde negrito", "verde", estilo="negrito"))
    print(cor("Texto com fundo azul", cor_fundo="fundo_azul"))

    # Teste de cabecalho
    print("\n" + cabecalho("TESTE DE CABECALHO"))
    print(linha_separadora())

    # Teste de validacoes
    print("\nTestes de validacao:")
    print(f"  Email valido: {validar_email('teste@email.com')}")
    print(f"  Email invalido: {validar_email('teste@email')}")
    print(f"  Telefone valido: {validar_telefone('912345678')}")
    print(f"  Telefone valido: {validar_telefone('+351 912345678')}")
    print(f"  Telefone invalido: {validar_telefone('123456789')}")
    print(f"  NIF valido: {validar_nif('123456789')}")
    print(f"  NIF invalido: {validar_nif('12345678')}")
    print(f"  Documento valido: {validar_documento('AB123456')}")
    print(f"  Documento valido: {validar_documento('12345678')}")
    print(f"  Documento invalido: {validar_documento('AB12345')}")

    # Teste de formatacao
    print("\nTestes de formatacao:")
    print(f"  Preco: {formatar_preco(250.50)}")
    print(f"  Data: {formatar_data('2025-01-15')}")
    print(f"  Data/Hora atual: {obter_data_atual()}")

    # Teste de inputs (comentados para nao travar o teste)
    print("\nTestes de input (comentados para nao travar):")
    print("  # email = input_email()")
    print("  # telefone = input_telefone()")
    print("  # data = input_data()")

    print("\nTeste concluido com sucesso!")
