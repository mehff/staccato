import grpc
from concurrent import futures
from orchestrator.orchestrator_servicer import OrchestratorServicer
from musician_service_pb2_grpc import add_MusicianServiceServicer_to_server

def serve_with_tls():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_MusicianServiceServicer_to_server(OrchestratorServicer(), server)

    with open("certs/server.key", "rb") as f:
        private_key = f.read()
    with open("certs/server.crt", "rb") as f:
        certificate_chain = f.read()
    with open("certs/ca.crt", "rb") as f:
        root_certificates = f.read()

    server_credentials = grpc.ssl_server_credentials(
        [(private_key, certificate_chain)],
        root_certificates=root_certificates,
        require_client_auth=True
    )

    server.add_secure_port("[::]:50051", server_credentials)
    print("Secure gRPC server running on port 50051...")
    server.start()
    server.wait_for_termination()
