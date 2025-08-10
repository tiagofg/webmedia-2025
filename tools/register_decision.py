from autogen.agentchat.group import AgentTarget, ContextVariables, ReplyResult, TerminateTarget

from agents import rewriter

def register_decision(decision: str, justification: str, context_variables: ContextVariables) -> ReplyResult:
    """
    Register the decision and justification in the context variables, and handle the decision accordingly.
    If the decision is 'ANSWER_REVISED', set the final answer to the revised answer and terminate the process.
    If the decision is 'REWRITE', set the original answer and scores, and hand over to the Rewriter to write a new answer.
    If the decision is 'DO_NOT_ANSWER', set the final answer to 'DO_NOT_ANSWER' and terminate the process.
    """
    context_variables["decision"] = decision
    context_variables["decision_justification"] = justification

    if decision == "ANSWER_REVISED":
        context_variables["final_answer"] = context_variables["revised_answer"]

        return ReplyResult(
            context_variables=context_variables,
            target=TerminateTarget(),
            message="The decision is 'ANSWER_REVISED', terminating the process.",
        )
    elif decision == "REWRITE":
        context_variables["original_answer"] = context_variables["revised_answer"]
        context_variables["original_answer_semantic_score"] = context_variables["revised_answer_semantic_score"]
        context_variables["original_answer_justification_semantic"] = context_variables["revised_answer_justification_semantic"]
        context_variables["original_answer_contextual_score"] = context_variables["revised_answer_contextual_score"]
        context_variables["original_answer_justification_contextual"] = context_variables["revised_answer_justification_contextual"]
        context_variables["original_score"] = context_variables["new_score"]
        context_variables["revised_answer"] = None
        context_variables["revised_answer_semantic_score"] = None
        context_variables["revised_answer_justification_semantic"] = None
        context_variables["revised_answer_contextual_score"] = None
        context_variables["revised_answer_justification_contextual"] = None
        context_variables["new_score"] = None

        return ReplyResult(
            context_variables=context_variables,
            target=AgentTarget(rewriter),
            message="The decision is 'REWRITE', handing over to the Rewriter to write a new answer.",
        )

    context_variables["final_answer"] = "DO_NOT_ANSWER"

    return ReplyResult(
        context_variables=context_variables,
        target=TerminateTarget(),
        message="The decision is 'DO_NOT_ANSWER', terminating the process.",
    )