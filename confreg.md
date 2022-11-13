# Configuration Registers

| Register Address | Read/Write | Name | Describe ||||| Comments |
| 00H | Read / Write | ADDH | ADDH (default 0) ||||| The high byte and low byte of the module address. Note: When the module address is equal to FFFF, it can be used as the broadcast and listening address, and the module will no longer perform address filtering. |
| 01H | Read / Write | ADDL ADDL (default 0) ||||| ^ |
| 02H | Read / Write | NETID | NETID (default 0) ||||| Network address, used to distinguish the network, when communicating with each other, it should be set to the same |
| 03H | Read / Write | REG0 | 7 | 6 | 5 | UART Serial rate (bps) | For the two modules that communicate with each other, the serial port baud rate can be different, and the verification method can also be different; when transmitting large data packets continuously, the user needs to consider the data blockage caused by the same baud rate, and may even be lost; it is generally recommended to communicate Both sides have the same baud rate |
| ^ | ^ | ^ | 0 | 0 | 0 | Baud Rate 1200 | ^ |
| ^ | ^ | ^ | 0 | 0 | 1 | Baud Rate 2400 | ^ |
| ^ | ^ | ^ | 0 | 1 | 0 | Baud Rate 4800 | ^ | 
| ^ | ^ | ^ | 0 | 1 | 1 | Baud Rate 9600 (default) | ^ |
| ^ | ^ | ^ | 1 | 0 | 0 | Baud Rate 19200 | ^ |
| ^ | ^ | ^ | 1 | 0 | 1 | Baud Rate 38400 | ^ |
| ^ | ^ | ^ | 1 | 1 | 0 | Baud Rate 57600 | ^ |
| ^ | ^ | ^ | 1 | 1 | 1 | Baud Rate 115200 | ^ |
| ^ | ^ | ^ || 4 | 3 | Port Mode | The serial port mode of both sides of the communication can be different |
| ^ | ^ | ^ || 0 | 0 | 8N1 | ^ |
| ^ | ^ | ^ || 0 | 1 | 8O1 | ^ |
| ^ | ^ | ^ || 1 | 0 | 8E1 | ^ |
| ^ | ^ | ^ || 1 | 1 | 8N1 00 | ^ |
| ^ | ^ | ^ | 2 | 1 | 0 | Wireless AirRate (bps) | The air rate of both parties must be the same; the higher the air rate, the smaller the delay and the shorter the transmission distance |
| ^ | ^ | ^ | 0 | 0 | 0 | 0.3 | ^ |
| ^ | ^ | ^ | 0 | 0 | 1 | 1.2 | ^ |
| ^ | ^ | ^ | 0 | 1 | 0 | 2.4 (default) | ^ |
| ^ | ^ | ^ | 0 | 1 | 1 | 4.8K | ^ |
| ^ | ^ | ^ | 1 | 0 | 0 | 9.6K | ^ |
| ^ | ^ | ^ | 1 | 0 | 1 | 19.2K | ^ |
| ^ | ^ | ^ | 1 | 1 | 0 | 38.4K | ^ |
| ^ | ^ | ^ | 1 | 1 | 1 | 92.5K | ^ |
| 04H | Read / Write | REG0 || 7 | 6 | Packet Length (bytes) | If the data sent by the user is less than the sub-packet length, the serial port output at the receiving end will appear as uninterrupted continuous output; if the data sent by the user is greater than the sub-packet length, the serial port on the receiving end will be output in sub-packets |
| ^ | ^ | ^ || 0 | 0 | 240 (default) | ^ |
| ^ | ^ | ^ || 0 | 1 | 128 | ^ |
| ^ | ^ | ^ || 1 | 0 | 64 | ^ |
| ^ | ^ | ^ || 1 | 1 | 32 | ^ |
| ^ | ^ | ^ ||| 5 | Ambient Noise | After enabling, you can send the command C0 C1 C2 C3 to read the register in transmission mode or WOR transmission mode; register 0x00: current environmental noise RSSI; register 0x01: RSSI when data was received last time (current channel noise is: dBm =-(256 -RSSI); command format: C0 C1 C2 C3 + start address + read length; return format: C1 + address + read length + read valid value; such as: send C0 C1 C2 C3 00 01 return C1 00 01 RSSI ( Addresses can only start from 00)
| ^ | ^ | ^ ||| 0 | disabled (default) | ^ |
| ^ | ^ | ^ ||| 1 | enable | ^ |
| ^ | ^ | ^ | 4 | 3 | 2 | reserve | Reserved for Future use |
| ^ | ^ | ^ || 1 | 0 | Tx Power | The relationship between power and current is non-linear. When the power is maximum, the efficiency of the power supply is the highest; the current will not decrease in the same proportion as the power decreases.
| ^ | ^ | ^ || 0 | 0 | 22dBm (default) | ^ |
| ^ | ^ | ^ || 0 | 1 | 17dBm | ^ |
| ^ | ^ | ^ || 1 | 0 | 13dBm | ^ |
| ^ | ^ | ^ || 1 | 1 | 10dBm | ^ |
| 05H | Read / Write | REG2 |||| Channel Control | 0-83 represents a total of 84 channels, respectively. Actual Frequency = 410.125 + CH *1MHz，default433.125MHz or 850.125+CH*1MHz,default868.125MHz |
| 06H | Read / Write | REG3 ||| 7 | RSSI Bytes | When enabled, the module receives wireless data and outputs it through the serial port TXD, followed by an RSSI strength byte. |
| ^ | ^ | ^ ||| 0 | disabled (default) | ^ |
| ^ | ^ | ^ ||| 1 | enable | ^ |
| ^ | ^ | ^ ||| 6 | Transfer Mode | During fixed-point transmission, the module will recognize the first three bytes of the serial port data as: address high + address low + channel, and use it as the wireless transmission target |
| ^ | ^ | ^ ||| 0 | Transparent (default) | ^ |
| ^ | ^ | ^ ||| 1 | Fixed Point | ^ |
| ^ | ^ | ^ ||| 5 | Relay Mode | After the relay function is enabled, if the destination address is not the module itself, the module will start a forwarding; in order to prevent data backhaul, it is recommended to use it with the fixed-point mode; that is, the destination address and the source address are different |
| ^ | ^ | ^ ||| 0 | disabled (default) | ^ |
| ^ | ^ | ^ ||| 2 | enable | ^ |
| ^ | ^ | ^ ||| 4 | LBT Mode | After enabling, the wireless data will be monitored before transmission, which can avoid interference to a certain extent, but may cause data delay; the maximum stay time of LBT is 2 seconds, and it will be sent out forcibly when it reaches two seconds |
| ^ | ^ | ^ ||| 0 | disabled (default) | ^ |
| ^ | ^ | ^ ||| 2 | enable | ^ |
| ^ | ^ | ^ ||| 3 | WOR Mode | Only valid for mode 1; after the WOR receiver receives the wireless data and outputs it through the serial port, it will wait for 1000ms before entering WOR again. During this period, the user can input the serial port data and return it through the wireless; each serial port byte will be refreshed for 1000ms time ; The user must initiate the first byte within 1000ms |
| ^ | ^ | ^ ||| 0 | WOR transmitter (default) module transceiver is turned on, and when transmitting data, a wake-up code for a certain period of time is added | ^ |
| ^ | ^ | ^ ||| 1 | WOR receiver. The module cannot transmit data, and it works in WOR monitoring mode, which can save a lot of power consumption |
| ^ | ^ | ^ | 2 | 1 | 0 | WOR Cycle | Only valid for mode 1; period T= (1+WOR)*500ms, maximum 4000ms, minimum 500ms; The longer the WOR monitoring interval period, the lower the average power consumption, but the greater the data delay; the sender and receiver must be consistent (very important) |
| ^ | ^ | ^ | 0 | 0 | 0 | 500ms | ^ |
| ^ | ^ | ^ | 0 | 0 | 0 | 1000ms | ^ |
| ^ | ^ | ^ | 0 | 0 | 0 | 1500ms | ^ |
| ^ | ^ | ^ | 0 | 0 | 0 | 2000ms | ^ |
| ^ | ^ | ^ | 0 | 0 | 0 | 2500ms | ^ |
| ^ | ^ | ^ | 0 | 0 | 0 | 3000ms | ^ |
| ^ | ^ | ^ | 0 | 0 | 0 | 3500ms | ^ |
| ^ | ^ | ^ | 0 | 0 | 0 | 4000ms | ^ |
| 07H | Write | CRYPT_H |||| Key High Byte (default 0) | Write-only, read returns 0; used for encryption to avoid interception of wireless data in the air by similar modules; the module will use these two bytes as calculation factors to transform and encrypt wireless wireless signals in the air |
| 08H | Write | CRYPT_L |||| Key Low Byte (default 0) | ^ |
| 80H ~ 86H | Read | PID |||| Product Information 7 Bytes | Product Information 7 Bytes |