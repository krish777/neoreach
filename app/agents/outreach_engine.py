from crewai import Agent
from app.core.llm.api import MistralAPI
from app.core.llm.prompts import get_prompt
from typing import Dict

class OutreachEngine:
    def __init__(self):
        self.llm = MistralAPI()
        self.agent = Agent(
            role="Executive Outreach Strategist",
            goal="Create personalized communications for new executives",
            backstory=(
                "Former management consultant who crafted C-level outreach for Fortune 500 clients, "
                "now automating high-touch communication at scale"
            ),
            verbose=True
        )

    def generate_outreach(self, change: Dict) -> Dict:
        """Create email and call script"""
        return {
            "email": self._generate_email(change),
            "call_script": self._generate_call_script(change),
            "meta": change
        }

    def _generate_email(self, change: Dict) -> str:
        """Generate email using template"""
        return get_prompt(
            "initial_contact",
            {
                "name": change["name"],
                "title": change["new_title"],
                "company": change["company"],
                "previous_company": change.get("previous_company", ""),
                "industry": "technology",  # Dynamically set this
                "tone": "professional"
            }
        )

    def _generate_call_script(self, change: Dict) -> str:
        """Generate conversation flow"""
        return self.llm.generate(
            f"Create a 5-bullet call script for {change['name']}, "
            f"new {change['new_title']} at {change['company']}. "
            "Focus on their experience at "
            f"{change.get('previous_company', 'previous roles')}"
        )