import time
import pygame
import os
import sys
import subprocess
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
# gain the starting directory
start_dir = os.getcwd()
# INITIATING RICKROLL
pygame.mixer.init()
pygame.mixer.music.load(f'{start_dir}\HUB_data\definatelynotarickroll.mp3')
pygame.mixer.music.set_volume(0.15)


class HUB(QWidget):
    def __init__(self):
        super().__init__()
        self.count = 0
        # load UI and audio
        uic.loadUi(f'{start_dir}\HUB_data/Ui\hub.ui', self)

        # entitle the window
        self.setWindowTitle('OLD GAMES HUB')
        # create icons for buttons
        self.setWindowIcon(QtGui.QIcon(f'{start_dir}/HUB_data/Img/hubico.png'))
        self.TTR.setIcon(QIcon(f'{start_dir}/HUB_data/Img/TETRIS.png'))
        self.TTR.setIconSize(QSize(90, 90))
        self.SNK.setIcon(QIcon(f'{start_dir}/HUB_data/Img/SNAKE.png'))
        self.SNK.setIconSize(QSize(90, 90))
        self.TTT.setIcon(QIcon(f'{start_dir}/HUB_data/Img/TICTACTOE.png'))
        self.TTT.setIconSize(QSize(80, 80))
        self.SBF.setIcon(QIcon(f'{start_dir}/HUB_data/Img/GAMEPAD.png'))
        self.SBF.setIconSize(QSize(200, 200))
        self.TIR.setIcon(QIcon(f'{start_dir}/HUB_data/Img/THREE.png'))
        self.TIR.setIconSize(QSize(90, 90))
        self.REV.setIcon(QIcon(f'{start_dir}/HUB_data/Img/REVERSI.png'))
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
            os.chdir(f"{start_dir}\HUB_data\WData\SNAKE")
            subpro = subprocess.Popen([r"SNAKE.exe"])
            os.chdir(start_dir)
        elif name == "TTR":
            os.chdir(f"{start_dir}\HUB_data\WData\TETRIS")
            subpro = subprocess.Popen([r"TETRIS.exe"])
            os.chdir(start_dir)
        elif name == "REV":
            os.chdir(f"{start_dir}\HUB_data\WData\REVERSI")
            subpro = subprocess.Popen([r"main.exe"])
            os.chdir(start_dir)
        elif name == "TTT":
            os.chdir(f"{start_dir}\HUB_data\WData\CROSS")
            subpro = subprocess.Popen([r"main.exe"])
            os.chdir(start_dir)
        elif name == "TIR":
            os.chdir(f"{start_dir}\HUB_data\WData\THREEINROW")
            subpro = subprocess.Popen([r"main.exe"])
            os.chdir(start_dir)
        while subpro.poll() is None:
            self.showMinimized()
        self.showMaximized()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = HUB()
    ex.show()
    sys.exit(app.exec())