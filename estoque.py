# ============================================================
# estoque.py - GESTAO DE ESTOQUE
# ============================================================
# Modulo responsavel por gerenciar o inventario do hostel.
# Controla produtos, consumos, alertas e solicitacoes de compra.
#
# Dependencias:
#   - dados.py: Para acesso a base de dados em memoria
#   - utils.py: Para funcoes auxiliares
#   - unidades.py: Para associar produtos a unidades
# ============================================================

from dados import (
    produtos,
    consumos,
    proximo_id_produto,
    proximo_id_consumo,
    mostrar_estado_dados,
)
from utils import (
    cor,
    cabecalho,
    input_data,
    linha_separadora,
    input_obrigatorio,
    input_float,
    input_int,
    input_sim_nao,
    input_opcao,
    formatar_preco,
    obter_data_atual,
)
from unidades import Unidade

# ------------------------------------------------------------
# 1. CLASSE PRODUTO
# ------------------------------------------------------------


class Produto:
    """
    Classe que representa um produto no estoque.

    Atributos:
        id (int): Identificador unico do produto
        nome (str): Nome do produto
        codigo (str): Codigo interno (ex: LIM-001)
        categoria (str): Categoria do produto
        unidade_medida (str): Litros, Unidades, Rolos, Pacotes
        quantidade_atual (int): Quantidade em stock
        quantidade_minima (int): Nivel minimo para alerta
        unidade_id (int): ID da unidade associada (None = stock central)
        tipo_unidade_destino (str): "Mensal", "Airbnb" ou "Ambos"
        preco_unitario (float): Preco por unidade
        fornecedor (str): Nome do fornecedor
        observacoes (str): Observacoes gerais
    """

    CATEGORIAS = ["Limpeza", "Roupa", "Snacks", "Cafe", "Higiene", "Outros"]
    UNIDADES_MEDIDA = ["Litros", "Unidades", "Rolos", "Pacotes", "Kilos", "Metros"]
    TIPOS_DESTINO = ["Mensal", "Airbnb", "Ambos"]

    def __init__(
        self,
        nome,
        categoria,
        unidade_medida,
        quantidade_atual,
        quantidade_minima,
        unidade_id=None,
        tipo_unidade_destino="Ambos",
        preco_unitario=0.0,
        fornecedor="",
        codigo="",
        observacoes="",
    ):
        """
        Inicializa um novo produto.

        Parametros:
            nome (str): Nome do produto
            categoria (str): Categoria do produto
            unidade_medida (str): Unidade de medida
            quantidade_atual (int): Quantidade em stock
            quantidade_minima (int): Nivel minimo para alerta
            unidade_id (int): ID da unidade (None = central)
            tipo_unidade_destino (str): "Mensal", "Airbnb", "Ambos"
            preco_unitario (float): Preco por unidade
            fornecedor (str): Nome do fornecedor
            codigo (str): Codigo interno
            observacoes (str): Observacoes
        """
        self.id = proximo_id_produto()
        self.nome = nome
        self.codigo = codigo if codigo else self._gerar_codigo(categoria)
        self.categoria = categoria
        self.unidade_medida = unidade_medida
        self.quantidade_atual = quantidade_atual
        self.quantidade_minima = quantidade_minima
        self.unidade_id = unidade_id
        self.tipo_unidade_destino = tipo_unidade_destino
        self.preco_unitario = preco_unitario
        self.fornecedor = fornecedor
        self.observacoes = observacoes
        self.data_criacao = obter_data_atual("%Y-%m-%d %H:%M:%S")

    def _gerar_codigo(self, categoria):
        """
        Gera um codigo automatico baseado na categoria.

        Parametros:
            categoria (str): Categoria do produto

        Retorna:
            str: Codigo gerado
        """
        prefixos = {
            "Limpeza": "LIM",
            "Roupa": "ROP",
            "Snacks": "SNK",
            "Cafe": "CAF",
            "Higiene": "HIG",
            "Outros": "OUT",
        }
        prefixo = prefixos.get(categoria, "PRD")

        # Conta quantos produtos existem com este prefixo
        count = sum(1 for p in produtos if p["codigo"].startswith(prefixo))
        return f"{prefixo}-{count + 1:03d}"

    def to_dict(self):
        """
        Converte o produto para um dicionario.

        Retorna:
            dict: Dicionario com todos os atributos do produto
        """
        return {
            "id": self.id,
            "nome": self.nome,
            "codigo": self.codigo,
            "categoria": self.categoria,
            "unidade_medida": self.unidade_medida,
            "quantidade_atual": self.quantidade_atual,
            "quantidade_minima": self.quantidade_minima,
            "unidade_id": self.unidade_id,
            "tipo_unidade_destino": self.tipo_unidade_destino,
            "preco_unitario": self.preco_unitario,
            "fornecedor": self.fornecedor,
            "observacoes": self.observacoes,
            "data_criacao": self.data_criacao,
        }

    @staticmethod
    def from_dict(dados):
        """
        Cria uma instancia de Produto a partir de um dicionario.

        Parametros:
            dados (dict): Dicionario com os dados do produto

        Retorna:
            Produto: Instancia do produto
        """
        produto = Produto(
            nome=dados["nome"],
            categoria=dados["categoria"],
            unidade_medida=dados["unidade_medida"],
            quantidade_atual=dados["quantidade_atual"],
            quantidade_minima=dados["quantidade_minima"],
            unidade_id=dados.get("unidade_id"),
            tipo_unidade_destino=dados.get("tipo_unidade_destino", "Ambos"),
            preco_unitario=dados.get("preco_unitario", 0.0),
            fornecedor=dados.get("fornecedor", ""),
            codigo=dados.get("codigo", ""),
            observacoes=dados.get("observacoes", ""),
        )
        produto.id = dados["id"]
        produto.data_criacao = dados.get("data_criacao", obter_data_atual())
        return produto

    def exibir(self):
        """
        Exibe os detalhes do produto formatados no terminal.
        """
        print("\n" + linha_separadora(50))
        print(cor(f"ID: {self.id}", "azul", estilo="negrito"))
        print(f"Nome: {self.nome}")
        print(f"Codigo: {self.codigo}")
        print(f"Categoria: {self.categoria}")
        print(f"Unidade: {self.unidade_medida}")

        # Stock com alerta se estiver baixo
        stock_texto = f"{self.quantidade_atual} / {self.quantidade_minima} (min)"
        if self.quantidade_atual <= self.quantidade_minima:
            print(
                f"Quantidade: {cor(stock_texto, 'vermelho', estilo='negrito')} - ALERTA!"
            )
        else:
            print(f"Quantidade: {cor(stock_texto, 'verde')}")

        print(f"Preco Unitario: {formatar_preco(self.preco_unitario)}")

        # Localizacao
        if self.unidade_id is None:
            print("Localizacao: Stock Central")
        else:
            unidade = Unidade.buscar_por_id(self.unidade_id)
            nome_unidade = unidade["nome"] if unidade else f"ID {self.unidade_id}"
            print(f"Localizacao: {nome_unidade}")

        print(f"Tipo Destino: {self.tipo_unidade_destino}")
        print(f"Fornecedor: {self.fornecedor if self.fornecedor else 'Nao definido'}")
        print(f"Data Criacao: {self.data_criacao}")

        if self.observacoes:
            print(f"Observacoes: {self.observacoes}")
        print(linha_separadora(50))

    def alterar_quantidade(self, nova_quantidade):
        """
        Altera a quantidade atual do produto.

        Parametros:
            nova_quantidade (int): Nova quantidade

        Retorna:
            bool: True se alterado com sucesso
        """
        if nova_quantidade < 0:
            print(cor("Quantidade nao pode ser negativa.", "vermelho"))
            return False

        self.quantidade_atual = nova_quantidade

        # Atualiza na lista de dados
        for i, produto in enumerate(produtos):
            if produto["id"] == self.id:
                produtos[i] = self.to_dict()
                break

        # Verifica se esta abaixo do minimo
        if self.quantidade_atual <= self.quantidade_minima:
            print(cor(f"ALERTA: {self.nome} esta abaixo do stock minimo!", "vermelho"))

        return True

    def adicionar_quantidade(self, quantidade):
        """
        Adiciona quantidade ao stock.

        Parametros:
            quantidade (int): Quantidade a adicionar

        Retorna:
            bool: True se adicionado com sucesso
        """
        if quantidade <= 0:
            print(cor("Quantidade deve ser positiva.", "vermelho"))
            return False

        self.quantidade_atual += quantidade

        # Atualiza na lista de dados
        for i, produto in enumerate(produtos):
            if produto["id"] == self.id:
                produtos[i] = self.to_dict()
                break

        print(
            cor(
                f"Adicionados {quantidade} {self.unidade_medida} de {self.nome}.",
                "verde",
            )
        )
        return True

    def consumir(
        self, quantidade, unidade_id, staff_nome, motivo="", criar_solicitacao=True
    ):
        """
        Consome uma quantidade do produto e registra o consumo.

        Parametros:
            quantidade (int): Quantidade a consumir
            unidade_id (int): ID da unidade onde ocorre o consumo
            staff_nome (str): Nome do staff que registou
            motivo (str): Motivo do consumo
            criar_solicitacao (bool): Se deve criar solicitacao se estoque baixo

        Retorna:
            bool: True se consumido com sucesso
        """
        if quantidade <= 0:
            print(cor("Quantidade deve ser positiva.", "vermelho"))
            return False

        if self.quantidade_atual < quantidade:
            print(
                cor(f"Stock insuficiente. Atual: {self.quantidade_atual}", "vermelho")
            )
            return False

        # Registra o consumo
        from estoque import Consumo

        consumo = Consumo(
            produto_id=self.id,
            unidade_id=unidade_id,
            quantidade=quantidade,
            staff_nome=staff_nome,
            motivo=motivo,
        )
        consumo.salvar()

        # Atualiza a quantidade
        self.quantidade_atual -= quantidade

        # Atualiza na lista de dados
        for i, produto in enumerate(produtos):
            if produto["id"] == self.id:
                produtos[i] = self.to_dict()
                break

        print(
            cor(
                f"Consumidos {quantidade} {self.unidade_medida} de {self.nome}.",
                "amarelo",
            )
        )

        # Verifica alerta
        if self.quantidade_atual <= self.quantidade_minima:
            print(cor(f"ALERTA: {self.nome} esta abaixo do stock minimo!", "vermelho"))

            if criar_solicitacao:
                self._criar_solicitacao_compra(unidade_id, staff_nome)

        return True

    def _criar_solicitacao_compra(self, unidade_id, staff_nome):
        """
        Cria uma solicitacao de compra quando o stock esta baixo.

        Parametros:
            unidade_id (int): ID da unidade
            staff_nome (str): Nome do staff que solicitou
        """
        print(cor(f"Gerando solicitacao de compra para {self.nome}...", "amarelo"))

        # Busca a unidade
        unidade = Unidade.buscar_por_id(unidade_id)
        nome_unidade = unidade["nome"] if unidade else f"ID {unidade_id}"

        solicitacao = {
            "produto_id": self.id,
            "produto_nome": self.nome,
            "unidade_id": unidade_id,
            "unidade_nome": nome_unidade,
            "quantidade_sugerida": self.quantidade_minima * 2,
            "quantidade_atual": self.quantidade_atual,
            "staff_nome": staff_nome,
            "data": obter_data_atual("%Y-%m-%d %H:%M:%S"),
            "status": "Pendente",
        }

        # Aqui podemos adicionar a solicitacao a uma lista futura
        # Por enquanto, apenas exibimos no terminal
        print("\n" + linha_separadora(50))
        print(cor("SOLICITACAO DE COMPRA", "amarelo", estilo="negrito"))
        print(f"Produto: {self.nome}")
        print(f"Unidade: {nome_unidade}")
        print(f"Stock Atual: {self.quantidade_atual} {self.unidade_medida}")
        print(f"Minimo: {self.quantidade_minima} {self.unidade_medida}")
        print(f"Sugerido: {self.quantidade_minima * 2} {self.quantidade_medida}") # type: ignore
        print(f"Solicitado por: {staff_nome}")
        print(f"Data: {solicitacao['data']}")
        print(linha_separadora(50))

        return solicitacao

    def salvar(self):
        """
        Salva o produto na base de dados em memoria.

        Retorna:
            bool: True se salvo com sucesso
        """
        # Verifica se o produto ja existe (atualizacao)
        for i, produto in enumerate(produtos):
            if produto["id"] == self.id:
                produtos[i] = self.to_dict()
                print(cor(f"Produto '{self.nome}' atualizado com sucesso!", "verde"))
                return True

        # Se nao existe, adiciona novo
        produtos.append(self.to_dict())
        print(
            cor(f"Produto '{self.nome}' criado com sucesso! (ID: {self.id})", "verde")
        )
        return True

    @staticmethod
    def listar_todos():
        """
        Lista todos os produtos cadastrados.
        """
        if not produtos:
            print(cor("Nenhum produto cadastrado.", "amarelo"))
            return

        print("\n" + cabecalho("LISTA DE PRODUTOS"))
        print(f"Total: {len(produtos)} produtos\n")

        for produto in produtos:
            # Cor para o stock
            if produto["quantidade_atual"] <= produto["quantidade_minima"]:
                status = cor("BAIXO", "vermelho")
            else:
                status = cor("OK", "verde")

            # Localizacao
            local = (
                "Central"
                if produto["unidade_id"] is None
                else f"Unidade {produto['unidade_id']}"
            )

            print(f"ID: {produto['id']} | {produto['nome']}")
            print(f"  Codigo: {produto['codigo']} | Categoria: {produto['categoria']}")
            print(
                f"  Stock: {produto['quantidade_atual']} {produto['unidade_medida']} [{status}]"
            )
            print(f"  Local: {local} | Destino: {produto['tipo_unidade_destino']}")
            print(linha_separadora(40))

    @staticmethod
    def listar_com_alerta():
        """
        Lista apenas produtos com stock abaixo do minimo.
        """
        alertas = [
            p for p in produtos if p["quantidade_atual"] <= p["quantidade_minima"]
        ]

        if not alertas:
            print(cor("Nenhum produto com alerta de stock baixo.", "verde"))
            return

        print("\n" + cabecalho("PRODUTOS COM STOCK BAIXO"))
        print(
            cor(
                "ATENCAO: Os seguintes produtos precisam de reposicao!",
                "vermelho",
                estilo="negrito",
            )
        )
        print()

        for produto in alertas:
            falta = produto["quantidade_minima"] - produto["quantidade_atual"]
            print(f"  {cor(produto['nome'], 'amarelo')}")
            print(
                f"    Atual: {produto['quantidade_atual']} {produto['unidade_medida']}"
            )
            print(
                f"    Minimo: {produto['quantidade_minima']} {produto['unidade_medida']}"
            )
            print(f"    Falta: {falta} {produto['unidade_medida']}")
            print(linha_separadora(35))

    @staticmethod
    def buscar_por_id(id_produto):
        """
        Busca um produto pelo ID.

        Parametros:
            id_produto (int): ID do produto

        Retorna:
            dict: Dados do produto, ou None se nao encontrado
        """
        for produto in produtos:
            if produto["id"] == id_produto:
                return produto
        return None

    @staticmethod
    def buscar_por_codigo(codigo):
        """
        Busca um produto pelo codigo.

        Parametros:
            codigo (str): Codigo do produto

        Retorna:
            dict: Dados do produto, ou None se nao encontrado
        """
        codigo_upper = codigo.upper()
        for produto in produtos:
            if produto["codigo"].upper() == codigo_upper:
                return produto
        return None

    @staticmethod
    def buscar_por_unidade(unidade_id):
        """
        Busca produtos de uma unidade especifica.

        Parametros:
            unidade_id (int): ID da unidade

        Retorna:
            list: Lista de produtos da unidade
        """
        return [p for p in produtos if p["unidade_id"] == unidade_id]

    @staticmethod
    def remover(id_produto):
        """
        Remove um produto pelo ID.

        Parametros:
            id_produto (int): ID do produto

        Retorna:
            bool: True se removido com sucesso
        """
        for i, produto in enumerate(produtos):
            if produto["id"] == id_produto:
                nome = produto["nome"]
                del produtos[i]
                print(cor(f"Produto '{nome}' removido com sucesso!", "verde"))
                return True

        print(cor(f"Produto com ID {id_produto} nao encontrado.", "vermelho"))
        return False


