import grpc
import time
import threading
import csv
import socket
import queue
from musician_service_pb2 import ControlMessage, Pong, TaskResult, Registration
from musician_service_pb2_grpc import MusicianServiceStub
from actions import ping_test

def execute_task(task):
    reader = csv.DictReader(task.csv_data.splitlines())
    logs = []
    for row in reader:
        if row["ACTION"] == "ping_test":
            result = ping_test.execute(row)
            logs.append(result)
    return "\n".join(logs)

def run_client():
    while True:
        try:
            creds = grpc.ssl_channel_credentials(
                root_certificates=open("certs/ca.crt", "rb").read(),
                private_key=open("certs/client.key", "rb").read(),
                certificate_chain=open("certs/client.crt", "rb").read()
            )
            channel = grpc.secure_channel("localhost:50051", creds)
            stub = MusicianServiceStub(channel)

            # Create a queue for outgoing messages
            outgoing_messages_queue = queue.Queue()

            # Function to generate messages for the gRPC stream
            def generate_outgoing_messages():
                # Send initial registration message
                outgoing_messages_queue.put(ControlMessage(
                    registration=Registration(
                        hostname=socket.gethostname(),
                        ip=socket.gethostbyname(socket.gethostname())
                    )
                ))
                while True:
                    yield outgoing_messages_queue.get()

            # Start the bidirectional stream
            responses = stub.Connect(generate_outgoing_messages())

            # Process incoming messages and send responses
            for msg in responses:
                if msg.HasField("ping"):
                    response = ControlMessage(pong=Pong(id=msg.ping.id, timestamp=int(time.time() * 1000), latency_ms=10))
                    outgoing_messages_queue.put(response) # Put response into the queue
                elif msg.HasField("task"):
                    logs = execute_task(msg.task)
                    response = ControlMessage(result=TaskResult(id=msg.task.id, status="success", log=logs))
                    outgoing_messages_queue.put(response) # Put response into the queue
        except grpc.RpcError as e:
            print(f"[ERROR] Lost connection to orchestrator: {e}. Retrying in 5 seconds...")
            time.sleep(5)
