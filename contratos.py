# ============================================================
# contratos.py - GESTAO DE CONTRATOS E RESERVAS
# ============================================================
# Modulo responsavel por gerenciar contratos mensais e
# reservas Airbnb do hostel.
#
# Dependencias:
#   - dados.py: Para acesso a base de dados em memoria
#   - utils.py: Para funcoes auxiliares
#   - unidades.py: Para aceder a dados das unidades
#   - clientes.py: Para aceder a dados dos clientes
# ============================================================

from dados import (
    contratos,
    unidades,
    clientes,
    produtos,
    proximo_id_contrato,
    mostrar_estado_dados
)
from utils import (
    cor,
    cabecalho,
    linha_separadora,
    input_obrigatorio,
    input_data,
    input_float,
    input_int,
    input_sim_nao,
    input_opcao,
    formatar_preco,
    formatar_data,
    obter_data_atual
)
from unidades import Unidade
from clientes import Cliente


# ------------------------------------------------------------
# 1. CLASSE CONTRATO (Mensal)
# ------------------------------------------------------------

class Contrato:
    """
    Classe que representa um contrato mensal com um morador.
    
    Atributos:
        id (int): Identificador unico do contrato
        unidade_id (int): ID da unidade associada
        cliente_id (int): ID do cliente (morador)
        data_inicio (str): Data de inicio do contrato
        data_fim (str): Data de fim do contrato (prevista)
        duracao_meses (int): Duracao em meses
        valor_renda (float): Valor da renda mensal
        dia_vencimento (int): Dia do mes para pagamento (default: 5)
        status (str): "Ativo", "Finalizado", "Cancelado"
        caução (float): Valor da caução
        renovacao_automatica (bool): Se renova automaticamente
        tipo_contrato (str): "Fisico" ou "Digital"
        data_proximo_vencimento (str): Proxima data de vencimento
        observacoes (str): Observacoes gerais
    """
    
    def __init__(self, unidade_id, cliente_id, data_inicio, duracao_meses,
                 valor_renda, dia_vencimento=5, caução=150.00,
                 renovacao_automatica=True, tipo_contrato="Fisico",
                 observacoes=""):
        """
        Inicializa um novo contrato mensal.
        
        Parametros:
            unidade_id (int): ID da unidade
            cliente_id (int): ID do cliente
            data_inicio (str): Data de inicio (YYYY-MM-DD)
            duracao_meses (int): Duracao em meses
            valor_renda (float): Valor da renda mensal
            dia_vencimento (int): Dia do mes para pagamento
            caução (float): Valor da caução
            renovacao_automatica (bool): Renovacao automatica
            tipo_contrato (str): "Fisico" ou "Digital"
            observacoes (str): Observacoes
        """
        self.id = proximo_id_contrato()
        self.unidade_id = unidade_id
        self.cliente_id = cliente_id
        self.data_inicio = data_inicio
        self.duracao_meses = duracao_meses
        self.valor_renda = valor_renda
        self.dia_vencimento = dia_vencimento
        self.caução = caução
        self.renovacao_automatica = renovacao_automatica
        self.tipo_contrato = tipo_contrato
        self.observacoes = observacoes
        self.status = "Ativo"
        self.data_criacao = obter_data_atual("%Y-%m-%d %H:%M:%S")
        
        # Calcula data de fim
        self.data_fim = self._calcular_data_fim(data_inicio, duracao_meses)
        
        # Calcula proximo vencimento
        self.data_proximo_vencimento = self._calcular_proximo_vencimento()
    
    def _calcular_data_fim(self, data_inicio, meses):
        """
        Calcula a data de fim do contrato.
        
        Parametros:
            data_inicio (str): Data de inicio
            meses (int): Numero de meses
        
        Retorna:
            str: Data de fim no formato YYYY-MM-DD
        """
        from datetime import datetime, timedelta
        data = datetime.strptime(data_inicio, "%Y-%m-%d")
        # Aproximacao: 1 mes = 30 dias
        data_fim = data + timedelta(days=meses * 30)
        return data_fim.strftime("%Y-%m-%d")
    
    def _calcular_proximo_vencimento(self):
        """
        Calcula a proxima data de vencimento da renda.
        
        Retorna:
            str: Proxima data de vencimento no formato YYYY-MM-DD
        """
        from datetime import datetime, timedelta
        
        hoje = datetime.now()
        dia_venc = self.dia_vencimento
        
        # Se o dia de vencimento ja passou neste mes, vai para o proximo mes
        if hoje.day >= dia_venc:
            # Proximo mes
            if hoje.month == 12:
                proximo = datetime(hoje.year + 1, 1, dia_venc)
            else:
                proximo = datetime(hoje.year, hoje.month + 1, dia_venc)
        else:
            # Ainda este mes
            proximo = datetime(hoje.year, hoje.month, dia_venc)
        
        return proximo.strftime("%Y-%m-%d")
    
    def to_dict(self):
        """
        Converte o contrato para um dicionario.
        
        Retorna:
            dict: Dicionario com todos os atributos do contrato
        """
        return {
            "id": self.id,
            "unidade_id": self.unidade_id,
            "cliente_id": self.cliente_id,
            "data_inicio": self.data_inicio,
            "data_fim": self.data_fim,
            "duracao_meses": self.duracao_meses,
            "valor_renda": self.valor_renda,
            "dia_vencimento": self.dia_vencimento,
            "status": self.status,
            "caução": self.caução,
            "renovacao_automatica": self.renovacao_automatica,
            "tipo_contrato": self.tipo_contrato,
            "data_proximo_vencimento": self.data_proximo_vencimento,
            "data_criacao": self.data_criacao,
            "observacoes": self.observacoes
        }
    
    @staticmethod
    def from_dict(dados):
        """
        Cria uma instancia de Contrato a partir de um dicionario.
        
        Parametros:
            dados (dict): Dicionario com os dados do contrato
        
        Retorna:
            Contrato: Instancia do contrato
        """
        contrato = Contrato(
            unidade_id=dados["unidade_id"],
            cliente_id=dados["cliente_id"],
            data_inicio=dados["data_inicio"],
            duracao_meses=dados["duracao_meses"],
            valor_renda=dados["valor_renda"],
            dia_vencimento=dados["dia_vencimento"],
            caução=dados["caução"],
            renovacao_automatica=dados["renovacao_automatica"],
            tipo_contrato=dados["tipo_contrato"],
            observacoes=dados.get("observacoes", "")
        )
        contrato.id = dados["id"]
        contrato.data_fim = dados["data_fim"]
        contrato.status = dados["status"]
        contrato.data_proximo_vencimento = dados["data_proximo_vencimento"]
        contrato.data_criacao = dados["data_criacao"]
        return contrato
    
    def exibir(self):
        """
        Exibe os detalhes do contrato formatados no terminal.
        """
        # Busca dados da unidade e cliente
        unidade = Unidade.buscar_por_id(self.unidade_id)
        cliente = Cliente.buscar_por_id(self.cliente_id)
        
        nome_unidade = unidade["nome"] if unidade else f"ID {self.unidade_id}"
        nome_cliente = cliente["nome"] if cliente else f"ID {self.cliente_id}"
        
        # Cor para o status
        cores_status = {
            "Ativo": "verde",
            "Finalizado": "azul",
            "Cancelado": "vermelho"
        }
        cor_status = cores_status.get(self.status, "branco")
        
        print("\n" + linha_separadora(50))
        print(cor(f"CONTRATO ID: {self.id}", "azul", estilo="negrito"))
        print(f"Unidade: {nome_unidade}")
        print(f"Cliente: {nome_cliente}")
        print(f"Data Inicio: {formatar_data(self.data_inicio)}")
        print(f"Data Fim: {formatar_data(self.data_fim)}")
        print(f"Duracao: {self.duracao_meses} meses")
        print(f"Valor Renda: {formatar_preco(self.valor_renda)}")
        print(f"Vencimento: Dia {self.dia_vencimento}")
        print(f"Proximo Vencimento: {formatar_data(self.data_proximo_vencimento)}")
        print(f"Caução: {formatar_preco(self.caução)}")
        print(f"Status: {cor(self.status, cor_status, estilo='negrito')}")
        print(f"Renovacao: {'Automatica' if self.renovacao_automatica else 'Manual'}")
        print(f"Tipo Contrato: {self.tipo_contrato}")
        
        # Verifica se esta vencido
        if self.verificar_vencimento():
            print(cor("ATENCAO: Renda em atraso!", "vermelho"))
        
        if self.observacoes:
            print(f"Observacoes: {self.observacoes}")
        print(linha_separadora(50))
    
    def verificar_vencimento(self):
        """
        Verifica se a renda esta vencida.
        
        Retorna:
            bool: True se vencida, False se em dia
        """
        from datetime import datetime
        hoje = datetime.now().strftime("%Y-%m-%d")
        return hoje > self.data_proximo_vencimento
    
    def calcular_juros(self, dias_atraso):
        """
        Calcula os juros por atraso.
        Taxa: 10% ao mes (pro-rata diario)
        
        Parametros:
            dias_atraso (int): Numero de dias de atraso
        
        Retorna:
            float: Valor dos juros
        """
        # 10% ao mes = 10/30 % ao dia
        taxa_diaria = 0.10 / 30
        return self.valor_renda * taxa_diaria * dias_atraso
    
    def calcular_total_em_atraso(self):
        """
        Calcula o valor total em atraso (renda + juros).
        
        Retorna:
            dict: Dicionario com valor_renda, juros, total
        """
        from datetime import datetime
        
        hoje = datetime.now()
        vencimento = datetime.strptime(self.data_proximo_vencimento, "%Y-%m-%d")
        
        if hoje <= vencimento:
            return {
                "valor_renda": self.valor_renda,
                "juros": 0.0,
                "total": self.valor_renda,
                "dias_atraso": 0
            }
        
        # Calcula dias de atraso
        dias_atraso = (hoje - vencimento).days
        
        # Calcula juros
        juros = self.calcular_juros(dias_atraso)
        
        return {
            "valor_renda": self.valor_renda,
            "juros": juros,
            "total": self.valor_renda + juros,
            "dias_atraso": dias_atraso
        }
    
    def renovar(self, meses=3):
        """
        Renova o contrato por mais meses.
        
        Parametros:
            meses (int): Numero de meses para renovar
        
        Retorna:
            bool: True se renovado com sucesso
        """
        if self.status != "Ativo":
            print(cor("Nao e possivel renovar um contrato inativo.", "vermelho"))
            return False
        
        from datetime import datetime, timedelta
        
        # Atualiza duracao
        self.duracao_meses += meses
        
        # Atualiza data de fim
        data_fim = datetime.strptime(self.data_fim, "%Y-%m-%d")
        data_fim = data_fim + timedelta(days=meses * 30)
        self.data_fim = data_fim.strftime("%Y-%m-%d")
        
        # Atualiza proximo vencimento
        self.data_proximo_vencimento = self._calcular_proximo_vencimento()
        
        # Salva no banco de dados
        self.salvar()
        
        print(cor(f"Contrato renovado com sucesso! Nova data fim: {formatar_data(self.data_fim)}", "verde"))
        return True
    
    def encerrar(self, motivo="Fim do contrato"):
        """
        Encerra o contrato.
        
        Parametros:
            motivo (str): Motivo do encerramento
        
        Retorna:
            bool: True se encerrado com sucesso
        """
        if self.status != "Ativo":
            print(cor("O contrato ja esta inativo.", "amarelo"))
            return False
        
        # Verifica se ha rendas em atraso
        if self.verificar_vencimento():
            atraso = self.calcular_total_em_atraso()
            print(cor(f"ATENCAO: Existem rendas em atraso no valor de {formatar_preco(atraso['total'])}", "vermelho"))
            
            if not input_sim_nao("Deseja encerrar mesmo com rendas em atraso? (S/N): "):
                print(cor("Encerramento cancelado.", "amarelo"))
                return False
        
        self.status = "Finalizado"
        self.observacoes = f"{self.observacoes} | Encerrado: {motivo}"
        
        # Atualiza estado da unidade para Livre
        self._liberar_unidade()
        
        # Salva no banco de dados
        self.salvar()
        
        print(cor(f"Contrato encerrado com sucesso! Motivo: {motivo}", "verde"))
        return True
    
    def _liberar_unidade(self):
        """
        Libera a unidade associada ao contrato.
        """
        unidade = Unidade.buscar_por_id(self.unidade_id)
        if unidade:
            unidade_obj = Unidade.from_dict(unidade)
            unidade_obj.alterar_estado("Livre")
    
    def salvar(self):
        """
        Salva o contrato na base de dados em memoria.
        
        Retorna:
            bool: True se salvo com sucesso
        """
        for i, contrato in enumerate(contratos):
            if contrato["id"] == self.id:
                contratos[i] = self.to_dict()
                return True
        
        contratos.append(self.to_dict())
        print(cor(f"Contrato criado com sucesso! (ID: {self.id})", "verde"))
        return True
    
    @staticmethod
    def listar_todos():
        """
        Lista todos os contratos cadastrados (apenas contratos mensais).
        """
        # Filtra apenas contratos mensais (ignora reservas Airbnb)
        contratos_mensais = [c for c in contratos if c.get("tipo") != "Airbnb"]
        
        if not contratos_mensais:
            print(cor("Nenhum contrato cadastrado.", "amarelo"))
            return
        
        print("\n" + cabecalho("LISTA DE CONTRATOS"))
        print(f"Total: {len(contratos_mensais)} contratos\n")
        
        for contrato in contratos_mensais:
            unidade = Unidade.buscar_por_id(contrato["unidade_id"])
            cliente = Cliente.buscar_por_id(contrato["cliente_id"])
            
            nome_unidade = unidade["nome"] if unidade else f"ID {contrato['unidade_id']}"
            nome_cliente = cliente["nome"] if cliente else f"ID {contrato['cliente_id']}"
            
            # Cor para o status
            cores_status = {
                "Ativo": "verde",
                "Finalizado": "azul",
                "Cancelado": "vermelho"
            }
            cor_status = cores_status.get(contrato["status"], "branco")
            
            # Verifica se esta vencido
            atraso = " ⚠️" if contrato["data_proximo_vencimento"] < obter_data_atual("%Y-%m-%d") else ""
            
            print(f"ID: {contrato['id']} | {nome_cliente}")
            print(f"  Unidade: {nome_unidade}")
            print(f"  Periodo: {formatar_data(contrato['data_inicio'])} -> {formatar_data(contrato['data_fim'])}")
            print(f"  Renda: {formatar_preco(contrato['valor_renda'])}")
            print(f"  Status: {cor(contrato['status'], cor_status)}{atraso}")
            print(linha_separadora(40))
    
    @staticmethod
    def listar_ativos():
        """
        Lista apenas contratos ativos (apenas contratos mensais).
        """
        # Filtra apenas contratos mensais ativos
        ativos = [c for c in contratos if c["status"] == "Ativo" and c.get("tipo") != "Airbnb"]
        
        if not ativos:
            print(cor("Nenhum contrato ativo.", "amarelo"))
            return
        
        print("\n" + cabecalho("CONTRATOS ATIVOS"))
        print(f"Total: {len(ativos)} contratos ativos\n")
        
        for contrato in ativos:
            unidade = Unidade.buscar_por_id(contrato["unidade_id"])
            cliente = Cliente.buscar_por_id(contrato["cliente_id"])
            
            nome_unidade = unidade["nome"] if unidade else f"ID {contrato['unidade_id']}"
            nome_cliente = cliente["nome"] if cliente else f"ID {contrato['cliente_id']}"
            
            print(f"ID: {contrato['id']} | {nome_cliente} | {nome_unidade}")
            print(f"  Renda: {formatar_preco(contrato['valor_renda'])}")
            print(f"  Prox. Vencimento: {formatar_data(contrato['data_proximo_vencimento'])}")
    
    @staticmethod
    def listar_vencidos():
        """
        Lista contratos com rendas em atraso (apenas contratos mensais).
        """
        from datetime import datetime
        hoje = datetime.now().strftime("%Y-%m-%d")
        
        # Filtra apenas contratos mensais ativos com vencimento vencido
        vencidos = [
            c for c in contratos 
            if c["status"] == "Ativo" 
            and c.get("tipo") != "Airbnb" 
            and c["data_proximo_vencimento"] < hoje
        ]
        
        if not vencidos:
            print(cor("Nenhum contrato com rendas em atraso.", "verde"))
            return
        
        print("\n" + cabecalho("CONTRATOS COM RENDAS EM ATRASO"))
        print(cor("ATENCAO: Os seguintes contratos estao com rendas vencidas!", "vermelho", estilo="negrito"))
        print()
        
        for contrato in vencidos:
            unidade = Unidade.buscar_por_id(contrato["unidade_id"])
            cliente = Cliente.buscar_por_id(contrato["cliente_id"])
            
            nome_unidade = unidade["nome"] if unidade else f"ID {contrato['unidade_id']}"
            nome_cliente = cliente["nome"] if cliente else f"ID {contrato['cliente_id']}"
            
            # Calcula dias de atraso
            vencimento = datetime.strptime(contrato["data_proximo_vencimento"], "%Y-%m-%d")
            dias_atraso = (datetime.now() - vencimento).days
            
            print(f"  {nome_cliente} - {nome_unidade}")
            print(f"    Vencido ha: {dias_atraso} dias")
            print(f"    Valor: {formatar_preco(contrato['valor_renda'])}")
            print(linha_separadora(35))
    
    @staticmethod
    def listar_a_expirar(dias_antecedencia=15):
        """
        Lista contratos que vao expirar em breve (apenas contratos mensais).
        
        Parametros:
            dias_antecedencia (int): Dias de antecedencia para alerta
        """
        from datetime import datetime, timedelta
        hoje = datetime.now()
        data_alerta = hoje + timedelta(days=dias_antecedencia)
        data_alerta_str = data_alerta.strftime("%Y-%m-%d")
        
        # Filtra apenas contratos mensais ativos com fim proximo
        a_expirar = [
            c for c in contratos 
            if c["status"] == "Ativo" 
            and c.get("tipo") != "Airbnb" 
            and c["data_fim"] <= data_alerta_str
        ]
        
        if not a_expirar:
            print(cor(f"Nenhum contrato a expirar nos proximos {dias_antecedencia} dias.", "verde"))
            return
        
        print(f"\n{cabecalho(f'CONTRATOS A EXPIRAR ({dias_antecedencia} DIAS)')}")
        print(cor(f"ATENCAO: {len(a_expirar)} contratos vao expirar em breve!", "amarelo", estilo="negrito"))
        print()
        
        for contrato in a_expirar:
            unidade = Unidade.buscar_por_id(contrato["unidade_id"])
            cliente = Cliente.buscar_por_id(contrato["cliente_id"])
            
            nome_unidade = unidade["nome"] if unidade else f"ID {contrato['unidade_id']}"
            nome_cliente = cliente["nome"] if cliente else f"ID {contrato['cliente_id']}"
            
            # Calcula dias restantes
            data_fim = datetime.strptime(contrato["data_fim"], "%Y-%m-%d")
            dias_restantes = (data_fim - datetime.now()).days
            
            print(f"  {nome_cliente} - {nome_unidade}")
            print(f"    Expira em: {formatar_data(contrato['data_fim'])} ({dias_restantes} dias)")
            print(f"    Renovacao: {'Automatica' if contrato['renovacao_automatica'] else 'Manual'}")
            print(linha_separadora(35))
    
    @staticmethod
    def buscar_por_id(id_contrato):
        """
        Busca um contrato pelo ID.
        
        Parametros:
            id_contrato (int): ID do contrato
        
        Retorna:
            dict: Dados do contrato, ou None se nao encontrado
        """
        for contrato in contratos:
            if contrato["id"] == id_contrato:
                return contrato
        return None
    
    @staticmethod
    def buscar_por_unidade(unidade_id):
        """
        Busca contratos de uma unidade (apenas contratos mensais).
        
        Parametros:
            unidade_id (int): ID da unidade
        
        Retorna:
            list: Lista de contratos da unidade
        """
        return [c for c in contratos if c["unidade_id"] == unidade_id and c.get("tipo") != "Airbnb"]
    
    @staticmethod
    def buscar_por_cliente(cliente_id):
        """
        Busca contratos de um cliente (apenas contratos mensais).
        
        Parametros:
            cliente_id (int): ID do cliente
        
        Retorna:
            list: Lista de contratos do cliente
        """
        return [c for c in contratos if c["cliente_id"] == cliente_id and c.get("tipo") != "Airbnb"]


