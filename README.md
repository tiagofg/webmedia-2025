# Multi-Agent LLM Approach for Moderating E-Commerce Customer Service Responses

This repository is a research companion associated with WebMedia 2025. It presents the agent prompts and context-update tools for a multi-agent workflow that reviews and, when needed, rewrites customer-service answers in Portuguese or Spanish.

The repository contains the workflow's components rather than a complete application: there is no runner, dependency manifest, API, dataset, automated test suite, or CI configuration here.

## Workflow

The intended control flow is encoded by the return targets in the tools:

1. The semantic reviewer scores how directly and clearly an answer addresses the question on a 0–5 scale.
2. The contextual reviewer scores consistency with the supplied context and metadata on a 0–5 scale and adds the two scores.
3. An original total above 8 terminates the flow. Otherwise, the suggester records concrete improvements and hands off to the rewriter.
4. The rewriter creates a candidate answer or returns `CANNOT REWRITE`, which terminates with `DO_NOT_ANSWER`.
5. A revised answer is reviewed again. The decider can accept it, request another rewrite, or reject it.

The decider's prompt instructs it to reject an answer after two unsuccessful revisions. That constraint is prompt guidance; the tool functions record and route the decision but do not independently enforce the revision limit.

## Agents

| Agent | Responsibility |
| --- | --- |
| [Semantic reviewer](agents/semantic_reviewer.py) | Evaluates relevance, completeness, language, and clarity |
| [Contextual reviewer](agents/contextual_reviewer.py) | Checks claims against context and metadata and calculates a combined score |
| [Suggester](agents/suggester.py) | Turns review findings into revision guidance |
| [Rewriter](agents/rewriter.py) | Produces a revised answer in the question's language |
| [Decider](agents/decider.py) | Chooses `ANSWER_REVISED`, `REWRITE`, or `DO_NOT_ANSWER` |

All five agents are configured for `qwen3:8b` through Ollama's OpenAI-compatible endpoint at `http://localhost:11434/v1`, with temperature `0.0`.

## Tools

| Tool | State transition |
| --- | --- |
| [`register_semantic_score`](tools/register_semantic_score.py) | Stores the original or revised semantic score, then routes to the contextual reviewer |
| [`register_contextual_score`](tools/register_contextual_score.py) | Stores the contextual score, calculates the total, then terminates or routes to the suggester/decider |
| [`register_suggestions`](tools/register_suggestions.py) | Stores improvement guidance, then routes to the rewriter |
| [`register_revised_answer`](tools/register_revised_answer.py) | Stores a candidate, increments the revision count, then terminates or routes to semantic review |
| [`register_decision`](tools/register_decision.py) | Accepts, rejects, or promotes the candidate into another rewrite round |

The modules use cross-package imports such as `from agents import ...` and `from tools import ...`, but the tree does not include package initializer files that re-export those names. In particular, several agent modules import a `register_*` name from `tools` rather than importing the function from its module, unlike `semantic_reviewer.py`. An integrating runner may need to make those imports resolve to callables. It must also initialize `ContextVariables` with every field the tools read, construct the AG2 group pattern, supply an initial message, and ensure the repository root is importable. Those wiring pieces are outside this repository.

## Related implementation

The separate [`answer_reviewer`](https://github.com/tiagofg/answer_reviewer) repository contains FastAPI experiments around related answer-review workflows. It is a separate codebase and is not required by these modules.
