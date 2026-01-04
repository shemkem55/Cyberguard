import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

class Neo4jService:
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "password")
        self._driver = None
        
        if self.uri and self.password:
            try:
                self._driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            except Exception as e:
                print(f"Warning: Could not connect to Neo4j: {e}")

    def close(self):
        if self._driver:
            self._driver.close()

    def create_vulnerability_relationship(self, asset_name, cve_id, relationship_type="AFFECTS"):
        if not self._driver:
            return
            
        with self._driver.session() as session:
            session.execute_write(self._create_rel, asset_name, cve_id, relationship_type)

    @staticmethod
    def _create_rel(tx, asset_name, cve_id, relationship_type):
        query = (
            f"MERGE (a:Asset {{name: $asset_name}}) "
            f"MERGE (v:Vulnerability {{cve_id: $cve_id}}) "
            f"MERGE (a)-[r:{relationship_type}]->(v)"
        )
        tx.run(query, asset_name=asset_name, cve_id=cve_id)

    def get_asset_context(self, asset_name):
        """Retrieve graph context for RAG"""
        if not self._driver:
            return []
            
        with self._driver.session() as session:
            return session.execute_read(self._find_context, asset_name)
            
    @staticmethod
    def _find_context(tx, asset_name):
        query = (
            "MATCH (a:Asset {name: $asset_name})-[r]-(n) "
            "RETURN type(r) as rel, labels(n) as labels, n.name as name, n.cve_id as cve_id LIMIT 10"
        )
        result = tx.run(query, asset_name=asset_name)
        return [record.data() for record in result]

neo4j_service = Neo4jService()
