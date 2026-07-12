# ============================================================
# unidades.py - GESTAO DE UNIDADES
# ============================================================
# Modulo responsavel por gerenciar as unidades do hostel.
# Cada unidade pode ser do tipo Mensal ou Airbnb.
#
# Dependencias:
#   - dados.py: Para acesso a base de dados em memoria
#   - utils.py: Para funcoes auxiliares (cores, validacoes, etc.)
# ============================================================

from dados import unidades, proximo_id_unidade, mostrar_estado_dados
from utils import (
    cor,
    cabecalho,
    linha_separadora,
    input_obrigatorio,
    input_float,
    input_int,
    input_sim_nao,
    input_opcao,
    formatar_preco,
)

# ------------------------------------------------------------
# 1. CLASSE UNIDADE
# ------------------------------------------------------------


class Unidade:
    """
    Classe que representa uma unidade do hostel.

    Atributos:
        id (int): Identificador unico da unidade
        nome (str): Nome da unidade (ex: "Foz Velha")
        tipo (str): "Mensal" ou "Airbnb"
        capacidade (int): Numero maximo de pessoas
        qtd_camas_solteiro (int): Quantidade de camas de solteiro
        qtd_camas_casal (int): Quantidade de camas de casal
        tem_cama_extra (bool): Indica se possui cama extra
        preco_base (float): Preco base (renda mensal ou diaria)
        preco_alta_temporada (float): Preco na alta temporada (apenas Airbnb)
        estado (str): "Livre", "Ocupado", "Manutencao", "Reservado"
        data_criacao (str): Data de criacao do registo
        observacoes (str): Observacoes gerais
    """

    def __init__(
        self,
        nome,
        tipo,
        capacidade=4,
        qtd_camas_solteiro=0,
        qtd_camas_casal=0,
        tem_cama_extra=False,
        preco_base=0.0,
        preco_alta_temporada=None,
        estado="Livre",
        observacoes="",
    ):
        """
        Inicializa uma nova unidade.

        Parametros:
            nome (str): Nome da unidade
            tipo (str): "Mensal" ou "Airbnb"
            capacidade (int): Capacidade maxima de pessoas
            qtd_camas_solteiro (int): Quantidade de camas de solteiro
            qtd_camas_casal (int): Quantidade de camas de casal
            tem_cama_extra (bool): Possui cama extra
            preco_base (float): Preco base
            preco_alta_temporada (float): Preco na alta temporada
            estado (str): Estado inicial da unidade
            observacoes (str): Observacoes
        """
        self.id = proximo_id_unidade()
        self.nome = nome
        self.tipo = tipo
        self.capacidade = capacidade
        self.qtd_camas_solteiro = qtd_camas_solteiro
        self.qtd_camas_casal = qtd_camas_casal
        self.tem_cama_extra = tem_cama_extra
        self.preco_base = preco_base
        self.preco_alta_temporada = preco_alta_temporada
        self.estado = estado
        self.data_criacao = None  # Sera preenchido ao salvar
        self.observacoes = observacoes

        # Preenche a data de criacao
        from utils import obter_data_atual

        self.data_criacao = obter_data_atual("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """
        Converte a unidade para um dicionario.

        Retorna:
            dict: Dicionario com todos os atributos da unidade
        """
        return {
            "id": self.id,
            "nome": self.nome,
            "tipo": self.tipo,
            "capacidade": self.capacidade,
            "qtd_camas_solteiro": self.qtd_camas_solteiro,
            "qtd_camas_casal": self.qtd_camas_casal,
            "tem_cama_extra": self.tem_cama_extra,
            "preco_base": self.preco_base,
            "preco_alta_temporada": self.preco_alta_temporada,
            "estado": self.estado,
            "data_criacao": self.data_criacao,
            "observacoes": self.observacoes,
        }

    @staticmethod
    def from_dict(dados):
        """
        Cria uma instancia de Unidade a partir de um dicionario.

        Parametros:
            dados (dict): Dicionario com os dados da unidade

        Retorna:
            Unidade: Instancia da unidade
        """
        unidade = Unidade(
            nome=dados["nome"],
            tipo=dados["tipo"],
            capacidade=dados["capacidade"],
            qtd_camas_solteiro=dados["qtd_camas_solteiro"],
            qtd_camas_casal=dados["qtd_camas_casal"],
            tem_cama_extra=dados["tem_cama_extra"],
            preco_base=dados["preco_base"],
            preco_alta_temporada=dados["preco_alta_temporada"],
            estado=dados["estado"],
            observacoes=dados["observacoes"],
        )
        unidade.id = dados["id"]
        unidade.data_criacao = dados["data_criacao"]
        return unidade

    def exibir(self):
        """
        Exibe os detalhes da unidade formatados no terminal.
        """
        print("\n" + linha_separadora(50))
        print(cor(f"ID: {self.id}", "azul", estilo="negrito"))
        print(f"Nome: {self.nome}")
        print(f"Tipo: {self.tipo}")
        print(f"Capacidade: {self.capacidade} pessoas")
        print(f"Camas Solteiro: {self.qtd_camas_solteiro}")
        print(f"Camas Casal: {self.qtd_camas_casal}")
        print(f"Cama Extra: {'Sim' if self.tem_cama_extra else 'Nao'}")
        print(f"Preco Base: {formatar_preco(self.preco_base)}")

        if self.preco_alta_temporada:
            print(f"Preco Alta Temporada: {formatar_preco(self.preco_alta_temporada)}")

        # Cores para o estado
        cores_estado = {
            "Livre": "verde",
            "Ocupado": "vermelho",
            "Manutencao": "amarelo",
            "Reservado": "ciano",
        }
        cor_estado = cores_estado.get(self.estado, "branco")
        print(f"Estado: {cor(self.estado, cor_estado, estilo='negrito')}")
        print(f"Data Criacao: {self.data_criacao}")

        if self.observacoes:
            print(f"Observacoes: {self.observacoes}")
        print(linha_separadora(50))

    def alterar_estado(self, novo_estado):
        """
        Altera o estado da unidade.

        Parametros:
            novo_estado (str): Novo estado ("Livre", "Ocupado",
                               "Manutencao", "Reservado")

        Retorna:
            bool: True se alterado com sucesso, False caso contrario
        """
        estados_validos = ["Livre", "Ocupado", "Manutencao", "Reservado"]

        if novo_estado not in estados_validos:
            print(
                cor(
                    f"Estado invalido. Opcoes: {', '.join(estados_validos)}", "vermelho"
                )
            )
            return False

        # Atualiza o estado na lista de dados
        for unidade in unidades:
            if unidade["id"] == self.id:
                unidade["estado"] = novo_estado
                self.estado = novo_estado
                print(cor(f"Estado alterado para: {novo_estado}", "verde"))
                return True

        print(cor("Erro ao alterar estado. Unidade nao encontrada.", "vermelho"))
        return False

    def salvar(self):
        """
        Salva a unidade na base de dados em memoria.

        Retorna:
            bool: True se salvo com sucesso, False caso contrario
        """
        # Verifica se a unidade ja existe (atualizacao)
        for i, unidade in enumerate(unidades):
            if unidade["id"] == self.id:
                unidades[i] = self.to_dict()
                print(cor(f"Unidade '{self.nome}' atualizada com sucesso!", "verde"))
                return True

        # Se nao existe, adiciona nova
        unidades.append(self.to_dict())
        print(
            cor(f"Unidade '{self.nome}' criada com sucesso! (ID: {self.id})", "verde")
        )
        return True

    @staticmethod
    def listar_todas():
        """
        Lista todas as unidades cadastradas.
        """
        if not unidades:
            print(cor("Nenhuma unidade cadastrada.", "amarelo"))
            return

        print("\n" + cabecalho("LISTA DE UNIDADES"))
        print(f"Total: {len(unidades)} unidades\n")

        for unidade in unidades:
            # Cores para o estado
            cores_estado = {
                "Livre": "verde",
                "Ocupado": "vermelho",
                "Manutencao": "amarelo",
                "Reservado": "ciano",
            }
            cor_estado = cores_estado.get(unidade["estado"], "branco")

            print(f"ID: {unidade['id']} | {unidade['nome']}")
            print(
                f"  Tipo: {unidade['tipo']} | Capacidade: {unidade['capacidade']} pessoas"
            )
            print(f"  Preco: {formatar_preco(unidade['preco_base'])}")
            print(f"  Estado: {cor(unidade['estado'], cor_estado, estilo='negrito')}")
            print(linha_separadora(40))

    @staticmethod
    def listar_por_tipo(tipo):
        """
        Lista unidades filtradas por tipo.

        Parametros:
            tipo (str): "Mensal" ou "Airbnb"
        """
        if tipo not in ["Mensal", "Airbnb"]:
            print(cor("Tipo invalido. Use 'Mensal' ou 'Airbnb'.", "vermelho"))
            return

        filtradas = [u for u in unidades if u["tipo"] == tipo]

        if not filtradas:
            print(cor(f"Nenhuma unidade do tipo '{tipo}' encontrada.", "amarelo"))
            return

        print(f"\n{cabecalho(f'UNIDADES - {tipo.upper()}')}")
        print(f"Total: {len(filtradas)} unidades\n")

        for unidade in filtradas:
            print(f"ID: {unidade['id']} | {unidade['nome']}")
            print(f"  Capacidade: {unidade['capacidade']} pessoas")
            print(f"  Preco: {formatar_preco(unidade['preco_base'])}")
            print(f"  Estado: {unidade['estado']}")
            print(linha_separadora(40))

    @staticmethod
    def buscar_por_id(id_unidade):
        """
        Busca uma unidade pelo ID.

        Parametros:
            id_unidade (int): ID da unidade

        Retorna:
            dict: Dados da unidade, ou None se nao encontrada
        """
        for unidade in unidades:
            if unidade["id"] == id_unidade:
                return unidade
        return None

    @staticmethod
    def buscar_por_nome(nome):
        """
        Busca uma unidade pelo nome (busca parcial).

        Parametros:
            nome (str): Nome ou parte do nome

        Retorna:
            list: Lista de unidades que correspondem a busca
        """
        nome_lower = nome.lower()
        return [u for u in unidades if nome_lower in u["nome"].lower()]

    @staticmethod
    def remover(id_unidade):
        """
        Remove uma unidade pelo ID.

        Parametros:
            id_unidade (int): ID da unidade

        Retorna:
            bool: True se removido com sucesso, False caso contrario
        """
        for i, unidade in enumerate(unidades):
            if unidade["id"] == id_unidade:
                # Verifica se a unidade esta ocupada
                if unidade["estado"] == "Ocupado":
                    print(
                        cor("Nao e possivel remover uma unidade ocupada.", "vermelho")
                    )
                    return False

                nome = unidade["nome"]
                del unidades[i]
                print(cor(f"Unidade '{nome}' removida com sucesso!", "verde"))
                return True

        print(cor(f"Unidade com ID {id_unidade} nao encontrada.", "vermelho"))
        return False


# ------------------------------------------------------------
# 2. FUNCOES DE INTERFACE (CRUD)
# ------------------------------------------------------------


def criar_unidade():
    """
    Interface para criar uma nova unidade.
    Solicita os dados ao utilizador e cria a unidade.
    """
    print("\n" + cabecalho("CRIAR NOVA UNIDADE"))

    # Nome
    nome = input_obrigatorio("Nome da unidade: ")

    # Tipo
    tipo = input_opcao("Tipo da unidade", ["Mensal", "Airbnb"])

    # Capacidade
    print("\nDefinicao de capacidade:")
    capacidade = input_int("Capacidade maxima de pessoas: ", min_valor=1)

    # Camas
    print("\nDefinicao de camas:")
    qtd_camas_solteiro = input_int("Quantidade de camas de solteiro: ", min_valor=0)
    qtd_camas_casal = input_int("Quantidade de camas de casal: ", min_valor=0)

    # Cama extra
    tem_cama_extra = input_sim_nao("Possui cama extra? (S/N): ")

    # Precos
    print("\nDefinicao de precos:")
    preco_base = input_float(
        "Preco base (Mensal: renda | Airbnb: diaria): ", min_valor=0
    )

    preco_alta_temporada = None
    if tipo == "Airbnb":
        preco_alta_temporada = input_float(
            "Preco alta temporada (opcional, Enter para pular): ", obrigatorio=False
        )

    # Estado inicial
    estado = input_opcao("Estado inicial", ["Livre", "Manutencao"])

    # Observacoes
    observacoes = input("Observacoes (opcional): ").strip()

    # Cria a unidade
    unidade = Unidade(
        nome=nome,
        tipo=tipo,
        capacidade=capacidade, # type: ignore
        qtd_camas_solteiro=qtd_camas_solteiro, # type: ignore
        qtd_camas_casal=qtd_camas_casal, # type: ignore
        tem_cama_extra=tem_cama_extra,
        preco_base=preco_base, # type: ignore
        preco_alta_temporada=preco_alta_temporada,
        estado=estado,
        observacoes=observacoes,
    )

    # Salva
    unidade.salvar()

    # Exibe a unidade criada
    unidade.exibir()

    return unidade


def editar_unidade():
    """
    Interface para editar uma unidade existente.
    """
    print("\n" + cabecalho("EDITAR UNIDADE"))

    # Lista as unidades para o utilizador escolher
    Unidade.listar_todas()

    if not unidades:
        return

    # Seleciona a unidade
    try:
        id_unidade = input_int("ID da unidade para editar: ", min_valor=1)
    except:
        print(cor("Operacao cancelada.", "amarelo"))
        return

    # Busca a unidade
    dados_unidade = Unidade.buscar_por_id(id_unidade)

    if not dados_unidade:
        print(cor(f"Unidade com ID {id_unidade} nao encontrada.", "vermelho"))
        return

    # Cria objeto para edicao
    unidade = Unidade.from_dict(dados_unidade)

    print(f"\nEditando: {cor(unidade.nome, 'azul', estilo='negrito')}")
    print("(Deixe em branco para manter o valor atual)")

    # Edita os campos
    novo_nome = input(f"Nome ({unidade.nome}): ").strip()
    if novo_nome:
        unidade.nome = novo_nome

    nova_capacidade = input(f"Capacidade ({unidade.capacidade}): ").strip()
    if nova_capacidade:
        try:
            unidade.capacidade = int(nova_capacidade)
        except ValueError:
            print(cor("Valor invalido. Mantendo o atual.", "amarelo"))

    novo_preco = input(f"Preco Base ({unidade.preco_base}): ").strip()
    if novo_preco:
        try:
            unidade.preco_base = float(novo_preco.replace(",", "."))
        except ValueError:
            print(cor("Valor invalido. Mantendo o atual.", "amarelo"))

    novas_obs = input(f"Observacoes ({unidade.observacoes}): ").strip()
    if novas_obs:
        unidade.observacoes = novas_obs

    # Confirma a edicao
    print("\nDados atualizados:")
    unidade.exibir()

    if input_sim_nao("Confirmar alteracoes? (S/N): "):
        unidade.salvar()
    else:
        print(cor("Edicao cancelada.", "amarelo"))


def listar_unidades():
    """
    Interface para listar unidades com filtros.
    """
    print("\n" + cabecalho("LISTAR UNIDADES"))

    print("Opcoes de filtro:")
    print("  1 - Todas as unidades")
    print("  2 - Apenas Mensal")
    print("  3 - Apenas Airbnb")
    print("  4 - Buscar por nome")
    print("  0 - Voltar")

    opcao = input("\nEscolha uma opcao: ").strip()

    if opcao == "1":
        Unidade.listar_todas()
    elif opcao == "2":
        Unidade.listar_por_tipo("Mensal")
    elif opcao == "3":
        Unidade.listar_por_tipo("Airbnb")
    elif opcao == "4":
        nome = input_obrigatorio("Digite o nome (ou parte): ")
        resultados = Unidade.buscar_por_nome(nome)
        if resultados:
            print(f"\n{cabecalho('RESULTADOS DA BUSCA')}")
            for unidade in resultados:
                print(f"ID: {unidade['id']} | {unidade['nome']} | {unidade['tipo']}")
        else:
            print(cor("Nenhuma unidade encontrada.", "amarelo"))
    elif opcao == "0":
        return
    else:
        print(cor("Opcao invalida.", "vermelho"))


def alterar_estado_unidade():
    """
    Interface para alterar o estado de uma unidade.
    """
    print("\n" + cabecalho("ALTERAR ESTADO DA UNIDADE"))

    Unidade.listar_todas()

    if not unidades:
        return

    try:
        id_unidade = input_int("ID da unidade: ", min_valor=1)
    except:
        print(cor("Operacao cancelada.", "amarelo"))
        return

    dados_unidade = Unidade.buscar_por_id(id_unidade)

    if not dados_unidade:
        print(cor(f"Unidade com ID {id_unidade} nao encontrada.", "vermelho"))
        return

    unidade = Unidade.from_dict(dados_unidade)

    print(f"\nUnidade: {cor(unidade.nome, 'azul', estilo='negrito')}")
    print(f"Estado atual: {cor(unidade.estado, 'amarelo')}")

    print("\nNovo estado:")
    print("  1 - Livre")
    print("  2 - Ocupado")
    print("  3 - Manutencao")
    print("  4 - Reservado")
    print("  0 - Cancelar")

    opcao = input("\nEscolha: ").strip()

    estados = {"1": "Livre", "2": "Ocupado", "3": "Manutencao", "4": "Reservado"}

    if opcao == "0":
        print(cor("Operacao cancelada.", "amarelo"))
        return

    if opcao not in estados:
        print(cor("Opcao invalida.", "vermelho"))
        return

    novo_estado = estados[opcao]

    if input_sim_nao(f"Alterar estado para '{novo_estado}'? (S/N): "):
        unidade.alterar_estado(novo_estado)


def remover_unidade():
    """
    Interface para remover uma unidade.
    """
    print("\n" + cabecalho("REMOVER UNIDADE"))

    Unidade.listar_todas()

    if not unidades:
        return

    try:
        id_unidade = input_int("ID da unidade para remover: ", min_valor=1)
    except:
        print(cor("Operacao cancelada.", "amarelo"))
        return

    dados_unidade = Unidade.buscar_por_id(id_unidade)

    if not dados_unidade:
        print(cor(f"Unidade com ID {id_unidade} nao encontrada.", "vermelho"))
        return

    # Exibe a unidade para confirmacao
    unidade = Unidade.from_dict(dados_unidade)
    unidade.exibir()

    print(
        cor(
            "ATENCAO: Esta operacao nao pode ser desfeita!",
            "vermelho",
            estilo="negrito",
        )
    )

    if input_sim_nao("Tem certeza que deseja remover esta unidade? (S/N): "):
        # Dupla confirmacao para remocao
        if input_sim_nao("Confirmar novamente? (S/N): "):
            Unidade.remover(id_unidade)


# ------------------------------------------------------------
# 3. MENU DE UNIDADES
# ------------------------------------------------------------


def menu_unidades():
    """
    Menu principal do modulo de unidades.
    """
    while True:
        print("\n" + cabecalho("GESTAO DE UNIDADES"))
        print("  1 - Criar unidade")
        print("  2 - Listar unidades")
        print("  3 - Editar unidade")
        print("  4 - Alterar estado")
        print("  5 - Remover unidade")
        print("  0 - Voltar")
        print(linha_separadora())

        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            criar_unidade()
        elif opcao == "2":
            listar_unidades()
        elif opcao == "3":
            editar_unidade()
        elif opcao == "4":
            alterar_estado_unidade()
        elif opcao == "5":
            remover_unidade()
        elif opcao == "0":
            print(cor("Voltando...", "amarelo"))
            break
        else:
            print(cor("Opcao invalida. Tente novamente.", "vermelho"))


# ------------------------------------------------------------
# 4. DADOS DE EXEMPLO
# ------------------------------------------------------------


def carregar_unidades_exemplo():
    """
    Carrega unidades de exemplo no sistema.
    Util para testes e demonstracao.
    """
    # Unidades Mensal
    unidades_exemplo = [
        {
            "nome": "Foz Velha",
            "tipo": "Mensal",
            "capacidade": 15,
            "qtd_camas_solteiro": 6,
            "qtd_camas_casal": 4,
            "tem_cama_extra": False,
            "preco_base": 250.00,
            "preco_alta_temporada": None,
            "estado": "Livre",
            "observacoes": "Unidade principal",
        },
        {
            "nome": "Foz Pinhais",
            "tipo": "Mensal",
            "capacidade": 12,
            "qtd_camas_solteiro": 4,
            "qtd_camas_casal": 4,
            "tem_cama_extra": False,
            "preco_base": 250.00,
            "preco_alta_temporada": None,
            "estado": "Livre",
            "observacoes": "",
        },
        {
            "nome": "Aldoar",
            "tipo": "Mensal",
            "capacidade": 10,
            "qtd_camas_solteiro": 4,
            "qtd_camas_casal": 3,
            "tem_cama_extra": False,
            "preco_base": 250.00,
            "preco_alta_temporada": None,
            "estado": "Livre",
            "observacoes": "",
        },
    ]

    # Unidades Airbnb
    for i in range(1, 14):
        unidades_exemplo.append(
            {
                "nome": f"Rei Ramiro {i}",
                "tipo": "Airbnb",
                "capacidade": 4,
                "qtd_camas_solteiro": 2,
                "qtd_camas_casal": 1,
                "tem_cama_extra": True,
                "preco_base": 45.00,
                "preco_alta_temporada": 90.00,
                "estado": "Livre",
                "observacoes": "",
            }
        )

    # Mais Airbnb
    airbnb_extra = [
        {"nome": "Beco", "capacidade": 4},
        {"nome": "Santa Catarina AP2", "capacidade": 4},
        {"nome": "Santa Catarina AP3", "capacidade": 4},
        {"nome": "Santa Catarina AP4", "capacidade": 4},
        {"nome": "Casa da Musica", "capacidade": 4},
    ]

    for item in airbnb_extra:
        unidades_exemplo.append(
            {
                "nome": item["nome"],
                "tipo": "Airbnb",
                "capacidade": item["capacidade"],
                "qtd_camas_solteiro": 2,
                "qtd_camas_casal": 1,
                "tem_cama_extra": True,
                "preco_base": 45.00,
                "preco_alta_temporada": 90.00,
                "estado": "Livre",
                "observacoes": "",
            }
        )

    # Carrega as unidades
    for dados in unidades_exemplo:
        unidade = Unidade(
            nome=dados["nome"],
            tipo=dados["tipo"],
            capacidade=dados["capacidade"],
            qtd_camas_solteiro=dados["qtd_camas_solteiro"],
            qtd_camas_casal=dados["qtd_camas_casal"],
            tem_cama_extra=dados["tem_cama_extra"],
            preco_base=dados["preco_base"],
            preco_alta_temporada=dados["preco_alta_temporada"],
            estado=dados["estado"],
            observacoes=dados["observacoes"],
        )
        unidade.salvar()

    print(cor(f"{len(unidades_exemplo)} unidades de exemplo carregadas!", "verde"))


# ------------------------------------------------------------
# 5. BLOCO DE TESTE
# ------------------------------------------------------------

if __name__ == "__main__":

    print("\n" + cabecalho("TESTE DO MODULO DE UNIDADES"))

    # Carrega dados de exemplo
    carregar_unidades_exemplo()

    # Mostra o estado dos dados
    mostrar_estado_dados()

    # Lista as unidades
    Unidade.listar_todas()

    # Testa a busca por ID
    print("\n" + cabecalho("TESTE DE BUSCA POR ID"))
    unidade = Unidade.buscar_por_id(1)
    if unidade:
        print(f"Unidade encontrada: {unidade['nome']}")

    # Testa a busca por nome
    print("\n" + cabecalho("TESTE DE BUSCA POR NOME"))
    resultados = Unidade.buscar_por_nome("Ramiro")
    print(f"Encontradas {len(resultados)} unidades com 'Ramiro'")

    # Exibe menu (comentado para nao travar o teste)
    # menu_unidades()

    print("\n" + cabecalho("TESTE CONCLUIDO"))