# ------------------------------------------------------------
# 2. CLASSE RESERVA (Airbnb)
# ------------------------------------------------------------

class Reserva:
    """
    Classe que representa uma reserva Airbnb.
    
    Atributos:
        id (int): Identificador unico da reserva
        unidade_id (int): ID da unidade associada
        cliente_id (int): ID do cliente (hospede)
        data_checkin (str): Data de check-in
        data_checkout (str): Data de check-out
        num_noites (int): Numero de noites
        valor_diaria (float): Valor da diaria
        valor_total (float): Valor total da reserva
        status (str): "Pendente", "Ativa", "Finalizada", "Cancelada"
        checkin_realizado (bool): Se check-in foi realizado
        checkout_realizado (bool): Se check-out foi realizado
        data_checkin_real (str): Data/hora do check-in real
        data_checkout_real (str): Data/hora do check-out real
        multa_checkin_tardio (float): Multa por check-in tardio
        observacoes (str): Observacoes
    """
    
    def __init__(self, unidade_id, cliente_id, data_checkin, data_checkout,
                 valor_diaria, observacoes=""):
        """
        Inicializa uma nova reserva Airbnb.
        
        Parametros:
            unidade_id (int): ID da unidade
            cliente_id (int): ID do cliente
            data_checkin (str): Data de check-in (YYYY-MM-DD)
            data_checkout (str): Data de check-out (YYYY-MM-DD)
            valor_diaria (float): Valor da diaria
            observacoes (str): Observacoes
        """
        self.id = proximo_id_contrato()
        self.unidade_id = unidade_id
        self.cliente_id = cliente_id
        self.data_checkin = data_checkin
        self.data_checkout = data_checkout
        self.valor_diaria = valor_diaria
        self.observacoes = observacoes
        self.status = "Pendente"
        self.checkin_realizado = False
        self.checkout_realizado = False
        self.data_checkin_real = None
        self.data_checkout_real = None
        self.multa_checkin_tardio = 0.0
        
        # Calcula numero de noites
        self.num_noites = self._calcular_noites(data_checkin, data_checkout)
        
        # Calcula valor total
        self.valor_total = self.num_noites * valor_diaria
    
    def _calcular_noites(self, data_checkin, data_checkout):
        """
        Calcula o numero de noites entre duas datas.
        
        Parametros:
            data_checkin (str): Data de check-in
            data_checkout (str): Data de check-out
        
        Retorna:
            int: Numero de noites
        """
        from datetime import datetime
        checkin = datetime.strptime(data_checkin, "%Y-%m-%d")
        checkout = datetime.strptime(data_checkout, "%Y-%m-%d")
        return (checkout - checkin).days
    
    def to_dict(self):
        """
        Converte a reserva para um dicionario.
        
        Retorna:
            dict: Dicionario com todos os atributos da reserva
        """
        return {
            "id": self.id,
            "tipo": "Airbnb",
            "unidade_id": self.unidade_id,
            "cliente_id": self.cliente_id,
            "data_checkin": self.data_checkin,
            "data_checkout": self.data_checkout,
            "num_noites": self.num_noites,
            "valor_diaria": self.valor_diaria,
            "valor_total": self.valor_total,
            "status": self.status,
            "checkin_realizado": self.checkin_realizado,
            "checkout_realizado": self.checkout_realizado,
            "data_checkin_real": self.data_checkin_real,
            "data_checkout_real": self.data_checkout_real,
            "multa_checkin_tardio": self.multa_checkin_tardio,
            "observacoes": self.observacoes
        }
    
    @staticmethod
    def from_dict(dados):
        """
        Cria uma instancia de Reserva a partir de um dicionario.
        
        Parametros:
            dados (dict): Dicionario com os dados da reserva
        
        Retorna:
            Reserva: Instancia da reserva
        """
        reserva = Reserva(
            unidade_id=dados["unidade_id"],
            cliente_id=dados["cliente_id"],
            data_checkin=dados["data_checkin"],
            data_checkout=dados["data_checkout"],
            valor_diaria=dados["valor_diaria"],
            observacoes=dados.get("observacoes", "")
        )
        reserva.id = dados["id"]
        reserva.num_noites = dados["num_noites"]
        reserva.valor_total = dados["valor_total"]
        reserva.status = dados["status"]
        reserva.checkin_realizado = dados["checkin_realizado"]
        reserva.checkout_realizado = dados["checkout_realizado"]
        reserva.data_checkin_real = dados.get("data_checkin_real")
        reserva.data_checkout_real = dados.get("data_checkout_real")
        reserva.multa_checkin_tardio = dados.get("multa_checkin_tardio", 0.0)
        return reserva
    
    def exibir(self):
        """
        Exibe os detalhes da reserva formatados no terminal.
        """
        unidade = Unidade.buscar_por_id(self.unidade_id)
        cliente = Cliente.buscar_por_id(self.cliente_id)
        
        nome_unidade = unidade["nome"] if unidade else f"ID {self.unidade_id}"
        nome_cliente = cliente["nome"] if cliente else f"ID {self.cliente_id}"
        
        cores_status = {
            "Pendente": "amarelo",
            "Ativa": "verde",
            "Finalizada": "azul",
            "Cancelada": "vermelho"
        }
        cor_status = cores_status.get(self.status, "branco")
        
        print("\n" + linha_separadora(50))
        print(cor(f"RESERVA ID: {self.id}", "azul", estilo="negrito"))
        print(f"Unidade: {nome_unidade}")
        print(f"Cliente: {nome_cliente}")
        print(f"Check-in: {formatar_data(self.data_checkin)}")
        print(f"Check-out: {formatar_data(self.data_checkout)}")
        print(f"Noites: {self.num_noites}")
        print(f"Diaria: {formatar_preco(self.valor_diaria)}")
        print(f"Total: {formatar_preco(self.valor_total)}")
        print(f"Status: {cor(self.status, cor_status, estilo='negrito')}")
        
        if self.checkin_realizado:
            print(f"Check-in Real: {self.data_checkin_real}")
        
        if self.checkout_realizado:
            print(f"Check-out Real: {self.data_checkout_real}")
        
        if self.multa_checkin_tardio > 0:
            print(cor(f"Multa Check-in Tardio: {formatar_preco(self.multa_checkin_tardio)}", "vermelho"))
        
        if self.observacoes:
            print(f"Observacoes: {self.observacoes}")
        print(linha_separadora(50))
    
    def realizar_checkin(self, horario=None, multa_tardia=0.0):
        """
        Realiza o check-in da reserva.
        
        Parametros:
            horario (str): Horario do check-in (HH:MM)
            multa_tardia (float): Multa por check-in tardio
        
        Retorna:
            bool: True se realizado com sucesso
        """
        if self.status in ["Finalizada", "Cancelada"]:
            print(cor("Nao e possivel fazer check-in de uma reserva finalizada ou cancelada.", "vermelho"))
            return False
        
        if self.checkin_realizado:
            print(cor("Check-in ja foi realizado.", "amarelo"))
            return False
        
        self.checkin_realizado = True
        self.data_checkin_real = obter_data_atual("%Y-%m-%d %H:%M:%S")
        self.multa_checkin_tardio = multa_tardia
        self.status = "Ativa"
        
        # Atualiza estado da unidade
        self._alterar_estado_unidade("Ocupado")
        
        # Salva no banco de dados
        self.salvar()
        
        print(cor(f"Check-in realizado com sucesso! Unidade: {self.unidade_id}", "verde"))
        return True
    
    def realizar_checkout(self, registar_consumos=True):
        """
        Realiza o check-out da reserva.
        
        Parametros:
            registar_consumos (bool): Se deve registrar consumos de stock
        
        Retorna:
            bool: True se realizado com sucesso
        """
        if self.status in ["Finalizada", "Cancelada"]:
            print(cor("Nao e possivel fazer check-out de uma reserva finalizada ou cancelada.", "vermelho"))
            return False
        
        if not self.checkin_realizado:
            print(cor("Check-in nao foi realizado.", "vermelho"))
            return False
        
        if self.checkout_realizado:
            print(cor("Check-out ja foi realizado.", "amarelo"))
            return False
        
        self.checkout_realizado = True
        self.data_checkout_real = obter_data_atual("%Y-%m-%d %H:%M:%S")
        self.status = "Finalizada"
        
        # Libera a unidade
        self._alterar_estado_unidade("Livre")
        
        # Registra consumos de stock (Airbnb)
        if registar_consumos:
            self._registrar_consumos_airbnb()
        
        # Salva no banco de dados
        self.salvar()
        
        print(cor(f"Check-out realizado com sucesso! Unidade: {self.unidade_id}", "verde"))
        return True
    
    def _alterar_estado_unidade(self, novo_estado):
        """
        Altera o estado da unidade associada.
        
        Parametros:
            novo_estado (str): Novo estado da unidade
        """
        unidade = Unidade.buscar_por_id(self.unidade_id)
        if unidade:
            unidade_obj = Unidade.from_dict(unidade)
            unidade_obj.alterar_estado(novo_estado)
    
    def _registrar_consumos_airbnb(self):
        """
        Registra os consumos padrao de uma estadia Airbnb.
        """
        # Aqui serao registrados os consumos automaticos de stock
        # Esta funcionalidade sera implementada na integracao com o modulo de estoque
        print(cor(f"Registando consumos da estadia Airbnb (unidade {self.unidade_id})...", "ciano"))
    
    def cancelar(self, motivo="Cancelamento pelo cliente"):
        """
        Cancela a reserva.
        
        Parametros:
            motivo (str): Motivo do cancelamento
        
        Retorna:
            bool: True se cancelado com sucesso
        """
        if self.status == "Finalizada":
            print(cor("Nao e possivel cancelar uma reserva finalizada.", "vermelho"))
            return False
        
        if self.checkin_realizado:
            print(cor("Nao e possivel cancelar uma reserva com check-in realizado.", "vermelho"))
            return False
        
        self.status = "Cancelada"
        self.observacoes = f"{self.observacoes} | Cancelado: {motivo}"
        
        # Salva no banco de dados
        self.salvar()
        
        print(cor(f"Reserva cancelada com sucesso! Motivo: {motivo}", "amarelo"))
        return True
    
    def salvar(self):
        """
        Salva a reserva na base de dados em memoria.
        
        Retorna:
            bool: True se salvo com sucesso
        """
        # Usamos a mesma lista de contratos para guardar reservas
        for i, contrato in enumerate(contratos):
            if contrato["id"] == self.id:
                dados = self.to_dict()
                contratos[i] = dados
                return True
        
        # Novo registo
        dados = self.to_dict()
        contratos.append(dados)
        print(cor(f"Reserva criada com sucesso! (ID: {self.id})", "verde"))
        return True
    
    @staticmethod
    def listar_todas():
        """
        Lista todas as reservas Airbnb.
        """
        reservas = [c for c in contratos if c.get("tipo") == "Airbnb"]
        
        if not reservas:
            print(cor("Nenhuma reserva Airbnb cadastrada.", "amarelo"))
            return
        
        print("\n" + cabecalho("LISTA DE RESERVAS AIRBNB"))
        print(f"Total: {len(reservas)} reservas\n")
        
        for reserva in reservas:
            unidade = Unidade.buscar_por_id(reserva["unidade_id"])
            cliente = Cliente.buscar_por_id(reserva["cliente_id"])
            
            nome_unidade = unidade["nome"] if unidade else f"ID {reserva['unidade_id']}"
            nome_cliente = cliente["nome"] if cliente else f"ID {reserva['cliente_id']}"
            
            cores_status = {
                "Pendente": "amarelo",
                "Ativa": "verde",
                "Finalizada": "azul",
                "Cancelada": "vermelho"
            }
            cor_status = cores_status.get(reserva["status"], "branco")
            
            print(f"ID: {reserva['id']} | {nome_cliente}")
            print(f"  Unidade: {nome_unidade}")
            print(f"  Periodo: {formatar_data(reserva['data_checkin'])} -> {formatar_data(reserva['data_checkout'])}")
            print(f"  Total: {formatar_preco(reserva['valor_total'])}")
            print(f"  Status: {cor(reserva['status'], cor_status)}")
            print(linha_separadora(40))


