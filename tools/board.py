
import serial
import tempfile
import os
import subprocess
from datetime import datetime
import time
import re

class Board:
    def __init__(self, name, com, usb, device, baudrate=115200, timeout=10):
        self.name = name

        self.com = serial.Serial(com, baudrate, timeout=timeout)
        self.com_his = ""

        self.usb = usb
        self.device = device
    
    def set_save_folder(self, folder):
        folder = os.path.abspath(folder)
        if not os.path.exists(folder):
            os.makedirs(folder)

        self.save_folder = folder

    def reset(self, clear_history_log=True):

        if clear_history_log:
            self.com_his = ""

        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)

        try:
            # write reset cmd into a file
            jlink_reset_cmd = ""
            jlink_reset_cmd += "SelectInterface SWD\n"
            jlink_reset_cmd += "speed 4000\n"
            jlink_reset_cmd += "Reset\n"
            jlink_reset_cmd += "r0\n"
            jlink_reset_cmd += "r1\n"
            jlink_reset_cmd += "Exit\n"

            temp_file.write(jlink_reset_cmd)
            temp_file.close()

            # Use J-Link Commander to perform reset
            reset_command = f"Jlink -device {self.device} -CommandFile {temp_file.name} -USB {self.usb}"
            
            res = subprocess.run(reset_command, capture_output=True, text=True)
            if res.returncode != 0:
                print(f"Error resetting device: {res.stderr}")
            else:
                # print(f"Device reset successfully: {self.device} {self.usb}")
                pass

        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
    
    @classmethod
    def flash(self, elf_file):
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)

        try:
            # write reset cmd into a file
            jlink_reset_cmd = ""
            jlink_reset_cmd += "SelectInterface SWD\n"
            jlink_reset_cmd += "speed 4000\n"
            jlink_reset_cmd += f"LoadFile {os.path.abspath(elf_file)}\n"
            jlink_reset_cmd += "Exit\n"

            temp_file.write(jlink_reset_cmd)
            temp_file.close()

            # Use J-Link Commander to perform reset
            reset_command = f"Jlink -device {self.device} -CommandFile {temp_file.name} -USB {self.usb}"
            
            res = subprocess.run(reset_command, capture_output=True, text=True)
            if res.returncode != 0:
                print(f"Error flash device: {res.stderr}")
            else:
                # print(f"Device flash successfully: {self.device} {self.usb}")
                pass

        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

    def close(self):
        self.com.close()

    def __bytes_to_str(self, bytes_data):
        return bytes_data.decode('utf-8')
    
    def __str_find(self, text, pattern, flags=re.M):
        match = re.search(pattern, text, flags=flags)
        return match.group(0) if match else None
    
    def send_command(self, command, expect_response=None, timeout=10):
        # read any existing data in buffer first
        self.com_his += self.__bytes_to_str(self.com.read_all())
        # insert the command into communication history
        self.com_his += "\nCMD -> " + command + "\n"
        # encode command and send over serial
        encoded_command = command.encode('utf-8') + b'\n'
        self.com.write(encoded_command)
        # If expecting
        if expect_response:
            return self.wait_for_response(expect_response, timeout)

        return None

    def wait_for_response(self, expect_response, timeout=10):
        start_time = time.time()
        response = ""
        while time.time() - start_time < timeout:
            if self.com.in_waiting:
                new_data = self.__bytes_to_str(self.com.read(self.com.in_waiting))
                response += new_data
                self.com_his += new_data

                if self.__str_find(response, expect_response):
                    return response

            time.sleep(0.1)

        return None

    def check_history(self, pattern, flags=re.M):
        return self.__str_find(self.com_his, pattern, flags=flags)

    def save_log(self, name=None):
        """
        Save communication history to a log file.

        Args:
            log_path (str, optional): Path to save log file. If None, uses a default path.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if name == None:
            name = self.name
        
        log_path = f"{self.save_folder}/{timestamp}_{name}.txt"

        # readout all com data in buffer.
        self.com_his += self.__bytes_to_str(self.com.read_all())

        with open(log_path, 'w') as log_file:
            log_file.write(self.com_his)


if __name__ == "__main__":

    board = Board("MyBoard", "COM31")
    
    Board.reset(1065330230)
    time.sleep(5)

    board.save_log()
    board.close()