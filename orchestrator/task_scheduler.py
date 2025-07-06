from queue import Queue
from threading import Thread
import time
from orchestrator.database import get_db, Musician
from orchestrator.orchestrator_client_stub import send_task_to_musician

class TaskScheduler:
    def __init__(self):
        self.task_queue = Queue()

    def add_task(self, task):
        self.task_queue.put(task)

    def start(self):
        Thread(target=self.worker_loop, daemon=True).start()

    def worker_loop(self):
        db_gen = get_db()
        db = next(db_gen)
        try:
            while True:
                task = self.task_queue.get()
                musician = db.query(Musician).filter_by(locked=False).first()
                if musician:
                    musician.locked = True
                    musician.current_task = task["id"]
                    db.commit()
                    send_task_to_musician(musician.id, task)
                else:
                    # Requeue the task if no musician is available
                    self.task_queue.put(task)
                    time.sleep(5)
        finally:
            db_gen.close()
