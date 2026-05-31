from graph.neo4j_client import driver

with driver.session() as session:
    session.run("""
    MERGE (billing:System {name:'Billing Service'})
    MERGE (search:System {name:'Search Service'})

    MERGE (sarah:Person {name:'Sarah Chen'})
    SET sarah.commits=42, sarah.incidents=6

    MERGE (alex:Person {name:'Alex Kumar'})
    SET alex.commits=65, alex.incidents=10

    MERGE (john:Person {name:'John Patel'})
    SET john.commits=15, john.incidents=2

    MERGE (sarah)-[:WORKS_ON]->(billing)
    MERGE (alex)-[:WORKS_ON]->(billing)
    MERGE (john)-[:WORKS_ON]->(search)
    """)