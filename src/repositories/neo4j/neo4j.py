from neo4j import GraphDatabase

neo4j = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "admin123"))

# MATCH (n) OPTIONAL MATCH (n)-[r]->(m) RETURN n, r, m