# ------------------------------------------------------------
# 3. FUNCOES DE INTERFACE
# ------------------------------------------------------------

def criar_contrato():
    """
    Interface para criar um novo contrato mensal.
    """
    print("\n" + cabecalho("CRIAR CONTRATO MENSAL"))
    
    # Lista unidades disponiveis
    print("\nUnidades disponiveis para contrato:")
    unidades_livres = [u for u in unidades if u["tipo"] == "Mensal" and u["estado"] == "Livre"]
    
    if not unidades_livres:
        print(cor("Nenhuma unidade Mensal disponivel para contrato.", "vermelho"))
        return
    
    for u in unidades_livres:
        print(f"  ID: {u['id']} | {u['nome']} | Capacidade: {u['capacidade']} pessoas")
    
    try:
        unidade_id = input_int("ID da unidade: ", min_valor=1)
        if not Unidade.buscar_por_id(unidade_id):
            print(cor("Unidade nao encontrada.", "vermelho"))
            return
    except:
        print(cor("Operacao cancelada.", "amarelo"))
        return
    
    # Lista clientes do tipo Morador
    clientes_moradores = [c for c in clientes if c["tipo"] == "Morador"]
    
    if not clientes_moradores:
        print(cor("Nenhum morador cadastrado. Crie um cliente do tipo Morador primeiro.", "vermelho"))
        return
    
    print("\nMoradores disponiveis:")
    for c in clientes_moradores:
        print(f"  ID: {c['id']} | {c['nome']}")
    
    try:
        cliente_id = input_int("ID do morador: ", min_valor=1)
        if not Cliente.buscar_por_id(cliente_id):
            print(cor("Cliente nao encontrado.", "vermelho"))
            return
    except:
        print(cor("Operacao cancelada.", "amarelo"))
        return
    
    # Dados do contrato
    data_inicio = input_data("Data de inicio (YYYY-MM-DD): ")
    duracao_meses = input_int("Duracao em meses (minimo 3): ", min_valor=3)
    valor_renda = input_float("Valor da renda mensal (€): ", min_valor=0)
    
    dia_vencimento = input_int("Dia de vencimento (1-31, default 5): ", obrigatorio=False)
    if dia_vencimento is None:
        dia_vencimento = 5
    elif dia_vencimento < 1 or dia_vencimento > 31:
        print(cor("Dia invalido. Usando dia 5.", "amarelo"))
        dia_vencimento = 5
    
    caução = input_float("Valor da caução (default 150.00): ", obrigatorio=False, min_valor=0)
    if caução is None:
        caução = 150.00
    
    renovacao = input_sim_nao("Renovacao automatica? (S/N): ")
    tipo_contrato = input_opcao("Tipo de contrato", ["Fisico", "Digital"])
    observacoes = input("Observacoes (opcional): ").strip()
    
    # Cria o contrato
    contrato = Contrato(
        unidade_id=unidade_id,
        cliente_id=cliente_id,
        data_inicio=data_inicio,
        duracao_meses=duracao_meses,
        valor_renda=valor_renda,
        dia_vencimento=dia_vencimento,
        caução=caução,
        renovacao_automatica=renovacao,
        tipo_contrato=tipo_contrato,
        observacoes=observacoes
    )
    
    # Atualiza estado da unidade
    unidade = Unidade.buscar_por_id(unidade_id)
    if unidade:
        unidade_obj = Unidade.from_dict(unidade)
        unidade_obj.alterar_estado("Ocupado")
    
    contrato.salvar()
    contrato.exibir()
    
    return contrato


