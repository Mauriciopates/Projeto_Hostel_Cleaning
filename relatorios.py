# ============================================================
# relatorios.py - RELATORIOS E ANALYTICS
# ============================================================
# Modulo responsavel por gerar relatorios e analises do sistema.
# Consome dados de todos os outros modulos.
#
# Dependencias:
#   - dados.py: Para acesso aos dados
#   - utils.py: Para formatacao e cores
#   - unidades.py, clientes.py, contratos.py, estoque.py
# ============================================================

from dados import (
    unidades,
    clientes,
    contratos,
    produtos,
    consumos,
    transacoes,
    logs,
    mostrar_estado_dados,
)
from utils import (
    cor,
    cabecalho,
    linha_separadora,
    formatar_preco,
    formatar_data,
    formatar_data_hora,
    obter_data_atual,
    input_data,
    input_int,
    input_sim_nao,
    input_opcao,
)
from unidades import Unidade
from clientes import Cliente
from contratos import Contrato, Reserva
from estoque import Produto

# ------------------------------------------------------------
# 1. FUNCOES AUXILIARES PARA RELATORIOS
# ------------------------------------------------------------


def _contar_unidades_ocupadas():
    """
    Conta o numero de unidades ocupadas e livres.

    Retorna:
        dict: Dicionario com totais
    """
    total = len(unidades)
    ocupadas = len([u for u in unidades if u["estado"] in ["Ocupado", "Reservado"]])

    return {"total": total, "ocupadas": ocupadas, "livres": total - ocupadas}


def _calcular_taxa_ocupacao():
    """
    Calcula a taxa de ocupacao geral.

    Retorna:
        float: Taxa de ocupacao em percentagem
    """
    dados = _contar_unidades_ocupadas()
    if dados["total"] == 0:
        return 0.0
    return (dados["ocupadas"] / dados["total"]) * 100


def _contar_contratos_ativos():
    """
    Conta o numero de contratos ativos.

    Retorna:
        int: Numero de contratos ativos
    """
    return len(
        [c for c in contratos if c.get("tipo") != "Airbnb" and c["status"] == "Ativo"]
    )


def _contar_reservas_ativas():
    """
    Conta o numero de reservas ativas.

    Retorna:
        int: Numero de reservas ativas
    """
    return len(
        [c for c in contratos if c.get("tipo") == "Airbnb" and c["status"] == "Ativa"]
    )


# ------------------------------------------------------------
# 2. RELATORIOS DE OCUPACAO
# ------------------------------------------------------------


def relatorio_ocupacao_diaria():
    """
    Gera relatorio de ocupacao diaria.
    """
    print("\n" + cabecalho("RELATORIO DE OCUPACAO DIARIA"))

    data = input_data("Data (YYYY-MM-DD, Enter para hoje): ", obrigatorio=False)
    if not data:
        data = obter_data_atual("%Y-%m-%d")

    print(f"\nData: {formatar_data(data)}")
    print(linha_separadora())

    # Conta ocupacao
    dados = _contar_unidades_ocupadas()
    taxa = _calcular_taxa_ocupacao()

    print(f"Total de Unidades: {dados['total']}")
    print(f"Unidades Ocupadas: {cor(str(dados['ocupadas']), 'vermelho')}")
    print(f"Unidades Livres:   {cor(str(dados['livres']), 'verde')}")
    print(f"Taxa de Ocupacao:  {cor(f'{taxa:.1f}%', 'azul', estilo='negrito')}")

    # Detalhamento por tipo
    print("\n" + linha_separadora(30))
    print("Detalhamento por tipo:")

    mensal = [u for u in unidades if u["tipo"] == "Mensal"]
    airbnb = [u for u in unidades if u["tipo"] == "Airbnb"]

    ocupados_mensal = len(
        [u for u in mensal if u["estado"] in ["Ocupado", "Reservado"]]
    )
    ocupados_airbnb = len(
        [u for u in airbnb if u["estado"] in ["Ocupado", "Reservado"]]
    )

    taxa_mensal = (ocupados_mensal / len(mensal)) * 100 if len(mensal) > 0 else 0
    taxa_airbnb = (ocupados_airbnb / len(airbnb)) * 100 if len(airbnb) > 0 else 0

    print(f"  Mensal:  {ocupados_mensal}/{len(mensal)} ({taxa_mensal:.1f}%)")
    print(f"  Airbnb:  {ocupados_airbnb}/{len(airbnb)} ({taxa_airbnb:.1f}%)")

    # Lista unidades ocupadas
    print("\n" + linha_separadora(30))
    print("Unidades ocupadas:")

    ocupadas_lista = [u for u in unidades if u["estado"] in ["Ocupado", "Reservado"]]
    if ocupadas_lista:
        for u in ocupadas_lista:
            tipo_cor = "verde" if u["tipo"] == "Mensal" else "ciano"
            print(f"  {u['nome']} ({cor(u['tipo'], tipo_cor)}) - {u['estado']}")
    else:
        print("  Nenhuma unidade ocupada.")


