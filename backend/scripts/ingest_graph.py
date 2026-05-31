import json
import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from graph.neo4j_client import driver


def load_employees():
    with open("data/employees.json", "r", encoding="utf-8") as f:
        employees = json.load(f)

    with driver.session() as session:
        for emp in employees:
            session.run("""
                MERGE (e:Employee {
                    employee_id:$employee_id
                })
                SET e.name=$name,
                    e.role=$role,
                    e.team=$team
            """,
            employee_id=emp["employee_id"],
            name=emp["name"],
            role=emp["role"],
            team=emp["team"])

    print(f"Loaded {len(employees)} employees")


def load_systems():
    with open("data/systems.json", "r", encoding="utf-8") as f:
        systems = json.load(f)

    with driver.session() as session:
        for system in systems:

            session.run("""
                MERGE (s:System {
                    system_id:$system_id
                })
                SET s.name=$name,
                    s.team=$team,
                    s.criticality=$criticality
            """,
            system_id=system["system_id"],
            name=system["name"],
            team=system["team"],
            criticality=system["criticality"])

            session.run("""
                MATCH (e:Employee {
                    employee_id:$owner
                })
                MATCH (s:System {
                    system_id:$system_id
                })
                MERGE (e)-[:OWNS]->(s)
            """,
            owner=system["owner"],
            system_id=system["system_id"])

            session.run("""
                MATCH (e:Employee {
                    employee_id:$backup_owner
                })
                MATCH (s:System {
                    system_id:$system_id
                })
                MERGE (e)-[:BACKUP_OWNER]->(s)
            """,
            backup_owner=system["backup_owner"],
            system_id=system["system_id"])

    print(f"Loaded {len(systems)} systems")



def load_projects():
    with open("data/projects.json", "r", encoding="utf-8") as f:
        projects = json.load(f)

    with driver.session() as session:
        for project in projects:

            session.run("""
                MERGE (p:Project {
                    project_id:$project_id
                })
            """,
            project_id=project["project_id"])

            for system_id in project["systems"]:

                session.run("""
                    MATCH (p:Project {
                        project_id:$project_id
                    })
                    MATCH (s:System {
                        system_id:$system_id
                    })
                    MERGE (p)-[:USES]->(s)
                """,
                project_id=project["project_id"],
                system_id=system_id)

    print(f"✅ Loaded {len(projects)} projects")

def load_incidents():
    with open("data/incidents.json", "r", encoding="utf-8") as f:
        incidents = json.load(f)

    with driver.session() as session:
        for incident in incidents:

            session.run("""
                MERGE (i:Incident {
                    incident_id:$incident_id
                })
                SET i.title=$title,
                    i.affected_system=$affected_system,
                    i.created_at=$created_at
            """,
            incident_id=incident["incident_id"],
            title=incident["title"],
            affected_system=incident["affected_system"],
            created_at=incident["created_at"])

            for responder in incident["responders"]:
                session.run("""
                    MATCH (e:Employee {employee_id:$employee_id})
                    MATCH (i:Incident {incident_id:$incident_id})
                    MERGE (e)-[:RESPONDED_TO]->(i)
                """,
                employee_id=responder,
                incident_id=incident["incident_id"])

    print(f"✅ Loaded {len(incidents)} incidents")


def load_adrs():
    with open("data/adrs.json", "r", encoding="utf-8") as f:
        adrs = json.load(f)

    with driver.session() as session:
        for adr in adrs:

            session.run("""
                MERGE (a:ADR {
                    adr_id:$adr_id
                })
                SET a.title=$title,
                    a.date=$date,
                    a.outcome=$outcome
            """,
            adr_id=adr["adr_id"],
            title=adr["title"],
            date=adr["date"],
            outcome=adr["outcome"])

            for participant in adr["participants"]:
                session.run("""
                    MATCH (e:Employee {employee_id:$employee_id})
                    MATCH (a:ADR {adr_id:$adr_id})
                    MERGE (e)-[:PARTICIPATED_IN]->(a)
                """,
                employee_id=participant,
                adr_id=adr["adr_id"])

    print(f"✅ Loaded {len(adrs)} ADRs")
