import serial
import serial.tools.list_ports
import threading
import math
import csv
import time

#import signal  #Se suponía quería que la comunicación serial fuera silenciosa al finalizar el programa

exit_event = threading.Event()
mean_1 = 0
mean_2 = 0

def find_port(identf):
    """
        Esta función busca determinar el puerto serial que vamos a utilizar,
        se ingresa el identificador y si lo encuentra nos devuelve el nombre 
        del puerto al que esta conectado, de no ser así devuelve un 0. 
    """
    for port in serial.tools.list_ports.comports():
        if identf in str(port.hwid):
            return port.name

#Nombre de las antenas y los tag
ant_1 = 'PID=0403:6015 SER=D200C017A'
ant_2 = 'PID=0403:6015 SER=D200BZVHA'
tag_1 = ":CCF957966AC9"

#Revisión de la correcta conexión de las antenas
#print(find_port(ant_2))
#print(find_port(ant_1))

#Arreglo donde guardaremos los datos
gData_1 = []
gData_1.append([0.0])
gData_2 = []
gData_2.append([0.0])

#Abriendo los puertos
try:
    U_Blox_1 = serial.Serial(str(find_port(ant_1)),115200,timeout=2,write_timeout=1)
    U_Blox_2 = serial.Serial(str(find_port(ant_2)),115200,timeout=2,write_timeout=1)
except:
    U_Blox_1 = 0
    U_Blox_2 = 0

#Prueba de conexión con los puertos seriales
#print(U_Blox_1)
#print(U_Blox_2)

def CalculoAngulo(ang_1,ang_2):
    """
        Calculamos ambos ángulo formado entre las dos antenas y el tag
    """
    Alfa = 0.0
    Beta = 0.0
    if ang_1 > 0.0:
        #Caso 1: Ángulo 1 positivo y Ángulo 2 negativo
        if ang_2 < 0.0:
            Alfa = 90.0 - ang_1
            Beta = 90.0 + ang_2
            return Alfa,Beta
        #Caso 2:
        elif ang_2 > 0.0:
            Alfa = 90.0 - ang_1
            Beta = 90.0 + ang_2
            return Alfa,Beta
        #Caso 3:    
        elif ang_2 == 0.0:
            Alfa = 90.0 - ang_1
            Beta = 90.0
            return Alfa,Beta 
    #caso 4:
    elif ang_1 < 0.0:
        if ang_2 < 0.0:
            Alfa = 90.0 - ang_1
            Beta = 90.0 + ang_2
            return Alfa,Beta
    #Caso 5:
    elif ang_1 == 0.0:
        if ang_2 < 0.0:
            Alfa = 90.0
            Beta = 90.0 + ang_2
            return Alfa,Beta

def getData(U_Blox,out_data_Ang,tag,ant):
    """
        Recogemos del puerto serial las cadenas de caracteres para
        su posterior tratamiento, de momento solo estamos entregando
        el dato de ángulo de azimuth (Ángulo en la horizontal)
    """
    global mean_1
    global mean_2
    while True:
        line = U_Blox.readline().decode('utf-8')
        try:
            if tag in line:
                x = line.split(",")
                RSSI_1p = int(x[1])
                Azimuth_angle = int(x[2])
                Elevation_angle = int(x[3])
                RSSI_2p = int(x[4])
                Adv_Channel = int(x[5])
                target = x[6]
                #print(target)
                out_data_Ang[0].append(Azimuth_angle)
                if len(out_data_Ang[0]) > 15:
                    if ant == ant_1:
                        mean_1 = sum(out_data_Ang[0])/len(out_data_Ang[0])
                    if ant == ant_2:
                        mean_2 = sum(out_data_Ang[0])/len(out_data_Ang[0])
                    out_data_Ang[0].pop(0)
            #elif not tag in line:
            #    print("revisar si el tag está con bateria")
            #    print("tag no reconocido:",tag)
        except:
            print("Existe un error comunicate con Jocsan y espera lo mejor u.u")
            pass

def signal_handler(signum, frame):
    exit_event.set()

#Condición de conexión
if not U_Blox_1 or not U_Blox_2:
    Estado_Conexion = 0
else:
    Estado_Conexion = 1

if Estado_Conexion:
    dataCollector_1 = threading.Thread(target = getData, args = (U_Blox_1,gData_1,tag_1,ant_1))
    dataCollector_2 = threading.Thread(target = getData, args = (U_Blox_2,gData_2,tag_1,ant_2))
    dataCollector_1.start()
    dataCollector_2.start()

#signal.signal(signal.SIGINT, signal_handler)
#dataCollector_1.join()
#dataCollector_2.join()

else:
    print("No se pudo establecer conexión exitosamente, prueba nuevamente")
count = 0

try:    
    while Estado_Conexion: 
        #print("data antena 1")
        #print(gData_1)
        #print("data antena 2")
        #print(gData_2)
        x = (0.0,0.0)
        print("Alfa",x[0])
        print("Beta",x[1])
        print("Beta:",type(x))
        x = CalculoAngulo(mean_1,mean_2)
        print("Promedio de los datos obtenidos en la antena 1: ",mean_1,type(mean_1))
        print("Alfa:",x)
        #
        try:
            print("Alfa",x[0])
            print("Beta",x[1])
            #Distancia desde el punto C a A
            #con a definido como la distancia entre las dos antenas
            a = 70 #cm
            b = a * math.sin(x[0])/math.sin(180-x[1]-x[0]) # b=a*sin(beta)/sin(sigma)
            c = a * math.sin(x[1])/math.sin(180-x[1]-x[0]) # c=a*sin(alfa)/sin(sigma)
            l = a * (math.sin(x[0])*math.sin(x[1])) / math.sin(x[0]+x[1])      

            new = [x[0],x[1],[a],[c],[b]]
            count = count + 1

            #dataCollector_1.join()
            #dataCollector_2.join()
            #Los datos anteriores almacenados en un CSV
            File = open('example.csv','r')
            reader = File.readlines()
            File.close()

            File = open ('example.csv','w')
            File.writelines(reader)
            #csv.writer(File).writerow(reader)
            csv.writer(File,delimiter=';').writerow(new)
            File.close()

            time.sleep(0.1)

            #datos que se imprimen en pantalla
            print("numero de vez que pasa por aquí",count)
            print("La distancia desde la antena '2' al tag es:",b,"[cm]")
            print("La distancia desde la antena '1' al tag es:",c,"[cm]")
            print("la altura del triangulo h es:",l,"[cm]")

        except:
            pass
        #
        print("Promedio de los datos obtenidos en la antena 2: ",mean_2,type(mean_2))
        print("Beta:",type(x))
except KeyboardInterrupt:
    pass        

if Estado_Conexion:
    U_Blox_1.close()
    U_Blox_2.close()
print("Fin de la recolección de datos")