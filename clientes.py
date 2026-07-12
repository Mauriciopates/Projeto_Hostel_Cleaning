# ============================================================
# clientes.py - GESTAO DE CLIENTES
# ============================================================
# Modulo responsavel por gerenciar os clientes do hostel.
# Suporta dois tipos de clientes:
#   - Morador: Clientes com contrato mensal
#   - Airbnb: Hospedes de curta duracao
#
# Dependencias:
#   - dados.py: Para acesso a base de dados em memoria
#   - utils.py: Para funcoes auxiliares (cores, validacoes, etc.)
# ============================================================

from dados import clientes, proximo_id_cliente, mostrar_estado_dados
from utils import (
    cor,
    cabecalho,
    input_float,
    linha_separadora,
    input_obrigatorio,
    input_email,
    input_telefone,
    input_nif,
    input_data,
    input_documento,
    input_sim_nao,
    input_opcao,
    formatar_data,
    validar_data,
    obter_data_atual,
)

# ------------------------------------------------------------
# 1. CLASSE CLIENTE
# ------------------------------------------------------------


class Cliente:
    """
    Classe que representa um cliente do hostel.

    Atributos Comuns:
        id (int): Identificador unico do cliente
        nome (str): Nome completo
        email (str): Email de contacto
        telefone (str): Numero de telefone
        data_nascimento (str): Data de nascimento (YYYY-MM-DD)
        endereco (str): Morada completa
        nacionalidade (str): Nacionalidade do cliente
        tipo (str): "Morador" ou "Airbnb"
        observacoes (str): Observacoes gerais
        data_cadastro (str): Data de criacao do registo
        historico (list): Lista de estadias anteriores

    Atributos Especificos - Morador:
        nif (str): Numero de identificacao fiscal
        caução (float): Valor da caução
        contrato_tipo (str): "Fisico" ou "Digital"
        comprovativo_rendimentos (bool): Se possui comprovativo

    Atributos Especificos - Airbnb:
        documento (str): Numero do passaporte ou CC
        validade_documento (str): Data de validade do documento
        contacto_emergencia (str): Contacto de emergencia
    """

    def __init__(
        self,
        nome,
        email,
        telefone,
        data_nascimento,
        endereco,
        nacionalidade,
        tipo,
        observacoes="",
    ):
        """
        Inicializa um novo cliente.

        Parametros:
            nome (str): Nome completo
            email (str): Email de contacto
            telefone (str): Numero de telefone
            data_nascimento (str): Data de nascimento (YYYY-MM-DD)
            endereco (str): Morada completa
            nacionalidade (str): Nacionalidade
            tipo (str): "Morador" ou "Airbnb"
            observacoes (str): Observacoes (opcional)
        """
        self.id = proximo_id_cliente()
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.nacionalidade = nacionalidade
        self.tipo = tipo
        self.observacoes = observacoes
        self.data_cadastro = obter_data_atual("%Y-%m-%d %H:%M:%S")
        self.historico = []

        # Atributos especificos - Morador
        self.nif = None
        self.caução = None
        self.contrato_tipo = None
        self.comprovativo_rendimentos = False

        # Atributos especificos - Airbnb
        self.documento = None
        self.validade_documento = None
        self.contacto_emergencia = None

    def definir_dados_morador(
        self,
        nif=None,
        caução=150.00,
        contrato_tipo="Fisico",
        comprovativo_rendimentos=False,
    ):
        """
        Define os dados especificos para um cliente do tipo Morador.

        Parametros:
            nif (str): NIF do cliente
            caução (float): Valor da caução
            contrato_tipo (str): "Fisico" ou "Digital"
            comprovativo_rendimentos (bool): Possui comprovativo?
        """
        if self.tipo != "Morador":
            print(cor("Este cliente nao e do tipo Morador.", "vermelho"))
            return False

        self.nif = nif
        self.caução = caução
        self.contrato_tipo = contrato_tipo
        self.comprovativo_rendimentos = comprovativo_rendimentos
        return True

    def definir_dados_airbnb(self, documento, validade_documento, contacto_emergencia):
        """
        Define os dados especificos para um cliente do tipo Airbnb.

        Parametros:
            documento (str): Numero do passaporte ou CC
            validade_documento (str): Data de validade (YYYY-MM-DD)
            contacto_emergencia (str): Contacto de emergencia
        """
        if self.tipo != "Airbnb":
            print(cor("Este cliente nao e do tipo Airbnb.", "vermelho"))
            return False

        self.documento = documento
        self.validade_documento = validade_documento
        self.contacto_emergencia = contacto_emergencia
        return True

    def to_dict(self):
        """
        Converte o cliente para um dicionario.

        Retorna:
            dict: Dicionario com todos os atributos do cliente
        """
        dados = {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "data_nascimento": self.data_nascimento,
            "endereco": self.endereco,
            "nacionalidade": self.nacionalidade,
            "tipo": self.tipo,
            "observacoes": self.observacoes,
            "data_cadastro": self.data_cadastro,
            "historico": self.historico,
        }

        # Dados especificos - Morador
        if self.tipo == "Morador":
            dados["nif"] = self.nif
            dados["caução"] = self.caução
            dados["contrato_tipo"] = self.contrato_tipo
            dados["comprovativo_rendimentos"] = self.comprovativo_rendimentos

        # Dados especificos - Airbnb
        elif self.tipo == "Airbnb":
            dados["documento"] = self.documento
            dados["validade_documento"] = self.validade_documento
            dados["contacto_emergencia"] = self.contacto_emergencia

        return dados

    @staticmethod
    def from_dict(dados):
        """
        Cria uma instancia de Cliente a partir de um dicionario.

        Parametros:
            dados (dict): Dicionario com os dados do cliente

        Retorna:
            Cliente: Instancia do cliente
        """
        cliente = Cliente(
            nome=dados["nome"],
            email=dados["email"],
            telefone=dados["telefone"],
            data_nascimento=dados["data_nascimento"],
            endereco=dados["endereco"],
            nacionalidade=dados["nacionalidade"],
            tipo=dados["tipo"],
            observacoes=dados.get("observacoes", ""),
        )

        # Restaura o ID e data de cadastro
        cliente.id = dados["id"]
        cliente.data_cadastro = dados["data_cadastro"]
        cliente.historico = dados.get("historico", [])

        # Dados especificos - Morador
        if dados["tipo"] == "Morador":
            cliente.nif = dados.get("nif")
            cliente.caução = dados.get("caução", 150.00)
            cliente.contrato_tipo = dados.get("contrato_tipo", "Fisico")
            cliente.comprovativo_rendimentos = dados.get(
                "comprovativo_rendimentos", False
            )

        # Dados especificos - Airbnb
        elif dados["tipo"] == "Airbnb":
            cliente.documento = dados.get("documento")
            cliente.validade_documento = dados.get("validade_documento")
            cliente.contacto_emergencia = dados.get("contacto_emergencia")

        return cliente

    def exibir(self):
        """
        Exibe os detalhes do cliente formatados no terminal.
        """
        print("\n" + linha_separadora(50))
        print(cor(f"ID: {self.id}", "azul", estilo="negrito"))
        print(f"Nome: {self.nome}")
        print(f"Tipo: {cor(self.tipo, 'verde' if self.tipo == 'Morador' else 'ciano')}")
        print(f"Email: {self.email}")
        print(f"Telefone: {self.telefone}")
        print(f"Data Nascimento: {formatar_data(self.data_nascimento)}")
        print(f"Endereco: {self.endereco}")
        print(f"Nacionalidade: {self.nacionalidade}")
        print(f"Data Cadastro: {self.data_cadastro}")

        # Dados especificos - Morador
        if self.tipo == "Morador":
            print("\n[Dados do Morador]")
            print(f"NIF: {self.nif if self.nif else 'Nao informado'}")
            print(f"Caução: {self.caução:.2f} €")
            print(f"Contrato: {self.contrato_tipo}")
            print(
                f"Comprovativo Rendimentos: {'Sim' if self.comprovativo_rendimentos else 'Nao'}"
            )

        # Dados especificos - Airbnb
        elif self.tipo == "Airbnb":
            print("\n[Dados do Hóspede Airbnb]")
            print(f"Documento: {self.documento}")
            print(
                f"Validade: {formatar_data(self.validade_documento) if self.validade_documento else 'Nao informado'}"
            )
            print(f"Contacto Emergencia: {self.contacto_emergencia}")

        if self.observacoes:
            print(f"\nObservacoes: {self.observacoes}")

        if self.historico:
            print(f"\nHistorico de estadias: {len(self.historico)} registos")

        print(linha_separadora(50))

    def adicionar_historico(self, entrada):
        """
        Adiciona uma entrada ao historico do cliente.

        Parametros:
            entrada (dict): Dicionario com dados da estadia
        """
        self.historico.append(entrada)

    def salvar(self):
        """
        Salva o cliente na base de dados em memoria.

        Retorna:
            bool: True se salvo com sucesso, False caso contrario
        """
        # Verifica se o cliente ja existe (atualizacao)
        for i, cliente in enumerate(clientes):
            if cliente["id"] == self.id:
                clientes[i] = self.to_dict()
                print(cor(f"Cliente '{self.nome}' atualizado com sucesso!", "verde"))
                return True

        # Se nao existe, adiciona novo
        clientes.append(self.to_dict())
        print(
            cor(f"Cliente '{self.nome}' criado com sucesso! (ID: {self.id})", "verde")
        )
        return True

    @staticmethod
    def listar_todos():
        """
        Lista todos os clientes cadastrados.
        """
        if not clientes:
            print(cor("Nenhum cliente cadastrado.", "amarelo"))
            return

        print("\n" + cabecalho("LISTA DE CLIENTES"))
        print(f"Total: {len(clientes)} clientes\n")

        for cliente in clientes:
            # Cor por tipo
            cor_tipo = "verde" if cliente["tipo"] == "Morador" else "ciano"

            print(f"ID: {cliente['id']} | {cliente['nome']}")
            print(f"  Tipo: {cor(cliente['tipo'], cor_tipo)}")
            print(f"  Email: {cliente['email']}")
            print(f"  Telefone: {cliente['telefone']}")

            # Mostra documento se for Airbnb
            if cliente["tipo"] == "Airbnb" and cliente.get("documento"):
                print(f"  Documento: {cliente['documento']}")

            print(linha_separadora(40))

    @staticmethod
    def listar_por_tipo(tipo):
        """
        Lista clientes filtrados por tipo.

        Parametros:
            tipo (str): "Morador" ou "Airbnb"
        """
        if tipo not in ["Morador", "Airbnb"]:
            print(cor("Tipo invalido. Use 'Morador' ou 'Airbnb'.", "vermelho"))
            return

        filtrados = [c for c in clientes if c["tipo"] == tipo]

        if not filtrados:
            print(cor(f"Nenhum cliente do tipo '{tipo}' encontrado.", "amarelo"))
            return

        print(f"\n{cabecalho(f'CLIENTES - {tipo.upper()}')}")
        print(f"Total: {len(filtrados)} clientes\n")

        for cliente in filtrados:
            print(f"ID: {cliente['id']} | {cliente['nome']}")
            print(f"  Email: {cliente['email']}")
            print(f"  Telefone: {cliente['telefone']}")
            print(linha_separadora(40))

    @staticmethod
    def buscar_por_id(id_cliente):
        """
        Busca um cliente pelo ID.

        Parametros:
            id_cliente (int): ID do cliente

        Retorna:
            dict: Dados do cliente, ou None se nao encontrado
        """
        for cliente in clientes:
            if cliente["id"] == id_cliente:
                return cliente
        return None

    @staticmethod
    def buscar_por_nome(nome):
        """
        Busca clientes pelo nome (busca parcial).

        Parametros:
            nome (str): Nome ou parte do nome

        Retorna:
            list: Lista de clientes que correspondem a busca
        """
        nome_lower = nome.lower()
        return [c for c in clientes if nome_lower in c["nome"].lower()]

    @staticmethod
    def buscar_por_documento(documento):
        """
        Busca um cliente pelo documento (Airbnb).

        Parametros:
            documento (str): Numero do documento

        Retorna:
            dict: Dados do cliente, ou None se nao encontrado
        """
        documento_limpo = documento.strip().upper()
        for cliente in clientes:
            if (
                cliente["tipo"] == "Airbnb"
                and cliente.get("documento") == documento_limpo
            ):
                return cliente
        return None

    @staticmethod
    def remover(id_cliente):
        """
        Remove um cliente pelo ID.

        Parametros:
            id_cliente (int): ID do cliente

        Retorna:
            bool: True se removido com sucesso, False caso contrario
        """
        for i, cliente in enumerate(clientes):
            if cliente["id"] == id_cliente:
                nome = cliente["nome"]
                del clientes[i]
                print(cor(f"Cliente '{nome}' removido com sucesso!", "verde"))
                return True

        print(cor(f"Cliente com ID {id_cliente} nao encontrado.", "vermelho"))
        return False


