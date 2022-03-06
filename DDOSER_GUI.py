import glob
import json
import os
from tkinter.messagebox import QUESTION
from turtle import right
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import Qt, pyqtSignal
import sys




def check_config_files() -> bool:
    needed_files = ['config.json', 'DDOSER_cli.py', 'DDOSER_GUI.py', 'Documentation', 'DOSBox 0.74-3 Manual.txt', 'DOSBox 0.74-3 Options.bat', 'DOSBox.exe', 'games', 'Reset KeyMapper.bat', 'Reset Options.bat', 'Screenshots & Recordings.bat', 'SDL.dll', 'SDL_net.dll', 'Video Codec', 'Documentation\\AUTHORS.txt', 'Documentation\\COPYING.txt', 'Documentation\\INSTALL.txt', 'Documentation\\NEWS.txt', 'Documentation\\README.txt', 'Documentation\\THANKS.txt', 'Video Codec\\Video Instructions.txt', 'Video Codec\\zmbv.dll', 'Video Codec\\zmbv.inf']
    cout = 0
    for ned in needed_files:
        for file in glob.glob('**/*', recursive=True):
            if file == ned:
                cout += 1
                if cout == len(needed_files):
                    return True
    return False


class API:
    @staticmethod
    def startgame(name):
        config_filename = "config.json"
        with open(config_filename, "r") as file:
            config = json.load(file)
        
        for i in range(len(config['Games'])):
            if (name == config['Games'][i]["Name"]):
                os.system("DOSBox.exe " + config['Games'][i]["Exec"] +' -conf dosconf.conf')

        


class AddGame(QMainWindow): # главное окно
    def __init__(self, parent=None):
        super(AddGame, self).__init__(parent, Qt.Window)
        self.setupUi()
        self.parent = parent

    def setupUi(self):
        widget = QWidget()
        layout = QVBoxLayout()
        self.setWindowTitle("Add Game") # заголовок окна

        self.name = QLineEdit(self)
        self.name.setPlaceholderText("Название игры")

        self.exec = QLineEdit(self)
        self.exec.setPlaceholderText("Путь до exe файла игры")
        self.add_button = QPushButton('Добавить', self)
        self.add_button.clicked.connect(self.add_game)
        self.add_button.setIcon(QIcon("Assets/start.png"))


        layout.addWidget(self.name)
        layout.addWidget(self.exec)
        layout.addWidget(self.add_button)       
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def add_game(self):
        exec = self.exec.text()
        name = self.name.text()
        CONFIGURATOR().AddGame(name, exec)
        self.close()
    def closeEvent(self, event):
        self.parent.reload()



class CONFIGURATOR:
    def __init__(self):
        self.config_filename = "config.json"
        with open(self.config_filename, "r") as file:
            self.config = json.load(file)


    def GameList(self) -> list:
        games = []
        for game in range(len(self.config['Games'])):
            games.append(self.config['Games'][game]["Name"])
        return games


    def AddGame(self, game_name, exec):
        new_game = {"Name":game_name, "Exec": exec}
        with open("config.json", "r+") as file:
            file_data = json.load(file)
            file_data['Games'].append(new_game)
            file.seek(0)
            json.dump(file_data, file, indent= 4)

    def DeleteGame(self, name):
        for i in range(len(self.config['Games'])):
            if self.config['Games'][i]['Name'] == name:
                del self.config['Games'][i]

        with open("config.json", "w") as file:
            json.dump(self.config, file, indent= 4)
                
        

    
class StandardItem(QStandardItem):
    def __init__(self, txt='', font_size=12, set_bold=False, color=QColor(0,0,0)):
        super().__init__()
        fnt = QFont('Open Sans', font_size)
        fnt.setBold(set_bold)

        self.setEditable(False)
        self.setForeground(color)
        self.setFont(fnt)
        self.setText(txt)

