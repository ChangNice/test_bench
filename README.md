# Environment Setup
1. Add Jlink.exe into your systemm PATH
2. Clone Logic2 Analyzer into `/tools` by `git clone https://github.com/AnChangNice/Logic2_HCI_UART_Extension.git ./tools/logic2`
3. Install required Python dependencies: `pip install -r ./requirements.txt`

```shell
git clone https://github.com/AnChangNice/Logic2_HCI_UART_Extension.git ./tools/logic2
pip install -r ./requirements.txt
```

# Tools
1. list all serial port `./tools/port_list.bat`
```shell
PS C:\Repos\test_bench> .\tools\port_list.bat

C:\Repos\test_bench>python -m serial.tools.list_ports -v
COM31
    desc: JLink CDC UART Port (COM31)
    hwid: USB VID:PID=1366:1024 SER=001065330230 LOCATION=1-3.4:x.0
COM36
    desc: JLink CDC UART Port (COM36)
    hwid: USB VID:PID=1366:1024 SER=001066419236 LOCATION=1-3.3:x.0
COM47
    desc: JLink CDC UART Port (COM47)
    hwid: USB VID:PID=1366:1024 SER=001068087631 LOCATION=1-3.2:x.0
4 ports found
```

# Sample
The sample test script for listing and interacting with serial ports and capture logic analyzer data:`test.py`

```shell
python test.py [test_name] [runtimes] [log_folder]
```
example:
```shell
PS C:\Repos\test_bench> python .\test.py bms 2 ./test
Analyzer launch Logic2 ...
Logic2 running!
========== bms run 2 ==========
bms - 1/2: start ...
Session: 1
bms - 1/2: end!
bms - 2/2: start ...
Session: 2
bms - 2/2: end!

PS C:\Repos\test_bench> ls ./test

    Directory: C:\Repos\test_bench\test

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         7/15/2025   3:04 PM           6920 20250715_150411_0_bms.csv
-a----         7/15/2025   3:04 PM           5671 20250715_150411_0_bms.sal
-a----         7/15/2025   3:04 PM           2138 20250715_150411_0_bms_btsnoop.log
-a----         7/15/2025   3:04 PM           3426 20250715_150428_0_log.txt
-a----         7/15/2025   3:04 PM           7562 20250715_150428_1_bms.csv
-a----         7/15/2025   3:04 PM           5872 20250715_150428_1_bms.sal
-a----         7/15/2025   3:04 PM           2336 20250715_150428_1_bms_btsnoop.log
-a----         7/15/2025   3:04 PM           3414 20250715_150435_1_log.txt

```
