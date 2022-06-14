import serial
import serial.tools.list_ports

try:

    # Buscamos obtener la dirección del puerto COM donde se conecto el primer u-Blox
    for port in serial.tools.list_ports.comports():
        if 'PID=0403:6015 SER=D200C017A' in str(port.hwid):
            Puerto_COM = port.name
            #print(port.hwid)
            #print(port.name)
            #print(port.description) 
            print(Puerto_COM)
            #Abrimos el puerto para poder obtener los datos
            U_Blox = serial.Serial(str(Puerto_COM),115200, timeout=2, write_timeout=1)

    # Buscamos obtener la dirección del puerto COM donde se conecto el segundo u-Blox
    for port in serial.tools.list_ports.comports():
        if 'PID=0403:6015 SER=D200BZVHA' in str(port.hwid):
            Puerto_COM_2 = port.name
            #print(port.hwid)
            #print(port.name)
            #print(port.description) 
            print(Puerto_COM_2)
            U_Blox = serial.Serial(str(Puerto_COM_2),115200, timeout=2, write_timeout=1)    
except:
    print('No se pudo establecer la comunicación serial, revise la conexión y intentelo nuevamente')

try:
    while(True):
        
        dato = U_Blox.readline()
        dato_string = dato.decode('utf-8')
        #dato_string = dato
        #dato_string = ''.join([str(item) for item in dato])
        print("Conversion de lista a string \n")
        print(dato_string)


        if ":CCF957966AC9" in dato_string:
        #Separamos los datos entregados por el U-Blox
            x = dato_string.split(",")
        #Convierto los valores numeros a enteros   
            RSSI_1p = int(x[1])
            Azimuth_angle = int(x[2])
            Elevation_angle = int(x[3])
            RSSI_2p = int(x[4])
            Adv_Channel = int(x[5])
            target = x[6]
        
        #Vemos los datos
            #Dato completo antes de dividir
            print(x) 
            #Valor numerico 
            print("RSSI_1p:",RSSI_1p)
            print("Azimuth_angle:",Azimuth_angle)
            print("Elevation_angle:",Elevation_angle)
            print("RSSI_2p:",RSSI_2p)
            print("Adv_Channel:",Adv_Channel)
            print("target identificado",target)

except KeyboardInterrupt:
    U_Blox.close()
    print("Fin de la recolección de datos")
