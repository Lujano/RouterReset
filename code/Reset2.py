""""
/////////////////////////////////////////////////////////////////////////////////
//                                                                             //
//                             Reinicio de Router por Software                 //
//                        (c) 2018 Luis Gabriel Lujano Chinchilla              //
//                                                                             //
/////////////////////////////////////////////////////////////////////////////////
//                                                                             //
//             Router: LANPRO LP-5420G           Lenguaje: Python3             //
//             github:  https://github.com/Lujano/RouterReset                   //
//                                                                             //
/////////////////////////////////////////////////////////////////////////////////
"""
import requests
from requests.auth import HTTPBasicAuth
 
session = requests.Session()
user = "NoTeLoVoyADecir"
password = "EstoMenos"
data = {'Reboot':'True'}
res = session.get('http://192.168.1.1/userRpm/SysRebootRpm.htm?Reboot=Reboot', 
auth=HTTPBasicAuth(user, password))
open('response.html', 'wb').write(res.content)