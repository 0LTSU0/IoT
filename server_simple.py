from os import close
import socket
import time

HOST = '192.168.1.6' #own ip
PORT = 65432        #own port

HOSTRASPB = '192.168.1.2' #Raspberry ip
PORTRASPB = 65431 #Raspberry port

filnum = 0

def main():
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Socket for phone app
    sock.bind((HOST, PORT))
    sock.listen()
    conn, addr = sock.accept()
    
    global filnum # these were used to collect sample data
    filnum += 1

    #filename = "data" + str(filnum) + ".txt"
    f = open("serverLOG_Simple.txt", "a")

    zvals = []
    vn = - 1
    ignorecounter = 0
    susopen = False
    susclose = False
    openorclose = False
    prev = "close"

    with conn:
        print('Connected by', addr)
        while True:
            sock.listen()
            data = conn.recv(1024)
            if data:
                decoded = data.decode(encoding='utf-8')
                decoded = decoded.strip("()")
                
                # If stop button was pressed, reset everything to be ready for new connection 
                if decoded == "STOP":
                    print(addr, ' disconnected')
                    packet = bytes("STOP", encoding='utf-8')
                    sock2.sendall(packet)
                    sock.close()
                    f.close()
                    main()

                datas = decoded.split(",")
                
                # After sensing open / close, must have a short ignore time for values, otherwise might produce nonsense results
                if ignorecounter > 20:
                    openorclose = False

                if openorclose == False:
                    if datas[2] != " None":
                        zvals.append(float(datas[2].strip(" ")))

                    #print(zvals)
                    #print(vn)
                    if len(zvals) > 2:
                        
                        # Suspect opening or closing based on data
                        if susopen == False and susclose == False:
                            if zvals[vn] - zvals[vn-1] > 0.65:
                                susopen = True
                                vn_on_sus = vn
                                #print("susopen")

                            elif zvals[vn] - zvals[vn-1] < -0.65:
                                susclose = True
                                vn_on_sus = vn
                                #print("susclose")
                        
                        # When suspecting door opening, check if actually happened
                        if susopen:
                            if max(zvals) - min(zvals) > 2:
                                if prev == "close":
                                    prev = "open"
                                    raspsend("open", sock2)
                                    f.write("Lights turned on at {} \n".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
                                elif prev == "open":
                                    prev = "close"
                                    raspsend("close", sock2)
                                    f.write("Lights turned off at {} \n".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
                                zvals = []
                                vn = -1
                                ignorecounter = 0
                                susopen = False
                                susclose = False
                                openorclose = True

                        #No need for closing handling

                        # If opening not found within 20 next data transmissions, or closing in 10, reset
                        if ((susopen and (vn - vn_on_sus > 20)) or (susclose and (vn - vn_on_sus > 10))):
                            zvals = []
                            vn = -1
                            ignorecounter = 0
                            susopen = False
                            susclose = False
                        
                    vn += 1
                ignorecounter += 1
                
                
def raspsend(function, soc):
    if function == "close":
        print("close")
        packet = bytes("close", encoding='utf-8')
        soc.sendall(packet)
    else:
        print("open")
        packet = bytes("open", encoding='utf-8')
        soc.sendall(packet)

sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Socket for raspberry pi
sock2.connect((HOSTRASPB, PORTRASPB))
main()