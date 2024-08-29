from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QTimer
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QInputDialog
from app.busy_tag_setup import BusyTagSetup
import random
import time
from app.serial_operations import send_serial_command

class DiceRollerApp(QWidget):
    setup_complete = pyqtSignal()

    def __init__(self, splash=None):
        super().__init__()
        self.splash = splash
        self.busy_tag_setup = BusyTagSetup(self.setup_complete_callback)
        self.busy_tag_setup.files_transferred.connect(self.on_files_transferred)
        self.busy_tag_setup.files_being_transferred.connect(self.on_files_being_transferred)
        self.initUI()
        self.busy_tag_setup.start_setup()

    def initUI(self):
        layout = QVBoxLayout()

        self.result_label = QLabel('Roll the dice!', self)
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)
        
        self.roll_button = QPushButton('ROLL', self)
        self.roll_button.clicked.connect(self.handle_roll_click)
        layout.addWidget(self.roll_button)

        self.setLayout(layout)
        self.setWindowTitle('Dice Roller')
        self.setGeometry(100, 100, 300, 200)

    @pyqtSlot()
    def setup_complete_callback(self):
        print("Setup complete callback called.")
        if self.splash:
            QTimer.singleShot(0, self.splash.close)
        QTimer.singleShot(0, self.show)

    @pyqtSlot(bool)
    def on_files_transferred(self, transferred):
        if transferred:
            QMessageBox.information(self, "Transfer Complete", "Assets have been successfully transferred to the Busy Tag device.")
        else:
            QMessageBox.critical(self, "Transfer Error", "An error occurred while transferring files.")
        self.reset_ui_after_file_transfer()

    @pyqtSlot(bool)
    def on_files_being_transferred(self, being_transferred):
        if being_transferred:
            self.set_ui_for_file_transfer()
        else:
            self.reset_ui_after_file_transfer()

    def set_ui_for_file_transfer(self):
        self.roll_button.setEnabled(False)
        self.result_label.setText('Transferring files... Please wait.')

    def reset_ui_after_file_transfer(self):
        self.roll_button.setEnabled(True)
        self.result_label.setText('Roll the dice!')

    def handle_roll_click(self):
        if not self.busy_tag_setup.drive_letter:
            drive_letter, ok = QInputDialog.getText(self, 'Input Drive Letter', 'Enter the Busy Tag drive letter (e.g., D):')
            if ok and drive_letter:
                self.busy_tag_setup.drive_letter = drive_letter.upper() + ':'
                if not self.busy_tag_setup.files_transferred_status:
                    self.busy_tag_setup.transfer_files_to_drive(self.busy_tag_setup.drive_letter)
                    return
            else:
                QMessageBox.warning(self, "Input Error", "Drive letter input was cancelled or invalid.")
                return

        result = self.roll_dice()
        self.result_label.setText(f'You rolled: {result}')
        self.display_result(result)

    def roll_dice(self):
        return random.randint(1, 6)

    def display_result(self, result):
        if self.busy_tag_setup.serial_conn:
            send_serial_command(self.busy_tag_setup.serial_conn, f"AT+SC=127,000000")
            send_serial_command(self.busy_tag_setup.serial_conn, f"AT+SP=roll.gif")
            send_serial_command(self.busy_tag_setup.serial_conn, f"AT+PP=1,6")
            time.sleep(5)
            send_serial_command(self.busy_tag_setup.serial_conn, f"AT+SP=dice_{result}.png")
            time.sleep(0.5)
            send_serial_command(self.busy_tag_setup.serial_conn, f"AT+SC=127,00FF00")

    def closeEvent(self, event):
        self.busy_tag_setup.cleanup()
        event.accept()