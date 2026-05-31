from graph.neo4j_client import driver

def get_experts(system_name):
    query = """
    MATCH (p:Person)-[:WORKS_ON]->(s:System)
    WHERE s.name = $system_name
    RETURN p.name AS name,
           p.commits AS commits,
           p.incidents AS incidents
    ORDER BY p.commits DESC
    """

    with driver.session() as session:
        result = session.run(query, system_name=system_name)
        return [record.data() for record in result]