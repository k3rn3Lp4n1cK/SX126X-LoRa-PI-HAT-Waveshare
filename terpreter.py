import serial
import pprint

class terpreter(object):
    def __init__(self, text, radio):
        self.text = text
        self.current_token = None
        self.radio = radio
        self.pp = pprint.PrettyPrinter(indent=4)

    
    def init_serial(self, comPort, baudrate):
        try:
            return serial.Serial(comPort, baudrate, timeout=2)
        except Exception as e:
            print("[*] Serial Port Error: ", e)
            exit(0)

    def set_confreg(self):
        pass

    def get_next_token(self):
        text = self.text
        
        if text == 'help':
            print("========== sx1262x ===========")
            print("Dock with Raspberry Pi")
            print("Remove the M0 and M1 Jumpers")
            print("Set Jumpers to B")
            print("==============================")
            print("\tget radio confreg\tDisplays Current Radio Configuration Register Settings")
            print("\tset radio confreg\t\tSets Radio Configuration Register Settings")
            print("\tdownload radio confreg\t\tRetrieves Radio Configuration Register Settings over serial")
            print("\tupload radio confreg\t\tSends Radio Configuration Register Settings over serial")
            print("==============================")
            print("\tset comm port <comm_port>\tSet the Serial Port")
            print("\tset baud rate <speed>\tSet the Serial Port Speed (default 9600)")
            print("\texit")

        elif text == 'get radio confreg':
            print("[+] Current Settings")
            self.pp.pprint(self.radio.get_radio_confreg())

        elif text == 'set radio confreg':
            self.radio.set_radio_confreg()

        elif text == 'download radio confreg':
            if self.radio.commport == None:
                print("[!] Please configure a comm port first")
            else:
                print("[+] Receiving confreg from COM Port: ", self.radio.commport)
                ser = self.init_serial(self.radio.commport, self.radio.baudrate)
                self.radio.download_radio_confreg(ser)
                self.pp.pprint(self.radio.get_radio_confreg())
        
        elif text == 'upload radio confreg':
            if self.radio.commport == None:
                print("[!] Please configure a comm port first")
            else:
                ser = self.init_serial(self.radio.commport, self.radio.baudrate)
                self.radio.upload_radio_confreg(ser)
                #print("[+] Downloading new confreg from radio")
                #self.radio.download_radio_confreg(ser)
                #self.pp.pprint(self.radio.get_radio_confreg())

        elif 'set comm port' in text:
            self.radio.commport = text.rsplit(' ', 1)[1]
            print("[+] Setting comm port to: ", self.radio.commport)

        elif 'set baud rate' in text:
            print("[+] Setting baud rate to: ")

        elif 'exit' in text:
            exit(0)

    def expr(self):
        self.current_token = self.get_next_token()
