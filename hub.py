import time
import pygame
import os
import sys
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
# INITIATING RICKROLL
pygame.mixer.init()
pygame.mixer.music.load("/MAIN_HUB/HUB_data/definatelynotarickroll.mp3")
pygame.mixer.music.set_volume(0.15)
# gain the starting directory
start_dir = os.getcwd()


class HUB(QWidget):
    def __init__(self):
        super().__init__()
        self.count = 0
        # load UI and audio
        uic.loadUi('D:/MAIN_HUB/HUB_data/Ui/hub.ui', self)

        # entitle the window
        self.setWindowTitle('OLD GAMES HUB')
        # create icons for buttons
        self.setWindowIcon(QtGui.QIcon('/MAIN_HUB/HUB_data/Img/hubico.png'))
        self.TTR.setIcon(QIcon('/MAIN_HUB/HUB_data/Img/TETRIS.png'))
        self.TTR.setIconSize(QSize(90, 90))
        self.SNK.setIcon(QIcon('/MAIN_HUB/HUB_data/Img/SNAKE.png'))
        self.SNK.setIconSize(QSize(90, 90))
        self.TTT.setIcon(QIcon('/MAIN_HUB/HUB_data/Img/TICTACTOE.png'))
        self.TTT.setIconSize(QSize(80, 80))
        self.SBF.setIcon(QIcon('/MAIN_HUB/HUB_data/Img/GAMEPAD.png'))
        self.SBF.setIconSize(QSize(200, 200))
        self.TIR.setIcon(QIcon('/MAIN_HUB/HUB_data/Img/THREE.png'))
        self.TIR.setIconSize(QSize(90, 90))
        self.REV.setIcon(QIcon('/MAIN_HUB/HUB_data/Img/REVERSI.png'))
        self.REV.setIconSize(QSize(70, 70))
        # make rickroll button
        self.SBF.clicked.connect(self.rolled)
        # make opening buttons
        self.SNK.clicked.connect(self.opened)
        self.TTR.clicked.connect(self.opened)
        self.TTT.clicked.connect(self.opened)
        self.TIR.clicked.connect(self.opened)
        self.REV.clicked.connect(self.opened)

        # create rickroll
    def rolled(self):
        if self.count == 0:
            pygame.mixer.music.play()
            time.sleep(0.1)
            self.count += 1
        elif self.count == 1:
            pygame.mixer.music.pause()
            time.sleep(0.1)
            self.count += 1
        elif self.count == 2:
            pygame.mixer.music.unpause()
            time.sleep(0.1)
            self.count = 1

        # create opening method
    def opened(self):
        global start_dir
        name = self.sender().objectName()
        # ВАЖНАЯ ПОМЕТКА \\\\
        # это НЕ костыль, если сделать все сразу, оно будет оперировать из папки с хабом
        if name == "SNK":
            self.showMinimized()
            os.chdir(f"{start_dir}\HUB_data\WData\SNAKE")
            os.system("SNAKE.exe")
            self.showMaximized()
            os.chdir(start_dir)
        elif name == "TTR":
            self.showMinimized()
            os.chdir(f"{start_dir}\HUB_data\WData\TETRIS")
            os.system("TETRIS.exe")
            self.showMaximized()
            os.chdir(start_dir)
        elif name == "REV":
            self.showMinimized()
            os.chdir(f"{start_dir}\HUB_data\WData\REVERSI")
            os.system("main.exe")
            self.showMaximized()
            os.chdir(start_dir)
        elif name == "TTT":
            self.showMinimized()
            os.chdir(f"{start_dir}\HUB_data\WData\CROSS")
            os.system("main.exe")
            self.showMaximized()
            os.chdir(start_dir)
        elif name == "TIR":
            self.showMinimized()
            os.chdir(f"{start_dir}\HUB_data\WData\THREEINROW")
            os.system("main.exe")
            self.showMaximized()
            os.chdir(start_dir)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = HUB()
    ex.show()
    sys.exit(app.exec())