""""
/////////////////////////////////////////////////////////////////////////////////
//                                                                             //
//                      Reinicio de Router por Software                        //
//                 (c) 2018 Luis Gabriel Lujano Chinchilla                     //
//                                                                             //
/////////////////////////////////////////////////////////////////////////////////
//                                                                             //
//             Router: LANPRO LP-5420G           Lenguaje: Python3             //
//             github:  https://github.com/Lujano/RouterReset                  //
//                                                                             //
/////////////////////////////////////////////////////////////////////////////////
"""
import requests
import subprocess
from requests.auth import HTTPBasicAuth
import time

# Parametros de red Wifi 
user = "No te lo voy a decir"
password = "Esto menos"

# Url que permite el reinicio (LANPRO LP-5420G)
urlToReboot = "http://192.168.1.1/userRpm/SysRebootRpm.htm?Reboot=Reboot" 

# Parametros de tiempo (s) (configurables segun preferencias)
timeToNextPing = 10.0     # Tiempo de espera entre pines de conexion a internet
timeToWakeUp = 10.0      # Tiempo de espera por reinicio del router
timeBetweenRetries = 1.0 # Tiempo entre reintentos
timeToWaitRetries = 2.0
timeFirstRetry = 5.0        # Tiempo de espera luego del primer intento fallido
numberOfRetries = 8      # Numero de reintetos despues de un ping fallido


def logToFile(line, appendNewLine = 0, logFile="rebootLog.log"):
    print(line)
    currentDate = time.strftime("%Y-%m-%d  %H:%M:%S")
    head = "{} >> {}".format(currentDate, line)
    if appendNewLine == 1:
        head += "\n"
    with open(logFile, "a") as file:
        file.write(head)
    return

def runPing(timeLimit = 3): # por defecto se esperan 3 segundos por la respuesta del ping
    pingResponse= subprocess.Popen(['ping','8.8.8.8','-c','1',"-W", str(int(timeLimit))],  stdout=subprocess.PIPE)
    # The -c es el numero de paquetes que se esperan de respuesta (en este caso 1)
    # -W es el tiempo de espera de la respuesta del ping
    pingResponse.wait() 
    return pingResponse.poll() # Respuesta al ping (0, satisfactiria)

def rebootRouter():  
    res = requests.get(urlToReboot, auth=HTTPBasicAuth(user, password))

    # Confirmar la respuesta del router confirmando el reincio
    # "Please wait a moment" pertenece a la respuesta en html que regresa este modelo de router
    # Si se quiere examinar la respuesta del router descomentar:
    # open("response.html", "wn").write(res.content) #esto guarda la respuesta en un archivo html
    reboot = res.text.find("Please wait a moment") #>0 si se encuntra el string. -1 de lo contrario

    return reboot


def main():
    # Creacion de log file
    currentDate = time.strftime("%Y_%m_%d_%H:%M:%S")
    fileName= "rebootLog_"+currentDate+".log"
    f= open(fileName,"w+")
    f.close()
    logToFile("Inicializando...", 1, fileName) # insertar lineas
    
    # Bucle principal
    while True:
        connection = runPing() # Consulta de conexion
        if connection == 0:    # Conectado a internet
            time.sleep(timeToNextPing) # Esperar por siguiente ping
        else:
            logToFile("Conexion Perdida...", 1, fileName) # insertar lineas
            # Se realizan nuevas confirmaciones de conexion
            for i in range(0,numberOfRetries):
                if i == 0:
                    time.sleep(timeFirstRetry)

                pingSuccessful = runPing(timeToWaitRetries)
                if pingSuccessful > 0:
                    logToFile("Conexion Reestablecida (ping {})...".format(i), 1, fileName) # insertar lineas
                    break
            
            if pingSuccessful == -1: # Si el ultimo intento de confirmacion es fallido
                logToFile("Reiniciando Router...", 1)
                rebootOk = rebootRouter();
                if rebootOk > 0: # Si se  reinicio el router
                    logToFile( "Esperando Conexion del Router...", 1)
                    time.sleep(timeToWakeUp);
                else:
                    logToFile( "Reinicio de Router fallido...", 1)

if __name__=="__main__":
    main()