import streamlit as st
from crewai import Crew, Process, Task
from agents.change_detector import ChangeDetector
from agents.graph_mapper import GraphMapper
from agents.outreach_engine import OutreachEngine
from ui.approval_ui import role_change_approval, email_approval
from ui.visualizer import Neo4jVisualizer
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()
st.set_page_config(layout="wide")

def _create_tasks(changes, mapper, outreach):
    """Generate parallel tasks"""
    tasks = []
    for change in changes:
        tasks.extend([
            Task(
                description=f"Update graph for {change['name']}",
                agent=mapper.agent,
                async_execution=True,
                action=lambda c=change: mapper.update_graph(c)
            ),
            Task(
                description=f"Create outreach for {change['name']}",
                agent=outreach.agent,
                async_execution=True,
                action=lambda c=change: outreach.generate_outreach(c)
            )
        ])
    return tasks

def main():
    # Initialize
    detector = ChangeDetector()
    mapper = GraphMapper()
    outreach = OutreachEngine()
    viz = Neo4jVisualizer(driver=mapper.db.driver)

    # UI Header
    st.title("NeoReach Executive Tracker")
    tab1, tab2 = st.tabs(["Pipeline", "Relationship Visualizer"])

    with tab1:
        # Step 1: Detect Role Changes
        with st.expander("1. Detect Role Changes", expanded=True):
            if st.button("Scan Sources"):
                try:
                    with st.spinner("Analyzing..."):
                        changes = detector.detect_changes(
                            ["linkedin", "news", "company_announcements"]
                        )
                        st.session_state.changes = changes
                        st.success("Changes detected!")
                        st.write("Detected Changes:", st.session_state.changes)  # DEBUG LINE
                except Exception as e:
                    st.error(f"Error detecting changes: {e}")

        # Step 2: Human Validation (NO outer expander here!)
        if st.session_state.get("changes"):
            approved_changes = []
            for change in st.session_state.changes:
                approved = role_change_approval(change)
                if approved.get("status") in ("approved", "modified"):
                    approved_changes.append(approved)
            st.session_state.approved_changes = approved_changes

        # Step 3: Execute Workflows
        if st.session_state.get("approved_changes"):
            with st.expander("3. Execute Workflows"):
                if st.button("Run Parallel Processing"):
                    try:
                        tasks = _create_tasks(st.session_state.approved_changes, mapper, outreach)
                        crew = Crew(
                            agents=[mapper.agent, outreach.agent],
                            tasks=tasks,
                            process=Process.parallel
                        )
                        results = crew.kickoff()
                        st.session_state.results = results
                        st.success("Workflows completed!")
                    except Exception as e:
                        st.error(f"Error running workflows: {e}")

        # Step 4: Finalize Outreach
        if st.session_state.get("results"):
            with st.expander("4. Finalize Outreach"):
                for result in st.session_state.results:
                    if isinstance(result, dict):
                        email_approval(result)

    with tab2:
        # Visualization Tab
        if hasattr(mapper.db, 'driver'):
            try:
                companies = mapper.db.execute("MATCH (c:Company) RETURN c.name")
                selected = st.selectbox(
                    "Select Company",
                    options=[c["c.name"] for c in companies]
                )
                viz.render_org_chart(selected)
            except Exception as e:
                st.error(f"Error loading visualizer: {e}")

if __name__ == "__main__":
    main()