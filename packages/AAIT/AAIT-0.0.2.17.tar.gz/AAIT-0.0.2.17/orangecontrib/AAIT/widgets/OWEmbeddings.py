import os
import sys

import Orange.data
from Orange.widgets import widget
from Orange.widgets.utils.signals import Input, Output

from orangecontrib.AAIT.llm import embeddings
from orangecontrib.AAIT.utils import shared_functions

from PyQt5 import uic
from AnyQt.QtWidgets import QApplication


class OWCreateEmbeddings(widget.OWWidget):
    name = "Create Embeddings"
    description = "Create embeddings on the column 'content' of a Table"
    icon = "icons/owembeddings.svg"
    gui = os.path.join(os.path.dirname(os.path.abspath(__file__)), "designer/owembeddings.ui")
    want_control_area = False

    class Inputs:
        data = Input("Data", Orange.data.Table)

    class Outputs:
        data = Output("Data", Orange.data.Table)

    @Inputs.data
    def set_data(self, in_data):
        self.data = in_data
        self.run()

    def __init__(self):
        super().__init__()
        # Path management
        self.current_ows = ""
        shared_functions.setup_shared_variables(self)
        model_name = "all-mpnet-base-v2"
        self.model_path = os.path.join(os.path.dirname(os.path.dirname(self.current_ows)), "Models", model_name)

        # Qt Management
        self.setFixedWidth(470)
        self.setFixedHeight(300)
        uic.loadUi(self.gui)

        # Data Management
        self.data = None

    def run(self):
        try:
            table = embeddings.create_embeddings(self.data, self.model_path)
            self.Outputs.data.send(table)
        except Exception as e:
            print("An error occurred when generating embeddings:", e)
            self.Outputs.data.send(None)
            return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_widget = OWCreateEmbeddings()
    my_widget.show()
    app.exec_()
