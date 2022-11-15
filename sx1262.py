# CONFIGURATION REGISTER BYTES
# 11 22 33 44 55 66 77 88 99 AA BB CC
# -----------------------------------
# 11 - Command Header Byte
# 22 - Address Byte
# 33 - Length Byte
#
# 00h - Module Address High Byte (default 0)
# 01h - Module Address Low Byte (default 0)
# 02h - Network Address NETID (default 0)
# 03h - BaudRate + PortMode + AirRate (default 9600, 8N1, 2.4)
# 04h - PacketSize + ChannelNoise + TxPower (default 240, disabled, 22)
# 05h - ControlChannel (default 0x12 or 18 decimal))
# 06h - RSSILevel + TransferMethod + RelayMode + LBT + WORMode + WORCycle
#      (default disabled, transparent, disabled, disabled, WORTransmitter)
# 07h - Crypt Key High Byte (default 0)
# 08h - Crypt Key Low Byte (default 0)
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

# 03H
BaudRate = {'1200':0b00000000, \
            '2400':0b00100000, \
            '4800':0b01000000, \
            '9600':0b01100000, \
            '19200':0b10000000, \
            '38400':0b10100000, \
            '57600':0b11000000, \
            '115200':0b11100000}
PortMode = { '8N1':0b00000000, \
                '8O1':0b00001000, \
                '8E1':0b00010000}
AirRate =  { '0.3':0b00000000, \
                '1.2':0b00000001, \
                '2.4':0b00000010, \
                '4.8':0b00000011, \
                '9.6':0b00000100, \
            '19.2':0b00000101, \
            '38.4':0b00000110, \
            '62.5':0b00000111}

# 04h - PacketSize(1) + ChannelNoise(2) + Reserved(3) + TxPower(4) (default 240, disabled, 22)
                        # 0b11233344
PacketSize =        {'240':0b00000000, \
                        '128':0b01000000, \
                        '64':0b10000000, \
                        '32':0b11000000}
ChannelNoise = {'disabled':0b00000000, \
                    'enabled':0b00100000}
TxPower =            {'22':0b00000000, \
                        '17':0b00000001, \
                        '13':0b00000010, \
                        '10':0b00000011}

# 06h - RSSILevel(1) + TransferMethod(2) + RelayMode(3) + LBT(4) + WORMode(5) + WORCycle(6)
                            #0b12345666
RSSILevel =       {'disabled':0b00000000, \
                    'enabled':0b10000000}
TransferMode = {'transparent':0b00000000, \
                        'fixed':0b01000000}
RelayMode =       {'disabled':0b00000000, \
                    'enabled':0b00100000}
Lbt =             {'disabled':0b00000000, \
                    'enabled':0b00010000}
WORMode =      {'transmitter':0b00000000, \
                    'receiver':0b00001000}
WORCycle =            { '500':0b00000000, \
                        '1000':0b00000001, \
                        '1500':0b00000010, \
                        '2000':0b00000011, \
                        '2500':0b00000100, \
                        '3000': 0b00000101, \
                        '3500': 0b00000110, \
                        '4000': 0b00000111}

