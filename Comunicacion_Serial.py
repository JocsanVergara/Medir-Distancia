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
        dato_string = dato.decode('utf-8')
        #dato_string = dato
        #dato_string = ''.join([str(item) for item in dato])
        print("Conversion de lista a string \n")
        print(dato_string)


        if ":CCF957966AC9" in dato_string:
        #Separamos los datos entregados por el U-Blox
            x = dato_string.split(",")
            RSSI_1p = x[1]
            Azimuth_angle = x[2]
            Elevation_angle = x[3]
            RSSI_2p = x[4]
            Adv_Channel = x[5]
        
        #     #Vemos los datos
            print(x)
            #print(dato)
            print("RSSI_1p:",RSSI_1p)
            print("Azimuth_angle:",Azimuth_angle)
            print("Elevation_angle:",Elevation_angle)
            print("RSSI_2p:",RSSI_2p)
            print("Adv_Channel:",Adv_Channel)

except KeyboardInterrupt:
    U_Blox.close()
    print("Fin de la recolección de datos")