# ------------------------------------------------------------
# 2. FUNCOES DE INTERFACE (CRUD)
# ------------------------------------------------------------


def criar_cliente():
    """
    Interface para criar um novo cliente.
    Solicita os dados ao utilizador e cria o cliente.
    """
    print("\n" + cabecalho("CRIAR NOVO CLIENTE"))

    # Tipo de cliente
    tipo = input_opcao("Tipo de cliente", ["Morador", "Airbnb"])

    # Dados comuns
    nome = input_obrigatorio("Nome completo: ")
    email = input_email()
    telefone = input_telefone()
    data_nascimento = input_data("Data de nascimento (YYYY-MM-DD): ")
    endereco = input_obrigatorio("Endereco completo: ")
    nacionalidade = input_obrigatorio("Nacionalidade: ")
    observacoes = input("Observacoes (opcional): ").strip()

    # Cria o cliente
    cliente = Cliente(
        nome=nome,
        email=email,
        telefone=telefone,
        data_nascimento=data_nascimento,
        endereco=endereco,
        nacionalidade=nacionalidade,
        tipo=tipo,
        observacoes=observacoes,
    )

    # Dados especificos - Morador
    if tipo == "Morador":
        print("\n[Dados do Morador]")
        nif = input_nif(mensagem="NIF (opcional): ", obrigatorio=False)
        caução = input_float(
            "Valor da caução (default 150.00): ", obrigatorio=False, min_valor=0
        )
        if caução is None:
            caução = 150.00

        contrato_tipo = input_opcao("Tipo de contrato", ["Fisico", "Digital"])
        comprovativo = input_sim_nao("Possui comprovativo de rendimentos? (S/N): ")

        cliente.definir_dados_morador(
            nif=nif if nif else None,
            caução=caução,
            contrato_tipo=contrato_tipo,
            comprovativo_rendimentos=comprovativo,
        )

    # Dados especificos - Airbnb
    elif tipo == "Airbnb":
        print("\n[Dados do Hóspede Airbnb]")
        documento = input_documento(mensagem="Documento (Passaporte ou CC): ")
        validade_documento = input_data("Validade do documento (YYYY-MM-DD): ")
        contacto_emergencia = input_telefone("Contacto de emergencia: ")

        cliente.definir_dados_airbnb(
            documento=documento,
            validade_documento=validade_documento,
            contacto_emergencia=contacto_emergencia,
        )

    # Salva
    cliente.salvar()

    # Exibe o cliente criado
    cliente.exibir()

    return cliente