def criar_reserva():
    """
    Interface para criar uma nova reserva Airbnb.
    """
    print("\n" + cabecalho("CRIAR RESERVA AIRBNB"))
    
    # Lista unidades disponiveis
    print("\nUnidades disponiveis para reserva:")
    unidades_livres = [u for u in unidades if u["tipo"] == "Airbnb" and u["estado"] in ["Livre", "Reservado"]]
    
    if not unidades_livres:
        print(cor("Nenhuma unidade Airbnb disponivel para reserva.", "vermelho"))
        return
    
    for u in unidades_livres:
        print(f"  ID: {u['id']} | {u['nome']} | Capacidade: {u['capacidade']} pessoas")
    
    try:
        unidade_id = input_int("ID da unidade: ", min_valor=1)
        if not Unidade.buscar_por_id(unidade_id):
            print(cor("Unidade nao encontrada.", "vermelho"))
            return
    except:
        print(cor("Operacao cancelada.", "amarelo"))
        return
    
    # Lista clientes do tipo Airbnb
    clientes_airbnb = [c for c in clientes if c["tipo"] == "Airbnb"]
    
    if not clientes_airbnb:
        print(cor("Nenhum hospede Airbnb cadastrado. Crie um cliente do tipo Airbnb primeiro.", "vermelho"))
        return
    
    print("\nHospedes Airbnb disponiveis:")
    for c in clientes_airbnb:
        print(f"  ID: {c['id']} | {c['nome']} | Documento: {c.get('documento', 'N/A')}")
    
    try:
        cliente_id = input_int("ID do hospede: ", min_valor=1)
        if not Cliente.buscar_por_id(cliente_id):
            print(cor("Cliente nao encontrado.", "vermelho"))
            return
    except:
        print(cor("Operacao cancelada.", "amarelo"))
        return
    
    # Dados da reserva
    data_checkin = input_data("Data de check-in (YYYY-MM-DD): ")
    data_checkout = input_data("Data de check-out (YYYY-MM-DD): ")
    
    # Validar datas
    from datetime import datetime
    checkin = datetime.strptime(data_checkin, "%Y-%m-%d")
    checkout = datetime.strptime(data_checkout, "%Y-%m-%d")
    
    if checkout <= checkin:
        print(cor("Check-out deve ser depois do check-in.", "vermelho"))
        return
    
    noites = (checkout - checkin).days
    
    if noites < 2:
        print(cor("Estadia minima: 2 noites (1 noite com autorizacao do Admin).", "amarelo"))
        if not input_sim_nao("Deseja continuar com 1 noite? (S/N): "):
            return
        print(cor("Reserva de 1 noite autorizada pelo Admin.", "verde"))
    
    if noites > 28:
        print(cor("Estadia maxima: 28 noites.", "amarelo"))
        return
    
    # Busca o preco da unidade
    unidade = Unidade.buscar_por_id(unidade_id)
    valor_diaria = unidade["preco_base"] if unidade else 45.00
    
    print(f"\nValor da diaria: {formatar_preco(valor_diaria)}")
    print(f"Total de noites: {noites}")
    print(f"Valor total: {formatar_preco(noites * valor_diaria)}")
    
    if not input_sim_nao("Confirmar reserva? (S/N): "):
        print(cor("Reserva cancelada.", "amarelo"))
        return
    
    # Cria a reserva
    reserva = Reserva(
        unidade_id=unidade_id,
        cliente_id=cliente_id,
        data_checkin=data_checkin,
        data_checkout=data_checkout,
        valor_diaria=valor_diaria,
        observacoes=input("Observacoes (opcional): ").strip()
    )
    
    # Atualiza estado da unidade
    unidade_obj = Unidade.from_dict(unidade)
    unidade_obj.alterar_estado("Reservado")
    
    reserva.salvar()
    reserva.exibir()
    
    return reserva


