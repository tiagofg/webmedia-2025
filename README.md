# Moderando Conteúdo Textual via Sistema Multiagentes com Modelos de Linguagem

Esse repositório tem como objetivo exibir os agentes e tools criados para o artigo submetido para a WebMedia 2025

## Agentes

Foram criados 5 agentes, distribuídos na seguinte estrutura:

1. [Revisor Semântico](agents/semantic_reviewer.py)
2. [Revisor Contextual](agents/contextual_reviewer.py)
3. [Recomendador de melhorias](agents/suggester.py)
4. [Reescritor](agents/rewriter.py)
5. [Decisor](agents/decider.py)

Cada um deles possui instruções claras em inglês sobre o papel deles, as informações que eles terão disponíveis para as tomadas de decisão e a tool que deve ser chamada para registrar as respostas deles no contexto.

## Tools

Todos os agentes tem funções associadas a eles que devem ser chamadas após cada execução, elas estão distribuídas da seguinte maneira:

1. [register_semantic_score](tools/register_semantic_score.py)
2. [register_contextual_score](tools/register_contextual_score.py)
3. [register_suggestions](tools/register_suggestions.py)
4. [register_revised_answer](tools/register_revised_answer.py)
5. [register_decision](tools/register_decision.py)

Através delas, os agentes registram no contexto suas resposta, realizam os processamentos necessários e decidem qual agente deve ser chamado na sequência.
