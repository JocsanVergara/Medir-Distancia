import csv

prueba = ['Prueba distancia 1'];
header = ['angulo Ant.1','angulo Ant.2','distancia entre Ant.1 y Ant.2','distancia Ant.1 al tag','distancia Ant.2 al tag']
new = ['1','10','24','54','2']

#Datos de salida que me permitan visualizar los datos
            #data = {
            #    'ángulo Ant.1':[x[0]],
            #    'ángulo Ant.2':[x[1]],
            #    'distancia entre Ant.1 y Ant.2':[a],
            #    'distancia Ant.1 al tag':[c],
            #    'distancia Ant.2 al tag':[b],
            #}

            #df = pd.DataFrame(data, columns = ['ángulo Ant.1','ángulo Ant.2','distancia entre Ant.1 y Ant.2','distancia Ant.1 al tag','distancia Ant.2 al tag'])
            #df.to_csv('prueba.csv')

with open('example.csv','w',newline='') as f:
    write = csv.writer(f,delimiter=';')
    write.writerow(prueba)
    write.writerow(header)


File = open('example.csv','r')
reader = File.readlines()
File.close()

File = open ('example.csv','w')
File.writelines(reader)
csv.writer(File,delimiter=';').writerow(new)
File.close()


with open('example.csv',newline='') as File:
    reader = csv.reader(File)
    for row in reader:
        print(row)

File = open('example.csv','r')
reader = File.readlines()
File.close()

File = open ('example.csv','w')
File.writelines(reader)
csv.writer(File,delimiter=';').writerow(new)
File.close()


with open('example.csv',newline='') as File:
    reader = csv.reader(File)
    for row in reader:
        print(row)

File = open('example.csv','r')
reader = File.readlines()
File.close()

File = open ('example.csv','w')
File.writelines(reader)
csv.writer(File,delimiter=';').writerow(new)
File.close()


with open('example.csv',newline='') as File:
    reader = csv.reader(File)
    for row in reader:
        print(row)
