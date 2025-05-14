from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, QThreadPool
from functools import partial
from backend import fetch_game_time
import time

__all__ = ['GameManager']

class WorkerSignals(QObject):
    finished = pyqtSignal(object)

class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.is_running = True

    def run(self):
        try:
            if self.is_running:
                result = self.fn(*self.args, **self.kwargs)
                self.signals.finished.emit(result)
        except Exception as e:
            print(f"Worker error: {e}")
        finally:
            self.is_running = False

class GameManager:
    def __init__(self, parent):
        self.parent = parent
        self.game_times_cache = {}
        self.active_workers = []
        self.started_image_queries = set()
        self.threadpool = QThreadPool.globalInstance()
        self.threadpool.setMaxThreadCount(8)  # Increase thread count for better performance

    def add_worker(self, worker):
        if not hasattr(worker, 'is_running'):
            worker.is_running = True
        self.active_workers.append(worker)
        worker.signals.finished.connect(lambda result: self.on_worker_finished(worker, result))

    def on_worker_finished(self, worker, result):
        if worker in self.active_workers:
            worker.is_running = False
            try:
                worker.signals.finished.disconnect()
            except (TypeError, RuntimeError):
                pass
            self.active_workers.remove(worker)

    def start_game_time_queries(self):
        # Batch process tags in groups of 10
        batch_size = 10
        for i in range(0, len(self.parent.all_tags), batch_size):
            batch = self.parent.all_tags[i:i + batch_size]
            for tag in batch:
                alias = tag["alias"]
                if alias not in self.game_times_cache:
                    worker = Worker(fetch_game_time, alias)
                    worker.signals.finished.connect(lambda result, a=alias: self.handle_game_time_update(a, result))
                    self.add_worker(worker)
                    self.threadpool.start(worker)
            # Small delay between batches to prevent overload
            time.sleep(0.1)

    def handle_game_time_update(self, alias, time_info):
        if isinstance(time_info, tuple):
            time_info = time_info[1] if len(time_info) > 1 else "N/A"
        self.game_times_cache[alias] = time_info
        
        # Use a copy of buttons to avoid modification during iteration
        buttons_to_update = []
        for docker_name, buttons in self.parent.tag_buttons.items():
            for button in buttons:
                try:
                    if button.tag_info["alias"] == alias:
                        buttons_to_update.append(button)
                except (RuntimeError, AttributeError):
                    # Button was deleted, skip it
                    continue

        for button in buttons_to_update:
            try:
                if button.parent():  # Check if button still exists
                    lines = button.text().splitlines()
                    if len(lines) >= 3:
                        lines[2] = f"Approx Time: {time_info}"
                    else:
                        lines.append(f"Approx Time: {time_info}")
                    button.setText("\n".join(lines))
            except (RuntimeError, AttributeError):
                # Button was deleted while we were processing, skip it
                continue

    def cleanup_workers(self):
        # Stop all workers immediately
        for worker in self.active_workers[:]:
            worker.is_running = False
            try:
                worker.signals.finished.disconnect()
            except (TypeError, RuntimeError):
                pass
            self.active_workers.remove(worker)
        
        # Wait for threadpool to finish with timeout
        self.threadpool.clear()
        if not self.threadpool.waitForDone(1000):  # 1 second timeout
            print("Warning: Some workers did not finish cleanly")

    def sort_tags_by_time(self, descending=True):
        def parse_time(time_str):
            try:
                time_str = time_str.lower().replace("approx time: ", "").replace("hours", "").strip()
                if "-" in time_str or "–" in time_str:
                    time_str = time_str.replace("–", "-").split("-")[1].strip()
                return float(time_str)
            except:
                return 0.0
        self.parent.all_tags.sort(key=lambda x: parse_time(x.get("approx_time", "0")), reverse=descending)
        self.parent.create_tag_buttons()

    def filter_buttons(self, text):
        for button in self.parent.buttons:
            if button.parent():
                button.setVisible(text.lower() in button.tag_info["alias"].lower())