class MainWindow(QMainWindow): # главное окно
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):


        self.setWindowTitle("DDOSER") # заголовок окна
        widget = QWidget()
        main_layout_vbox = QVBoxLayout()
        bar_layout_hbox = QHBoxLayout()
        right_layout_vbox = QVBoxLayout()
        left_and_right_layout = QHBoxLayout()
        
        
        
        # START GAME BUTTON
        self.start_game_button = QPushButton('Запустить', self)
        self.start_game_button.resize(100,32)
        self.start_game_button.move(0, 0)
        self.start_game_button.clicked.connect(self.start_game)
        self.start_game_button.setIcon(QIcon("Assets/start.png"))
        self.start_game_button.setFixedWidth(80)
        
        # ADD GAME BUTTON
        self.add_game_button = QPushButton('Добавить', self)
        self.add_game_button.resize(100,32)
        self.add_game_button.move(100, 0)   
        self.add_game_button.clicked.connect(self.add_game)
        self.add_game_button.setIcon(QIcon("Assets/plus.png"))
        self.add_game_button.setFixedWidth(80)
        
        # DELETE GAME BUTTON
        self.delete_game_button = QPushButton('Удалить', self)
        self.delete_game_button.resize(100,32)
        self.delete_game_button.move(200, 0)   
        self.delete_game_button.clicked.connect(self.delete_game)
        self.delete_game_button.setIcon(QIcon("Assets/minus.png"))
        self.delete_game_button.setFixedWidth(80)

        # SEARCH
        self.line = QLineEdit(self)
        self.line.resize(100, 32)
        self.line.setPlaceholderText("Искать")
        self.line.move(300, 0)
        self.line.setFixedWidth(100)

        # HORIZONTAL
        
        bar_layout_hbox.addWidget(self.start_game_button)
        bar_layout_hbox.addWidget(self.add_game_button)
        bar_layout_hbox.addWidget(self.delete_game_button)
        bar_layout_hbox.addWidget(self.line)
        bar_layout_hbox.addStretch()
        

        

        self.listWidget = QListWidget()
        for game in CONFIGURATOR().GameList():
            self.listWidget.addItem(game)

        self.ScreenList = QListWidget()
        self.ScreenList.addItem("None")
        self.ScreenList.setFixedHeight(200)
        self.listWidget.itemDoubleClicked.connect(self.show_screens)
        self.ScreenList.itemDoubleClicked.connect(self.show_screenshot)

        self.bbbb = QListWidget()
        self.bbbb.addItem("Общее")
        self.bbbb.setFixedWidth(200)

        main_layout_vbox.addLayout(bar_layout_hbox)

        right_layout_vbox.addWidget(self.listWidget)
        right_layout_vbox.addWidget(self.ScreenList)
        left_and_right_layout.addWidget(self.bbbb)
        left_and_right_layout.addLayout(right_layout_vbox)

        main_layout_vbox.addLayout(left_and_right_layout)

        
        widget.setLayout(main_layout_vbox)
        self.setCentralWidget(widget)

    def show_screens(self):
        name = self.listWidget.currentItem().text()
        print(name.lower())
        self.ScreenList.clear()
        for i in os.listdir("capture"):
            if name.lower() in i:
                path = "capture\\" + i
                print(path)
                icon = QIcon(path)
                item = QListWidgetItem(icon, i)
                size = QSize()
                size.setHeight(200)
                size.setWidth(400)
                item.setSizeHint(size)
                self.ScreenList.addItem(item)
                self.ScreenList.setIconSize(QSize(200, 200))
        self.ScreenList.setItemAlignment(Qt.AlignLeft)
    
    def show_screenshot(self):
        name = self.ScreenList.currentItem().text()
        os.system("explorer.exe capture")



    def start_game(self):
        name = self.listWidget.currentItem().text()
        API().startgame(name)

    def add_game(self):
        self.swin = AddGame(self)
        self.swin.show()
        
    
    def reload(self):
        print("Closed")
        self.listWidget.clear()
        for game in CONFIGURATOR().GameList():
            self.listWidget.addItem(game)
            #self.listWidget.update()

    def delete_game(self):
        name = self.listWidget.currentItem().text()
        CONFIGURATOR().DeleteGame(name)
        self.reload()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
