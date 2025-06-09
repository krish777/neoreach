OUTREACH_PROMPTS = {
    "initial_contact": """Compose a 200-word email to {name}, the new {title} at {company}.
Key Points:
- Reference their move from {previous_company}
- Highlight relevant case study
- Suggest intro call

Tone: {tone}"""
}

def get_prompt(prompt_name: str, variables: dict) -> str:
    return OUTREACH_PROMPTS[prompt_name].format(**variables)