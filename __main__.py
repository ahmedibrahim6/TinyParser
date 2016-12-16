import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QGridLayout, QLabel, QTextEdit, QWidget
from scanner import TinyScanner
from tinyparser import Parser
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
        scanned_code.scan()
        parse_code = Parser()
        parse_code.set_tokens_list_and_code_list(scanned_code.tokens_list, scanned_code.code_list)
        parse_code.run()
        nodes_list = parse_code.nodes_table
        edges_list = parse_code.edges_table

        self.G = nx.DiGraph()
        for node_number, node_value in nodes_list.items():
            self.G.add_node(node_number, value=node_value)
        self.G.add_edges_from(edges_list)
        self.draw()

app = QApplication(sys.argv)
w = TinyParserWidget()
sys.exit(app.exec_())
