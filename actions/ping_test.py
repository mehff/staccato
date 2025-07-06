import subprocess

def execute(row):
    source = row.get("SOURCE")
    destination = row.get("DESTINATION")
    try:
        result = subprocess.run(["ping", "-c", "4", destination], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return f"Ping from {source} to {destination} successful:\n{result.stdout}"
        else:
            return f"Ping from {source} to {destination} failed:\n{result.stderr}"
    except Exception as e:
        return f"Ping from {source} to {destination} encountered an error: {str(e)}"
