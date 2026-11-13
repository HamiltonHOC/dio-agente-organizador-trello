# Agente Organizador de Tarefas no Trello com Google ADK e Gemini

Projeto de conclusão do Bootcamp **DXC - IA: Do Zero ao Primeiro Agente** na [DIO](https://dio.me).

---

## 📌 Minha Visão e Contexto do Projeto
Tenho 44 anos, sou empresário, ex-atleta de basquete e estudante de **Produção Criativa com IA** na Faculdade Estácio. Não sou desenvolvedor de software de formação nem pretendo virar programador de sintaxe tradicional. O meu objetivo ao entrar neste bootcamp foi puramente estratégico: entender como um Agente de IA toma decisões, aciona ferramentas externas e executa ações práticas em sistemas reais de produtividade.

Para construir esta solução, trabalhei em modelo de **pair programming e mentoria guiada com IA** (Google Antigravity / DIO Agent). Toda a lógica foi dissecada e construída no detalhe: a criação do quadro no Trello, o registro da aplicação, a obtenção das credenciais de API, o entendimento do Google ADK e a resolução dos gargalos práticos do código.

---

## 🎯 O que o Agente Faz na Prática
O agente combina o modelo **Gemini 2.0 Flash** com o **Google Agent Development Kit (ADK)** para atuar como um assistente de rotina:

1. **Entrada do Usuário:** O usuário conversa em linguagem natural e informal sobre suas demandas do dia.
2. **Tomada de Decisão do Gemini:** O modelo interpreta a intenção e decide qual função em Python deve ser disparada (*Function Calling / Tools*).
3. **Execução no Trello:** A ação se reflete imediatamente no quadro **DIO**:
   - **`criar_tarefa`:** Adiciona o card na coluna *A fazer* com data e descrição.
   - **`listar_tarefas`:** Puxa o status atual do quadro para dar visibilidade ao usuário.
   - **`mover_tarefa`:** Move o card conforme o trabalho avança (*A fazer* ➔ *Em andamento* ➔ *Concluído*).

---

## 🚀 Melhorias que Implementei
O código original do laboratório apresentava pontos de atrito que quebravam a experiência do usuário comum. Apliquei melhorias diretas:

- **Tolerância a Acentos e Fala Natural:** O agente agora trata o texto antes de consultar o Trello. Tanto faz digitar `"concluído"` com acento ou `"concluido"` sem acento, o card é movido sem retornar erro de status inválido.
- **Ajuste de Fuso Horário nas Datas:** Correção no tratamento de fuso horário para evitar a defasagem clássica de UTC que fazia a tarefa chegar ao Trello com um dia a menos.
- **Conexão Centralizada e Proteção de Erros:** O cliente do Trello foi unificado em uma função utilitária com blocos `try/except` para dar respostas limpas caso a API falhe, sem derrubar o agente.

---

## 🛠️ Tecnologias
- **Google ADK (Agent Development Kit)**
- **Google Gemini 2.0 Flash** (via Google AI Studio)
- **py-trello** (API oficial do Trello)
- **Python 3.10+**
- **GitHub** (Versionamento e documentação)

---

## 💡 Reflexão Final
Na era da Inteligência Artificial, o valor não está em decorar linhas de código, mas em saber articular o problema, entender a arquitetura das ferramentas e orquestrar agentes que geram resultados concretos.

---
**Autor:** Hamilton Castro  
*Estudante de Produção Criativa com IA — Estácio*