def relatorio_ocupacao_semanal():
    """
    Gera relatorio de ocupacao semanal.
    """
    print("\n" + cabecalho("RELATORIO DE OCUPACAO SEMANAL"))

    from datetime import datetime, timedelta

    hoje = datetime.now()

    # Calcula inicio da semana (segunda-feira)
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    fim_semana = inicio_semana + timedelta(days=6)

    print(
        f"Semana: {formatar_data(inicio_semana.strftime('%Y-%m-%d'))} a {formatar_data(fim_semana.strftime('%Y-%m-%d'))}"
    )
    print(linha_separadora())

    # Estatisticas gerais
    dados = _contar_unidades_ocupadas()
    taxa = _calcular_taxa_ocupacao()

    print(f"Total de Unidades: {dados['total']}")
    print(f"Media de Ocupacao: {cor(f'{taxa:.1f}%', 'azul', estilo='negrito')}")

    # Previsao para os proximos 7 dias
    print("\n" + linha_separadora(30))
    print("Previsao para os proximos 7 dias:")

    for i in range(7):
        dia = hoje + timedelta(days=i)
        dia_str = dia.strftime("%Y-%m-%d")
        dia_semana = dia.strftime("%A")

        # Traduz dia da semana
        dias_semana_pt = {
            "Monday": "Segunda",
            "Tuesday": "Terca",
            "Wednesday": "Quarta",
            "Thursday": "Quinta",
            "Friday": "Sexta",
            "Saturday": "Sabado",
            "Sunday": "Domingo",
        }
        dia_semana_pt = dias_semana_pt.get(dia_semana, dia_semana)

        # Reservas para este dia
        reservas_dia = [
            c
            for c in contratos
            if c.get("tipo") == "Airbnb"
            and c.get("status") in ["Pendente", "Ativa"]
            and c.get("data_checkin") == dia_str
        ]

        print(f"  {dia_semana_pt}: {len(reservas_dia)} check-in(s)")


def relatorio_ocupacao_mensal():
    """
    Gera relatorio de ocupacao mensal.
    """
    print("\n" + cabecalho("RELATORIO DE OCUPACAO MENSAL"))

    print(f"Mes: {formatar_data(obter_data_atual('%Y-%m-01'), '%Y-%m-%d', '%B %Y')}")
    print(linha_separadora())

    # Estatisticas gerais
    dados = _contar_unidades_ocupadas()
    taxa = _calcular_taxa_ocupacao()

    print(f"Total de Unidades: {dados['total']}")
    print(f"Unidades Ocupadas: {cor(str(dados['ocupadas']), 'vermelho')}")
    print(f"Unidades Livres:   {cor(str(dados['livres']), 'verde')}")
    print(f"Taxa de Ocupacao:  {cor(f'{taxa:.1f}%', 'azul', estilo='negrito')}")

    # Contratos ativos vs reservas ativas
    contratos_ativos = _contar_contratos_ativos()
    reservas_ativas = _contar_reservas_ativas()

    print("\n" + linha_separadora(30))
    print("Detalhamento de ocupacao:")
    print(f"  Contratos Mensais Ativos: {contratos_ativos}")
    print(f"  Reservas Airbnb Ativas:   {reservas_ativas}")

    # Unidades por estado
    print("\n" + linha_separadora(30))
    print("Unidades por estado:")

    estados = {"Livre": 0, "Ocupado": 0, "Manutencao": 0, "Reservado": 0}
    for u in unidades:
        if u["estado"] in estados:
            estados[u["estado"]] += 1

    cores_estados = {
        "Livre": "verde",
        "Ocupado": "vermelho",
        "Manutencao": "amarelo",
        "Reservado": "ciano",
    }

    for estado, count in estados.items():
        cor_estado = cores_estados.get(estado, "branco")
        print(f"  {cor(estado, cor_estado)}: {count}")


