from PySide6.QtWidgets import QMessageBox


# Message boxes
DEFAULT_ERROR_TITLE = "Error"
DEFAULT_ERROR_TEXT = "Something went wrong"


class ErrorMessage(QMessageBox):
    def __init__(self, title=DEFAULT_ERROR_TITLE, msg=DEFAULT_ERROR_TEXT):
        super().__init__()
        self.setWindowTitle(title)
        self.setIcon(QMessageBox.Critical)
        self.setStandardButtons(QMessageBox.Ok)
        self.setDefaultButton(QMessageBox.Ok)
        self.setText(msg)


DEFAULT_INFO_TITLE = "Info"


class InfoMessage(QMessageBox):
    def __init__(self, msg, title=DEFAULT_INFO_TITLE):
        super().__init__()
        self.setWindowTitle(title)
        self.setIcon(QMessageBox.Information)
        self.setStandardButtons(QMessageBox.Ok)
        self.setDefaultButton(QMessageBox.Ok)
        self.setText(msg)


def process_server_response(response):
    parsed = response.json()
    if parsed["status"] == "err":
        raise Exception(parsed["message"])

    return parsed["data"]
