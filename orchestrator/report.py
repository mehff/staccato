import os
import json
import xml.etree.ElementTree as ET
from datetime import datetime

def export_junit(task_id, status, log):
    testsuite = ET.Element("testsuite", name=task_id)
    testcase = ET.SubElement(testsuite, "testcase", name=task_id)
    
    if status.lower() != "success":
        failure = ET.SubElement(testcase, "failure", message="Task failed")
        failure.text = log

    tree = ET.ElementTree(testsuite)
    os.makedirs("reports", exist_ok=True)
    tree.write(f"reports/{task_id}.xml", encoding="utf-8", xml_declaration=True)

def export_allure(task_id, status, log):
    start_time = int(datetime.now().timestamp() * 1000)
    stop_time = start_time + 1000

    report = {
        "uuid": task_id,
        "status": status.lower(),
        "name": task_id,
        "start": start_time,
        "stop": stop_time,
        "steps": [
            {
                "name": "Task Execution",
                "status": status.lower(),
                "start": start_time,
                "stop": stop_time,
                "attachments": [
                    {
                        "name": "Execution Log",
                        "source": f"{task_id}.log",
                        "type": "text/plain"
                    }
                ]
            }
        ]
    }

    os.makedirs("allure-results", exist_ok=True)
    with open(f"allure-results/{task_id}-result.json", "w") as f:
        json.dump(report, f, indent=2)

    # Write log separately
    with open(f"allure-results/{task_id}.log", "w") as log_file:
        log_file.write(log)
