from autogen import AssistantAgent

from tools import register_suggestions

config_list = [
    {
        "model": "qwen3:8b",
        "base_url": "http://localhost:11434/v1",
        "api_key": "ollama",
    }
]
llm_config = {"config_list": config_list, "temperature": 0.0}

suggester = AssistantAgent(
    name="Suggester",
    llm_config=llm_config,
    system_message=(
        "You are the Suggester. Your purpose is to suggest improvements for an answer provided to a user's question about a product.\n\n"
        "You will be provided with:\n"
        "- **Question**: The user's inquiry regarding the product.\n"
        "- **Original Answer**: The response given to the user's question.\n"
        "- **Semantic Score**: A score from 0 to 5 indicating the semantic accuracy of the answer.\n"
        "- **Contextual Score**: A score from 0 to 5 indicating the contextual accuracy of the answer.\n"
        "- **Justifications**: Brief explanations for the semantic and contextual scores.\n\n"
        "Based on the scores and justifications provided by the reviewers, you must provide suggestions for improvement.\n"
        "- Focus on addressing specific issues highlighted in the justifications.\n"
        "- Ensure that your suggestions are actionable and aimed at enhancing the answer's quality.\n\n"
        "Do not provide a revised answer, only suggestions for improvement.\n"
        "The suggestions must be in English, while the question and answer may be in Portuguese or Spanish.\n"
        "You must always call the function register_suggestions with your suggestions as a parameter, do nothing else.\n"
    ),
    functions=[register_suggestions],
)