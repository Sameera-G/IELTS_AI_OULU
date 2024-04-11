import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPixmap, QPalette, QBrush
import pyttsx3
from PyQt5.QtCore import QTimer

from treplicator import FirestoreApp  # Import the pyttsx3 library for text-to-speech functionality.

class TaskReplicatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.speech_engine = pyttsx3.init()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateStopwatch)
        self.elapsedTime = 0
        self.startStopwatch()

    def initUI(self):
        # Set padding for the entire screen
        padding = 80  # Adjust the padding size as needed
        screen_geometry = QApplication.desktop().screenGeometry()
        self.setGeometry(
            padding, 
            padding, 
            screen_geometry.width() - 2 * padding, 
            screen_geometry.height() - 2 * padding
        )
        style_1 = "color: white; background-color: rgba(0, 0, 0, 150); border-radius: 15px; padding: 10px;"
        #title
        self.setWindowTitle('IELTS EXAM FOR YOU')
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap("images/background1.png")))
        self.setPalette(palette)
        

        layout = QHBoxLayout(self)
        layout.setContentsMargins(padding, padding, padding, padding)

        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, int(padding/3), int(padding/1.3))

        #stop watch
        self.stopwatchLabel = QLabel('00:00:00', self)
        self.stopwatchLabel.setFont(QFont('Arial', 14))
        left_layout.addWidget(self.stopwatchLabel)

        self.startStopButton = QPushButton('Start', self)
        self.startStopButton.setStyleSheet(style_1)
        self.startStopButton.clicked.connect(self.startStopwatch)
        screen_size = QApplication.primaryScreen().size()
        button_width = int(screen_size.width() * 0.06) 
        button_height = int(self.startStopButton.sizeHint().height()) 
        self.startStopButton.setFixedSize(QSize(button_width, button_height))
        left_layout.addWidget(self.startStopButton)

        self.resetButton = QPushButton('Reset', self)
        self.resetButton.setStyleSheet(style_1)
        self.resetButton.clicked.connect(self.resetStopwatch)
        screen_size = QApplication.primaryScreen().size()
        button_width = int(screen_size.width() * 0.06) 
        button_height = int(self.resetButton.sizeHint().height())
        self.resetButton.setFixedSize(QSize(button_width, button_height))
        left_layout.addWidget(self.resetButton)

        self.mainLabel = QLabel('IELTS Exam Support', self)
        self.mainLabel.setFont(QFont('Arial', 18))
        self.mainLabel.setAlignment(Qt.AlignCenter)
        self.mainLabel.setStyleSheet("border-radius: 15px;")
        self.mainLabel.setMaximumWidth(int(screen_size.width() * 0.6))
        left_layout.addWidget(self.mainLabel)

        self.descriptionLabel1 = QLabel(self)
        self.descriptionLabel1.setFont(QFont('Arial', 12))
        self.descriptionLabel1.setAlignment(Qt.AlignCenter)
        self.descriptionLabel1.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 150); border-radius: 15px; padding: 10px; text-align: justify;")
        self.descriptionLabel1.setMaximumWidth(int(screen_size.width() * 0.6))
        left_layout.addWidget(self.descriptionLabel1)

        # Listen button for the description, updated size and color as per request.
        self.listenButton = QPushButton("Listen", self)
        self.listenButton.clicked.connect(self.speakDescription)
        self.listenButton.setFont(QFont('Arial', 12))
        self.listenButton.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 150); border-radius: 15px; padding: 10px;")
        screen_size = QApplication.primaryScreen().size()
        button_width = int(screen_size.width() * 0.06)  # Convert to integer
        button_height = int(self.listenButton.sizeHint().height())  # Convert to integer
        self.listenButton.setFixedSize(QSize(button_width, button_height))
        left_layout.addWidget(self.listenButton)

        self.descriptionLabel = QLabel('Please select your desired paper to proceed', self)
        self.descriptionLabel.setFont(QFont('Arial', 12))
        self.descriptionLabel.setAlignment(Qt.AlignCenter)
        self.descriptionLabel.setStyleSheet("background-color: rgba(0, 0, 0, 150); color: white; border-radius: 15px; padding: 20px; text-align: justify;")
        self.descriptionLabel.setMaximumWidth(int(screen_size.width() * 0.6))
        self.descriptionLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        left_layout.addWidget(self.descriptionLabel)

        layout.addLayout(left_layout)

        right_layout = QVBoxLayout()
        self.buttons = []
        papers = ["Reading", "Listening", "Writing", "Speaking"]
        for paper in papers:
            button = QPushButton(paper, self)
            button.setFont(QFont('Arial', 20))
            button.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 150); border-radius: 15px; padding: 20px;")
            button.clicked.connect(lambda checked, r=paper: self.paper_selected(r))
            self.buttons.append(button)
            right_layout.addWidget(button)

        layout.addLayout(right_layout)

        self.loadDescriptionFromFile("paragraphs/main_description.txt")

    #stop watch
    def startStopwatch(self):
        if not self.timer.isActive():
            self.timer.start(1000)  # Update the timer every second.
            self.startStopButton.setText('Pause')
        else:
            self.timer.stop()
            self.startStopButton.setText('Continue')

    def updateStopwatch(self):
        self.elapsedTime += 1
        elapsed_time_string = '{:02d}:{:02d}:{:02d}'.format(self.elapsedTime // 3600, (self.elapsedTime % 3600 // 60), self.elapsedTime % 60)
        self.stopwatchLabel.setText(elapsed_time_string)

    def resetStopwatch(self):
        self.timer.stop()
        self.elapsedTime = 0
        self.stopwatchLabel.setText('00:00:00')
        self.startStopButton.setText('Start')

    #description of the main window
    def loadDescriptionFromFile(self, filename):
        try:
            with open(filename, "r") as file:
                description = file.read()
                self.descriptionLabel1.setText(description)
                self.descriptionLabel1.setWordWrap(True)
                self.descriptionLabel1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        except FileNotFoundError:
            print("Description file not found.")

    def speakDescription(self):
        """Reads the content of `descriptionLabel1` aloud."""
        text = self.descriptionLabel1.text()
        self.speech_engine.say(text)
        self.speech_engine.runAndWait()

    def paper_selected(self, selected_role):
        # Assume the existence of a class FirestoreApp
        self.firestore_window = FirestoreApp(selected_role, self)
        self.firestore_window.show()
        self.firestore_window.showFullScreen()
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TaskReplicatorApp()
    ex.showFullScreen()
    sys.exit(app.exec_())