def load_relationships():
    with open("data/relationships.json", "r", encoding="utf-8") as f:
        relationships = json.load(f)

    with driver.session() as session:

        for rel in relationships:

            source = rel["source"]
            target = rel["target"]
            relationship = rel["relationship"]

            # Employee -> System
            if source.startswith("EMP-") and target.startswith("SYS-"):

                session.run(f"""
                    MATCH (a:Employee {{employee_id:$source}})
                    MATCH (b:System {{system_id:$target}})
                    MERGE (a)-[:{relationship}]->(b)
                """,
                source=source,
                target=target)

            # ADR -> System
            elif source.startswith("ADR-") and target.startswith("SYS-"):

                session.run(f"""
                    MATCH (a:ADR {{adr_id:$source}})
                    MATCH (b:System {{system_id:$target}})
                    MERGE (a)-[:{relationship}]->(b)
                """,
                source=source,
                target=target)

            # Employee -> Incident
            elif source.startswith("EMP-") and target.startswith("INC-"):

                session.run(f"""
                    MATCH (a:Employee {{employee_id:$source}})
                    MATCH (b:Incident {{incident_id:$target}})
                    MERGE (a)-[:{relationship}]->(b)
                """,
                source=source,
                target=target)

    print(f"✅ Loaded {len(relationships)} relationships")
def load_jira_tickets():
    with open("data/jira_tickets.json", "r", encoding="utf-8") as f:
        tickets = json.load(f)

    with driver.session() as session:
        for ticket in tickets:

            session.run("""
                MERGE (t:JiraTicket {
                    ticket_id:$ticket_id
                })
                SET t.title=$title,
                    t.priority=$priority
            """,
            ticket_id=ticket["ticket_id"],
            title=ticket["title"],
            priority=ticket["priority"])

            session.run("""
                MATCH (e:Employee {
                    employee_id:$employee_id
                })
                MATCH (t:JiraTicket {
                    ticket_id:$ticket_id
                })
                MERGE (e)-[:ASSIGNED_TO]->(t)
            """,
            employee_id=ticket["assignee"],
            ticket_id=ticket["ticket_id"])

    print(f"✅ Loaded {len(tickets)} Jira tickets")

def load_slack_messages():
    with open("data/slack_messages.json", "r", encoding="utf-8") as f:
        messages = json.load(f)

    with driver.session() as session:
        for msg in messages:

            session.run("""
                MERGE (m:SlackMessage {
                    message_id:$message_id
                })
                SET m.channel=$channel,
                    m.timestamp=$timestamp,
                    m.message=$message
            """,
            message_id=msg["message_id"],
            channel=msg["channel"],
            timestamp=msg["timestamp"],
            message=msg["message"])

            session.run("""
                MATCH (e:Employee {
                    employee_id:$employee_id
                })
                MATCH (m:SlackMessage {
                    message_id:$message_id
                })
                MERGE (e)-[:POSTED]->(m)
            """,
            employee_id=msg["employee"],
            message_id=msg["message_id"])

    print(f"✅ Loaded {len(messages)} Slack messages")

def load_github_prs():
    with open("data/github_prs.json", "r", encoding="utf-8") as f:
        prs = json.load(f)

    with driver.session() as session:
        for pr in prs:

            session.run("""
                MERGE (p:PullRequest {
                    pr_id:$pr_id
                })
                SET p.repository=$repository,
                    p.title=$title,
                    p.linked_ticket=$linked_ticket,
                    p.linked_system=$linked_system,
                    p.created_at=$created_at,
                    p.merged_at=$merged_at
            """,
            pr_id=pr["pr_id"],
            repository=pr["repository"],
            title=pr["title"],
            linked_ticket=pr["linked_ticket"],
            linked_system=pr["linked_system"],
            created_at=pr["created_at"],
            merged_at=pr["merged_at"])

            # Author
            session.run("""
                MATCH (e:Employee {employee_id:$employee_id})
                MATCH (p:PullRequest {pr_id:$pr_id})
                MERGE (e)-[:AUTHORED]->(p)
            """,
            employee_id=pr["author"],
            pr_id=pr["pr_id"])

            # Reviewers
            for reviewer in pr["reviewers"]:
                session.run("""
                    MATCH (e:Employee {employee_id:$employee_id})
                    MATCH (p:PullRequest {pr_id:$pr_id})
                    MERGE (e)-[:REVIEWED]->(p)
                """,
                employee_id=reviewer,
                pr_id=pr["pr_id"])

            # System linkage
            session.run("""
                MATCH (p:PullRequest {pr_id:$pr_id})
                MATCH (s:System {system_id:$system_id})
                MERGE (p)-[:MODIFIES]->(s)
            """,
            pr_id=pr["pr_id"],
            system_id=pr["linked_system"])

    print(f"✅ Loaded {len(prs)} GitHub PRs")
if __name__ == "__main__":
    load_employees()
    load_systems()
    load_projects()
    load_incidents()
    load_adrs()
    load_relationships()
    load_jira_tickets()
    load_slack_messages()
    load_github_prs()
    print("✅ Graph ingestion complete")