from tools.board import Board
from tools.logic2.logic2_analyzer import Logic2_Analyzer

import time
import sys
import os

def get_user_input():
    args = sys.argv[1:]
    if len(args) != 3:
        print("[test_name] [runtimes] [log_folder]")
        sys.exit()

    test_name  = args[0]
    runtimes   = int(args[1])
    log_folder = args[2]

    log_folder = os.path.abspath(log_folder)
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    
    return test_name, runtimes, log_folder

if __name__ == "__main__":

    # handle user input [test_name] [runtimes] [log_folder]
    test_name, runtimes, log_folder = get_user_input()
    
    # Init analyzer
    analyzer = Logic2_Analyzer()
    analyzer.set_save_folder(log_folder)
    analyzer.capture_config(digital_channels=[0, 1], 
                           digital_sample_rate=16000000)
    # Init board
    board = Board("bms", "COM31", 1065330230, "MIMXRT1176XXXA_M7")
    board.set_save_folder(log_folder)
    
    # test start
    print(f"{'='*10} {test_name} run {runtimes} {'='*10} ")
    for i in range(runtimes):
        print(f"{test_name} - {i+1}/{runtimes}: start ...")

        try:
            analyzer.capture_start()
            board.reset()
            
            board.wait_for_response("Please open the wav file you want use", timeout=10)
            board.send_command("wav_open 1:/music_48000_2ch_16bits.wav", "Please select lc3 preset use", timeout=10)
            board.send_command("lc3_preset 48_2_1", "Broadcast source started", timeout=10)

            analyzer.capture_stop()
        except Exception as ex:
            print(f"Exception: {ex}")
            break
        finally:
            analyzer.export_btsnoop(f'{i}_bms', tx_channel=0, rx_channel=1, bit_rate=3000000)
            analyzer.capture_save(f'{i}_bms')
            board.save_log(f"{i}_log")
        
        print(f"{test_name} - {i+1}/{runtimes}: end!")

    # close the analyzer
    analyzer.close()
