import re
import base64
from datetime import datetime
from PyQt5.QtCore import QBuffer, QIODevice
from PyQt5.QtGui import QImage

# Optional word segmentation
try:
    import wordninja
except ImportError:
    wordninja = None

def normalize_game_title(tag):
    if " " in tag:
        return tag
    if any(c.isupper() for c in tag[1:]):
        return re.sub(r'(?<!^)(?=[A-Z])', ' ', tag).strip()
    if wordninja is not None:
        return " ".join(wordninja.split(tag))
    return tag.title()

def parse_date(date_str):
    try:
        return datetime.fromisoformat(date_str.replace("Z", ""))
    except Exception:
        return datetime.min

def pixmap_to_base64(pixmap):
    buffer = QBuffer()
    buffer.open(QIODevice.WriteOnly)
    pixmap.save(buffer, "PNG")
    b64_data = base64.b64encode(buffer.data()).decode('utf-8')
    buffer.close()
    return b64_data
