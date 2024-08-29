import sys
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from app.dice_roller_app import DiceRollerApp

def main():
    app = QApplication(sys.argv)

    splash = QSplashScreen()
    splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    splash.setFont(QFont('Arial', 18)) 
    
    splash.resize(600, 200)
    splash.setStyleSheet("background-color: white; color: black;")
    
    splash.showMessage("Loading... Please wait", Qt.AlignCenter, Qt.black)
    splash.show()

    dice_roller = DiceRollerApp(splash=splash)

    dice_roller.setup_complete.connect(lambda: QTimer.singleShot(0, dice_roller.show)) 

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()