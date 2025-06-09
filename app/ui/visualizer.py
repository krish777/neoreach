import streamlit as st
from neo4j import GraphDatabase
from pyvis.network import Network
import pandas as pd

class Neo4jVisualizer:
    def __init__(self, driver):
        self.driver = driver

    def render_org_chart(self, company: str, height: int = 600):
        """Interactive org chart using Pyvis"""
        query = """
        MATCH path=(c:Company {name: $company})<-[:AFFILIATED_WITH]-(r:Role)<-[:APPOINTED]-(p:Person)
        RETURN p.name as person, r.title as role, c.name as company
        """
        with self.driver.session() as session:
            results = session.run(query, {"company": company})
            data = pd.DataFrame([dict(r) for r in results])

        if data.empty:
            st.warning(f"No data found for {company}")
            return

        net = Network(height=f"{height}px", notebook=True)
        
        # Add nodes
        for _, row in data.iterrows():
            net.add_node(row['person'], label=row['person'], group=row['role'])
            net.add_node(row['company'], label=row['company'], group="Company")
            
            # Add edges
            net.add_edge(row['person'], row['company'], 
                        label=row['role'], 
                        color="#4581c3")

        # Generate HTML
        net.save_graph("temp.html")
        with open("temp.html", "r") as f:
            html = f.read()
        
        # Render in Streamlit
        st.components.v1.html(html, height=height)

    def show_influence_network(self, person: str):
        """Force-directed graph of relationships"""
        query = """
        MATCH (p:Person {name: $name})-[:APPOINTED]->(r)
        WITH r
        MATCH path=(r)-[rel*1..2]-(other)
        UNWIND rel as r
        RETURN startNode(r).name as source, 
               endNode(r).name as target,
               type(r) as relationship
        """
        with self.driver.session() as session:
            results = session.run(query, {"name": person})
            st.vega_lite_chart({
                "mark": {"type": "arc", "tooltip": True},
                "encoding": {
                    "source": {"field": "source", "type": "nominal"},
                    "target": {"field": "target", "type": "nominal"},
                    "color": {"field": "relationship", "type": "nominal"}
                }
            }, data=list(results))