def relatorio_calendario_ocupacao():
    """
    Gera um calendario de ocupacao para o mes atual.
    """
    print("\n" + cabecalho("CALENDARIO DE OCUPACAO"))

    from datetime import datetime, timedelta

    hoje = datetime.now()

    ano = hoje.year
    mes = hoje.month

    # Primeiro dia do mes
    primeiro_dia = datetime(ano, mes, 1)

    # Numero de dias no mes
    if mes == 12:
        ultimo_dia = datetime(ano + 1, 1, 1) - timedelta(days=1)
    else:
        ultimo_dia = datetime(ano, mes + 1, 1) - timedelta(days=1)

    dias_no_mes = ultimo_dia.day
    dia_semana = primeiro_dia.weekday()

    # Nomes dos meses e dias
    nomes_meses = [
        "Janeiro",
        "Fevereiro",
        "Marco",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]
    dias_semana_pt = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]

    print(f"  {nomes_meses[mes-1]} {ano}")
    print("  " + " ".join(dias_semana_pt))
    print("  " + "-" * 28)

    # Linha do calendario
    linha = "  "

    # Espacos iniciais
    for _ in range(dia_semana):
        linha += "    "

    # Dias do mes
    for dia in range(1, dias_no_mes + 1):
        data_str = f"{ano}-{mes:02d}-{dia:02d}"

        # Verifica se o dia tem ocupacao
        ocupado = False
        for u in unidades:
            if u["estado"] in ["Ocupado", "Reservado"]:
                # Verifica se ha contrato ou reserva para este dia
                for c in contratos:
                    if c.get("unidade_id") == u["id"]:
                        if c.get("tipo") == "Airbnb":
                            if (
                                c.get("data_checkin")
                                <= data_str
                                <= c.get("data_checkout")
                            ):
                                ocupado = True
                                break
                        else:
                            if c.get("data_inicio") <= data_str <= c.get("data_fim"):
                                ocupado = True
                                break
                if ocupado:
                    break

        # Formata o dia
        if data_str == hoje.strftime("%Y-%m-%d"):
            dia_texto = cor(f"{dia:2d}", "verde", estilo="negrito")
        elif ocupado:
            dia_texto = cor(f"{dia:2d}", "vermelho")
        else:
            dia_texto = f"{dia:2d}"

        linha += f"{dia_texto} "

        # Nova linha no final da semana
        if (dia_semana + dia) % 7 == 0:
            print(linha)
            linha = "  "

    if linha.strip():
        print(linha)

    print("=" * 30)
    print(cor("Legenda:", "azul"))
    print(f"  {cor('Verde', 'verde')} = Hoje")
    print(f"  {cor('Vermelho', 'vermelho')} = Ocupado")
    print("=" * 30)


def relatorio_unidades_mais_menos_ocupadas():
    """
    Gera relatorio das unidades mais e menos ocupadas.
    """
    print("\n" + cabecalho("UNIDADES MAIS E MENOS OCUPADAS"))

    # Conta ocupacoes por unidade
    ocupacao_unidades = {}

    for unidade in unidades:
        unidade_id = unidade["id"]
        unidade_nome = unidade["nome"]

        # Conta dias ocupados
        dias_ocupados = 0
        for contrato in contratos:
            if contrato.get("unidade_id") == unidade_id:
                if contrato.get("tipo") == "Airbnb":
                    # Conta noites da reserva
                    from datetime import datetime

                    checkin = datetime.strptime(contrato["data_checkin"], "%Y-%m-%d")
                    checkout = datetime.strptime(contrato["data_checkout"], "%Y-%m-%d")
                    dias_ocupados += (checkout - checkin).days
                else:
                    # Conta meses do contrato
                    dias_ocupados += contrato.get("duracao_meses", 0) * 30

        ocupacao_unidades[unidade_nome] = dias_ocupados

    # Ordena por ocupacao
    ordenadas = sorted(ocupacao_unidades.items(), key=lambda x: x[1], reverse=True)

    if not ordenadas:
        print(cor("Nenhuma unidade com registo de ocupacao.", "amarelo"))
        return

    print("\nUnidades mais ocupadas:")
    for nome, dias in ordenadas[:5]:
        print(f"  {nome}: {dias} dias/meses ocupados")

    print("\nUnidades menos ocupadas:")
    for nome, dias in ordenadas[-5:]:
        print(f"  {nome}: {dias} dias/meses ocupados")


# ------------------------------------------------------------
# 3. RELATORIOS FINANCEIROS
# ------------------------------------------------------------


