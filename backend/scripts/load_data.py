import json
from graph.neo4j_client import driver


def load_employees():
    with open("data/employees.json", "r", encoding="utf-8") as f:
        employees = json.load(f)

    with driver.session() as session:
        for emp in employees:
            print(emp)


if __name__ == "__main__":
    load_employees()