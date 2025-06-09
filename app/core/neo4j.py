from neo4j import GraphDatabase
import os

class Neo4jConnector:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URL"),
            auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
        )
    
    def test_connection(self):
        with self.driver.session() as session:
            return session.run("RETURN 1 AS test").single()[0] == 1
    
    def execute(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            # Return list of records, or you can customize what to return
            return [record for record in result]
    
    def close(self):
        self.driver.close()