def relatorio_lucro_liquido():
    """
    Gera relatorio de lucro liquido (receitas - despesas).
    """
    print("\n" + cabecalho("RELATORIO DE LUCRO LIQUIDO"))

    print("Opcoes:")
    print("  1 - Lucro do mes atual")
    print("  2 - Lucro acumulado do ano")
    print("  0 - Voltar")

    opcao = input("\nEscolha uma opcao: ").strip()

    if opcao == "0":
        return
    elif opcao not in ["1", "2"]:
        print(cor("Opcao invalida.", "vermelho"))
        return

    # Calcula receitas e despesas
    total_receitas = 0
    total_despesas = 0

    for transacao in transacoes:
        if transacao.get("tipo") == "Receita":
            total_receitas += transacao.get("valor", 0)
        elif transacao.get("tipo") == "Despesa":
            total_despesas += transacao.get("valor", 0)

    # Se nao houver transacoes, usa dados estimados
    if not transacoes:
        # Estimativa a partir de contratos
        for contrato in contratos:
            if contrato.get("tipo") != "Airbnb" and contrato.get("status") == "Ativo":
                total_receitas += contrato.get("valor_renda", 0)
            elif contrato.get("tipo") == "Airbnb" and contrato.get("status") in [
                "Ativa",
                "Finalizada",
            ]:
                total_receitas += contrato.get("valor_total", 0)

    lucro_liquido = total_receitas - total_despesas

    print("\n" + linha_separadora())
    print(f"Total de Receitas:  {cor(formatar_preco(total_receitas), 'verde')}")
    print(f"Total de Despesas:  {cor(formatar_preco(total_despesas), 'vermelho')}")
    print(
        f"Lucro Liquido:     {cor(formatar_preco(lucro_liquido), 'azul', estilo='negrito')}"
    )

    if lucro_liquido > 0:
        print(cor("Situacao: LUCRO", "verde", estilo="negrito"))
    elif lucro_liquido < 0:
        print(cor("Situacao: PREJUIZO", "vermelho", estilo="negrito"))
    else:
        print(cor("Situacao: EQUILIBRIO", "amarelo", estilo="negrito"))

    if total_receitas > 0:
        margem = (lucro_liquido / total_receitas) * 100
        print(f"Margem: {margem:.1f}%")


def relatorio_fluxo_caixa():
    """
    Gera relatorio de fluxo de caixa.
    """
    print("\n" + cabecalho("RELATORIO DE FLUXO DE CAIXA"))

    print("Opcoes:")
    print("  1 - Fluxo do mes atual")
    print("  2 - Fluxo de um periodo especifico")
    print("  0 - Voltar")

    opcao = input("\nEscolha uma opcao: ").strip()

    if opcao == "0":
        return
    elif opcao not in ["1", "2"]:
        print(cor("Opcao invalida.", "vermelho"))
        return

    from datetime import datetime, timedelta

    if opcao == "1":
        # Mes atual
        hoje = datetime.now()
        data_inicio = datetime(hoje.year, hoje.month, 1).strftime("%Y-%m-%d")
        hoje_str = hoje.strftime("%Y-%m-%d")
    else:
        data_inicio = input_data("Data inicio (YYYY-MM-DD): ")
        data_fim = input_data("Data fim (YYYY-MM-DD): ")
        hoje_str = data_fim

    print(f"\nPeriodo: {formatar_data(data_inicio)} a {formatar_data(hoje_str)}")
    print(linha_separadora())

    # Filtra transacoes do periodo
    transacoes_periodo = [
        t for t in transacoes if data_inicio <= t.get("data", "") <= hoje_str
    ]

    receitas = sum(
        t.get("valor", 0) for t in transacoes_periodo if t.get("tipo") == "Receita"
    )
    despesas = sum(
        t.get("valor", 0) for t in transacoes_periodo if t.get("tipo") == "Despesa"
    )
    saldo = receitas - despesas

    print(f"Receitas:  {cor(formatar_preco(receitas), 'verde')}")
    print(f"Despesas:  {cor(formatar_preco(despesas), 'vermelho')}")
    print(f"Saldo:     {cor(formatar_preco(saldo), 'azul', estilo='negrito')}")

    # Lista transacoes
    if transacoes_periodo:
        print("\n" + linha_separadora(30))
        print("Transacoes do periodo:")
        for t in sorted(
            transacoes_periodo, key=lambda x: x.get("data", ""), reverse=True
        ):
            tipo_cor = "verde" if t.get("tipo") == "Receita" else "vermelho"
            print(
                f"  {formatar_data(t.get('data', ''))}: {cor(t.get('tipo', ''), tipo_cor)} - {formatar_preco(t.get('valor', 0))}"
            )


def relatorio_contas_receber():
    """
    Gera relatorio de contas a receber (rendas em atraso).
    """
    print("\n" + cabecalho("RELATORIO DE CONTAS A RECEBER"))

    from datetime import datetime

    # Busca contratos com rendas em atraso
    atrasados = []

    for contrato in contratos:
        if contrato.get("tipo") != "Airbnb" and contrato.get("status") == "Ativo":
            if contrato.get("data_proximo_vencimento") < datetime.now().strftime(
                "%Y-%m-%d"
            ):
                # Calcula valor em atraso
                vencimento = datetime.strptime(
                    contrato["data_proximo_vencimento"], "%Y-%m-%d"
                )
                dias_atraso = (datetime.now() - vencimento).days

                # Busca cliente
                cliente = Cliente.buscar_por_id(contrato["cliente_id"])
                nome_cliente = (
                    cliente["nome"] if cliente else f"ID {contrato['cliente_id']}"
                )

                atrasados.append(
                    {
                        "contrato_id": contrato["id"],
                        "cliente": nome_cliente,
                        "unidade_id": contrato["unidade_id"],
                        "valor": contrato["valor_renda"],
                        "dias_atraso": dias_atraso,
                        "juros": contrato.get("valor_renda", 0)
                        * 0.10
                        * (dias_atraso / 30),
                    }
                )

    if not atrasados:
        print(cor("Nenhuma conta em atraso.", "verde"))
        return

    print(f"\nTotal em atraso: {len(atrasados)} contratos")
    print(linha_separadora())

    total_em_atraso = 0
    for item in atrasados:
        total_item = item["valor"] + item["juros"]
        total_em_atraso += total_item

        print(f"  {item['cliente']}")
        print(f"    Contrato ID: {item['contrato_id']}")
        print(f"    Valor Renda: {formatar_preco(item['valor'])}")
        print(f"    Dias em Atraso: {item['dias_atraso']}")
        print(f"    Juros: {formatar_preco(item['juros'])}")
        print(f"    Total Devido: {cor(formatar_preco(total_item), 'vermelho')}")
        print(linha_separadora(35))

    print(
        f"Total Geral em Atraso: {cor(formatar_preco(total_em_atraso), 'vermelho', estilo='negrito')}"
    )


