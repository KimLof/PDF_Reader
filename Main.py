import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog
import pyttsx3
import PyPDF2
import threading

class PDFReaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Reader")

        self.label = QLabel("Select a PDF file:")
        self.open_button = QPushButton("Open")
        self.open_button.clicked.connect(self.open_pdf)
        self.pause_button = QPushButton("Pause")
        self.pause_button.setEnabled(False)
        self.pause_button.clicked.connect(self.pause_reading)
        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_reading)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.open_button)
        layout.addWidget(self.pause_button)
        layout.addWidget(self.stop_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.player = pyttsx3.init()
        self.player.setProperty('rate', 150)
        self.book = None
        self.pdfreader = None
        self.pages = 0
        self.page_num = 0
        self.paused = False
        self.stopped = False
        self.thread = None

    def open_pdf(self):
        self.book, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf)")
        if self.book:
            self.pdfreader = PyPDF2.PdfReader(open(self.book, 'rb'))
            self.pages = len(self.pdfreader.pages)
            self.page_num = 0
            self.open_button.setEnabled(False)
            self.pause_button.setEnabled(True)
            self.stop_button.setEnabled(True)
            self.thread = threading.Thread(target=self.read_pdf)
            self.thread.start()

    def read_pdf(self):
        while self.page_num < self.pages and not self.stopped:
            page = self.pdfreader.pages[self.page_num]
            text = page.extract_text()
            self.player.say(text)
            self.page_num += 1
            if not self.paused:
                self.player.runAndWait()

    def pause_reading(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_button.setText("Resume")
        else:
            self.pause_button.setText("Pause")
            if not self.paused:
                self.thread = threading.Thread(target=self.read_pdf)
                self.thread.start()

    def stop_reading(self):
        self.stopped = True
        self.player.stop()
        self.open_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)



def main():
    app = QApplication(sys.argv)
    window = PDFReaderApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


