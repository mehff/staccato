import grpc
from musician_service_pb2 import ControlMessage, Task
from musician_service_pb2_grpc import MusicianServiceStub

# Simulated connection pool (will change to stream)
musician_connections = {}

def register_connection(musician_id, stream_stub):
    musician_connections[musician_id] = stream_stub

def send_task_to_musician(musician_id, task_data):
    if musician_id not in musician_connections:
        print(f"[ERROR] No connection to musician {musician_id}")
        return

    stub = musician_connections[musician_id]
    task = Task(id=task_data["id"], csv_data=task_data["csv_data"])
    msg = ControlMessage(task=task)

    try:
        stub.Connect(iter([msg]))
        print(f"[INFO] Task {task_data['id']} sent to musician {musician_id}")
    except grpc.RpcError as e:
        print(f"[ERROR] Failed to send task to {musician_id}: {e}")