def relatorio_rentabilidade_unidades():
    """
    Gera relatorio de rentabilidade por unidade.
    """
    print("\n" + cabecalho("RELATORIO DE RENTABILIDADE POR UNIDADE"))

    print("Calculando rentabilidade por unidade...")
    print(linha_separadora())

    # Agrupa receitas por unidade
    receitas_por_unidade = {}
    despesas_por_unidade = {}

    for transacao in transacoes:
        unidade_id = transacao.get("unidade_id")
        if unidade_id is None:
            continue

        unidade = Unidade.buscar_por_id(unidade_id)
        if not unidade:
            continue

        nome_unidade = unidade["nome"]

        if transacao.get("tipo") == "Receita":
            if nome_unidade not in receitas_por_unidade:
                receitas_por_unidade[nome_unidade] = 0
            receitas_por_unidade[nome_unidade] += transacao.get("valor", 0)
        elif transacao.get("tipo") == "Despesa":
            if nome_unidade not in despesas_por_unidade:
                despesas_por_unidade[nome_unidade] = 0
            despesas_por_unidade[nome_unidade] += transacao.get("valor", 0)

    # Se nao houver transacoes, usa estimativa de contratos
    if not transacoes:
        for contrato in contratos:
            unidade = Unidade.buscar_por_id(contrato["unidade_id"])
            if not unidade:
                continue

            nome_unidade = unidade["nome"]

            if contrato.get("tipo") == "Airbnb":
                if contrato.get("status") in ["Ativa", "Finalizada"]:
                    if nome_unidade not in receitas_por_unidade:
                        receitas_por_unidade[nome_unidade] = 0
                    receitas_por_unidade[nome_unidade] += contrato.get("valor_total", 0)
            else:
                if contrato.get("status") == "Ativo":
                    if nome_unidade not in receitas_por_unidade:
                        receitas_por_unidade[nome_unidade] = 0
                    receitas_por_unidade[nome_unidade] += contrato.get("valor_renda", 0)

    if not receitas_por_unidade:
        print(cor("Nenhuma receita registada por unidade.", "amarelo"))
        return

    # Calcula rentabilidade
    rentabilidade = {}
    for nome, receita in receitas_por_unidade.items():
        despesa = despesas_por_unidade.get(nome, 0)
        rentabilidade[nome] = receita - despesa

    # Ordena por rentabilidade (melhor para pior)
    ordenadas = sorted(rentabilidade.items(), key=lambda x: x[1], reverse=True)

    print("\nRentabilidade por unidade:")
    for nome, valor in ordenadas:
        cor_valor = "verde" if valor > 0 else "vermelho" if valor < 0 else "amarelo"
        print(f"  {nome}: {cor(formatar_preco(valor), cor_valor)}")
        print(f"    Receitas: {formatar_preco(receitas_por_unidade.get(nome, 0))}")
        print(f"    Despesas: {formatar_preco(despesas_por_unidade.get(nome, 0))}")
        print(linha_separadora(35))


# ------------------------------------------------------------
# 4. RELATORIOS DE STOCK
# ------------------------------------------------------------


def relatorio_stock_baixo():
    """
    Gera relatorio de produtos com stock baixo.
    """
    print("\n" + cabecalho("RELATORIO DE STOCK BAIXO"))

    alertas = [p for p in produtos if p["quantidade_atual"] <= p["quantidade_minima"]]

    if not alertas:
        print(cor("Nenhum produto com stock baixo.", "verde"))
        return

    print(f"\nTotal de produtos com alerta: {len(alertas)}")
    print(linha_separadora())

    for produto in alertas:
        falta = produto["quantidade_minima"] - produto["quantidade_atual"]
        local = (
            "Central"
            if produto["unidade_id"] is None
            else f"Unidade {produto['unidade_id']}"
        )

        print(f"  {cor(produto['nome'], 'amarelo')}")
        print(f"    Codigo: {produto['codigo']}")
        print(f"    Categoria: {produto['categoria']}")
        print(f"    Stock Atual: {cor(str(produto['quantidade_atual']), 'vermelho')}")
        print(f"    Minimo: {produto['quantidade_minima']}")
        print(f"    Falta: {falta}")
        print(f"    Local: {local}")
        print(linha_separadora(35))