class sx1262():
    # 03h  - BaudRate(1) + PortMode(2) + AirRate(3) (default 9600, 8N1, 2.4)
                    # 0b11122333

    def __init__(self):
        # 00H High Address
        addh = 0b00000000
        self.x00h = hex(addh)
        # 01H Low Address
        addl = 0b00000000
        self.x01h = hex(addl)
        # 02H Network Address
        netid = 0b00000000
        self.x02h = hex(netid)
        # 03H 
        self.x03h = hex(BaudRate['9600'] + PortMode['8N1'] + AirRate['2.4'])
        # 04H
        self.x04h = hex(PacketSize['240'] + ChannelNoise['disabled'] + TxPower['22'])
        # 05H Control Channel
        channel = 0b00010010
        self.x05h = hex(channel)
        # 06H
        self.x06h = hex(RSSILevel['disabled'] + TransferMode['transparent'] + RelayMode['disabled'] \
                        + Lbt['disabled'] + WORMode['transmitter'] + WORCycle['2000'])
        # 07H - KeyHigh
        self.x07h = hex(0b00000000)
        # 08H - KeyLow
        self.x08h = hex(0b00000000)
        # Sync
        self.sync = False
        # Connection Settings
        self.commport = None
        self.baudrate = "9600"

    def set_radio_confreg(self):
        # 00H High Address
        x00h = input("Address High Byte (0x00): ")
        if x00h == None: self.x00h = hex(0b00000000)
        
        # 01H Low Address
        x01h = input("Address Low Byte (0x00): ")
        if x01h == None: self.x01h = hex(0b00000000)
        
        # 02H NETID
        x02h = input("Network ID (0x00): ")
        if x02h == None: self.x02h = hex(0b00000000)
        
        # 03H Baudrate
        print("Baudrate (9600)")
        for k in BaudRate.keys(): print(k, '--', BaudRate[k])
        try: x03h_baudrate = int(input("Enter Selection Number: "))
        except: print("[-] Error: Please enter a number")

        # 03H Portmode
        print("PortMode (240)")
        for k in PortMode.keys(): print(k, '--', PortMode[k])
        try: x03h_portmode = int(input("Enter Selection Number: "))
        except: print("[-] Error: Please enter a number")

        # 03H Air Rate
        print("Air Rate (2.4)")
        for k in AirRate.keys(): print(k, '--', AirRate[k])
        try: x03h_airrate = int(input("Enter Selection Number: "))
        except: print("[-] Error: Please enter a number")

        # 04H Packet Size
        print("Packet Size (240): ")
        for k in PacketSize.keys(): print(k, '--', PacketSize[k])

        # 04H Channel Noise
        print("Channel Noise (disabled)")
        for k in ChannelNoise.keys(): print(k, '--', ChannelNoise[k])

        # 04H Transmit Power
        print("Transmit Power (22)")
        for k in TxPower.keys(): print(k, '--', TxPower[k])

        # 05H Control Channel
        print("Control Channel (18): ")

        # 06H RSSI level
        print("RSSI Level")
        for k in RSSILevel.keys(): print(k, '--', RSSILevel[k])

        # 06H Transfer Mode
        print("Transfer Mode")
        for k in TransferMode.keys(): print(k, '--', TransferMode[k])

        # 06H Relay Mode
        print("Relay Mode")
        for k in RelayMode.keys(): print(k, '--', RelayMode[k])

        # 06H LBT
        print("LBT")
        for k in Lbt.keys(): print(k, '--', Lbt[k])

        # 06H WOR Mode
        print("WOR Mode")
        for k in WORMode.keys(): print(k, '--', WORMode[k])

        # 06H WOR Cycle
        print("WOR Cycle")
        for k in WORCycle.keys(): print(k, '--', WORCycle[k])

        # 07H Key High
        print("Crypto Key High")

        # 08H Key Low
        print("Crypto Key Low")


    def get_radio_confreg(self):
        # Return a Dictionary with all the confreg settings 

        if self.sync == False:
            print("[!] Settings have not been retrieved from Radio - Please sync with your radio")
            return None
        else:
            high_addr = self.x00h
            low_addr = self.x01h
            netid = self.x02h
            bz = f'{int(self.x03h, 16):0>8b}'
            baudrate = [k for k, v in BaudRate.items() if v == int(bz[:3], 2) << 5]
            portmode = [k for k, v in PortMode.items() if v == int(bz[3:5], 2) << 3]
            airrate = [k for k, v in AirRate.items() if v == int(bz[5:], 2)]
            bz = f'{int(self.x04h, 16):0>8b}'
            packetsize = [k for k, v in PacketSize.items() if v == int(bz[:2], 2) << 6]
            channelnoise = [k for k, v in ChannelNoise.items() if v == int(bz[2:3], 2) << 5]
            txpower = [k for k, v in TxPower.items() if v == int(bz[6:], 2)]
            controlchannel = self.x05h
            bz = f'{int(self.x06h, 16):0>8b}'
            rssilevel = [k for k, v in RSSILevel.items() if v == int(bz[:1], 2) << 7]
            transfermode = [k for k, v in TransferMode.items() if v == int(bz[1:2], 2) << 6]
            relaymode = [k for k, v in RelayMode.items() if v == int(bz[2:3], 2) << 5]
            lbt = [k for k, v in Lbt.items() if v == int(bz[3:4], 2) << 4]
            wormode = [k for k, v in WORMode.items() if v == int(bz[4:5], 2) << 3]
            worcycle = [k for k, v in WORCycle.items() if v == int(bz[5:], 2)]
            keyhigh = self.x07h
            keylow = self.x08h

            return({'High Address' : high_addr, \
                'Low Address' : low_addr, \
                'Network ID' : netid, \
                'Baudrate ' : baudrate, \
                'Port Mode' : portmode, \
                'Air Rate' : airrate, \
                'Packet Size' : packetsize, \
                'Channel Noise' : channelnoise, \
                'Transmit Power' : txpower, \
                'Control Channel' : controlchannel, \
                'RSSI Level' : rssilevel, \
                'Transfer Mode' : transfermode, \
                'Relay Mode' : relaymode, \
                'LBT' : lbt, \
                'WOR Mode' : wormode, \
                'WOR Cycle' : worcycle, \
                'Crypto High Byte' : keyhigh, \
                'Crypto Low Byte' : keylow })
    
    def download_radio_confreg(self, ser):
        # Retreive radio's confreg settings over serial port

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
            print("".join("{:02x} ".format(c) for c in confreg).upper())
            split = [confreg[i] for i in range(0, len(confreg))]
            self.x00h = hex(split[3])
            self.x01h = hex(split[4])
            self.x02h = hex(split[5])
            self.x03h = hex(split[6])
            self.x04h = hex(split[7])
            self.x05h = hex(split[8])
            self.x06h = hex(split[9])
            self.x07h = hex(split[10])
            self.x08h = hex(split[11])
            self.sync = True
        except Exception as e:
            print("[*] get_confreg Error: ", e)
            self.sync = False
        finally:
            ser.close()

    def upload_radio_confreg(self, ser):
        # Send new confreg to the Radio over serial

        # send cmd to set confreg settings
        # \xc0 - command header byte
        # \x00 - initial address byte
        # \x09 - length byte
        setcmd = b'\xc1\x00\x09'