# ------------------------------------------------------------
# 2. CLASSE CONSUMO
# ------------------------------------------------------------


class Consumo:
    """
    Classe que representa um consumo de produto.

    Atributos:
        id (int): Identificador unico do consumo
        produto_id (int): ID do produto consumido
        unidade_id (int): ID da unidade onde ocorreu
        quantidade (int): Quantidade consumida
        data (str): Data do consumo
        staff_nome (str): Nome do staff que registou
        motivo (str): Motivo do consumo
        status (str): "Pendente", "Aprovado", "Reposto"
        observacao (str): Observacoes adicionais
    """

    def __init__(
        self, produto_id, unidade_id, quantidade, staff_nome, motivo="", observacao=""
    ):
        """
        Inicializa um novo consumo.

        Parametros:
            produto_id (int): ID do produto
            unidade_id (int): ID da unidade
            quantidade (int): Quantidade consumida
            staff_nome (str): Nome do staff
            motivo (str): Motivo do consumo
            observacao (str): Observacoes
        """
        self.id = proximo_id_consumo()
        self.produto_id = produto_id
        self.unidade_id = unidade_id
        self.quantidade = quantidade
        self.data = obter_data_atual("%Y-%m-%d %H:%M:%S")
        self.staff_nome = staff_nome
        self.motivo = motivo
        self.status = "Pendente"
        self.observacao = observacao

    def to_dict(self):
        """
        Converte o consumo para um dicionario.

        Retorna:
            dict: Dicionario com todos os atributos do consumo
        """
        return {
            "id": self.id,
            "produto_id": self.produto_id,
            "unidade_id": self.unidade_id,
            "quantidade": self.quantidade,
            "data": self.data,
            "staff_nome": self.staff_nome,
            "motivo": self.motivo,
            "status": self.status,
            "observacao": self.observacao,
        }

    @staticmethod
    def from_dict(dados):
        """
        Cria uma instancia de Consumo a partir de um dicionario.

        Parametros:
            dados (dict): Dicionario com os dados do consumo

        Retorna:
            Consumo: Instancia do consumo
        """
        consumo = Consumo(
            produto_id=dados["produto_id"],
            unidade_id=dados["unidade_id"],
            quantidade=dados["quantidade"],
            staff_nome=dados["staff_nome"],
            motivo=dados.get("motivo", ""),
            observacao=dados.get("observacao", ""),
        )
        consumo.id = dados["id"]
        consumo.data = dados["data"]
        consumo.status = dados.get("status", "Pendente")
        return consumo

    def salvar(self):
        """
        Salva o consumo na base de dados em memoria.
        """
        consumos.append(self.to_dict())
        return True

    def aprovar(self):
        """
        Aprova o consumo.
        """
        self.status = "Aprovado"
        for i, consumo in enumerate(consumos):
            if consumo["id"] == self.id:
                consumos[i] = self.to_dict()
                break
        print(cor(f"Consumo {self.id} aprovado.", "verde"))

    def reprovar(self):
        """
        Reprova o consumo.
        """
        self.status = "Reposto"
        for i, consumo in enumerate(consumos):
            if consumo["id"] == self.id:
                consumos[i] = self.to_dict()
                break
        print(cor(f"Consumo {self.id} registado como reposto.", "amarelo"))

    @staticmethod
    def listar_todos():
        """
        Lista todos os consumos registados.
        """
        if not consumos:
            print(cor("Nenhum consumo registado.", "amarelo"))
            return

        print("\n" + cabecalho("LISTA DE CONSUMOS"))
        print(f"Total: {len(consumos)} consumos\n")

        for consumo in consumos:
            # Busca o nome do produto
            produto = Produto.buscar_por_id(consumo["produto_id"])
            nome_produto = produto["nome"] if produto else f"ID {consumo['produto_id']}"

            # Busca o nome da unidade
            unidade = Unidade.buscar_por_id(consumo["unidade_id"])
            nome_unidade = unidade["nome"] if unidade else f"ID {consumo['unidade_id']}"

            # Cor para o status
            cores_status = {
                "Pendente": "amarelo",
                "Aprovado": "verde",
                "Reposto": "azul",
            }
            cor_status = cores_status.get(consumo["status"], "branco")

            print(f"ID: {consumo['id']} | {nome_produto}")
            print(f"  Unidade: {nome_unidade}")
            print(f"  Quantidade: {consumo['quantidade']}")
            print(f"  Staff: {consumo['staff_nome']}")
            print(f"  Data: {consumo['data']}")
            print(f"  Status: {cor(consumo['status'], cor_status)}")
            if consumo["motivo"]:
                print(f"  Motivo: {consumo['motivo']}")
            print(linha_separadora(40))

    @staticmethod
    def listar_por_unidade(unidade_id):
        """
        Lista consumos de uma unidade especifica.

        Parametros:
            unidade_id (int): ID da unidade
        """
        filtrados = [c for c in consumos if c["unidade_id"] == unidade_id]

        if not filtrados:
            print(cor("Nenhum consumo encontrado para esta unidade.", "amarelo"))
            return

        print(f"\n{cabecalho(f'CONSUMOS DA UNIDADE {unidade_id}')}")

        for consumo in filtrados:
            produto = Produto.buscar_por_id(consumo["produto_id"])
            nome_produto = produto["nome"] if produto else f"ID {consumo['produto_id']}"

            print(f"  {consumo['data']} | {nome_produto}")
            print(
                f"    Quantidade: {consumo['quantidade']} | Staff: {consumo['staff_nome']}"
            )

    @staticmethod
    def listar_por_periodo(data_inicio, data_fim):
        """
        Lista consumos entre duas datas.

        Parametros:
            data_inicio (str): Data inicio (YYYY-MM-DD)
            data_fim (str): Data fim (YYYY-MM-DD)
        """
        filtrados = []
        for consumo in consumos:
            data_consumo = consumo["data"].split(" ")[0]  # Pega apenas a data
            if data_inicio <= data_consumo <= data_fim:
                filtrados.append(consumo)

        if not filtrados:
            print(cor("Nenhum consumo encontrado no periodo.", "amarelo"))
            return

        print(f"\n{cabecalho(f'CONSUMOS DE {data_inicio} A {data_fim}')}")

        for consumo in filtrados:
            produto = Produto.buscar_por_id(consumo["produto_id"])
            nome_produto = produto["nome"] if produto else f"ID {consumo['produto_id']}"

            unidade = Unidade.buscar_por_id(consumo["unidade_id"])
            nome_unidade = unidade["nome"] if unidade else f"ID {consumo['unidade_id']}"

            print(f"  {consumo['data']} | {nome_produto} | {nome_unidade}")
            print(
                f"    Quantidade: {consumo['quantidade']} | Staff: {consumo['staff_nome']}"
            )


