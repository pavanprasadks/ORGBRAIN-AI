from graph.neo4j_client import driver

with driver.session() as session:
    session.run("""
        MERGE (p:Person {name:'Sarah Chen'})
        SET p.team='Platform',
            p.commits=42,
            p.incidents=6

        MERGE (s:System {name:'Billing Service'})

        MERGE (p)-[:WORKS_ON]->(s)
    """)

print("Seeded successfully!")