def realizar_checkin():
    """
    Interface para realizar check-in de uma reserva.
    """
    print("\n" + cabecalho("REALIZAR CHECK-IN"))
    
    # Lista reservas pendentes
    reservas_pendentes = [
        c for c in contratos 
        if c.get("tipo") == "Airbnb" and c.get("status") == "Pendente"
    ]
    
    if not reservas_pendentes:
        print(cor("Nenhuma reserva pendente para check-in.", "amarelo"))
        return
    
    print("\nReservas pendentes:")
    for r in reservas_pendentes:
        cliente = Cliente.buscar_por_id(r["cliente_id"])
        unidade = Unidade.buscar_por_id(r["unidade_id"])
        nome_cliente = cliente["nome"] if cliente else f"ID {r['cliente_id']}"
        nome_unidade = unidade["nome"] if unidade else f"ID {r['unidade_id']}"
        
        print(f"  ID: {r['id']} | {nome_cliente} | {nome_unidade}")
        print(f"    Check-in: {formatar_data(r['data_checkin'])}")
    
    try:
        reserva_id = input_int("ID da reserva: ", min_valor=1)
    except:
        print(cor("Operacao cancelada.", "amarelo"))
        return
    
    dados_reserva = None
    for r in reservas_pendentes:
        if r["id"] == reserva_id:
            dados_reserva = r
            break
    
    if not dados_reserva:
        print(cor("Reserva nao encontrada.", "vermelho"))
        return
    
    reserva = Reserva.from_dict(dados_reserva)
    
    # Verifica check-in tardio (apos as 17:00)
    from datetime import datetime
    hora_atual = datetime.now().hour
    
    multa_tardia = 0.0
    if hora_atual >= 17:
        print(cor("Check-in tardio (apos as 17:00)!", "vermelho"))
        multa_tardia = input_float("Valor da multa por check-in tardio (€): ", min_valor=0)
    
    reserva.realizar_checkin(multa_tardia=multa_tardia) # type: ignore
    reserva.exibir()


