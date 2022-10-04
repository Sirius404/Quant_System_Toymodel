from PyQt5.QtWidgets import QMessageBox


def message_dialog(t: int, title: str, content: str):
    type_dict = [QMessageBox.Warning,
                 QMessageBox.Question, QMessageBox.Critical]

    msg_box = QMessageBox(type_dict[t], title, content)
    msg_box.exec_()
