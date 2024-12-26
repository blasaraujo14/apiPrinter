### horizontal?????????? FWB
### vertical???????????? FWN

with open("cmdEZPL.txt", encoding="utf-8") as file:
    commands = file.readlines()

def getSize(c):
    if c == 'A':
        return 15
    if c == 'B':
        return 20
    if c == 'C':
        return 30
    if c == 'D':
        return 40
    else:
        return 25

currSize = 'X'
with open("cmdZPL.txt", "w") as zpl:
    zpl.write("^XA\n^FWR\n")
    for cmd in commands:
        aux = cmd.split(',')
        if cmd[0] == "A":
            if (cmd[1]!=currSize):
                currSize = cmd[1]
                zpl.write("^CF0," + str(getSize(currSize)) + "\n")
            zpl.write("^FO"+str(int(aux[1])-getSize(currSize))+','+aux[2]+"^FD"+ aux[7][:-1])
        elif cmd[0] == "L":
            zpl.write("^FO"+aux[1]+','+aux[2]+"^GB"+str(int(aux[3])-int(aux[1]))+",1,1")
        elif cmd[0] == "B":
            #ancho del codigo de barras
            zpl.write("^BY2,2,90^BC")
            #escribe el codigo
            zpl.write("^FO"+str(int(aux[1])-90)+','+aux[2]+"^FD"+aux[8][:-1])
        elif cmd[0] == "W":
            zpl.write("^BY2,2,1^BQR,2,5")
            "^FO100,550^BQN,2,20^FDQA,12345678^FS"
            try:
                zpl.write("^FO"+str(int(aux[0][1:])-200)+','+aux[1]+"^FDQ0"+aux[9][:-1])
            except:
                zpl.write("^FO"+str(int(aux[0][1:])-200)+','+aux[1]+"^FDQ0")
        else:
            continue
        zpl.write("^FS\n")
    zpl.write("^XZ")