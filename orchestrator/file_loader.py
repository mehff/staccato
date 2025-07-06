import yaml
import csv

def load_csv(file_path):
    with open(file_path, newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return [
        {
            "id": f"task_{i}",
            "csv_data": "\n".join([",".join(reader.fieldnames)] + [",".join(row[field] for field in reader.fieldnames) for row in [rows[i]]])
        }
        for i in range(len(rows))
    ]

def load_yaml(file_path):
    with open(file_path) as f:
        yaml_data = yaml.safe_load(f)

    tasks = []
    for i, entry in enumerate(yaml_data):
        fields = entry.keys()
        values = entry.values()
        csv_data = ",".join(fields) + "\n" + ",".join(str(v) for v in values)
        tasks.append({
            "id": f"task_{i}",
            "csv_data": csv_data
        })
    return tasks

def load_tasks(path):
    if path.endswith(".csv"):
        return load_csv(path)
    elif path.endswith(".yaml") or path.endswith(".yml"):
        return load_yaml(path)
    else:
        raise ValueError("Unsupported file format: must be .csv or .yaml")
