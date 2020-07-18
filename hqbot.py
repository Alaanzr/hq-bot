import sys
import tkinter as tk
import os
import ocr
import re
import pyscreenshot as ImageGrab
from bs4 import BeautifulSoup
from colorama import Fore, Style
from PyQt5 import QtWidgets, QtCore, QtGui
from urllib.request import Request, urlopen

class HQBotWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        root = tk.Tk()

        self.setWindowTitle('HQBot')

        # Calculate the size of the screen that the script is being executed on
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0, 0, screen_width, screen_height)

        self.drag_start = QtCore.QPoint()
        self.drag_end = QtCore.QPoint()
        self.setWindowOpacity(0.3)

        # Override our system cursor with the QT cursor
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor(255, 100, 100), 1))
        qp.setBrush(QtGui.QColor(200, 100, 100))
        qp.drawRect(QtCore.QRect(self.drag_start, self.drag_end))

    def mousePressEvent(self, event):
        self.drag_start = event.pos()
        # Set the drag_end position to be equal to our start position so that the rectangle appears to be 1px on initial press
        self.drag_end = self.drag_start
        self.update()

    def mouseMoveEvent(self, event):
        self.drag_end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.close()

        x1 = min(self.drag_start.x(), self.drag_end.x())
        y1 = min(self.drag_start.y(), self.drag_end.y())
        x2 = max(self.drag_start.x(), self.drag_end.x())
        y2 = max(self.drag_start.y(), self.drag_end.y())

        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        img.save('capture.png')

        text = ocr.readImg()
        print('TEXT', text)
        self.buildQAndA(text)

    def buildQAndA(self, text):
        print('text', text)
        lines = text.splitlines()
        question = ''
        questionAsked = False
        answers = list()

        for line in lines:
            line = line.lower()
            if line == '':
                continue

            if not questionAsked:
                question += f'{line} '      

            if '?' in line:
                questionAsked = True
                continue

            if questionAsked:
                answers.append(line)

        print(f'{Fore.GREEN}Q: {Fore.WHITE}{question}')
        for index, answer in enumerate(answers):
            print(f'{index}: {answer}')

        answer_dict = { key: 0 for key in answers }

        question_params = '+'.join(question.split(' '))
        url = f'https://www.google.co.uk/search?q={question_params}'

        self.search(question, answers, answer_dict, url, recursive = True)

    def search(self, question, answers, answer_dict, url, recursive = False):
        try:
            # print('url', url)
            # Set request Headers to avoid 403 errors
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            uClient = urlopen(req)
            search_html = uClient.read()
            uClient.close()

            soup = BeautifulSoup(search_html, 'html.parser')
            parsed_text = soup.get_text().lower()
            
            # answer_dict = { key: 0 for key in answers }
            for key in answer_dict:
                answer_dict[key] += parsed_text.count(key)

            # if recursive == True:
            #     for link in soup.findAll('a'):
            #         print('link', link.get('href'))
            #         test = link
            #         try:
            #             test = link['href'].split('/url?q=')[1]
            #             print('test', test)
            #         except Exception as e:
            #             print('split test', e)
            #         self.search(question, answers, answer_dict, test, recursive = False)

            # print('soup text', soup)

            print('dict', answer_dict)

            
        except Exception as e:
            print('search error', e)


        
            
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = HQBotWidget()
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())