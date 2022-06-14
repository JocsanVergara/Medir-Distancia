from cmath import sin
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
            U_Blox_2 = serial.Serial(str(Puerto_COM_2),115200, timeout=2, write_timeout=1)    
except:
    print('No se pudo establecer la comunicación serial, revise la conexión y intentelo nuevamente')

try:
    while(True):
        
        #Antena 1
        dato = U_Blox.readline()
        dato_string = dato.decode('utf-8')
        print("Antena 1 \n")
        print(dato_string)

        #Antena 2
        dato_2 = U_Blox_2.readline()
        dato_string_2 = dato_2.decode('utf-8')
        print("Antena_2 \n")
        print(dato_string_2)

        #Antena 1
        #target 1
        if ":CCF957966AC9" in dato_string:
        #Separamos los datos entregados por el U-Blox
            x_1 = dato_string.split(",")
        #Convierto los valores numeros a enteros   
            RSSI_1p_1 = int(x_1[1])
            Azimuth_angle_1 = int(x_1[2])
            Elevation_angle_1 = int(x_1[3])
            RSSI_2p_1 = int(x_1[4])
            Adv_Channel_1 = int(x_1[5])
            target_1 = x_1[6]
        
        #Antena 2
        #target 2
        if ":CCF957966AC9" in dato_string_2:
        #Separamos los datos entregados por el U-Blox
            x_2 = dato_string_2.split(",")
        #Convierto los valores numeros a enteros   
            RSSI_1p_2 = int(x_2[1])
            Azimuth_angle_2 = int(x_2[2])
            Elevation_angle_2 = int(x_2[3])
            RSSI_2p_2 = int(x_2[4])
            Adv_Channel_2 = int(x_2[5])
            target_2 = x_2[6]
        
        #Vemos los datos
            #Antena 1
            #Dato completo antes de dividir
            print(x_1) 
            #Valor numerico 
            print("RSSI_1p:",RSSI_1p_1)
            print("Azimuth_angle:",Azimuth_angle_1)
            print("Elevation_angle:",Elevation_angle_1)
            print("RSSI_2p:",RSSI_2p_1)
            print("Adv_Channel:",Adv_Channel_1)
            print("target identificado",target_1)

            #Antena 2
            #Dato completo antes de dividir
            print(x_2) 
            #Valor numerico 
            print("RSSI_1p:",RSSI_1p_2)
            print("Azimuth_angle:",Azimuth_angle_2)
            print("Elevation_angle:",Elevation_angle_2)
            print("RSSI_2p:",RSSI_2p_2)
            print("Adv_Channel:",Adv_Channel_2)
            print("target identificado",target_2)

#Comenzamos con el tema de los calculos
#Calculos en el eje horizontal
            d_BC_h = 100 #cm        #Distancia desde la antena 1 (B) a la antena 2 (C)
            d_BA_h = d_BC_h * sin(Azimuth_angle_2)/sin(180-Elevation_angle_2-Elevation_angle_1) #Distancia entre la antena 1 (B) y el objetivo (A)
            d_CA_h = d_BC_h * sin(Azimuth_angle_1)/sin(180-Elevation_angle_2-Elevation_angle_1) #Distancia entre la antena 2 (C) y el objetivo (A)
            l_h = d_BC_h * (sin(Azimuth_angle_1)*sin(Azimuth_angle_2))/(sin(Azimuth_angle_1+Azimuth_angle_2))

#A los angulos debes sumarle 90° y multiplicarlo por -1 así debería funcionar bien




except KeyboardInterrupt:
    U_Blox.close()
    print("Fin de la recolección de datos")
