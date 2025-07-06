
import grpc
import time
import threading
from datetime import datetime

from musician_service_pb2 import ControlMessage, Ping
from musician_service_pb2_grpc import MusicianServiceServicer
from orchestrator.database import SessionLocal, Musician
from orchestrator.report import export_junit, export_allure

ping_trackers = {}

class OrchestratorServicer(MusicianServiceServicer):
    def Connect(self, request_iterator, context):
        peer = context.peer()
        db = SessionLocal()
        musician = db.query(Musician).get(peer)
        if not musician:
            musician = Musician(id=peer, hostname="unknown", ip="unknown")
        musician.last_seen = datetime.utcnow()
        musician.offline = False
        db.add(musician)
        db.commit()

        ping_trackers[peer] = {"last_sent": None, "waiting": False, "start_time": None}

        def handle_requests():
            for msg in request_iterator:
                if msg.HasField("registration"):
                    musician.hostname = msg.registration.hostname
                    musician.ip = msg.registration.ip
                    musician.last_seen = datetime.utcnow()
                    musician.offline = False
                    db.add(musician)
                    db.commit()

                elif msg.HasField("pong"):
                    now = datetime.utcnow()
                    if ping_trackers[peer]["start_time"]:
                        rtt = (now - ping_trackers[peer]["start_time"]).total_seconds()
                        if not musician.avg_latency:
                            musician.avg_latency = rtt
                        else:
                            musician.avg_latency = (musician.avg_latency + rtt) / 2
                        musician.last_seen = now
                        musician.offline = False
                        db.commit()
                        ping_trackers[peer]["waiting"] = False

                elif msg.HasField("result"):
                    print(f"Received result from {peer}")
                    export_junit(msg.result.id, msg.result.status, msg.result.log)
                    export_allure(msg.result.id, msg.result.status, msg.result.log)
                    musician.locked = False
                    musician.current_task = None
                    db.commit()

            db.close()

        threading.Thread(target=handle_requests, daemon=True).start()

        while True:
            now = datetime.utcnow()
            tracker = ping_trackers[peer]

            if tracker["waiting"]:
                elapsed = (now - tracker["start_time"]).total_seconds()
                timeout_threshold = (musician.avg_latency or 1) * 5
                if elapsed > timeout_threshold:
                    print(f"[WARN] Musician {peer} marked offline due to ping timeout.")
                    musician.last_seen = None
                    musician.offline = True
                    db.commit()
                    tracker["waiting"] = False

            tracker["start_time"] = now
            tracker["waiting"] = True
            yield ControlMessage(ping=Ping(id="ping123", timestamp=int(now.timestamp() * 1000)))
            time.sleep(30)