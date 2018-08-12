import subprocess
import time
import requests
import json
 
printLevel = 1;
timeToWakeUp = 200;
numberOfRetries = 5;
timeToNextPing = 120;
timeBetweenRetries = 10;
firstWait = 250;
logFile = "/var/log/rebootRouter.log";
 
#level    =    0, debug
#              1, info
#              2, critical
#              
def printDbg(level, arg):
    if level >= printLevel:
        print(arg);
        
    return;
    
def logToFile(line, appendNewLine = 0, logFilePath = logFile):
    currentDate = time.strftime("%Y-%m-%d  %H:%M:%S");
    head = "[%s] >> %s" % (currentDate, line, );
    if appendNewLine == 1:
        head += "\n";
    with open( logFilePath, "a") as file:
        file.write(head);
    return;
    
def runPing():
    pingResponse = subprocess.Popen(["/bin/ping", "-c1", "8.8.8.8"], stdout=subprocess.PIPE).stdout.read();
    pingResponse = pingResponse.decode('utf-8');
    pingSuccessful = pingResponse.find("1 received");
    return pingSuccessful;
    
def rebootRouter():
    ret = 0;
    payload = { 'operation': 'login', 'username': 'PointCloudLM', 'password': 'lugalu26' } 
    with requests.Session() as s:
        p = s.post('http://192.168.1.1/cgi-bin/luci/;stok=/login?form=login', data=payload) 
        data=json.loads(p.text);
        try:
            rebootUrl = "http://192.168.1.1/cgi-bin/luci/;stok=%s/admin/system?form=reboot" % (data['data']['stok'],);
            r = s.get(rebootUrl);
            ret = 1;
        except:
            logToFile("Can't reboot. Someone has already logged in", 1);
    return ret;
 
if __name__=="__main__":
    logToFile("++++", 1);
    logToFile("Application started", 1);    
        
    time.sleep(firstWait);
    
    while True:
        pingSuccessful = runPing();
        
        if pingSuccessful > 0:
            printDbg(0, "Ping successful");
            time.sleep(timeToNextPing);
            continue;
            
        for i in range(0,numberOfRetries):
            time.sleep(timeBetweenRetries);
            pingSuccessful = runPing();
            if pingSuccessful > 0:
                break;
            printDbg(0, "Ping unsuccessful, retry %d/%d" % (i+1, numberOfRetries,));
        
        
        if pingSuccessful == -1:
            printDbg(0, "Rebooting router");
            logToFile("Rebooting router ...", 1);
            rebootOk = rebootRouter();
            if rebootOk == 1:
                printDbg(0, "Waiting for router to weak up");
                time.sleep(timeToWakeUp);