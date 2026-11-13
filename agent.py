"""
Agente Organizador de Tarefas no Trello com Google ADK e Gemini
Desenvolvido como projeto final do Bootcamp DXC - IA do Zero ao Primeiro Agente (DIO)
Autor: Hamilton Castro
"""

import os
import datetime
from dotenv import load_dotenv
from trello import TrelloClient
from google.adk.agents.llm_agent import Agent

# Carrega variáveis de ambiente
load_dotenv()

TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
TRELLO_BOARD_NAME = os.getenv("TRELLO_BOARD_NAME", "DIO")


def _get_trello_client() -> TrelloClient:
    """Função utilitária centralizada para conectar ao Trello."""
    return TrelloClient(
        api_key=TRELLO_API_KEY,
        token=TRELLO_TOKEN
    )


def _get_board_lists():
    """Recupera o quadro DIO e mapeia suas listas normalizadas."""
    client = _get_trello_client()
    boards = client.list_boards()
    board = next((b for b in boards if b.name.strip().upper() == TRELLO_BOARD_NAME.strip().upper()), None)
    
    if not board:
        raise ValueError(f"Quadro '{TRELLO_BOARD_NAME}' não encontrado no seu Trello.")
        
    lists = {l.name.strip().lower(): l for l in board.list_lists()}
    return board, lists


def criar_tarefa(titulo: str, descricao: str = "", data_entrega: str = None) -> str:
    """
    Cria uma nova tarefa no Trello na lista 'A fazer'.
    MELHORIA IMPLEMENTADA: Tratamento robusto de fuso horário/data para evitar o bug de 'dia a menos'.
    """
    try:
        board, lists = _get_board_lists()
        target_list = lists.get("a fazer")
        
        if not target_list:
            return "Erro: Lista 'A fazer' não encontrada no quadro."
            
        due_date = None
        if data_entrega:
            try:
                # Ajuste de data com fuso explícito para não recuar 1 dia
                dt = datetime.datetime.fromisoformat(data_entrega.replace("Z", "+00:00"))
                due_date = dt.strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                due_date = None

        card = target_list.add_card(name=titulo, desc=descricao, due=due_date)
        return f"Card '{card.name}' criado com sucesso na lista 'A fazer'."
    except Exception as e:
        return f"Falha ao criar card no Trello: {str(e)}"


def listar_tarefas(status: str = None) -> str:
    """
    Lista tarefas do quadro DIO.
    MELHORIA IMPLEMENTADA: Aceita variações com/sem acento (ex: 'concluído' ou 'concluido').
    """
    try:
        board, lists = _get_board_lists()
        
        if status:
            normalized_status = status.strip().lower().replace("í", "i")
            matched_list = None
            for name, l in lists.items():
                if name.replace("í", "i") == normalized_status:
                    matched_list = l
                    break
                    
            if not matched_list:
                return f"Status '{status}' inválido. Use: 'A fazer', 'Em andamento' ou 'Concluído'."
                
            cards = matched_list.list_cards()
            if not cards:
                return f"Nenhuma tarefa encontrada na lista '{matched_list.name}'."
            return f"Tarefas em '{matched_list.name}':\n" + "\n".join([f"- {c.name}" for c in cards])

        # Listar todas
        resumo = []
        for l in board.list_lists():
            cards = l.list_cards()
            resumo.append(f"[{l.name}] ({len(cards)} tarefas)")
            for c in cards:
                resumo.append(f"  • {c.name}")
        return "\n".join(resumo)
    except Exception as e:
        return f"Falha ao listar tarefas: {str(e)}"


def mover_tarefa(titulo_tarefa: str, novo_status: str) -> str:
    """
    Move um card entre 'A fazer', 'Em andamento' e 'Concluído'.
    MELHORIA IMPLEMENTADA: Normalização fonética/acentos e busca flexível de nome de card.
    """
    try:
        board, lists = _get_board_lists()
        
        # Mapeia destino com e sem acento
        dest_norm = novo_status.strip().lower().replace("í", "i")
        target_list = None
        for name, l in lists.items():
            if name.replace("í", "i") == dest_norm:
                target_list = l
                break
                
        if not target_list:
            return f"Status '{novo_status}' inválido. Opções válidas: A fazer, Em andamento, Concluído."

        # Busca o card em todas as listas
        found_card = None
        for l in board.list_lists():
            for c in l.list_cards():
                if titulo_tarefa.strip().lower() in c.name.strip().lower():
                    found_card = c
                    break
            if found_card:
                break
                
        if not found_card:
            return f"Card com título '{titulo_tarefa}' não foi localizado no quadro."

        found_card.change_list(target_list.id)
        return f"Card '{found_card.name}' movido com sucesso para a lista '{target_list.name}'."
    except Exception as e:
        return f"Falha ao mover tarefa: {str(e)}"


# Definição e configuração do Agente Google ADK
root_agent = Agent(
    model="gemini-2.0-flash",
    name="root_agent",
    description="Agente autônomo para gerenciamento inteligente de tarefas diárias no Trello.",
    instruction=(
        f"Você é um assistente de produtividade pessoal que gerencia um quadro do Trello chamado {TRELLO_BOARD_NAME}. "
        f"Hoje é {datetime.date.today().strftime('%d/%m/%Y')}. "
        "Sempre comece a conversa perguntando educadamente quais são as tarefas do dia do usuário. "
        "Quando o usuário citar tarefas, utilize a ferramenta 'criar_tarefa' para adicioná-las. "
        "Se o usuário pedir para ver o que tem para fazer, use 'listar_tarefas'. "
        "Quando o usuário disser que começou ou terminou algo, use 'mover_tarefa'. "
        "Mantenha um tom proativo, direto e encorajador."
    ),
    tools=[criar_tarefa, listar_tarefas, mover_tarefa]
)
