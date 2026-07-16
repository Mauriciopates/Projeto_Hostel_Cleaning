# ============================================================
# main.py - SISTEMA DE GESTAO DE HOSTEL
# ============================================================
# Ponto de entrada do sistema. Integra todos os modulos
# num menu hierarquico completo.
#
# Dependencias:
#   - Todos os modulos do sistema
# ============================================================

import os
import sys
import json
from datetime import datetime

# Importa os modulos do sistema
from utils import (
    cor,
    cabecalho,
    linha_separadora,
    input_opcao,
    input_sim_nao,
    obter_data_atual,
)
from dados import (
    unidades,
    clientes,
    contratos,
    produtos,
    consumos,
    transacoes,
    logs,
    mostrar_estado_dados,
    resetar_dados,
)
from unidades import menu_unidades, carregar_unidades_exemplo
from clientes import menu_clientes, carregar_clientes_exemplo
from estoque import menu_estoque, carregar_produtos_exemplo
from contratos import menu_contratos, carregar_contratos_exemplo
from relatorios import menu_relatorios

# ------------------------------------------------------------
# 1. FUNCOES DE PERSISTENCIA (JSON)
# ------------------------------------------------------------


def guardar_dados_json(nome_ficheiro="dados_hostel.json"):
    """
    Guarda todos os dados num ficheiro JSON.

    Parametros:
        nome_ficheiro (str): Nome do ficheiro para guardar
    """
    try:
        dados = {
            "unidades": unidades,
            "clientes": clientes,
            "contratos": contratos,
            "produtos": produtos,
            "consumos": consumos,
            "transacoes": transacoes,
            "logs": logs,
            "data_guardar": obter_data_atual(),
        }

        with open(nome_ficheiro, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)

        print(cor(f"Dados guardados com sucesso em '{nome_ficheiro}'", "verde"))
        return True

    except Exception as e:
        print(cor(f"Erro ao guardar dados: {e}", "vermelho"))
        return False


def carregar_dados_json(nome_ficheiro="dados_hostel.json"):
    """
    Carrega dados de um ficheiro JSON.

    Parametros:
        nome_ficheiro (str): Nome do ficheiro para carregar

    Retorna:
        bool: True se carregado com sucesso
    """
    try:
        if not os.path.exists(nome_ficheiro):
            print(cor(f"Ficheiro '{nome_ficheiro}' nao encontrado.", "amarelo"))
            return False

        with open(nome_ficheiro, "r", encoding="utf-8") as f:
            dados = json.load(f)

        # Limpa os dados atuais
        resetar_dados()

        # Carrega os dados
        unidades.extend(dados.get("unidades", []))
        clientes.extend(dados.get("clientes", []))
        contratos.extend(dados.get("contratos", []))
        produtos.extend(dados.get("produtos", []))
        consumos.extend(dados.get("consumos", []))
        transacoes.extend(dados.get("transacoes", []))
        logs.extend(dados.get("logs", []))

        print(cor(f"Dados carregados com sucesso de '{nome_ficheiro}'", "verde"))
        print(cor(f"  Unidades: {len(unidades)}", "ciano"))
        print(cor(f"  Clientes: {len(clientes)}", "ciano"))
        print(cor(f"  Contratos: {len(contratos)}", "ciano"))
        print(cor(f"  Produtos: {len(produtos)}", "ciano"))
        return True

    except json.JSONDecodeError as e:
        print(cor(f"Erro ao ler ficheiro JSON: {e}", "vermelho"))
        return False
    except Exception as e:
        print(cor(f"Erro ao carregar dados: {e}", "vermelho"))
        return False


# ------------------------------------------------------------
# 2. FUNCOES DE CONFIGURACAO
# ------------------------------------------------------------


def configurar_sistema():
    """
    Menu de configuracao do sistema.
    """
    print("\n" + cabecalho("CONFIGURACAO DO SISTEMA"))

    print("  1 - Carregar dados de exemplo")
    print("  2 - Resetar dados (limpar tudo)")
    print("  3 - Mostrar estado dos dados")
    print("  0 - Voltar")
    print(linha_separadora())

    opcao = input("Escolha uma opcao: ").strip()

    if opcao == "1":
        carregar_dados_exemplo()
    elif opcao == "2":
        if input_sim_nao("Tem certeza que deseja apagar TODOS os dados? (S/N): "):
            if input_sim_nao("Confirmar novamente? (S/N): "):
                resetar_dados()
                print(cor("Todos os dados foram resetados.", "amarelo"))
    elif opcao == "3":
        mostrar_estado_dados()
    elif opcao == "0":
        return
    else:
        print(cor("Opcao invalida.", "vermelho"))


