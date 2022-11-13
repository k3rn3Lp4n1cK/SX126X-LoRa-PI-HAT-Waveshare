# CONFIGURATION REGISTER BYTES
# 11 22 33 44 55 66 77 88 99 AA BB CC
# -----------------------------------
# 11 - Command Header Byte
# 22 - Address Byte
# 33 - Length Byte
#
# 44 - Module Address High Byte (default 0)
# 55 - Module Address Low Byte (default 0)
# 66 - Network Address NETID (default 0)
# 77 - BaudRate + PortMode + AirRate (default 9600, 8N1, 2.4)
# 88 - PacketSize + ChannelNoise + TxPower (default 240, disabled, 22)
# 99 - ControlChannel (default 0x12 or 18 decimal))
# AA - RSSILevel + TransferMethod + RelayMode + LBT + WORMode + WORCycle
#      (default disabled, transparent, disabled, disabled, WORTransmitter)
# BB - Crypt Key High Byte (default 0)
# CC - Crypt Key Low Byte (default 0)
#-------------------------------------
# Air Rate - Higher the value - Shorter the TX distance
# Control Channel - Valid Channels 0-83 = 84 channels
#    850.125MHz + Channel (default 868.125MHz)
# ChannelNoise - send cmd \xc0\xc1\xc2\xc3 to read registers
#     Register 0x00: Current environmental noise RSSI
#     Register 0x01: RSSI when data was received last
#     channel noise: dBm = -(256-RSSI)
#     command format: \xc0\xc1\xc2\c3 + start_addr (\x00) + read_len
#     return format: \xc1 + addr + read_len + value
#     i.e. \xc1\xc2\xc3\xc4\x00\x01
# RSSILevel - RSSI strength byte will be send after data on serial TXD
# Transfer Method - 

import serial
from Terpreter import Terpreter

# 77  - BaudRate(1) + PortMode(2) + AirRate(3) (default 9600, 8N1, 2.4)
                  # 0b11122333
BaudRate = {'1200':'0b00000000', \
            '2400':'0b00100000', \
            '4800':'0b01000000', \
            '9600':'0b01100000', \
           '19200':'0b10000000', \
           '38400':'0b10100000', \
           '57600':'0b11000000', \
          '115200':'0b11100000'}
PortMode = { '8N1':'0b00000000', \
             '8O1':'0b00001000', \
             '8E1':'0b00010000'}
AirRate =  { '0.3':'0b00000000', \
             '1.2':'0b00000001', \
             '2.4':'0b00000010', \
             '4.8':'0b00000011', \
             '9.6':'0b00000100', \
            '19.2':'0b00000101', \
            '38.4':'0b00000110', \
            '62.5':'0b00000111'}

# 88 - PacketSize(1) + ChannelNoise(2) + Reserved(3) + TxPower(4) (default 240, disabled, 22)
                          # 0b11233344
PacketSize =        {'240':'0b00000000', \
                     '128':'0b01000000', \
                      '64':'0b10000000', \
                      '32':'0b11000000'}
ChannelNoise = {'disabled':'0b00000000', \
                 'enabled':'0b00100000'}
TxPower =            {'22':'0b00000000', \
                      '17':'0b00000001', \
                      '13':'0b00000010', \
                      '10':'0b00000011'}

# AA - RSSILevel(1) + TransferMethod(2) + RelayMode(3) + LBT(4) + WORMode(5) + WORCycle(6)
                              #0b12345666
RSSILevel =       {'disabled':'0b00000000', \
                    'enabled':'0b10000000'}
TransferMode = {'transparent':'0b00000000', \
                      'fixed':'0b01000000'}
RelayMode =       {'disabled':'0b00000000', \
                    'enabled':'0b00100000'}
LBT =             {'disabled':'0b00000000', \
                    'enabled':'0b00010000'}
WORMode =      {'transmitter':'0b00000000', \
                   'receiver':'0b00001000'}
WORCycle =            { '500':'0b00000000', \
                       '1000':'0b00000001', \
                       '1500':'0b00000010', \
                       '2000':'0b00000011', \
                       '2500':'0b00000100', \
                       '3000':'0b00000101', \
                       '3500':'0b00000110', \
                       '4000':'0b00000111'}


def get_confreg(ser):
    # send cmd to get confreg settings
    # \xc1 - command header byte
    # \x00 - initial address byte
    # \x09 - length byte
    getcmd = b'\xc1\x00\x09'
    closecmd = b'\xc1\x80\x07'
    try:
        ser.write(getcmd)
        confreg = ser.read_until()
        ser.write(closecmd)
        closemsg = ser.read_until()
        if closemsg != b'\xc1\x80\x07\x00\x22\x19\x16\x0b\x00\x00':
            print("[*] Close Message Mismatch: ", closemsg)
            raise Exception
    except Exception as e:
          print("[*] get_confreg Error: ", e)
          exit(0)
    finally:
        ser.close()
        return confreg


def init_serial(comPort, baudrate):
    try:
        return serial.Serial(comPort, baudrate, timeout=2)
    except Exception as e:
        print("[*] Serial Port Error: ", e)
        exit(0)



def main():
    while True:
        try:
            text = input('sx126x> ')
        except EOFError:
            break
        if not text:
            continue
        terpreter = Terpreter(text)
        result = terpreter.expr()
        print(result)
    #s = init_serial("COM3", 9600)

    #print("[+] Retreiving Current Configuration Register Settings")
    #curr_confreg = get_confreg(s)
    #print("[+] Current Configuration Register Settings:")
    #print("".join("{:02x} ".format(c) for c in curr_confreg).upper())

if __name__ == "__main__":
    main()