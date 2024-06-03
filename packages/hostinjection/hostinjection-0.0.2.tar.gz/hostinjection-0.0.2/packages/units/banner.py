import getpass

def help_banner():
    banner = f"""
    hey {getpass.getuser}

                              v1.0
      ____ _____    _____   ____  
     /    \\__  \  /     \_/ __ \ 
    |   |  \/ __ \|  Y Y  \  ___/ 
    |___|  (____  /__|_|  /\___  >
         \/     \/      \/     \/ 

    $toolname.py [options]

    usage: toolname.py [options]

    Options:
    -h, --help help menu
    -u,--url URL to Scan 
    -i,--input <filename> read input from txt
    -o, --output <filename> write a op file name
    -b ,--blog  to read about the bug
"""
    print(banner)

def banner():
    banner = f"""
    hey {getpass.getuser}

                              v1.0
      ____ _____    _____   ____  
     /    \\__  \  /     \_/ __ \ 
    |   |  \/ __ \|  Y Y  \  ___/ 
    |___|  (____  /__|_|  /\___  >
         \/     \/      \/     \/ 

    $toolname.py [options]
    """
    print(banner)