def relatorio_consumo_periodo():
    """
    Gera relatorio de consumo de produtos por periodo.
    """
    print("\n" + cabecalho("RELATORIO DE CONSUMO POR PERIODO"))

    data_inicio = input_data("Data inicio (YYYY-MM-DD): ")
    data_fim = input_data("Data fim (YYYY-MM-DD): ")

    # Filtra consumos do periodo
    consumos_periodo = [
        c for c in consumos if data_inicio <= c.get("data", "")[:10] <= data_fim
    ]

    if not consumos_periodo:
        print(cor("Nenhum consumo registado no periodo.", "amarelo"))
        return

    # Agrupa por produto
    consumo_por_produto = {}
    for consumo in consumos_periodo:
        produto = Produto.buscar_por_id(consumo["produto_id"])
        nome_produto = produto["nome"] if produto else f"ID {consumo['produto_id']}"

        if nome_produto not in consumo_por_produto:
            consumo_por_produto[nome_produto] = 0
        consumo_por_produto[nome_produto] += consumo["quantidade"]

    print(f"\nPeriodo: {formatar_data(data_inicio)} a {formatar_data(data_fim)}")
    print(f"Total de consumos: {len(consumos_periodo)}")
    print(linha_separadora())

    # Ordena por quantidade (mais consumido primeiro)
    ordenados = sorted(consumo_por_produto.items(), key=lambda x: x[1], reverse=True)

    print("Consumos por produto:")
    for produto, quantidade in ordenados:
        print(f"  {produto}: {quantidade} unidades")

    print(linha_separadora())
    total_consumido = sum(consumo_por_produto.values())
    print(f"Total de itens consumidos: {total_consumido}")


def relatorio_custo_stock_unidade():
    """
    Gera relatorio de custo de stock por unidade.
    """
    print("\n" + cabecalho("RELATORIO DE CUSTO DE STOCK POR UNIDADE"))

    # Agrupa produtos por unidade
    stock_por_unidade = {"Central": []}

    for produto in produtos:
        if produto["unidade_id"] is None:
            stock_por_unidade["Central"].append(produto)
        else:
            unidade = Unidade.buscar_por_id(produto["unidade_id"])
            nome_unidade = unidade["nome"] if unidade else f"ID {produto['unidade_id']}"
            if nome_unidade not in stock_por_unidade:
                stock_por_unidade[nome_unidade] = []
            stock_por_unidade[nome_unidade].append(produto)

    if not stock_por_unidade:
        print(cor("Nenhum produto em stock.", "amarelo"))
        return

    print(linha_separadora())

    total_geral = 0
    for local, produtos_lista in stock_por_unidade.items():
        valor_total = sum(
            p["quantidade_atual"] * p.get("preco_unitario", 0) for p in produtos_lista
        )
        total_geral += valor_total

        print(f"{cor(local, 'azul', estilo='negrito')}:")
        print(f"  Produtos: {len(produtos_lista)}")
        print(f"  Valor Total: {formatar_preco(valor_total)}")

        if produtos_lista:
            print("  Itens:")
            for p in produtos_lista[:5]:  # Mostra apenas os 5 primeiros
                print(f"    {p['nome']}: {p['quantidade_atual']} {p['unidade_medida']}")
            if len(produtos_lista) > 5:
                print(f"    ... e mais {len(produtos_lista) - 5} produtos")

        print(linha_separadora(35))

    print(
        f"Valor Total do Stock: {cor(formatar_preco(total_geral), 'azul', estilo='negrito')}"
    )


# ------------------------------------------------------------
# 5. RELATORIOS DE CLIENTES
# ------------------------------------------------------------