# ------------------------------------------------------------
# 3. FUNCOES DE INTERFACE (CRUD)
# ------------------------------------------------------------


def criar_produto():
    """
    Interface para criar um novo produto.
    """
    print("\n" + cabecalho("CRIAR NOVO PRODUTO"))

    # Dados basicos
    nome = input_obrigatorio("Nome do produto: ")
    categoria = input_opcao("Categoria", Produto.CATEGORIAS)
    unidade_medida = input_opcao("Unidade de medida", Produto.UNIDADES_MEDIDA)

    # Quantidades
    quantidade_atual = input_int("Quantidade atual em stock: ", min_valor=0)
    quantidade_minima = input_int("Quantidade minima (alerta): ", min_valor=0)

    # Localizacao
    print("\nLocalizacao do stock:")
    print("  1 - Stock Central")
    print("  2 - Unidade especifica")

    local_opcao = input("Opcao: ").strip()
    unidade_id = None

    if local_opcao == "2":
        from unidades import Unidade

        Unidade.listar_todas()
        try:
            unidade_id = input_int("ID da unidade: ", min_valor=1)
            if not Unidade.buscar_por_id(unidade_id):
                print(cor("Unidade nao encontrada. Usando Stock Central.", "amarelo"))
                unidade_id = None
        except:
            print(cor("Operacao cancelada. Usando Stock Central.", "amarelo"))
            unidade_id = None

    # Tipo de destino
    tipo_destino = input_opcao("Tipo de unidade destino", Produto.TIPOS_DESTINO)

    # Preco e fornecedor
    preco_unitario = (
        input_float("Preco unitario (€): ", min_valor=0, obrigatorio=False) or 0.0
    )
    fornecedor = input("Fornecedor (opcional): ").strip()
    observacoes = input("Observacoes (opcional): ").strip()

    # Cria o produto
    produto = Produto(
        nome=nome,
        categoria=categoria,
        unidade_medida=unidade_medida,
        quantidade_atual=quantidade_atual,
        quantidade_minima=quantidade_minima,
        unidade_id=unidade_id,
        tipo_unidade_destino=tipo_destino,
        preco_unitario=preco_unitario,
        fornecedor=fornecedor,
        observacoes=observacoes,
    )

    produto.salvar()
    produto.exibir()

    # Verifica alerta inicial
    if produto.quantidade_atual <= produto.quantidade_minima: # type: ignore
        print(cor("ALERTA: Produto criado com stock abaixo do minimo!", "vermelho"))

    return produto


