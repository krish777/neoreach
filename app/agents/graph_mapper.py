from crewai import Agent
from app.core.neo4j import Neo4jConnector
from typing import Dict

class GraphMapper:
    def __init__(self):
        self.db = Neo4jConnector()
        self.agent = Agent(
            role="Organizational Graph Architect",
            goal="Maintain accurate executive relationships in Neo4j",
            backstory=(
                "Data scientist with a passion for transforming messy organizational data "
                "into clear, actionable relationship graphs"
            ),
            verbose=True
        )

    def update_graph(self, change: Dict) -> str:
        """Thread-safe Neo4j update"""
        query = """
        MERGE (p:Person {name: $name})
        ON CREATE SET p.id = apoc.create.uuid()
        MERGE (c:Company {name: $company})
        MERGE (r:Role {title: $title, company: $company})
        CREATE (p)-[rel:APPOINTED {
            date: date(),
            source: $source,
            confidence: $confidence
        }]->(r)
        CREATE (r)-[:AFFILIATED_WITH]->(c)
        RETURN rel
        """
        params = {
            "name": change["name"],
            "title": change["new_title"],
            "company": change["company"],
            "source": change.get("source", "unknown"),
            "confidence": change.get("confidence_score", 0.8)
        }
        result = self.db.execute(query, params)
        return result[0]["rel"].element_id if result else None