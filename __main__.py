import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QGridLayout, QLabel, QTextEdit, QWidget
from scanner import TinyScanner


class TinyParserWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        lbl = QLabel('Enter Tiny Code', self)
        self.input_code = QTextEdit()
        submit_button = QPushButton('Parse')
        submit_button.clicked.connect(self.submitted)
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(lbl, 1, 0)
        grid.addWidget(self.input_code, 1, 1)
        grid.addWidget(submit_button, 2, 1)
        self.setLayout(grid)
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Tiny Parser')
        self.show()

    def submitted(self):
        scanned_code = TinyScanner(self.input_code.toPlainText())
        scanned_code.createOutputFile('output.tiny')
app = QApplication(sys.argv)
w = TinyParserWidget()
sys.exit(app.exec_())
