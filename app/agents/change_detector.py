import streamlit as st
from typing import List, Dict
import json

# Dummy MistralAPI mock for example
class MistralAPI:
    def generate(self, prompt: str) -> str:
        # This should call your real LLM; here we simulate a JSON response
        sample_response = json.dumps([
            {
                "name": "Alice Johnson",
                "new_title": "CEO",
                "company": "Acme Corp",
                "previous_role": "COO",
                "confidence_score": 0.95,
                "source": "https://news.example.com/article1"
            },
            {
                "name": "Bob Smith",
                "new_title": "CTO",
                "company": "Tech Solutions",
                "previous_role": None,
                "confidence_score": 0.87,
                "source": "https://news.example.com/article2"
            }
        ])
        return sample_response


class ChangeDetector:
    def __init__(self):
        self.llm = MistralAPI()
        # The Agent is not used in this example to keep it simple.
        # Add it if you want your agent-based prompt workflow.

    def detect_changes(self, sources: List[str]) -> List[Dict]:
        prompt = f"""
        Analyze these sources for executive role changes:
        {json.dumps(sources, indent=2)}
        
        Extract JSON with:
        - name (string)
        - new_title (string)
        - company (string)
        - previous_role (string or null)
        - confidence_score (float 0-1)
        - source (string)
        """
        response = self.llm.generate(prompt)
        print("DEBUG: LLM response:", repr(response))
        return self._parse_response(response)

    def _parse_response(self, raw: str) -> List[Dict]:
        raw = raw.strip()
        print("LLM RAW RESPONSE:", repr(raw))
        if not raw:
            print("Empty response from LLM")
            return []
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            print("JSON PARSE ERROR:", e)
            return []

# UI for approving or rejecting detected changes, no nested expanders
def role_change_approval(change: dict) -> dict:
    st.subheader(f"New Role: {change['name']}")
    st.json(change, expanded=False)

    approved = {}
    if st.button("✅ Approve", key=f"approve_{change['name']}"):
        approved["status"] = "approved"
    elif st.button("❌ Reject", key=f"reject_{change['name']}"):
        approved["status"] = "rejected"
    return approved


def main():
    st.title("Executive Leadership Change Detector")

    # Example sources - you can replace this with user input
    sources = [
        "https://news.example.com/article1",
        "https://news.example.com/article2"
    ]

    if st.button("Detect Changes"):
        detector = ChangeDetector()
        changes = detector.detect_changes(sources)
        st.session_state.changes = changes
        st.success(f"Detected {len(changes)} changes.")

    if "changes" in st.session_state and st.session_state.changes:
        with st.expander("2. Validate Changes"):
            approved_changes = []
            for change in st.session_state.changes:
                result = role_change_approval(change)
                if result.get("status") == "approved":
                    approved_changes.append(change)

            st.write(f"✅ Approved changes count: {len(approved_changes)}")
            st.session_state.approved_changes = approved_changes


if __name__ == "__main__":
    main()