def registrar_consumo():
    """
    Interface para registrar consumo de um produto.
    """
    print("\n" + cabecalho("REGISTRAR CONSUMO"))

    # Lista produtos com stock disponivel
    produtos_disponiveis = [p for p in produtos if p["quantidade_atual"] > 0]

    if not produtos_disponiveis:
        print(cor("Nenhum produto com stock disponivel.", "amarelo"))
        return

    print("\nProdutos disponiveis:")
    for p in produtos_disponiveis:
        print(
            f"  ID: {p['id']} | {p['nome']} | Stock: {p['quantidade_atual']} {p['unidade_medida']}"
        )

    try:
        produto_id = input_int("ID do produto: ", min_valor=1)
    except:
        print(cor("Operacao cancelada.", "amarelo"))
        return

    produto_dict = Produto.buscar_por_id(produto_id)
    if not produto_dict:
        print(cor("Produto nao encontrado.", "vermelho"))
        return

    produto = Produto.from_dict(produto_dict)

    # Unidade
    from unidades import Unidade

    Unidade.listar_todas()

    try:
        unidade_id = input_int("ID da unidade onde ocorre o consumo: ", min_valor=1)
    except:
        print(cor("Operacao cancelada.", "amarelo"))
        return

    if not Unidade.buscar_por_id(unidade_id):
        print(cor("Unidade nao encontrada.", "vermelho"))
        return

    # Quantidade
    print(f"\nStock atual: {produto.quantidade_atual} {produto.unidade_medida}")
    quantidade = input_int("Quantidade a consumir: ", min_valor=1)

    if quantidade > produto.quantidade_atual:
        print(cor("Quantidade superior ao stock disponivel.", "vermelho"))
        return

    # Dados do staff
    staff_nome = input_obrigatorio("Nome do staff que registou: ")
    motivo = input("Motivo do consumo (opcional): ").strip()

    # Confirma
    print("\nResumo do consumo:")
    print(f"  Produto: {produto.nome}")
    print(f"  Quantidade: {quantidade} {produto.unidade_medida}")
    print(f"  Unidade: {Unidade.buscar_por_id(unidade_id)['nome']}") # type: ignore
    print(f"  Staff: {staff_nome}")

    if input_sim_nao("Confirmar consumo? (S/N): "):
        produto.consumir(quantidade, unidade_id, staff_nome, motivo)

    return


