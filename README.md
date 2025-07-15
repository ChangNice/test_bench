# Environment Setup
1. Add Jlink.exe into your systemm PATH
2. Clone Logic2 Analyzer into `/tools` by `git clone https://github.com/AnChangNice/Logic2_HCI_UART_Extension.git ./tools/logic2`
3. Install required Python dependencies: `pip install -r ./requirements.txt`

```shell
git clone https://github.com/AnChangNice/Logic2_HCI_UART_Extension.git ./tools/logic2
pip install -r ./tools/logic2/requirements.txt
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