def editar_cliente():
    """
    Interface para editar um cliente existente.
    """
    print("\n" + cabecalho("EDITAR CLIENTE"))

    # Lista os clientes para o utilizador escolher
    Cliente.listar_todos()

    if not clientes:
        return

    # Seleciona o cliente
    try:
        id_cliente = int(input("\nID do cliente para editar: ").strip())
    except ValueError:
        print(cor("Operacao cancelada.", "amarelo"))
        return

    # Busca o cliente
    dados_cliente = Cliente.buscar_por_id(id_cliente)

    if not dados_cliente:
        print(cor(f"Cliente com ID {id_cliente} nao encontrado.", "vermelho"))
        return

    # Cria objeto para edicao
    cliente = Cliente.from_dict(dados_cliente)

    print(f"\nEditando: {cor(cliente.nome, 'azul', estilo='negrito')}")
    print("(Deixe em branco para manter o valor atual)")

    # Edita os campos comuns
    novo_nome = input(f"Nome ({cliente.nome}): ").strip()
    if novo_nome:
        cliente.nome = novo_nome

    novo_email = input(f"Email ({cliente.email}): ").strip()
    if novo_email:
        from utils import validar_email

        if validar_email(novo_email):
            cliente.email = novo_email
        else:
            print(cor("Email invalido. Mantendo o atual.", "amarelo"))

    novo_telefone = input(f"Telefone ({cliente.telefone}): ").strip()
    if novo_telefone:
        from utils import validar_telefone

        if validar_telefone(novo_telefone):
            cliente.telefone = novo_telefone
        else:
            print(cor("Telefone invalido. Mantendo o atual.", "amarelo"))

    novo_endereco = input(f"Endereco ({cliente.endereco}): ").strip()
    if novo_endereco:
        cliente.endereco = novo_endereco

    novas_obs = input(f"Observacoes ({cliente.observacoes}): ").strip()
    if novas_obs:
        cliente.observacoes = novas_obs

    # Confirma a edicao
    print("\nDados atualizados:")
    cliente.exibir()

    if input_sim_nao("Confirmar alteracoes? (S/N): "):
        cliente.salvar()
    else:
        print(cor("Edicao cancelada.", "amarelo"))


