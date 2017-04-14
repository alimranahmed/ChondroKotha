import sys

from PyQt4 import QtGui, QtCore

from src.core.Engine import Engine


class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.engine = Engine()
        self.last_eng_chars = [' ', ' ', ' ']

        self.setGeometry(50, 50, 700, 400)
        self.setWindowTitle("Chondralok")
        self.setWindowIcon(QtGui.QIcon("pencil.png"))

        self.text_editor = QtGui.QTextEdit()

        # menu action
        action_quit = QtGui.QAction("&Quit", self)
        action_quit.setShortcut("Ctrl+Q")
        action_quit.triggered.connect(self.close_application)

        action_editor = QtGui.QAction("&Open Editor", self)
        action_editor.setShortcut("Ctrl+E")
        action_editor.triggered.connect(self.open_editor)

        # status bar
        self.statusBar().showMessage("Write in Bangla...")

        # menu bar
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(action_quit)
        file_menu.addAction(action_editor)

        self.organize_home()
        self.show()

    def organize_home(self):
        # close action
        open_editor = QtGui.QAction(QtGui.QIcon("pencil.png"), 'Open editor', self)
        open_editor.triggered.connect(self.open_editor)

        # toolbar
        toolbar = self.addToolBar("A Toolbar")
        toolbar.addAction(open_editor)

        self.show()

    def open_editor(self):
        self.setCentralWidget(self.text_editor)
        self.text_editor.setFocus()
        self.text_editor.keyPressEvent = self.editor_key_press_event

    def editor_key_press_event(self, key_event):
        try:
            modifier = QtGui.QApplication.keyboardModifiers()
            shift_modifier = QtCore.Qt.ShiftModifier
            bengali_char = chr(key_event.key())  # Value Error occur here

            if ord('A') <= key_event.key() <= ord('Z'):
                english_char = Window.get_eng_char(key_event, modifier, shift_modifier)
                bengali_char = self.engine.get_ban_char(english_char, self.last_eng_chars)

            self.text_editor.insertPlainText(bengali_char)
            self.last_eng_chars[0] = self.last_eng_chars[1]
            self.last_eng_chars[1] = english_char
        except Exception as e:
            print("ERROR Caught: ")
            print(e)

    @staticmethod
    def get_eng_char(key_event, modifier, is_shift):
        key = key_event.key()
        return chr(key) if modifier and is_shift else chr(key + 32)

    @staticmethod
    def close_application():
        print("Application closed")
        sys.exit()


def run():
    app = QtGui.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

run()

