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

#Abrimos el puerto para poder obtener los datos
U_Blox = serial.Serial(str(Puerto_COM),115200, timeout=2, write_timeout=1)

try:
    while(True):
        dato = U_Blox.readline()
        dato = dato.decode('utf-8')
        print(dato)
except KeyboardInterrupt:
    U_Blox.close()
    print("Fin de la recolección de datos")