def listar_produtos():
    """
    Interface para listar produtos com filtros.
    """
    print("\n" + cabecalho("LISTAR PRODUTOS"))

    print("Opcoes de filtro:")
    print("  1 - Todos os produtos")
    print("  2 - Produtos com alerta (stock baixo)")
    print("  3 - Produtos de uma categoria")
    print("  4 - Produtos de uma unidade")
    print("  0 - Voltar")

    opcao = input("\nEscolha uma opcao: ").strip()

    if opcao == "1":
        Produto.listar_todos()
    elif opcao == "2":
        Produto.listar_com_alerta()
    elif opcao == "3":
        categoria = input_opcao("Categoria", Produto.CATEGORIAS)
        filtrados = [p for p in produtos if p["categoria"] == categoria]
        if filtrados:
            print(f"\n{cabecalho(f'PRODUTOS - {categoria}')}")
            for p in filtrados:
                print(
                    f"ID: {p['id']} | {p['nome']} | Stock: {p['quantidade_atual']} {p['unidade_medida']}"
                )
        else:
            print(cor("Nenhum produto encontrado nesta categoria.", "amarelo"))
    elif opcao == "4":
        from unidades import Unidade

        Unidade.listar_todas()
        try:
            unidade_id = input_int("ID da unidade: ", min_valor=1)
        except:
            print(cor("Operacao cancelada.", "amarelo"))
            return

        filtrados = Produto.buscar_por_unidade(unidade_id)
        if filtrados:
            unidade = Unidade.buscar_por_id(unidade_id)
            print(
                f"\n{cabecalho(f'PRODUTOS - {unidade["nome"] if unidade else unidade_id}')}"
            )
            for p in filtrados:
                print(
                    f"ID: {p['id']} | {p['nome']} | Stock: {p['quantidade_atual']} {p['unidade_medida']}"
                )
        else:
            print(cor("Nenhum produto encontrado para esta unidade.", "amarelo"))
    elif opcao == "0":
        return
    else:
        print(cor("Opcao invalida.", "vermelho"))


