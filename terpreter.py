import serial
import RPi.GPIO as GPIO
import pprint
import time

class OptionError(Exception):
    def __init__(self, message="Option is not available"):
        self.message = message
        super().__init__(self.message)

class terpreter(object):
    def __init__(self, text, radio):
        self.text = text
        self.current_token = None
        self.radio = radio
        self.pp = pprint.PrettyPrinter(indent=4)

        # M0 LOW & M1 LOW = Transmission Mode
        # M0 LOW & M1 HIGH = Configuration Mode
        # M0 HIGH & M1 LOW = WOR Mode
        # M0 HIGH & M1 HIGH = Deep Sleep Mode
        self.M0 = 22
        self.M1 = 27
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.M0, GPIO.OUT)
        GPIO.setup(self.M1, GPIO.OUT)
        GPIO.output(self.M0, False)
        GPIO.output(self.M1, False)

    def gpio_mode(self, mode):
        GPIO.output(self.M0, False)
        GPIO.output(self.M1, False)
        if mode == 'conf':
            GPIO.output(self.M1, True)
        elif mode == 'wor':
            GPIO.output(self.M0, True)
        elif mode == 'sleep':
            GPIO.output(self.M0, True)
            GPIO.output(self.M1, True)
        print("[+] Setting GPIO Pins")
        time.sleep(.5)
        
    def init_serial(self, comPort, br, to=1):
        try:
            return serial.Serial(port=comPort, \
                    baudrate=br, \
                    timeout=to, \
                    parity=serial.PARITY_NONE, \
                    stopbits=serial.STOPBITS_ONE, \
                    bytesize=serial.EIGHTBITS)
        except Exception as e: raise e
            

    def set_confreg(self, ser):
        # 00H High Address
        try:
            x00h = int(input("Address High Byte - 0-255 (0): ") or 0)
            if x00h < 0 or x00h > 255:
                print("[*] Integer value must be between 0-255")
                raise OptionError()
        except Exception as e: raise e
        print("[+} Address High Byte set to: ", x00h)
                                 
        # 01H Low Address
        try:
            x01h = int(input("Address Low Byte - 0-255 (0): ") or 0)
            if x01h < 0 or x01h > 255:
                print("[*] Integer value must be between 0-255")
                raise OptionError()
        except Exception as e: raise e
        print("[+] Address Low Byte set to: ", x01h)
        
        # 02H NETID
        try:
            x02h = int(input("Network ID - 0-255 (0): ") or 0)
            if x02h < 0 or x02h > 255:
                print("[*] Integer value must be between 0-255")
                raise OptionError()
        except Exception as e: raise e
        print("[+] Network ID set to: ", x02h)
                                
        # 03H Baudrate
        print("Baud Rates\r\n==========")
        for k in self.radio.BAUDRATE.keys(): print(k)
        x03h_baudrate = input("Enter BaudRate (9600): ") or '9600'
        if x03h_baudrate not in self.radio.BAUDRATE:
            raise OptionError()
        print("[+] Baudrate set to: ", x03h_baudrate)
                                              
        # 03H Portmode
        print("PortMode\r\n==========")
        for k in self.radio.PORTMODE.keys(): print(k)
        x03h_portmode = input("Enter PortMode (8N1): ") or '8N1'
        if x03h_portmode not in self.radio.PORTMODE:
            raise OptionError()
        print("[+] Port Mode set to ", x03h_portmode)

        # 03H Air Rate
        print("Air Rate\r\n==========")
        for k in self.radio.AIRRATE.keys(): print(k)
        x03h_airrate = input("Enter Selection Number (2.4): ") or '2.4'
        if x03h_airrate not in self.radio.AIRRATE:
            raise OptionError()
        print("[+] Air Rate set to: ", x03h_airrate)

        # 04H Packet Size
        print("Packet Size: ")
        for k in self.radio.PACKETSIZE.keys(): print(k)
        x04h_packetsize = input("Enter Packet Size (240): ") or '240'
        if x04h_packetsize not in self.radio.PACKETSIZE:
            raise OptionError()
        print("[+] Packet size set to: ", x04h_packetsize)

        # 04H Channel Noise
        print("Channel Noise (disabled)")
        for k in self.radio.CHANNELNOISE.keys(): print(k)
        x04h_channelnoise = input("Enter Channel Noise state (disabled): ") or 'disabled'
        if x04h_channelnoise not in self.radio.CHANNELNOISE:
            raise OptionError()
        print("[+] Channel Noise set to: ", x04h_channelnoise)

        # 04H Transmit Power
        print("Transmit Power")
        for k in self.radio.TXPOWER.keys(): print(k)
        x04h_txpower = input("Enter Transmit Power (22): ") or '22'
        if x04h_txpower not in self.radio.TXPOWER:
            raise OptionError()
        print("[+] Transmit Power set to: ", x04h_txpower)
                     
        # TODO: Add channel input validation
        # 05H Control Channel
        print("Control Channel: ")
        x05h = input("Enter Control Channel (18): ") or '18'
        print("[+] Control Channel set to: ", x05h)
                                                                                       
        # 06H RSSI level
        print("RSSI Level")
        for k in self.radio.RSSILEVEL.keys(): print(k)
        x06h_rssi = input("Enter RSSI Level Feedback (disabled): ") or 'disabled'
        if x06h_rssi not in self.radio.RSSILEVEL:
            raise OptionError()
        print("[+] RSSI Level set to: ", x06h_rssi)

        # 06H Transfer Mode
        print("Transfer Mode")
        for k in self.radio.TRANSFERMODE.keys(): print(k)
        x06h_transfermode = input("Enter Transfer Mode (transparent): ") or 'transparent'
        if x06h_transfermode not in self.radio.TRANSFERMODE:
            raise OptionError()
        print("[+] Transfer Mode set to: ", x06h_transfermode)

        # 06H Relay Mode
        print("Relay Mode")
        for k in self.radio.RELAYMODE.keys(): print(k)
        x06h_relaymode = input("Enter Relay Mode (disabled): ") or 'disabled'
        if x06h_relaymode not in self.radio.RELAYMODE:
            raise OptionError()
        print("[+] Relay Mode set to: ", x06h_relaymode)

        # 06H LBT
        print("LBT")
        for k in self.radio.LBT.keys(): print(k)
        x06h_lbt = input("Enter LBT Mode (disabled): ") or 'disabled'
        if x06h_lbt not in self.radio.LBT:
            raise OptionError()
        print("[+] LBT Mode set to: ", x06h_lbt)
        
        #06H WOR Mode
        print("WOR Mode")
        for k in self.radio.WORMODE.keys(): print(k)
        x06h_wormode = input("Enter WOR Mode (transmitter): ") or 'transmitter'
        if x06h_wormode not in self.radio.WORMODE:
            raise OptionError()
        print("[+] WOR Mode set to: ", x06h_wormode)

        # 06H WOR Cycle
        print("WOR Cycle")
        for k in self.radio.WORCYCLE.keys(): print(k)
        x06h_worcycle = input("Enter WOR Cycle (2000): ") or '2000'
        if x06h_worcycle not in self.radio.WORCYCLE:
            raise OptionError()
        print("[+] WOR Cycle set to: ", x06h_worcycle)

        # TODO: Input validation
        # 07H Key High
        print("Crypto Key High")
        x07h = input("Enter Crypto Key High (0): ") or '0'
        print("[+] Crypto Key High Byte set to: ", x07h)

        # "TODO: Iput validation
        # 08H Key Low
        print("Crypto Key Low")
        x08h = input("Enter Crypto Key Low (0): ") or '0'
        print("[+] Crypto Key Low Byte set to: ", x08h)

        self.radio.upload_radio_confreg(ser, x00h, x01h, x02h, x03h_baudrate, x03h_portmode, x03h_airrate, x04h_packetsize, x04h_channelnoise, x04h_txpower, x05h, x06h_rssi, x06h_transfermode, x06h_relaymode, x06h_lbt, x06h_wormode, x06h_worcycle, x07h, x08h)

    def get_next_token(self):
        text = self.text
        
        if text == 'help':
            print("============ sx1262 ===========")
            print("1. Dock sx1262 Radio with Raspberry Pi")
            print("2. Remove the M0 and M1 Jumpers")
            print("3. Set Jumpers to B")
            print("")
            print("==== Configuration Register ====")
            print("show confreg\t\t-- Displays Current Radio Configuration Register Settings")
            print("download confreg\t-- Retrieves Radio Configuration Register Settings over serial")
            print("upload confreg\t\t-- Sends Radio Configuration Register Settings over serial")
            print("")
            print("====     Communications     ====")
            print("send msg\t-- Send a test message")
            print("rcv msg\t\t-- Receive a test message")
            print("chat\t\t-- Enter Chat Mode")
            print("perf test\t-- Enter Performance Testing Mode")
            print("")
            print("====  Serial Port Setting   ====")
            print("set comm port <X>\t-- Set the Serial Port (default /dev/ttyS0)")
            print("set baud rate <X>\t-- Set the Serial Port Speed (default 9600)")
            print("================================")
            print("exit")

        elif text == 'show confreg':
            print("[+] Current Settings")
            ret = self.radio.show_radio_confreg()
            if ret: self.pp.pprint(ret)

        elif text == 'download confreg':
            self.gpio_mode('conf')
            print("[+] Receiving confreg from COM Port: ", self.radio.commport)
            ser = self.init_serial(self.radio.commport, self.radio.baudrate)
            self.radio.download_radio_confreg(ser)
            self.pp.pprint(self.radio.show_radio_confreg())
            self.gpio_mode('')
        
        elif text == 'upload confreg':
            self.gpio_mode('conf')
            ser = self.init_serial(self.radio.commport, self.radio.baudrate)
            self.set_confreg(ser)
            self.gpio_mode('')
        
        elif 'send msg' in text:
            self.gpio_mode('')
            ser = self.init_serial(self.radio.commport, self.radio.baudrate)
            msg = input("Enter Message to send (test1234): ") or "test1234\n"
            self.radio.send_message(ser, msg + '\n')

        elif 'rcv msg' in text:
            self.gpio_mode('')
            ser = self.init_serial(self.radio.commport, self.radio.baudrate, to=30)
            print("[+] Receiver will timeout in 30 secs if no data is received")
            self.radio.rcv_message(ser)
            
        elif 'set comm port' in text:
            self.radio.commport = text.rsplit(' ', 1)[1]
            print("[+] Setting comm port to: ", self.radio.commport)

        # TODO: Baudrate stuff
        elif 'set baud rate' in text:
            self.radio.baudrate = text.rsplit(' ', 1)[1]
            print("[+] Setting baud rate to: ", self.radio.baudrate)

        elif 'show comm settings' in text:
            print("[+] Serial Comm Port Settings")
            print("  ", self.radio.commport)
            print("  ", self.radio.baudrate)
        elif 'exit' in text:
            exit(0)

        else:
            print("[*] Command not recognized")

    def expr(self):
        self.current_token = self.get_next_token()
