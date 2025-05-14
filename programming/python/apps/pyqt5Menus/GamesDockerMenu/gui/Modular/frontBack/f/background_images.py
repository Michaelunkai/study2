from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QRunnable, pyqtSignal, QObject, QBuffer, QIODevice, pyqtSlot, Qt
from backend import fetch_image
import base64

class WorkerSignals(QObject):
    finished = pyqtSignal(object)

class ImageWorker(QRunnable):
    def __init__(self, query, button):
        super().__init__()
        self.query = query
        self.button = button
        self.signals = WorkerSignals()
        self.is_running = True
        self.setAutoDelete(True)  # Allow Qt to clean up the worker

    @pyqtSlot()
    def run(self):
        try:
            if not self.is_running:
                return
                
            if not self.button or self.button.isHidden() or not self.button.parent():
                return
                
            result = fetch_image(self.query)
            
            if not self.is_running:
                return
                
            self.signals.finished.emit(result)
        except Exception as e:
            print(f"ImageWorker error: {e}")
        finally:
            self.is_running = False

class BackgroundImages:
    def __init__(self, parent):
        self.parent = parent
        self.image_cache = {}

    def apply_background(self, app):
        app.setStyleSheet("""
            QWidget {
                background-color: transparent;
                color: white;
            }
            QMenu, QInputDialog, QMessageBox {
                background-color: transparent;
                color: white;
            }
        """)

    def start_image_worker(self, alias, button):
        worker = ImageWorker(alias, button)
        worker.signals.finished.connect(lambda result: self.handle_image_update(alias, button, result))
        self.parent.add_worker(worker)
        from PyQt5.QtCore import QThreadPool
        QThreadPool.globalInstance().start(worker)

    def handle_image_update(self, alias, button, result):
        if not button or not button.parent():
            return
        image_data = result[1] if isinstance(result, tuple) else result
        if image_data:
            image = QImage()
            image.loadFromData(image_data)
            if not image.isNull():
                scaled_image = image.scaled(button.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
                pixmap = QPixmap.fromImage(scaled_image)
                self.image_cache[alias] = pixmap
                buffer = QBuffer()
                buffer.open(QIODevice.WriteOnly)
                pixmap.save(buffer, "PNG")
                b64_data = base64.b64encode(buffer.data()).decode('utf-8')
                buffer.close()
                base_style = button.styleSheet()
                bg_style = f"background-image: url(data:image/png;base64,{b64_data}); background-position: center; background-repeat: no-repeat;"
                button.setStyleSheet(base_style + bg_style)
        else:
            button.setStyleSheet(button.styleSheet() + "background-image: none;")