def listar_clientes():
    """
    Interface para listar clientes com filtros.
    """
    print("\n" + cabecalho("LISTAR CLIENTES"))

    print("Opcoes de filtro:")
    print("  1 - Todos os clientes")
    print("  2 - Apenas Moradores")
    print("  3 - Apenas Airbnb")
    print("  4 - Buscar por nome")
    print("  0 - Voltar")

    opcao = input("\nEscolha uma opcao: ").strip()

    if opcao == "1":
        Cliente.listar_todos()
    elif opcao == "2":
        Cliente.listar_por_tipo("Morador")
    elif opcao == "3":
        Cliente.listar_por_tipo("Airbnb")
    elif opcao == "4":
        nome = input_obrigatorio("Digite o nome (ou parte): ")
        resultados = Cliente.buscar_por_nome(nome)
        if resultados:
            print(f"\n{cabecalho('RESULTADOS DA BUSCA')}")
            for cliente in resultados:
                print(f"ID: {cliente['id']} | {cliente['nome']} | {cliente['tipo']}")
        else:
            print(cor("Nenhum cliente encontrado.", "amarelo"))
    elif opcao == "0":
        return
    else:
        print(cor("Opcao invalida.", "vermelho"))


def remover_cliente():
    """
    Interface para remover um cliente.
    """
    print("\n" + cabecalho("REMOVER CLIENTE"))

    Cliente.listar_todos()

    if not clientes:
        return

    try:
        id_cliente = int(input("ID do cliente para remover: ").strip())
    except ValueError:
        print(cor("Operacao cancelada.", "amarelo"))
        return

    dados_cliente = Cliente.buscar_por_id(id_cliente)

    if not dados_cliente:
        print(cor(f"Cliente com ID {id_cliente} nao encontrado.", "vermelho"))
        return

    # Exibe o cliente para confirmacao
    cliente = Cliente.from_dict(dados_cliente)
    cliente.exibir()

    print(
        cor(
            "ATENCAO: Esta operacao nao pode ser desfeita!",
            "vermelho",
            estilo="negrito",
        )
    )

    if input_sim_nao("Tem certeza que deseja remover este cliente? (S/N): "):
        if input_sim_nao("Confirmar novamente? (S/N): "):
            Cliente.remover(id_cliente)