def relatorio_contratos_expirar():
    """
    Gera relatorio de contratos a expirar.
    """
    print("\n" + cabecalho("RELATORIO DE CONTRATOS A EXPIRAR"))

    dias = input_int("Antecedencia em dias (default 15): ", obrigatorio=False)
    if dias is None:
        dias = 15

    from datetime import datetime, timedelta

    hoje = datetime.now()
    data_alerta = hoje + timedelta(days=dias)
    data_alerta_str = data_alerta.strftime("%Y-%m-%d")

    a_expirar = []
    for contrato in contratos:
        if contrato.get("tipo") != "Airbnb" and contrato.get("status") == "Ativo":
            if contrato.get("data_fim") <= data_alerta_str:
                a_expirar.append(contrato)

    if not a_expirar:
        print(cor(f"Nenhum contrato a expirar nos proximos {dias} dias.", "verde"))
        return

    print(f"\nContratos a expirar nos proximos {dias} dias: {len(a_expirar)}")
    print(linha_separadora())

    for contrato in a_expirar:
        unidade = Unidade.buscar_por_id(contrato["unidade_id"])
        cliente = Cliente.buscar_por_id(contrato["cliente_id"])

        nome_unidade = unidade["nome"] if unidade else f"ID {contrato['unidade_id']}"
        nome_cliente = cliente["nome"] if cliente else f"ID {contrato['cliente_id']}"

        data_fim = datetime.strptime(contrato["data_fim"], "%Y-%m-%d")
        dias_restantes = (data_fim - datetime.now()).days

        print(f"  {nome_cliente}")
        print(f"    Unidade: {nome_unidade}")
        print(
            f"    Expira em: {formatar_data(contrato['data_fim'])} ({dias_restantes} dias)"
        )
        print(
            f"    Renovacao: {'Automatica' if contrato.get('renovacao_automatica') else 'Manual'}"
        )
        print(linha_separadora(35))


def relatorio_historico_cliente():
    """
    Gera relatorio de historico completo de um cliente.
    """
    print("\n" + cabecalho("HISTORICO DO CLIENTE"))

    Cliente.listar_todos()

    try:
        cliente_id = input_int("ID do cliente: ", min_valor=1)
    except:
        print(cor("Operacao cancelada.", "amarelo"))
        return

    cliente_dict = Cliente.buscar_por_id(cliente_id)
    if not cliente_dict:
        print(cor("Cliente nao encontrado.", "vermelho"))
        return

    cliente = Cliente.from_dict(cliente_dict)
    cliente.exibir()

    # Busca historico de contratos/reservas
    historico = []
    for contrato in contratos:
        if contrato["cliente_id"] == cliente_id:
            historico.append(contrato)

    if not historico:
        print(cor("\nNenhuma estadia registada para este cliente.", "amarelo"))
        return

    print("\n" + linha_separadora(30))
    print("Historico de estadias:")

    for item in sorted(historico, key=lambda x: x.get("data_inicio", ""), reverse=True):
        if item.get("tipo") == "Airbnb":
            print(
                f"  [Airbnb] {formatar_data(item.get('data_checkin', ''))} -> {formatar_data(item.get('data_checkout', ''))}"
            )
            print(f"    Status: {item.get('status', 'N/A')}")
        else:
            print(
                f"  [Mensal] {formatar_data(item.get('data_inicio', ''))} -> {formatar_data(item.get('data_fim', ''))}"
            )
            print(f"    Status: {item.get('status', 'N/A')}")
            print(f"    Renda: {formatar_preco(item.get('valor_renda', 0))}")
        print(linha_separadora(35))


# ------------------------------------------------------------
# 6. RELATORIOS DE LOGS
# ------------------------------------------------------------


def relatorio_logs():
    """
    Gera relatorio de logs de auditoria.
    """
    print("\n" + cabecalho("RELATORIO DE LOGS"))

    if not logs:
        print(cor("Nenhum log registado.", "amarelo"))
        return

    print("Opcoes de filtro:")
    print("  1 - Todos os logs")
    print("  2 - Logs de um modulo especifico")
    print("  3 - Logs de um utilizador especifico")
    print("  0 - Voltar")

    opcao = input("\nEscolha uma opcao: ").strip()

    if opcao == "0":
        return

    logs_filtrados = logs.copy()

    if opcao == "2":
        modulos = sorted(set(l.get("modulo", "N/A") for l in logs))
        print("\nModulos disponiveis:")
        for m in modulos:
            print(f"  {m}")
        modulo = input("\nModulo: ").strip()
        if modulo:
            logs_filtrados = [l for l in logs_filtrados if l.get("modulo") == modulo]

    elif opcao == "3":
        utilizadores = sorted(set(l.get("utilizador_nome", "N/A") for l in logs))
        print("\nUtilizadores disponiveis:")
        for u in utilizadores:
            print(f"  {u}")
        utilizador = input("\nUtilizador: ").strip()
        if utilizador:
            logs_filtrados = [
                l for l in logs_filtrados if l.get("utilizador_nome") == utilizador
            ]

    elif opcao != "1":
        print(cor("Opcao invalida.", "vermelho"))
        return

    if not logs_filtrados:
        print(cor("Nenhum log encontrado com os filtros selecionados.", "amarelo"))
        return

    print(f"\nTotal de logs: {len(logs_filtrados)}")
    print(linha_separadora())

    # Mostra os ultimos 50 logs
    for log in logs_filtrados[-50:]:
        print(f"{formatar_data_hora(log.get('data_hora', ''))}")
        print(f"  Utilizador: {log.get('utilizador_nome', 'N/A')}")
        print(f"  Acao: {log.get('acao', 'N/A')}")
        print(f"  Modulo: {log.get('modulo', 'N/A')}")
        if log.get("detalhes"):
            print(f"  Detalhes: {log['detalhes']}")
        print(linha_separadora(35))

    if len(logs_filtrados) > 50:
        print(
            cor(
                f"Mostrando apenas os ultimos 50 de {len(logs_filtrados)} logs.",
                "amarelo",
            )
        )