def realizar_checkout():
    """
    Interface para realizar check-out de uma reserva.
    """
    print("\n" + cabecalho("REALIZAR CHECK-OUT"))
    
    # Lista reservas ativas
    reservas_ativas = [
        c for c in contratos 
        if c.get("tipo") == "Airbnb" and c.get("status") == "Ativa"
    ]
    
    if not reservas_ativas:
        print(cor("Nenhuma reserva ativa para check-out.", "amarelo"))
        return
    
    print("\nReservas ativas:")
    for r in reservas_ativas:
        cliente = Cliente.buscar_por_id(r["cliente_id"])
        unidade = Unidade.buscar_por_id(r["unidade_id"])
        nome_cliente = cliente["nome"] if cliente else f"ID {r['cliente_id']}"
        nome_unidade = unidade["nome"] if unidade else f"ID {r['unidade_id']}"
        
        print(f"  ID: {r['id']} | {nome_cliente} | {nome_unidade}")
        print(f"    Check-out previsto: {formatar_data(r['data_checkout'])}")
    
    try:
        reserva_id = input_int("ID da reserva: ", min_valor=1)
    except:
        print(cor("Operacao cancelada.", "amarelo"))
        return
    
    dados_reserva = None
    for r in reservas_ativas:
        if r["id"] == reserva_id:
            dados_reserva = r
            break
    
    if not dados_reserva:
        print(cor("Reserva nao encontrada.", "vermelho"))
        return
    
    reserva = Reserva.from_dict(dados_reserva)
    
    # Verifica se o checkout e antes do horario (11:00)
    from datetime import datetime
    hora_atual = datetime.now().hour
    if hora_atual >= 11:
        print(cor("Check-out tardio (apos as 11:00)!", "amarelo"))
        if not input_sim_nao("Deseja continuar mesmo assim? (S/N): "):
            print(cor("Check-out cancelado.", "amarelo"))
            return
    
    # Pergunta se quer registrar consumos
    registrar = input_sim_nao("Registrar consumos de stock? (S/N): ")
    
    reserva.realizar_checkout(registar_consumos=registrar)
    reserva.exibir()


