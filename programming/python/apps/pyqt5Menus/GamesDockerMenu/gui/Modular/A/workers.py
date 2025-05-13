from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot

class WorkerSignals(QObject):
    finished = pyqtSignal(object)

class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
    @pyqtSlot()
    def run(self):
        result = self.fn(*self.args, **self.kwargs)
        self.signals.finished.emit(result)

class DockerPullWorker(QRunnable):
    def __init__(self, tag):
        super(DockerPullWorker, self).__init__()
        self.tag = tag
    @pyqtSlot()
    def run(self):
        import subprocess
        pull_cmd = f'wsl --distribution ubuntu --user root -- bash -lic "docker pull michadockermisha/backup:\\"{self.tag}\\""'
        try:
            subprocess.run(pull_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=600)
        except subprocess.TimeoutExpired:
            print(f"Timeout pulling image for {self.tag}")
        except Exception as e:
            print(f"Error pulling image for {self.tag}: {e}")

class ImageWorker(QRunnable):
    def __init__(self, query):
        super(ImageWorker, self).__init__()
        self.query = query
        self.signals = WorkerSignals()
    @pyqtSlot()
    def run(self):
        from network_ops import fetch_image
        result = fetch_image(self.query)
        self.signals.finished.emit(result)