# ------------------------------------------------------------
# 7. EXPORTACAO
# ------------------------------------------------------------


def exportar_excel():
    """
    Exporta relatorios para Excel.
    """
    print("\n" + cabecalho("EXPORTAR PARA EXCEL"))
    print(cor("Funcao em desenvolvimento (Fase 2.0)", "amarelo"))
    print("A exportacao para Excel sera implementada na proxima fase.")
    print("Utilizaremos a biblioteca 'openpyxl'.")


def exportar_pdf():
    """
    Exporta relatorios para PDF.
    """
    print("\n" + cabecalho("EXPORTAR PARA PDF"))
    print(cor("Funcao em desenvolvimento (Fase 2.0)", "amarelo"))
    print("A exportacao para PDF sera implementada na proxima fase.")
    print("Utilizaremos a biblioteca 'reportlab'.")


# ------------------------------------------------------------
# 8. MENU DE RELATORIOS
# ------------------------------------------------------------


def menu_relatorios():
    """
    Menu principal do modulo de relatorios.
    """
    while True:
        print("\n" + cabecalho("RELATORIOS E ANALYTICS"))
        print("  1 - Ocupacao Diaria")
        print("  2 - Ocupacao Semanal")
        print("  3 - Ocupacao Mensal")
        print("  4 - Calendario de Ocupacao")
        print("  5 - Unidades Mais/Menos Ocupadas")
        print("  6 - Lucro Liquido")
        print("  7 - Fluxo de Caixa")
        print("  8 - Contas a Receber")
        print("  9 - Rentabilidade por Unidade")
        print(" 10 - Stock Baixo")
        print(" 11 - Consumo por Periodo")
        print(" 12 - Custo de Stock por Unidade")
        print(" 13 - Contratos a Expirar")
        print(" 14 - Historico do Cliente")
        print(" 15 - Logs de Auditoria")
        print(" 16 - Exportar Excel")
        print(" 17 - Exportar PDF")
        print("  0 - Voltar")
        print(linha_separadora())

        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            relatorio_ocupacao_diaria()
        elif opcao == "2":
            relatorio_ocupacao_semanal()
        elif opcao == "3":
            relatorio_ocupacao_mensal()
        elif opcao == "4":
            relatorio_calendario_ocupacao()
        elif opcao == "5":
            relatorio_unidades_mais_menos_ocupadas()
        elif opcao == "6":
            relatorio_lucro_liquido()
        elif opcao == "7":
            relatorio_fluxo_caixa()
        elif opcao == "8":
            relatorio_contas_receber()
        elif opcao == "9":
            relatorio_rentabilidade_unidades()
        elif opcao == "10":
            relatorio_stock_baixo()
        elif opcao == "11":
            relatorio_consumo_periodo()
        elif opcao == "12":
            relatorio_custo_stock_unidade()
        elif opcao == "13":
            relatorio_contratos_expirar()
        elif opcao == "14":
            relatorio_historico_cliente()
        elif opcao == "15":
            relatorio_logs()
        elif opcao == "16":
            exportar_excel()
        elif opcao == "17":
            exportar_pdf()
        elif opcao == "0":
            print(cor("Voltando...", "amarelo"))
            break
        else:
            print(cor("Opcao invalida. Tente novamente.", "vermelho"))


# ------------------------------------------------------------
# 9. BLOCO DE TESTE
# ------------------------------------------------------------

if __name__ == "__main__":

    print("\n" + cabecalho("TESTE DO MODULO DE RELATORIOS"))

    # Carrega dados de exemplo de todos os modulos
    from unidades import carregar_unidades_exemplo
    from clientes import carregar_clientes_exemplo
    from estoque import carregar_produtos_exemplo
    from contratos import carregar_contratos_exemplo

    carregar_unidades_exemplo()
    carregar_clientes_exemplo()
    carregar_produtos_exemplo()
    carregar_contratos_exemplo()

    # Mostra o estado dos dados
    mostrar_estado_dados()

    # Testa relatorios
    relatorio_ocupacao_mensal()
    relatorio_stock_baixo()
    relatorio_contratos_expirar()

    print("\n" + cabecalho("TESTE CONCLUIDO"))
