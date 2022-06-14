import serial
import serial.tools.list_ports


# Buscamos obtener la dirección del puerto COM donde se conecto el segundo u-Blox
for port in serial.tools.list_ports.comports():
    if 'PID=0403:6015 SER=D200BZVHA' in str(port.hwid):
        Puerto_COM_2 = port.name
        print(port.hwid)
        print(port.name)
        print(port.description) 
        print(Puerto_COM_2)
        U_Blox = serial.Serial(str(Puerto_COM_2),115200, timeout=2, write_timeout=1)    

try:
    while(True):
        
        dato = U_Blox.readline()
        dato_string = dato.decode('utf-8')
        #dato_string = dato
        #dato_string = ''.join([str(item) for item in dato])
        print("Conversion de lista a string \n")
        print(dato_string)


        

except KeyboardInterrupt:
    U_Blox.close()
    print("Fin de la recolección de datos")
