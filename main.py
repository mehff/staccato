# main.py
import threading
from orchestrator.tls_server_setup import serve_with_tls
from orchestrator.task_scheduler import TaskScheduler
from orchestrator.file_loader import load_tasks

def main():
    task_scheduler = TaskScheduler()
    task_scheduler.start()

    # Load example tasks
    tasks = load_tasks("examples/tasks/basic_ping.yaml")
    for task in tasks:
        task_scheduler.add_task(task)

    # Start gRPC server in background thread
    grpc_thread = threading.Thread(target=serve_with_tls, daemon=True)
    grpc_thread.start()

    print("✅ Orchestrator started. Awaiting musicians and tasks...")
    threading.Event().wait()  # Keeps main thread alive

if __name__ == "__main__":
    main()