def ver_detalhes_cliente():
    """
    Interface para ver detalhes completos de um cliente.
    """
    print("\n" + cabecalho("DETALHES DO CLIENTE"))

    Cliente.listar_todos()

    if not clientes:
        return

    try:
        id_cliente = int(input("ID do cliente: ").strip())
    except ValueError:
        print(cor("Operacao cancelada.", "amarelo"))
        return

    dados_cliente = Cliente.buscar_por_id(id_cliente)

    if not dados_cliente:
        print(cor(f"Cliente com ID {id_cliente} nao encontrado.", "vermelho"))
        return

    cliente = Cliente.from_dict(dados_cliente)
    cliente.exibir()


# ------------------------------------------------------------
# 3. MENU DE CLIENTES
# ------------------------------------------------------------


def menu_clientes():
    """
    Menu principal do modulo de clientes.
    """
    while True:
        print("\n" + cabecalho("GESTAO DE CLIENTES"))
        print("  1 - Criar cliente")
        print("  2 - Listar clientes")
        print("  3 - Editar cliente")
        print("  4 - Ver detalhes do cliente")
        print("  5 - Remover cliente")
        print("  0 - Voltar")
        print(linha_separadora())

        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            criar_cliente()
        elif opcao == "2":
            listar_clientes()
        elif opcao == "3":
            editar_cliente()
        elif opcao == "4":
            ver_detalhes_cliente()
        elif opcao == "5":
            remover_cliente()
        elif opcao == "0":
            print(cor("Voltando...", "amarelo"))
            break
        else:
            print(cor("Opcao invalida. Tente novamente.", "vermelho"))