def listar_consumos():
    """
    Interface para listar consumos.
    """
    print("\n" + cabecalho("LISTAR CONSUMOS"))

    print("Opcoes de filtro:")
    print("  1 - Todos os consumos")
    print("  2 - Consumos de uma unidade")
    print("  3 - Consumos por periodo")
    print("  0 - Voltar")

    opcao = input("\nEscolha uma opcao: ").strip()

    if opcao == "1":
        Consumo.listar_todos()
    elif opcao == "2":
        from unidades import Unidade

        Unidade.listar_todas()
        try:
            unidade_id = input_int("ID da unidade: ", min_valor=1)
        except:
            print(cor("Operacao cancelada.", "amarelo"))
            return

        if not Unidade.buscar_por_id(unidade_id):
            print(cor("Unidade nao encontrada.", "vermelho"))
            return

        Consumo.listar_por_unidade(unidade_id)
    elif opcao == "3":
        data_inicio = input_data("Data inicio (YYYY-MM-DD): ")
        data_fim = input_data("Data fim (YYYY-MM-DD): ")
        Consumo.listar_por_periodo(data_inicio, data_fim)
    elif opcao == "0":
        return
    else:
        print(cor("Opcao invalida.", "vermelho"))


def editar_produto():
    """
    Interface para editar um produto existente.
    """
    print("\n" + cabecalho("EDITAR PRODUTO"))

    Produto.listar_todos()

    if not produtos:
        return

    try:
        produto_id = input_int("ID do produto para editar: ", min_valor=1)
    except:
        print(cor("Operacao cancelada.", "amarelo"))
        return

    produto_dict = Produto.buscar_por_id(produto_id)
    if not produto_dict:
        print(cor("Produto nao encontrado.", "vermelho"))
        return

    produto = Produto.from_dict(produto_dict)

    print(f"\nEditando: {cor(produto.nome, 'azul', estilo='negrito')}")
    print("(Deixe em branco para manter o valor atual)")

    # Edita campos
    novo_nome = input(f"Nome ({produto.nome}): ").strip()
    if novo_nome:
        produto.nome = novo_nome

    nova_quantidade = input(f"Quantidade atual ({produto.quantidade_atual}): ").strip()
    if nova_quantidade:
        try:
            produto.quantidade_atual = int(nova_quantidade)
        except ValueError:
            print(cor("Valor invalido. Mantendo o atual.", "amarelo"))

    novo_minimo = input(f"Quantidade minima ({produto.quantidade_minima}): ").strip()
    if novo_minimo:
        try:
            produto.quantidade_minima = int(novo_minimo)
        except ValueError:
            print(cor("Valor invalido. Mantendo o atual.", "amarelo"))

    novo_preco = input(f"Preco unitario ({produto.preco_unitario}): ").strip()
    if novo_preco:
        try:
            produto.preco_unitario = float(novo_preco.replace(",", "."))
        except ValueError:
            print(cor("Valor invalido. Mantendo o atual.", "amarelo"))

    novo_fornecedor = input(f"Fornecedor ({produto.fornecedor}): ").strip()
    if novo_fornecedor:
        produto.fornecedor = novo_fornecedor

    novas_obs = input(f"Observacoes ({produto.observacoes}): ").strip()
    if novas_obs:
        produto.observacoes = novas_obs

    # Confirma
    print("\nDados atualizados:")
    produto.exibir()

    if input_sim_nao("Confirmar alteracoes? (S/N): "):
        produto.salvar()
    else:
        print(cor("Edicao cancelada.", "amarelo"))


