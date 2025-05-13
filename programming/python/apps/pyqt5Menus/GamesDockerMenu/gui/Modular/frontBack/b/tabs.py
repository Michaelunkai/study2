from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QScrollArea, QStackedWidget, QInputDialog, QMessageBox, QDialog
from PyQt5.QtCore import Qt
from backend import load_tabs_config, save_tabs_config
from functools import partial

class TagContainerWidget(QWidget):
    def __init__(self, type_name, parent=None):
        super().__init__(parent)
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
        super().__init__(parent)
        self.tabs_config = tabs_config
        self.init_ui()

    def init_ui(self):
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

class MoveToDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Target Tab")
        self.selected_tab_id = None
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)
        layout.setSpacing(5)
        col = 0
        row = 0
        for tab in load_tabs_config():
            btn = QPushButton(tab["name"])
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #34495E, stop:1 #2C3E50);
                    color: #F1C40F;
                    padding: 6px 10px;
                    border-radius: 4px;
                }
                QPushButton:checked {
                    background: #F39C12;
                }
            """)
            btn.clicked.connect(partial(self.select_tab, tab["id"], btn))
            layout.addWidget(btn, row, col)
            col += 1
            if col >= 5:
                col = 0
                row += 1
        self.setLayout(layout)

    def select_tab(self, tab_id, btn):
        self.selected_tab_id = tab_id
        for widget in self.findChildren(QPushButton):
            if widget is not btn:
                widget.setChecked(False)
        self.accept()

class Tabs:
    def __init__(self, parent):
        self.parent = parent
        self.tabs_config = load_tabs_config()
        self.tab_pages = {}
        self.stacked = None

    def create_tab_management_buttons(self):
        buttons = []
        add_tab_btn = QPushButton("Add Tab")
        add_tab_btn.setStyleSheet("""
            QPushButton {
                background: #16A085;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #1ABC9C;
            }
        """)
        add_tab_btn.clicked.connect(lambda: self.parent.require_admin() and self.add_tab())
        buttons.append(add_tab_btn)

        rename_tab_btn = QPushButton("Rename Tab")
        rename_tab_btn.setStyleSheet("""
            QPushButton {
                background: #8E44AD;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #9B59B6;
            }
        """)
        rename_tab_btn.clicked.connect(lambda: self.parent.require_admin() and self.rename_tab())
        buttons.append(rename_tab_btn)

        delete_tab_btn = QPushButton("Delete Tab")
        delete_tab_btn.setStyleSheet("""
            QPushButton {
                background: #E74C3C;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #C0392B;
            }
        """)
        delete_tab_btn.clicked.connect(lambda: self.parent.require_admin() and self.delete_tab())
        buttons.append(delete_tab_btn)
        return buttons

    def create_tab_navigation(self):
        self.tab_nav = TabNavigationWidget(self.tabs_config, parent=self.parent)
        return self.tab_nav

    def create_tab_pages(self):
        self.stacked = QStackedWidget()
        self.tab_pages = {}
        for tab in self.tabs_config:
            container = TagContainerWidget(tab["id"], parent=self.parent)
            self.tab_pages[tab["id"]] = container
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setWidget(container)
            self.stacked.addWidget(scroll)
        return self.stacked

    def set_current_tab(self, tab_id):
        for i, tab in enumerate(self.tabs_config):
            if tab["id"] == tab_id:
                self.stacked.setCurrentIndex(i)
                break

    def add_tab(self):
        new_name, ok = QInputDialog.getText(self.parent, "Add Tab", "Enter new tab name:")
        if not (ok and new_name):
            return
        new_id = new_name.lower().replace(" ", "_")
        if any(tab["id"] == new_id for tab in self.tabs_config):
            QMessageBox.warning(self.parent, "Error", "A tab with that identifier already exists.")
            return
        self.tabs_config.append({"id": new_id, "name": new_name})
        save_tabs_config(self.tabs_config)
        container = TagContainerWidget(new_id, parent=self.parent)
        self.tab_pages[new_id] = container
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(container)
        self.stacked.addWidget(scroll)
        self.tab_nav.update_tabs(self.tabs_config)
        self.parent.create_tag_buttons()

    def rename_tab(self):
        current_index = self.stacked.currentIndex()
        current_tab = self.tabs_config[current_index]
        new_name, ok = QInputDialog.getText(self.parent, "Rename Tab", "Enter new tab name:", text=current_tab["name"])
        if not (ok and new_name):
            return
        self.tabs_config[current_index]["name"] = new_name
        save_tabs_config(self.tabs_config)
        self.tab_nav.update_tabs(self.tabs_config)
        self.parent.create_tag_buttons()

    def delete_tab(self):
        current_index = self.stacked.currentIndex()
        current_tab = self.tabs_config[current_index]
        if current_tab["id"] == "all":
            QMessageBox.warning(self.parent, "Error", "You cannot delete the 'All' tab.")
            return
        reply = QMessageBox.question(self.parent, "Delete Tab", f"Delete tab '{current_tab['name']}'?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        del self.tabs_config[current_index]
        save_tabs_config(self.tabs_config)
        self.tab_nav.update_tabs(self.tabs_config)
        widget_to_remove = self.stacked.widget(current_index)
        self.stacked.removeWidget(widget_to_remove)
        widget_to_remove.deleteLater()
        self.parent.create_tag_buttons()
