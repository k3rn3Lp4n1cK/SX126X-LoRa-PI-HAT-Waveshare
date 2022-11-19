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
import time

class sx1262():

    # 03H
    BAUDRATE = {'1200':0b00000000, \
                '2400':0b00100000, \
                '4800':0b01000000, \
                '9600':0b01100000, \
               '19200':0b10000000, \
               '38400':0b10100000, \
               '57600':0b11000000, \
              '115200':0b11100000}

    PORTMODE = { '8N1':0b00000000, \
                 '8O1':0b00001000, \
                 '8E1':0b00010000}

    AIRRATE = { '0.3':0b00000000, \
                '1.2':0b00000001, \
                '2.4':0b00000010, \
                '4.8':0b00000011, \
                '9.6':0b00000100, \
               '19.2':0b00000101, \
               '38.4':0b00000110, \
               '62.5':0b00000111}

    # 04h - PacketSize(1) + ChannelNoise(2) + Reserved(3) + TxPower(4) (default 240, disabled, 22)
    PACKETSIZE = {'240':0b00000000, \
                  '128':0b01000000, \
                   '64':0b10000000, \
                   '32':0b11000000}

    CHANNELNOISE = {'disabled':0b00000000, \
                    'enabled':0b00100000}

    TXPOWER = {'22':0b00000000, \
               '17':0b00000001, \
               '13':0b00000010, \
               '10':0b00000011}

    # 06h - RSSILevel(1) + TransferMethod(2) + RelayMode(3) + LBT(4) + WORMode(5) + WORCycle(6)
    RSSILEVEL = {'disabled':0b00000000, \
                  'enabled':0b10000000}

    TRANSFERMODE = {'transparent':0b00000000, \
                          'fixed':0b01000000}

    RELAYMODE = {'disabled':0b00000000, \
                  'enabled':0b00100000}

    LBT = {'disabled':0b00000000, \
            'enabled':0b00010000}

    WORMODE = {'transmitter':0b00000000, \
                  'receiver':0b00001000}

    WORCYCLE = { '500':0b00000000, \
                '1000':0b00000001, \
                '1500':0b00000010, \
                '2000':0b00000011, \
                '2500':0b00000100, \
                '3000': 0b00000101, \
                '3500': 0b00000110, \
                '4000': 0b00000111}

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
        self.x03h = hex(self.BAUDRATE['9600'] + self.PORTMODE['8N1'] + self.AIRRATE['2.4'])
        # 04H
        self.x04h = hex(self.PACKETSIZE['240'] + self.CHANNELNOISE['disabled'] + self.TXPOWER['22'])
        # 05H Control Channel
        channel = 0b00010010
        self.x05h = hex(channel)
        # 06H
        self.x06h = hex(self.RSSILEVEL['disabled'] + self.TRANSFERMODE['transparent'] + self.RELAYMODE['disabled'] \
                        + self.LBT['disabled'] + self.WORMODE['transmitter'] + self.WORCYCLE['2000'])
        # 07H - KeyHigh
        self.x07h = hex(0b00000000)
        # 08H - KeyLow
        self.x08h = hex(0b00000000)
        # Sync
        self.sync = False
        # Connection Settings
        self.commport = "/dev/ttyS0"
        self.baudrate = "9600"

    def send_message(self, ser, msg):
        try:
            b = bytes(msg, 'utf-8')
            ser.write(b)
            time.sleep(.2)
            ret = ser.readlines()
        except Exception as e:
            print("[*] send_message Error: ", e)
        finally:
            ser.close()

    def rcv_message(self, ser):
        try:
            data = ser.read_until()
            print(data.decode("utf-8"))
        except Exception as e:
            print("[*] rcv_message Error: ", e)
        finally:
            ser.close()

    def show_radio_confreg(self):
        # Return a Dictionary with all the confreg settings 

        if self.sync == False:
            print("[!] Settings have not been retrieved from Radio")
            return None
        else:
            high_addr = self.x00h
            low_addr = self.x01h
            netid = self.x02h
            bz = f'{int(self.x03h, 16):0>8b}'
            baudrate = [k for k, v in self.BAUDRATE.items() if v == int(bz[:3], 2) << 5]
            portmode = [k for k, v in self.PORTMODE.items() if v == int(bz[3:5], 2) << 3]
            airrate = [k for k, v in self.AIRRATE.items() if v == int(bz[5:], 2)]
            bz = f'{int(self.x04h, 16):0>8b}'
            packetsize = [k for k, v in self.PACKETSIZE.items() if v == int(bz[:2], 2) << 6]
            channelnoise = [k for k, v in self.CHANNELNOISE.items() if v == int(bz[2:3], 2) << 5]
            txpower = [k for k, v in self.TXPOWER.items() if v == int(bz[6:], 2)]
            controlchannel = self.x05h
            bz = f'{int(self.x06h, 16):0>8b}'
            rssilevel = [k for k, v in self.RSSILEVEL.items() if v == int(bz[:1], 2) << 7]
            transfermode = [k for k, v in self.TRANSFERMODE.items() if v == int(bz[1:2], 2) << 6]
            relaymode = [k for k, v in self.RELAYMODE.items() if v == int(bz[2:3], 2) << 5]
            lbt = [k for k, v in self.LBT.items() if v == int(bz[3:4], 2) << 4]
            wormode = [k for k, v in self.WORMODE.items() if v == int(bz[4:5], 2) << 3]
            worcycle = [k for k, v in self.WORCYCLE.items() if v == int(bz[5:], 2)]
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
            time.sleep(.5)
            confreg = ser.read_until()
            ser.write(closecmd)
            time.sleep(.5)
            closemsg = ser.read_until()
            if closemsg != b'\xc1\x80\x07\x00\x22\x19\x16\x0b\x00\x00':
                print("[*] Close Message Mismatch: ", closemsg)
                raise Exception
            if confreg == None or confreg == b'':
                print("[*] No data received from Radio")
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
            print("[*] download_radio_confreg Error: ", e)
            self.sync = False
        finally:
            ser.close()

    def upload_radio_confreg(self, ser, x00, x01, x02, x03b, x03p, x03a, x04p, x04c, x04t, x05, x06l, x06t, x06r, x06b, x06w, x06c, x07, x08):
        # Send new confreg to the Radio over serial
        # send cmd to set confreg settings
        # \xc0 - command header byte
        # \x00 - initial address byte
        # \x09 - length byte
        cmd = bytearray(b'\xc0\x00\x09')
        
        # 00H High Address
        cmd.append(int(x00))
        
        # 01H Low Address
        cmd.append(int(x01))
        
        # 02H Network Address
        cmd.append(int(x02))
        
        # 03H 
        x03 = hex(self.BAUDRATE[x03b] + self.PORTMODE[x03p] + self.AIRRATE[x03a])
        cmd.append(int(x03, 16))
        
        # 04H
        x04 = hex(self.PACKETSIZE[x04p] + self.CHANNELNOISE[x04c] + self.TXPOWER[x04t])
        cmd.append(int(x04, 16))
        
        # 05H Control Channel
        cmd.append(int(x05))

        # 06H
        x06 = hex(self.RSSILEVEL[x06l] + self.TRANSFERMODE[x06t] + \
                self.RELAYMODE[x06r] + self.LBT[x06b] + self.WORMODE[x06w] + \
                self.WORCYCLE[x06c])
        cmd.append(int(x06, 16))
        
        # 07H - KeyHigh
        cmd.append(int(x07))
        
        # 08H - KeyLow
        cmd.append(int(x08))
        
        print("[+] Sending new Configuration Register", flush=True)
        print(' '.join(['{:02X}'.format(x) for x in cmd]), flush=True)
        try:
            ser.write(bytes(cmd))
            time.sleep(.5)
            ret = ser.read_until()
            print("[+] Return value: ", ret)
        except Exception as e:
            print("[*] upload_radio_confreg Error: ", e)
        finally:
            ser.close()
