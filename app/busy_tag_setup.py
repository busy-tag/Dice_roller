import os
import shutil
import threading
import time
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QMessageBox
from app.serial_operations import open_serial_connection, send_serial_command, close_serial_connection, find_busy_tag_device

class BusyTagSetup(QObject):
    files_transferred = pyqtSignal(bool)
    files_being_transferred = pyqtSignal(bool)

    def __init__(self, setup_complete_callback=None):
        super().__init__()
        self.serial_conn = None
        self.busy_tag_port = None
        self.drive_letter = None
        self.assets_folder = 'assets'
        self.setup_complete_callback = setup_complete_callback
        self.files_transferred_status = False
        self.prompted_for_drive = False

    def start_setup(self):
        threading.Thread(target=self.setup_busy_tag, daemon=True).start()

    def setup_busy_tag(self):
        print("Starting Busy Tag setup...")
        self.busy_tag_port = find_busy_tag_device()
        if self.busy_tag_port:
            print(f"Found Busy Tag on port {self.busy_tag_port}.")
            self.serial_conn = open_serial_connection(port=self.busy_tag_port, baudrate=115200)
            if self.serial_conn:
                print("Serial connection established.")
                self.set_led_pattern()
                time.sleep(3)
                self.restart_busy_tag_device()
                print("Setup completed.")
        else:
            print("Busy Tag device not found.")
        if self.setup_complete_callback:
            self.setup_complete_callback()

    def set_led_pattern(self):
        if self.serial_conn:
            send_serial_command(self.serial_conn, 'AT+CP=7')
            pattern_file_path = "pattern.txt"
            with open(pattern_file_path, 'r') as file:
                for line in file:
                    send_serial_command(self.serial_conn, line)
                    time.sleep(0.5)

    def restart_busy_tag_device(self):
        if self.serial_conn:
            send_serial_command(self.serial_conn, "AT+RST")
            close_serial_connection(self.serial_conn)
            time.sleep(3)
            self.serial_conn = open_serial_connection(port=self.busy_tag_port, baudrate=115200)

    def transfer_files_to_drive(self, drive_letter):
        if not drive_letter:
            return

        destination_folder = f"{drive_letter}"
        files_to_transfer = [
            "roll.gif",
            "dice_1.png",
            "dice_2.png",
            "dice_3.png",
            "dice_4.png",
            "dice_5.png",
            "dice_6.png"
        ]

        self.files_being_transferred.emit(True) 

        def transfer():
            try:
                for file_name in files_to_transfer:
                    source_path = os.path.abspath(os.path.join(self.assets_folder, file_name))
                    destination_path = os.path.abspath(os.path.join(destination_folder, file_name))
                    print(f"Copying {source_path} to {destination_path}...")

                    if not os.path.isfile(source_path):
                        print(f"Source file does not exist: {source_path}")
                        continue

                    shutil.copy(source_path, destination_path)
                    print(f"Copied {file_name} to {destination_folder}")

                self.files_transferred_status = True
                self.files_transferred.emit(True)  
            except Exception as e:
                print(f"Error copying files: {e}")
                self.files_transferred.emit(False)  
            finally:
                self.files_being_transferred.emit(False)  

        threading.Thread(target=transfer, daemon=True).start()

    def cleanup(self):
        if self.serial_conn:
            close_serial_connection(self.serial_conn)