def listar_contratos():
    """
    Interface para listar contratos.
    """
    print("\n" + cabecalho("LISTAR CONTRATOS"))
    
    print("Opcoes:")
    print("  1 - Todos os contratos")
    print("  2 - Contratos ativos")
    print("  3 - Contratos com rendas em atraso")
    print("  4 - Contratos a expirar")
    print("  5 - Contratos de uma unidade")
    print("  0 - Voltar")
    
    opcao = input("\nEscolha uma opcao: ").strip()
    
    if opcao == "1":
        Contrato.listar_todos()
    elif opcao == "2":
        Contrato.listar_ativos()
    elif opcao == "3":
        Contrato.listar_vencidos()
    elif opcao == "4":
        dias = input_int("Antecedencia em dias (default 15): ", obrigatorio=False)
        if dias is None:
            dias = 15
        Contrato.listar_a_expirar(dias)
    elif opcao == "5":
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
        
        resultados = Contrato.buscar_por_unidade(unidade_id)
        if resultados:
            print(f"\n{cabecalho(f'CONTRATOS DA UNIDADE {unidade_id}')}")
            for c in resultados:
                cliente = Cliente.buscar_por_id(c["cliente_id"])
                nome_cliente = cliente["nome"] if cliente else f"ID {c['cliente_id']}"
                print(f"  ID: {c['id']} | {nome_cliente}")
                print(f"    Status: {c['status']} | Fim: {formatar_data(c['data_fim'])}")
        else:
            print(cor("Nenhum contrato encontrado para esta unidade.", "amarelo"))
    elif opcao == "0":
        return
    else:
        print(cor("Opcao invalida.", "vermelho"))


def listar_reservas():
    """
    Interface para listar reservas Airbnb.
    """
    print("\n" + cabecalho("LISTAR RESERVAS AIRBNB"))
    
    print("Opcoes:")
    print("  1 - Todas as reservas")
    print("  2 - Reservas pendentes")
    print("  3 - Reservas ativas")
    print("  0 - Voltar")
    
    opcao = input("\nEscolha uma opcao: ").strip()
    
    if opcao == "1":
        Reserva.listar_todas()
    elif opcao == "2":
        reservas = [c for c in contratos if c.get("tipo") == "Airbnb" and c.get("status") == "Pendente"]
        if reservas:
            print(f"\n{cabecalho('RESERVAS PENDENTES')}")
            for r in reservas:
                cliente = Cliente.buscar_por_id(r["cliente_id"])
                unidade = Unidade.buscar_por_id(r["unidade_id"])
                nome_cliente = cliente["nome"] if cliente else f"ID {r['cliente_id']}"
                nome_unidade = unidade["nome"] if unidade else f"ID {r['unidade_id']}"
                print(f"  ID: {r['id']} | {nome_cliente} | {nome_unidade}")
                print(f"    Check-in: {formatar_data(r['data_checkin'])}")
        else:
            print(cor("Nenhuma reserva pendente.", "amarelo"))
    elif opcao == "3":
        reservas = [c for c in contratos if c.get("tipo") == "Airbnb" and c.get("status") == "Ativa"]
        if reservas:
            print(f"\n{cabecalho('RESERVAS ATIVAS')}")
            for r in reservas:
                cliente = Cliente.buscar_por_id(r["cliente_id"])
                unidade = Unidade.buscar_por_id(r["unidade_id"])
                nome_cliente = cliente["nome"] if cliente else f"ID {r['cliente_id']}"
                nome_unidade = unidade["nome"] if unidade else f"ID {r['unidade_id']}"
                print(f"  ID: {r['id']} | {nome_cliente} | {nome_unidade}")
                print(f"    Check-out: {formatar_data(r['data_checkout'])}")
        else:
            print(cor("Nenhuma reserva ativa.", "amarelo"))
    elif opcao == "0":
        return
    else:
        print(cor("Opcao invalida.", "vermelho"))


def editar_contrato():
    """
    Interface para editar um contrato existente.
    """
    print("\n" + cabecalho("EDITAR CONTRATO"))
    
    Contrato.listar_todos()
    
    if not contratos:
        return
    
    try:
        contrato_id = input_int("ID do contrato para editar: ", min_valor=1)
    except:
        print(cor("Operacao cancelada.", "amarelo"))
        return
    
    dados_contrato = Contrato.buscar_por_id(contrato_id)
    if not dados_contrato:
        print(cor("Contrato nao encontrado.", "vermelho"))
        return
    
    if dados_contrato.get("tipo") == "Airbnb":
        print(cor("Esta e uma reserva Airbnb. Use o menu de reservas.", "amarelo"))
        return
    
    contrato = Contrato.from_dict(dados_contrato)
    
    if contrato.status != "Ativo":
        print(cor("Apenas contratos ativos podem ser editados.", "vermelho"))
        return
    
    print(f"\nEditando contrato: {cor(f'ID {contrato.id}', 'azul', estilo='negrito')}")
    print("(Deixe em branco para manter o valor atual)")
    
    # Permite editar apenas alguns campos
    novo_valor = input(f"Valor da renda ({contrato.valor_renda}): ").strip()
    if novo_valor:
        try:
            contrato.valor_renda = float(novo_valor.replace(",", "."))
        except ValueError:
            print(cor("Valor invalido. Mantendo o atual.", "amarelo"))
    
    novo_dia = input(f"Dia de vencimento ({contrato.dia_vencimento}): ").strip()
    if novo_dia:
        try:
            novo_dia_int = int(novo_dia)
            if 1 <= novo_dia_int <= 31:
                contrato.dia_vencimento = novo_dia_int
                contrato.data_proximo_vencimento = contrato._calcular_proximo_vencimento()
            else:
                print(cor("Dia invalido. Mantendo o atual.", "amarelo"))
        except ValueError:
            print(cor("Valor invalido. Mantendo o atual.", "amarelo"))
    
    novas_obs = input(f"Observacoes ({contrato.observacoes}): ").strip()
    if novas_obs:
        contrato.observacoes = novas_obs
    
    if input_sim_nao("Confirmar alteracoes? (S/N): "):
        contrato.salvar()
        contrato.exibir()
    else:
        print(cor("Edicao cancelada.", "amarelo"))


