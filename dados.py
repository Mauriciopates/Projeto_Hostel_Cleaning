# ============================================================
# dados.py - BASE DE DADOS EM MEMORIA
# ============================================================
# Modulo responsavel por armazenar todos os dados do sistema
# em memoria durante a execucao do programa.
# 
# Estrutura: Listas de dicionarios
# Cada lista representa uma entidade do sistema
# ============================================================

# ------------------------------------------------------------
# 1. CONTADORES DE ID
# ------------------------------------------------------------
# Cada entidade possui um identificador unico (ID) gerado
# sequencialmente. Os contadores controlam o proximo ID a ser
# atribuido a cada novo registo.
# ------------------------------------------------------------

contador_unidades = 1
contador_clientes = 1
contador_contratos = 1
contador_produtos = 1
contador_consumos = 1
contador_transacoes = 1
contador_logs = 1


# ------------------------------------------------------------
# 2. LISTAS DE DADOS
# ------------------------------------------------------------
# Cada lista armazena dicionarios representando registos
# da respectiva entidade.
# ------------------------------------------------------------

unidades = []          # Lista de unidades (quartos/estudios)
clientes = []          # Lista de clientes (moradores + airbnb)
contratos = []         # Lista de contratos (mensal) e reservas (airbnb)
produtos = []          # Lista de produtos de stock
consumos = []          # Lista de consumos registados
transacoes = []        # Lista de transacoes financeiras
logs = []              # Lista de logs de auditoria


# ------------------------------------------------------------
# 3. FUNCOES PARA GERACAO DE IDS
# ------------------------------------------------------------
# Cada funcao retorna o ID atual e incrementa o contador
# para o proximo registo.
# ------------------------------------------------------------

def proximo_id_unidade():
    """Retorna o proximo ID disponivel para uma unidade."""
    global contador_unidades
    id_atual = contador_unidades
    contador_unidades += 1
    return id_atual


def proximo_id_cliente():
    """Retorna o proximo ID disponivel para um cliente."""
    global contador_clientes
    id_atual = contador_clientes
    contador_clientes += 1
    return id_atual


def proximo_id_contrato():
    """Retorna o proximo ID disponivel para um contrato ou reserva."""
    global contador_contratos
    id_atual = contador_contratos
    contador_contratos += 1
    return id_atual


def proximo_id_produto():
    """Retorna o proximo ID disponivel para um produto."""
    global contador_produtos
    id_atual = contador_produtos
    contador_produtos += 1
    return id_atual


def proximo_id_consumo():
    """Retorna o proximo ID disponivel para um consumo."""
    global contador_consumos
    id_atual = contador_consumos
    contador_consumos += 1
    return id_atual


def proximo_id_transacao():
    """Retorna o proximo ID disponivel para uma transacao."""
    global contador_transacoes
    id_atual = contador_transacoes
    contador_transacoes += 1
    return id_atual


def proximo_id_log():
    """Retorna o proximo ID disponivel para um log."""
    global contador_logs
    id_atual = contador_logs
    contador_logs += 1
    return id_atual


# ------------------------------------------------------------
# 4. FUNCOES DE MANUTENCAO
# ------------------------------------------------------------

def resetar_dados():
    """
    Reseta todos os dados e contadores para o estado inicial.
    Util para testes e reinicializacao do sistema.
    """
    global contador_unidades, contador_clientes, contador_contratos
    global contador_produtos, contador_consumos, contador_transacoes, contador_logs

    # Limpa as listas
    unidades.clear()
    clientes.clear()
    contratos.clear()
    produtos.clear()
    consumos.clear()
    transacoes.clear()
    logs.clear()

    # Reinicia os contadores
    contador_unidades = 1
    contador_clientes = 1
    contador_contratos = 1
    contador_produtos = 1
    contador_consumos = 1
    contador_transacoes = 1
    contador_logs = 1


def mostrar_estado_dados():
    """
    Exibe um resumo da quantidade de registos em cada lista.
    Util para debug e verificacao do estado do sistema.
    """
    print("\n" + "="*50)
    print("ESTADO DA BASE DE DADOS EM MEMORIA")
    print("="*50)
    print(f"Unidades:    {len(unidades)} registos")
    print(f"Clientes:    {len(clientes)} registos")
    print(f"Contratos:   {len(contratos)} registos")
    print(f"Produtos:    {len(produtos)} registos")
    print(f"Consumos:    {len(consumos)} registos")
    print(f"Transacoes:  {len(transacoes)} registos")
    print(f"Logs:        {len(logs)} registos")
    print("="*50)


# ------------------------------------------------------------
# 5. BLOCO DE TESTE
# ------------------------------------------------------------
# O bloco abaixo executa apenas se o ficheiro for executado
# diretamente (python dados.py). Nao executa se for importado
# por outro modulo.
# ------------------------------------------------------------

if __name__ == "__main__":

    print("\nTESTANDO MODULO DE DADOS")
    print("="*30)

    # Estado inicial
    mostrar_estado_dados()

    # Criacao de dados de exemplo
    print("\nCriando dados de exemplo...")

    unidade_teste = {
        "id": proximo_id_unidade(),
        "nome": "Foz Velha",
        "tipo": "Mensal",
        "capacidade": 15,
        "estado": "Livre",
        "preco_base": 250.00
    }
    unidades.append(unidade_teste)
    print(f"  + Unidade criada: {unidade_teste['nome']} (ID: {unidade_teste['id']})")

    cliente_teste = {
        "id": proximo_id_cliente(),
        "nome": "Joao Silva",
        "email": "joao@email.com",
        "telefone": "912345678",
        "tipo": "Morador"
    }
    clientes.append(cliente_teste)
    print(f"  + Cliente criado: {cliente_teste['nome']} (ID: {cliente_teste['id']})")

    # Estado apos adicionar dados
    print("\nApos adicionar dados:")
    mostrar_estado_dados()

    print("\nTeste concluido com sucesso!")