def carregar_dados_exemplo():
    """
    Carrega todos os dados de exemplo no sistema.
    """
    print("\n" + cabecalho("CARREGAR DADOS DE EXEMPLO"))

    if unidades or clientes or contratos or produtos:
        print(cor("ATENCAO: Ja existem dados no sistema.", "amarelo"))
        if not input_sim_nao(
            "Deseja adicionar dados de exemplo aos existentes? (S/N): "
        ):
            if input_sim_nao("Deseja resetar os dados antes de carregar? (S/N): "):
                resetar_dados()
            else:
                print(cor("Operacao cancelada.", "amarelo"))
                return

    print("\nCarregando dados de exemplo...")
    carregar_unidades_exemplo()
    carregar_clientes_exemplo()
    carregar_produtos_exemplo()
    carregar_contratos_exemplo()

    print(cor("\nDados de exemplo carregados com sucesso!", "verde"))
    mostrar_estado_dados()


# ------------------------------------------------------------
# 3. MENU PRINCIPAL
# ------------------------------------------------------------


def menu_principal():
    """
    Menu principal do sistema.
    """
    while True:
        print("\n" + cabecalho("SISTEMA DE GESTAO DE HOSTEL"))
        print(
            cor("  Bem-vindo ao Sistema de Gestao do Hostel", "azul", estilo="negrito")
        )
        print()
        print("  GESTAO:")
        print("  1 - Unidades")
        print("  2 - Clientes")
        print("  3 - Contratos e Reservas")
        print("  4 - Estoque")
        print("  5 - Relatorios")
        print()
        print("  6 - Configuracao")
        print("  7 - Guardar Dados (JSON)")
        print("  8 - Carregar Dados (JSON)")
        print("  9 - Estado do Sistema")
        print()
        print("  0 - Sair")
        print(linha_separadora())

        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            menu_unidades()
        elif opcao == "2":
            menu_clientes()
        elif opcao == "3":
            menu_contratos()
        elif opcao == "4":
            menu_estoque()
        elif opcao == "5":
            menu_relatorios()
        elif opcao == "6":
            configurar_sistema()
        elif opcao == "7":
            nome_ficheiro = input(
                "Nome do ficheiro (default: dados_hostel.json): "
            ).strip()
            if not nome_ficheiro:
                nome_ficheiro = "dados_hostel.json"
            guardar_dados_json(nome_ficheiro)
        elif opcao == "8":
            nome_ficheiro = input(
                "Nome do ficheiro (default: dados_hostel.json): "
            ).strip()
            if not nome_ficheiro:
                nome_ficheiro = "dados_hostel.json"
            carregar_dados_json(nome_ficheiro)
        elif opcao == "9":
            mostrar_estado_dados()
        elif opcao == "0":
            print("\n" + cabecalho("SAIR"))
            if input_sim_nao("Deseja guardar os dados antes de sair? (S/N): "):
                guardar_dados_json()
            print(
                cor(
                    "Obrigado por usar o Sistema de Gestao do Hostel!",
                    "azul",
                    estilo="negrito",
                )
            )
            print(cor("Ate breve!", "azul"))
            sys.exit(0)
        else:
            print(cor("Opcao invalida. Tente novamente.", "vermelho"))


# ------------------------------------------------------------
# 4. PONTO DE ENTRADA DO SISTEMA
# ------------------------------------------------------------


def main():
    """
    Funcao principal que inicia o sistema.
    """
    print("\n" + "=" * 60)
    print(cor("  SISTEMA DE GESTAO DE HOSTEL - FASE 1.0", "azul", estilo="negrito"))
    print("=" * 60)
    print(cor("  Desenvolvido em Python - CLI", "ciano"))
    print("=" * 60)

    # Verifica se ha dados guardados
    if os.path.exists("dados_hostel.json"):
        print("\nFicheiro de dados encontrado!")
        resposta = input("Deseja carregar os dados guardados? (S/N): ").strip().upper()
        if resposta in ["S", "SIM", "Y", "YES"]:
            carregar_dados_json()
        else:
            if not unidades and not clientes and not contratos:
                resposta2 = (
                    input("Deseja carregar dados de exemplo? (S/N): ").strip().upper()
                )
                if resposta2 in ["S", "SIM", "Y", "YES"]:
                    carregar_dados_exemplo()
    else:
        resposta = (
            input("Nenhum dado encontrado. Deseja carregar dados de exemplo? (S/N): ")
            .strip()
            .upper()
        )
        if resposta in ["S", "SIM", "Y", "YES"]:
            carregar_dados_exemplo()

    print("\n" + linha_separadora())
    print(cor("Sistema pronto!", "verde", estilo="negrito"))

    # Inicia o menu principal
    menu_principal()


# ------------------------------------------------------------
# 5. PONTO DE ENTRADA
# ------------------------------------------------------------

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n" + cor("Sistema interrompido pelo utilizador.", "amarelo"))
        sys.exit(0)
    except Exception as e:
        print(cor(f"Erro inesperado: {e}", "vermelho"))
        sys.exit(1)