def encerrar_contrato():
    """
    Interface para encerrar um contrato.
    """
    print("\n" + cabecalho("ENCERRAR CONTRATO"))
    
    Contrato.listar_ativos()
    
    if not [c for c in contratos if c["status"] == "Ativo" and c.get("tipo") != "Airbnb"]:
        print(cor("Nenhum contrato ativo para encerrar.", "amarelo"))
        return
    
    try:
        contrato_id = input_int("ID do contrato para encerrar: ", min_valor=1)
    except:
        print(cor("Operacao cancelada.", "amarelo"))
        return
    
    dados_contrato = Contrato.buscar_por_id(contrato_id)
    if not dados_contrato:
        print(cor("Contrato nao encontrado.", "vermelho"))
        return
    
    if dados_contrato.get("tipo") == "Airbnb":
        print(cor("Esta e uma reserva Airbnb. Use o menu de reservas.", "amarelo"))
        return
    
    contrato = Contrato.from_dict(dados_contrato)
    
    if contrato.status != "Ativo":
        print(cor("Apenas contratos ativos podem ser encerrados.", "vermelho"))
        return
    
    contrato.exibir()
    
    print(cor("ATENCAO: Esta operacao nao pode ser desfeita!", "vermelho", estilo="negrito"))
    
    if not input_sim_nao("Tem certeza que deseja encerrar este contrato? (S/N): "):
        print(cor("Encerramento cancelado.", "amarelo"))
        return
    
    motivo = input_obrigatorio("Motivo do encerramento: ")
    contrato.encerrar(motivo)


def renovar_contrato():
    """
    Interface para renovar um contrato.
    """
    print("\n" + cabecalho("RENOVAR CONTRATO"))
    
    Contrato.listar_ativos()
    
    if not [c for c in contratos if c["status"] == "Ativo" and c.get("tipo") != "Airbnb"]:
        print(cor("Nenhum contrato ativo para renovar.", "amarelo"))
        return
    
    try:
        contrato_id = input_int("ID do contrato para renovar: ", min_valor=1)
    except:
        print(cor("Operacao cancelada.", "amarelo"))
        return
    
    dados_contrato = Contrato.buscar_por_id(contrato_id)
    if not dados_contrato:
        print(cor("Contrato nao encontrado.", "vermelho"))
        return
    
    if dados_contrato.get("tipo") == "Airbnb":
        print(cor("Esta e uma reserva Airbnb. Use o menu de reservas.", "amarelo"))
        return
    
    contrato = Contrato.from_dict(dados_contrato)
    
    if contrato.status != "Ativo":
        print(cor("Apenas contratos ativos podem ser renovados.", "vermelho"))
        return
    
    contrato.exibir()
    
    meses = input_int("Meses para renovar (default 3): ", obrigatorio=False, min_valor=1)
    if meses is None:
        meses = 3
    
    if input_sim_nao(f"Renovar por {meses} meses? (S/N): "):
        contrato.renovar(meses)


# ------------------------------------------------------------
# 4. MENU DE CONTRATOS
# ------------------------------------------------------------

def menu_contratos():
    """
    Menu principal do modulo de contratos e reservas.
    """
    while True:
        print("\n" + cabecalho("GESTAO DE CONTRATOS E RESERVAS"))
        print("  CONTRATOS MENSAIS:")
        print("  1 - Criar contrato")
        print("  2 - Listar contratos")
        print("  3 - Editar contrato")
        print("  4 - Renovar contrato")
        print("  5 - Encerrar contrato")
        print("")
        print("  RESERVAS AIRBNB:")
        print("  6 - Criar reserva")
        print("  7 - Listar reservas")
        print("  8 - Realizar check-in")
        print("  9 - Realizar check-out")
        print("")
        print("  0 - Voltar")
        print(linha_separadora())
        
        opcao = input("Escolha uma opcao: ").strip()
        
        if opcao == "1":
            criar_contrato()
        elif opcao == "2":
            listar_contratos()
        elif opcao == "3":
            editar_contrato()
        elif opcao == "4":
            renovar_contrato()
        elif opcao == "5":
            encerrar_contrato()
        elif opcao == "6":
            criar_reserva()
        elif opcao == "7":
            listar_reservas()
        elif opcao == "8":
            realizar_checkin()
        elif opcao == "9":
            realizar_checkout()
        elif opcao == "0":
            print(cor("Voltando...", "amarelo"))
            break
        else:
            print(cor("Opcao invalida. Tente novamente.", "vermelho"))


# ------------------------------------------------------------
# 5. DADOS DE EXEMPLO
# ------------------------------------------------------------

def carregar_contratos_exemplo():
    """
    Carrega contratos e reservas de exemplo no sistema.
    """
    from datetime import datetime, timedelta
    
    # Busca unidades e clientes existentes
    unidades_mensal = [u for u in unidades if u["tipo"] == "Mensal"]
    unidades_airbnb = [u for u in unidades if u["tipo"] == "Airbnb"]
    clientes_moradores = [c for c in clientes if c["tipo"] == "Morador"]
    clientes_airbnb = [c for c in clientes if c["tipo"] == "Airbnb"]
    
    # Contrato exemplo (se houver morador e unidade mensal)
    if unidades_mensal and clientes_moradores:
        contrato = Contrato(
            unidade_id=unidades_mensal[0]["id"],
            cliente_id=clientes_moradores[0]["id"],
            data_inicio=datetime.now().strftime("%Y-%m-%d"),
            duracao_meses=6,
            valor_renda=250.00,
            dia_vencimento=5,
            caução=150.00,
            renovacao_automatica=True,
            tipo_contrato="Fisico",
            observacoes="Contrato de exemplo"
        )
        contrato.salvar()
        print(cor(f"Contrato exemplo criado: ID {contrato.id}", "verde"))
    
    # Reserva exemplo (se houver hospede e unidade Airbnb)
    if unidades_airbnb and clientes_airbnb:
        hoje = datetime.now()
        checkin = (hoje + timedelta(days=7)).strftime("%Y-%m-%d")
        checkout = (hoje + timedelta(days=10)).strftime("%Y-%m-%d")
        
        reserva = Reserva(
            unidade_id=unidades_airbnb[0]["id"],
            cliente_id=clientes_airbnb[0]["id"],
            data_checkin=checkin,
            data_checkout=checkout,
            valor_diaria=45.00,
            observacoes="Reserva de exemplo"
        )
        reserva.salvar()
        print(cor(f"Reserva exemplo criada: ID {reserva.id}", "verde"))


# ------------------------------------------------------------
# 6. BLOCO DE TESTE
# ------------------------------------------------------------

if __name__ == "__main__":
    
    print("\n" + cabecalho("TESTE DO MODULO DE CONTRATOS"))
    
    # Carrega dados de exemplo
    from unidades import carregar_unidades_exemplo
    from clientes import carregar_clientes_exemplo
    
    carregar_unidades_exemplo()
    carregar_clientes_exemplo()
    carregar_contratos_exemplo()
    
    # Mostra o estado dos dados
    mostrar_estado_dados()
    
    # Lista contratos
    Contrato.listar_todos()
    
    # Lista contratos ativos
    Contrato.listar_ativos()
    
    # Lista reservas
    Reserva.listar_todas()
    
    # Verifica contratos a expirar
    Contrato.listar_a_expirar()
    
    print("\n" + cabecalho("TESTE CONCLUIDO"))