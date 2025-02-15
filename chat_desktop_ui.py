from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QComboBox,QPushButton, QLabel, QHBoxLayout,QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
import ollama

# Retrieving list of available models from Ollama Sever. Will be added to drop-down selector.
models = ollama.list()
model_lists = []
for i in range(0, (len(models['models']))):
    model_lists.append(models['models'][i]['model'])


# Application is created using class. Crucial app components/functions are initialized when class is called to
# enable features and functionality.
class Chat(QWidget):
    def __init__(self):
        super().__init__()
        # Crucial! The interface, settings, and button actions need to be initialized to ensure QT includes functions
        self.initUI()
        self.settings()
        self.button_clicks()

# Creating application widgets and layout design
    def initUI(self):
        # Chat window
        self.conversation_window = QTextEdit()
        self.conversation_window.setStyleSheet("padding: 5px")
        self.conversation_window.setReadOnly(True)
        self.conversation_window.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.conversation_window.setLineWrapMode(QTextEdit.WidgetWidth)
        self.conversation_window.setPlaceholderText("Chat will populate here")

        # User Query Window
        self.query_box = QTextEdit()
        self.query_box.setPlaceholderText("Type your query here")
        self.query_box.setFixedSize(400, 100)

        # LLM Selection Dropdown Initialization
        self.model_selector = QComboBox()
        self.model_selector_label = QLabel("Select LLM:")
        self.model_selector_label.setAlignment(Qt.AlignBottom)
        self.model_selector.addItems(model_lists) # Adding list of available models to drop down

        # Buttons Initialization
        self.submit_button = QPushButton('Submit Query')
        self.reset_button = QPushButton('Reset')

        # Creating app title
        self.title_label = QLabel('Ollama Chat UI', self)
        self.title_label.move(100, 500)
        self.title_label.setStyleSheet("font-size: 30px")
        self.title_label.setAlignment(Qt.AlignTop)
        self.title_label.setAlignment(Qt.AlignHCenter)

        # Master Layout is a horizontal layout. Row-wise
        self.master = QHBoxLayout()

        self.setStyleSheet("""
                    QWidget {
                        background-color: #333; /* Darker background color */
                        color: #fff; /* Text color */
                    }

                    QPushButton {
                        background-color: #66a3ff; /* Lighter background color for buttons */
                        color: #fff; /* Text color for buttons */
                        border: 1px solid #fff; /* White border for buttons */
                        border-radius: 5px; /* Rounded corners for buttons */
                        padding: 5px 10px; /* Padding for buttons */
                    }

                    QPushButton:hover {
                        background-color: #3399ff; /* Lighter background color for buttons on hover */
                    }
                    
                """)
        #self.conversation_window.setDisabled(True)

        #Columns are vertical layouts. Column-wise
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()

        # Adding widgets to column 1
        col1.addWidget(self.title_label)
        col1.addWidget(self.model_selector_label)
        col1.addWidget(self.model_selector)
        col1.addWidget(self.submit_button)
        col1.addWidget(self.reset_button)

        # Adding widgets to column 2
        col2.addWidget(self.conversation_window)
        col2.addWidget(self.query_box)

        # Adding columns to master layout
        self.master.addLayout(col1, 30)
        self.master.addLayout(col2, 70)

        # Setting layout using master which includes both vertical and horizontal layouts for tailoring
        self.setLayout(self.master)


# App settings
    def settings(self):
        self.setWindowTitle('Ollama Chat')
        self.setGeometry(300, 300, 700, 500)

# Button click actions/query submission
    def button_clicks(self):
        self.submit_button.clicked.connect(self.query_submission)
        self.reset_button.clicked.connect(self.conversation_window.clear)


# Clear chat and reset windows
    def query_submission(self):
        model_selected = self.model_selector.currentText()
        text = self.query_box.toPlainText()

        self.conversation_window.append(f"<p style='color:ivory'><i class='fas fa-cloud'></i>User: {text}</p>")
        self.conversation_window.setAlignment(Qt.AlignRight)


        self.script = self.chat(model_selected, text)
        self.conversation_window.append(f"<p style='color:darkseagreen'>Assistant: {self.script}</p>")
        self.conversation_window.setAlignment(Qt.AlignLeft)

        self.query_box.clear()

# Chat function to generate responses
    def chat(self, model_selection, query_string):
        result= ollama.chat(
            model_selection,
            messages=[{
                'role': 'user',
                'content': query_string,
            }],
        )

        return result['message']['content']

# Creating QApplication to execute, intializing chat class and showing UI
if __name__ in "__main__":
    app = QApplication([])
    main = Chat()
    main.show()
    app.exec_()