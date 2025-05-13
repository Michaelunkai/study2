def apply_background(app, image_path="b.png"):
    """
    Applies a global stylesheet to the app so that the given image completely covers the background.
    """
    style = f"""
    QWidget {{
        background-image: url({image_path});
        background-repeat: no-repeat;
        background-position: center;
        background-size: cover;
    }}
    QMenu, QInputDialog, QMessageBox {{
        background-image: url({image_path});
        background-repeat: no-repeat;
        background-position: center;
        background-size: cover;
    }}
    """
    app.setStyleSheet(style)
