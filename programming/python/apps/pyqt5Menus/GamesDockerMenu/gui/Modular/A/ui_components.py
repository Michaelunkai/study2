from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QMenu, QInputDialog
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
from functools import partial

class TagContainerWidget(QWidget):
    def __init__(self, type_name, parent=None):
        super(TagContainerWidget, self).__init__(parent)
        self.type_name = type_name  
        self.setAcceptDrops(True)
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
    def dragMoveEvent(self, event):
        event.acceptProposedAction()
    def dropEvent(self, event):
        docker_name = event.mimeData().text()
        main_window = self.window()
        if main_window and hasattr(main_window, "update_tag_category"):
            main_window.update_tag_category(docker_name, self.type_name)
        event.acceptProposedAction()

class TabNavigationWidget(QWidget):
    def __init__(self, tabs_config, parent=None):
        super(TabNavigationWidget, self).__init__(parent)
        self.tabs_config = tabs_config
        self.init_ui()
    def init_ui(self):
        from PyQt5.QtWidgets import QGridLayout
        self.layout = QGridLayout(self)
        self.layout.setSpacing(5)
        self.setLayout(self.layout)
        self.create_tab_buttons()
    def create_tab_buttons(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.buttons = {}
        col = 0
        row = 0
        for tab in self.tabs_config:
            btn = QPushButton(tab["name"])
            btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #2C3E50, stop:1 #34495E);
                    color: white;
                    padding: 8px 12px;
                    border: 1px solid #1ABC9C;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #1ABC9C, stop:1 #16A085);
                }
            """)
            btn.clicked.connect(partial(self.tab_clicked, tab["id"]))
            self.layout.addWidget(btn, row, col)
            self.buttons[tab["id"]] = btn
            col += 1
            if col >= 5:
                col = 0
                row += 1
    def tab_clicked(self, tab_id):
        self.parent().set_current_tab(tab_id)
    def update_tabs(self, tabs_config):
        self.tabs_config = tabs_config
        self.create_tab_buttons()

class TabGridWidget(QWidget):
    def __init__(self, tabs_config, parent=None):
        super(TabGridWidget, self).__init__(parent)
        self.tabs_config = tabs_config
        self.layout = QGridLayout(self)
        self.layout.setSpacing(5)
        self.setLayout(self.layout)
        self.selected_tab_id = None
        self.create_tab_buttons()
    def create_tab_buttons(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        col = 0
        row = 0
        self.buttons = {}
        for tab in self.tabs_config:
            if tab["id"] == "all":
                continue
            btn = QPushButton(tab["name"])
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton {
                    background: #16A085;
                    color: white;
                    padding: 6px 10px;
                    border-radius: 4px;
                }
                QPushButton:checked {
                    background: #1ABC9C;
                }
            """)
            btn.clicked.connect(partial(self.tab_clicked, tab["id"]))
            self.layout.addWidget(btn, row, col)
            self.buttons[tab["id"]] = btn
            col += 1
            if col >= 5:
                col = 0
                row += 1
    def tab_clicked(self, tid):
        self.selected_tab_id = tid
        for k, b in self.buttons.items():
            if k != tid:
                b.setChecked(False)

from PyQt5.QtWidgets import QPushButton, QMenu, QInputDialog
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
from functools import partial
class GameButton(QPushButton):
    dragThreshold = 10
    def __init__(self, text, parent=None):
        super(GameButton, self).__init__(text, parent)
        self.setCheckable(True)
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                             stop:0 #2C3E50, stop:1 #34495E);
                color: gold;
                font-size: 24px;
                padding: 20px;
                border: 2px solid #1ABC9C;
                border-radius: 10px;
                min-height: 200px;
                min-width: 200px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                             stop:0 #1ABC9C, stop:1 #16A085);
                border: 2px solid #F39C12;
            }
            QPushButton:pressed {
                background: #2980B9;
            }
        """)
        self._drag_start_pos = None
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_start_pos = event.pos()
        super(GameButton, self).mousePressEvent(event)
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            if (event.pos() - self._drag_start_pos).manhattanLength() >= self.dragThreshold:
                mimeData = QMimeData()
                mimeData.setText(self.tag_info["docker_name"])
                drag = QDrag(self)
                drag.setMimeData(mimeData)
                drag.exec_(Qt.MoveAction)
                return
        super(GameButton, self).mouseMoveEvent(event)
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        change_action = menu.addAction("Change Tag Name")
        move_to_action = menu.addAction("Move To")
        action = menu.exec_(event.globalPos())
        main_window = self.parent()
        while main_window and not hasattr(main_window, "handle_tag_move"):
            main_window = main_window.parent()
        if not main_window:
            return
        token = main_window.get_docker_token() if main_window else None
        if not token:
            return
        if action == change_action:
            new_alias, ok = QInputDialog.getText(self, "Change Tag Name",
                                                   "Enter new tag name:", QLineEdit.Normal, self.tag_info["alias"])
            if ok and new_alias:
                old_alias = self.tag_info["alias"]
                from dialogs import update_docker_tag_name
                if update_docker_tag_name(old_alias, new_alias):
                    self.tag_info["alias"] = new_alias
                    from persistence import load_settings, save_settings
                    persistent = load_settings().get(self.tag_info["docker_name"], {})
                    persistent["alias"] = new_alias
                    temp = load_settings()
                    temp[self.tag_info["docker_name"]] = persistent
                    save_settings(temp)
                    lines = self.text().splitlines()
                    lines[0] = new_alias
                    self.setText("\n".join(lines))
                    if hasattr(main_window, "handle_tag_rename"):
                        main_window.handle_tag_rename(self.tag_info["docker_name"], new_alias)
                    from network_ops import fetch_game_time
                    from workers import Worker
                    worker = Worker(fetch_game_time, new_alias)
                    worker.signals.finished.connect(partial(main_window.handle_game_time_update, new_alias))
                    main_window.add_worker(worker)
                    from PyQt5.QtCore import QThreadPool
                    QThreadPool.globalInstance().start(worker)
        elif action == move_to_action:
            from dialogs import MoveToDialog
            dialog = MoveToDialog(main_window.tabs_config, parent=main_window)
            if dialog.exec_():
                target_tab_id = dialog.selected_tab_id
                if target_tab_id:
                    main_window.handle_tag_move(self.tag_info["docker_name"], target_tab_id)