def remover_produto():
    """
    Interface para remover um produto.
    """
    print("\n" + cabecalho("REMOVER PRODUTO"))

    Produto.listar_todos()

    if not produtos:
        return

    try:
        produto_id = input_int("ID do produto para remover: ", min_valor=1)
    except:
        print(cor("Operacao cancelada.", "amarelo"))
        return

    produto_dict = Produto.buscar_por_id(produto_id)
    if not produto_dict:
        print(cor("Produto nao encontrado.", "vermelho"))
        return

    produto = Produto.from_dict(produto_dict)
    produto.exibir()

    print(
        cor(
            "ATENCAO: Esta operacao nao pode ser desfeita!",
            "vermelho",
            estilo="negrito",
        )
    )

    if input_sim_nao("Tem certeza que deseja remover este produto? (S/N): "):
        if input_sim_nao("Confirmar novamente? (S/N): "):
            Produto.remover(produto_id)


# ------------------------------------------------------------
# 4. MENU DE ESTOQUE
# ------------------------------------------------------------


def menu_estoque():
    """
    Menu principal do modulo de estoque.
    """
    while True:
        print("\n" + cabecalho("GESTAO DE ESTOQUE"))
        print("  1 - Criar produto")
        print("  2 - Listar produtos")
        print("  3 - Editar produto")
        print("  4 - Registrar consumo")
        print("  5 - Listar consumos")
        print("  6 - Remover produto")
        print("  0 - Voltar")
        print(linha_separadora())

        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            criar_produto()
        elif opcao == "2":
            listar_produtos()
        elif opcao == "3":
            editar_produto()
        elif opcao == "4":
            registrar_consumo()
        elif opcao == "5":
            listar_consumos()
        elif opcao == "6":
            remover_produto()
        elif opcao == "0":
            print(cor("Voltando...", "amarelo"))
            break
        else:
            print(cor("Opcao invalida. Tente novamente.", "vermelho"))


# ------------------------------------------------------------
# 5. DADOS DE EXEMPLO
# ------------------------------------------------------------