# ------------------------------------------------------------
# 4. DADOS DE EXEMPLO
# ------------------------------------------------------------


def carregar_clientes_exemplo():
    """
    Carrega clientes de exemplo no sistema.
    Util para testes e demonstracao.
    """
    # Morador exemplo
    morador = Cliente(
        nome="Joao Silva",
        email="joao.silva@email.com",
        telefone="912345678",
        data_nascimento="1990-05-15",
        endereco="Rua das Flores, 123, Porto",
        nacionalidade="Portuguesa",
        tipo="Morador",
        observacoes="Cliente desde 2024",
    )
    morador.definir_dados_morador(
        nif="123456789",
        caução=150.00,
        contrato_tipo="Fisico",
        comprovativo_rendimentos=True,
    )
    morador.salvar()

    # Airbnb exemplo
    airbnb = Cliente(
        nome="Maria Santos",
        email="maria.santos@email.com",
        telefone="967654321",
        data_nascimento="1985-10-20",
        endereco="Avenida da Liberdade, 45, Lisboa",
        nacionalidade="Brasileira",
        tipo="Airbnb",
        observacoes="Hospede frequente",
    )
    airbnb.definir_dados_airbnb(
        documento="AB123456",
        validade_documento="2030-05-20",
        contacto_emergencia="969999999",
    )
    airbnb.salvar()

    # Mais um Airbnb
    airbnb2 = Cliente(
        nome="John Smith",
        email="john.smith@email.com",
        telefone="936654321",
        data_nascimento="1992-03-10",
        endereco="Oxford Street, 100, London",
        nacionalidade="Britanica",
        tipo="Airbnb",
        observacoes="Cliente internacional",
    )
    airbnb2.definir_dados_airbnb(
        documento="UK987654",
        validade_documento="2028-12-31",
        contacto_emergencia="937777777",
    )
    airbnb2.salvar()

    print(cor("Clientes de exemplo carregados!", "verde"))


# ------------------------------------------------------------
# 5. BLOCO DE TESTE
# ------------------------------------------------------------

if __name__ == "__main__":

    print("\n" + cabecalho("TESTE DO MODULO DE CLIENTES"))

    # Carrega dados de exemplo
    carregar_clientes_exemplo()

    # Mostra o estado dos dados
    mostrar_estado_dados()

    # Lista os clientes
    Cliente.listar_todos()

    # Testa a busca por ID
    print("\n" + cabecalho("TESTE DE BUSCA POR ID"))
    cliente = Cliente.buscar_por_id(1)
    if cliente:
        print(f"Cliente encontrado: {cliente['nome']}")
        print(f"Tipo: {cliente['tipo']}")

    # Testa a busca por documento (Airbnb)
    print("\n" + cabecalho("TESTE DE BUSCA POR DOCUMENTO"))
    cliente = Cliente.buscar_por_documento("AB123456")
    if cliente:
        print(f"Cliente encontrado: {cliente['nome']}")
        print(f"Documento: {cliente['documento']}")

    # Exibe detalhes de um cliente
    print("\n" + cabecalho("TESTE DE EXIBICAO DE DETALHES"))
    dados_cliente = Cliente.buscar_por_id(1)
    if dados_cliente:
        cliente_obj = Cliente.from_dict(dados_cliente)
        cliente_obj.exibir()

    print("\n" + cabecalho("TESTE CONCLUIDO"))
