import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QGridLayout, QLabel, QTextEdit, QWidget
from scanner import TinyScanner
import networkx as nx
import matplotlib.pyplot as plt


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

    def draw(self):
        graph = self.G
        pos = nx.nx_pydot.graphviz_layout(graph, prog='dot')
        labels = dict((n, d['value']) for n, d in graph.nodes(data=True))
        nx.draw(graph, pos, labels=labels, with_labels=True, arrows=False)
        plt.show()

    def submitted(self):
        scanned_code = TinyScanner(self.input_code.toPlainText())
        scanned_code.createOutputFile('output.tiny')
        nodes_list = {1: "stmt-seq",
                      2: "stmt",
                      3: ";",
                      4: "stmt-seq",
                      5: "s",
                      6: "stmt",
                      7: ";",
                      8: "stmt-seq",
                      9: "s",
                      10: "stmt",
                      11: "s"}
        edges_list = [(1, 2), (1, 3), (1, 4), (2, 5), (4, 6), (4, 7), (4, 8),
                      (6, 9), (8, 10), (10, 11)]

        self.G = nx.DiGraph()
        for node_number, node_value in nodes_list.items():
            self.G.add_node(node_number, value=node_value)
        self.G.add_edges_from(edges_list)
        self.draw()

app = QApplication(sys.argv)
w = TinyParserWidget()
sys.exit(app.exec_())