def carregar_produtos_exemplo():
    """
    Carrega produtos de exemplo no sistema.
    """
    produtos_exemplo = [
        # Produtos de Limpeza
        {
            "nome": "Lixivia",
            "categoria": "Limpeza",
            "unidade_medida": "Litros",
            "quantidade_atual": 10,
            "quantidade_minima": 3,
            "unidade_id": None,
            "tipo_unidade_destino": "Ambos",
            "preco_unitario": 2.50,
        },
        {
            "nome": "Detergente Multiusos",
            "categoria": "Limpeza",
            "unidade_medida": "Litros",
            "quantidade_atual": 8,
            "quantidade_minima": 3,
            "unidade_id": None,
            "tipo_unidade_destino": "Ambos",
            "preco_unitario": 3.00,
        },
        {
            "nome": "Mistolin Bang",
            "categoria": "Limpeza",
            "unidade_medida": "Litros",
            "quantidade_atual": 5,
            "quantidade_minima": 2,
            "unidade_id": None,
            "tipo_unidade_destino": "Ambos",
            "preco_unitario": 4.50,
        },
        {
            "nome": "Saco de Lixo Grande",
            "categoria": "Limpeza",
            "unidade_medida": "Pacotes",
            "quantidade_atual": 15,
            "quantidade_minima": 5,
            "unidade_id": None,
            "tipo_unidade_destino": "Ambos",
            "preco_unitario": 1.50,
        },
        {
            "nome": "Saco de Lixo Pequeno",
            "categoria": "Limpeza",
            "unidade_medida": "Pacotes",
            "quantidade_atual": 20,
            "quantidade_minima": 5,
            "unidade_id": None,
            "tipo_unidade_destino": "Ambos",
            "preco_unitario": 1.00,
        },
        {
            "nome": "Papel Higienico",
            "categoria": "Limpeza",
            "unidade_medida": "Rolos",
            "quantidade_atual": 30,
            "quantidade_minima": 10,
            "unidade_id": None,
            "tipo_unidade_destino": "Airbnb",
            "preco_unitario": 0.50,
        },
        {
            "nome": "Ambientador",
            "categoria": "Limpeza",
            "unidade_medida": "Unidades",
            "quantidade_atual": 12,
            "quantidade_minima": 5,
            "unidade_id": None,
            "tipo_unidade_destino": "Airbnb",
            "preco_unitario": 2.00,
        },
        # Produtos de Roupa
        {
            "nome": "Lencois de Solteiro",
            "categoria": "Roupa",
            "unidade_medida": "Unidades",
            "quantidade_atual": 20,
            "quantidade_minima": 6,
            "unidade_id": None,
            "tipo_unidade_destino": "Ambos",
            "preco_unitario": 15.00,
        },
        {
            "nome": "Lencois de Casal",
            "categoria": "Roupa",
            "unidade_medida": "Unidades",
            "quantidade_atual": 15,
            "quantidade_minima": 5,
            "unidade_id": None,
            "tipo_unidade_destino": "Ambos",
            "preco_unitario": 20.00,
        },
        {
            "nome": "Toalhas de Banho",
            "categoria": "Roupa",
            "unidade_medida": "Unidades",
            "quantidade_atual": 25,
            "quantidade_minima": 8,
            "unidade_id": None,
            "tipo_unidade_destino": "Airbnb",
            "preco_unitario": 12.00,
        },
        # Snacks
        {
            "nome": "Cha",
            "categoria": "Snacks",
            "unidade_medida": "Unidades",
            "quantidade_atual": 50,
            "quantidade_minima": 15,
            "unidade_id": None,
            "tipo_unidade_destino": "Airbnb",
            "preco_unitario": 0.25,
        },
        {
            "nome": "Balas",
            "categoria": "Snacks",
            "unidade_medida": "Unidades",
            "quantidade_atual": 100,
            "quantidade_minima": 30,
            "unidade_id": None,
            "tipo_unidade_destino": "Airbnb",
            "preco_unitario": 0.10,
        },
        {
            "nome": "Bolachas",
            "categoria": "Snacks",
            "unidade_medida": "Pacotes",
            "quantidade_atual": 40,
            "quantidade_minima": 15,
            "unidade_id": None,
            "tipo_unidade_destino": "Airbnb",
            "preco_unitario": 1.50,
        },
    ]

    for dados in produtos_exemplo:
        produto = Produto(
            nome=dados["nome"],
            categoria=dados["categoria"],
            unidade_medida=dados["unidade_medida"],
            quantidade_atual=dados["quantidade_atual"],
            quantidade_minima=dados["quantidade_minima"],
            unidade_id=dados.get("unidade_id"),
            tipo_unidade_destino=dados["tipo_unidade_destino"],
            preco_unitario=dados["preco_unitario"],
        )
        produto.salvar()

    print(cor(f"{len(produtos_exemplo)} produtos de exemplo carregados!", "verde"))


# ------------------------------------------------------------
# 6. BLOCO DE TESTE
# ------------------------------------------------------------

if __name__ == "__main__":

    print("\n" + cabecalho("TESTE DO MODULO DE ESTOQUE"))

    # Carrega dados de exemplo
    carregar_produtos_exemplo()

    # Mostra o estado dos dados
    mostrar_estado_dados()

    # Lista todos os produtos
    Produto.listar_todos()

    # Lista produtos com alerta
    print("\n" + cabecalho("TESTE DE ALERTAS"))
    Produto.listar_com_alerta()

    # Testa consumo
    print("\n" + cabecalho("TESTE DE CONSUMO"))

    # Busca um produto
    produto_dict = Produto.buscar_por_id(1)
    if produto_dict:
        produto = Produto.from_dict(produto_dict)
        print(f"Consumindo 1 unidade de {produto.nome}...")
        produto.consumir(1, 1, "Staff Teste", "Teste de consumo")

    # Lista consumos
    Consumo.listar_todos()

    print("\n" + cabecalho("TESTE CONCLUIDO"))
