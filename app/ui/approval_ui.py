import streamlit as st
from typing import Dict, Any
import ast

def role_change_approval(change: dict) -> dict:
    key_prefix = change.get("name", "unknown").replace(" ", "_")

    st.markdown(f"### 🧑‍💼 New Role: {change['name']}")
    # Removed 'key' from expander to fix the TypeError
    with st.expander("Details"):
        st.json(change, expanded=False)

    approve_key = f"approve_{key_prefix}"
    edit_key = f"edit_{key_prefix}"

    col1, col2 = st.columns(2)

    result = {"status": "pending"}

    with col1:
        if st.button("✅ Approve", key=approve_key):
            result = {"status": "approved", **change}

    with col2:
        edited = st.text_area("Edit Details (Python dict format)", value=str(change), key=f"editbox_{key_prefix}")
        if st.button("✏️ Submit Edits", key=edit_key):
            try:
                parsed = ast.literal_eval(edited)
                if isinstance(parsed, dict):
                    result = {"status": "modified", **parsed}
                else:
                    st.error("Invalid format: not a dictionary.")
            except Exception as e:
                st.error(f"Error parsing edits: {e}")

    return result


def email_approval(package: Dict[str, Any]) -> Dict[str, Any]:
    st.subheader(f"✉️ Outreach for {package['meta']['name']}")

    tabs = st.tabs(["Email", "Call Script"])
    edited_email = package.get("email", "")
    edited_script = package.get("call_script", "")

    with tabs[0]:
        edited_email = st.text_area(
            "Edit Email", 
            value=package.get("email", ""), 
            height=300, 
            key=f"email_{package['meta']['name']}"
        )
    with tabs[1]:
        edited_script = st.text_area(
            "Edit Call Script", 
            value=package.get("call_script", ""), 
            height=200, 
            key=f"script_{package['meta']['name']}"
        )

    if st.button("✅ Approve Package", key=f"approve_pkg_{package['meta']['name']}"):
        return {
            **package,
            "email": edited_email,
            "call_script": edited_script,
            "status": "approved"
        }

    return {"status": "pending"}