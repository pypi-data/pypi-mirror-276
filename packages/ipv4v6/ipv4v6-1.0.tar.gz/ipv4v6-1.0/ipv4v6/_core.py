import binascii
import random
from socket import *
import requests
import json
__all__=['get_ipv4','get_ipv6','get_ipv4_location','get_ipv6_location','get_ip','ip_tuple']
def ipv4()->dict:
    headers={'Origin':'https:ip.zxinc.org','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}
    res=requests.get('https://v4.ip.zxinc.org/info.php?type=json',headers=headers)
    ipv4=json.loads(res.text)
    return ipv4['data']
def ipv6()->dict:
    headers={'Origin':'https:ip.zxinc.org','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}
    res=requests.get('https://v6.ip.zxinc.org/info.php?type=json',headers=headers)
    ipv6=json.loads(res.text)
    return ipv6['data']
def get_ipv4()->str:
    return ipv4()['myip']
def get_ipv6()->str:
    return ipv6()['myip']
def get_ipv4_location():
    return ipv4()['location']
def get_ipv6_location():
    return ipv6()['location']
def get_ip(csock:socket=None,local_port:int=8888,stun_server:str='stun.l.google.com',stun_port:int=19302):
    tranid=''.join(random.choice('0123456789ABCDEF') for i in range(32))
    data=binascii.a2b_hex('00010000'+tranid)
    sock=None
    if csock==None:
        sock=socket(AF_INET,SOCK_DGRAM)
        sock.bind(('0.0.0.0',local_port))
    else:
        sock=csock
    sock.sendto(data,(stun_server,stun_port))
    buf,addr=sock.recvfrom(2048)
    if csock==None:
        sock.close()
    if tranid.upper()==binascii.b2a_hex(buf[4:20]).upper().decode() and binascii.b2a_hex(buf[0:2]).decode()=='0101':
        port = int(binascii.b2a_hex(buf[26:28]), 16)
        ip = ".".join([
            str(int(binascii.b2a_hex(buf[28:29]), 16)),
            str(int(binascii.b2a_hex(buf[29:30]), 16)),
            str(int(binascii.b2a_hex(buf[30:31]), 16)),
            str(int(binascii.b2a_hex(buf[31:32]), 16))
        ])
        return (ip+':'+str(port))
    return 'Failed'
def ip_tuple(csock:socket=None,local_port:int=8888,stun_server:str='stun.l.google.com',stun_port:int=19302):
    ret=get_ip(csock,local_port,stun_server,stun_port)
    if ret=='Failed':
        return 'Failed'
    ret=ret.split(':')
    return (ret[0],int(ret[1]))
if __name__=='__main__':
    print(get_ip())