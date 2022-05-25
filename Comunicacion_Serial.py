import serial
import serial.tools.list_ports

# Buscamos obtener la dirección del puerto COM donde se conecto el u-Blox
for port in serial.tools.list_ports.comports():
    if 'PID=0403:6015 SER=D200C017A' in str(port.hwid):
        Puerto_COM = port.name
    #print(port.hwid)
    #print(port.name)
    #print(port.description) 
print(Puerto_COM)