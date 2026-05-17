import machine
import time
import BG77
import random
import ujson

def configRadio():
    time.sleep(0.2)
    module.sendCommand("AT+CGDCONT=1,\"IP\",\"lpwa.vodafone.iot\"\r\n")
    time.sleep(0.3)
    module.setOperator(BG77.COPS_AUTO)
    time.sleep(0.3)
    module.sendCommand("AT+QCFG=\"iotopmode\",0,1\r\n")
    time.sleep(0.3)
    module.sendCommand("AT+QPTWEDRXS=2,4,\"0011\",\"0110\"\r\n")
    time.sleep(2)
    module.sendCommand("AT+QPSMS=0\r\n")
    time.sleep(2)
    module.setRadio(1)

msg_id = 100

def createPacket(token, payload):
    global msg_id
    msg_id += 1
    header = bytes([0x40, 0x02, (msg_id >> 8) & 0xFF, msg_id & 0xFF])
    opt = b''
    opt += b'\xb3api'
    opt += b'\x02v1'
    t = token.encode()
    opt += bytes([0x0D, len(t) - 13]) + t
    opt += b'\x09telemetry'
    opt += b'\x11\x32'
    return header + opt + b'\xFF' + payload.encode()

def sendCoap(sock, token, payload):
    packet = createPacket(token, payload)
    print("SENDING:", payload)

    if not sock.sendBytes(packet):
        print("SEND FAILED")
        return False

    sock.setDataFormats(BG77.FORMAT_PLAIN_TEXT, BG77.FORMAT_HEX)
    
    print("Waiting for server response...")
    for _ in range(10):
        time.sleep(0.5)
        if sock.isDataInBuffer():
            data_len, resp = sock.recvBytes(100)
            if data_len > 0:
                print("COAP RESP (HEX):", resp.hex())
                return True
    
    print("COAP RESP: Timeout (Server did not respond)")
    return True

BRNO_LAT_MIN, BRNO_LAT_MAX = 49.17, 49.23
BRNO_LON_MIN, BRNO_LON_MAX = 16.55, 16.68
current_lat, current_lon = 49.1951, 16.6068

def get_random_gps():
    global current_lat, current_lon
    current_lat += random.uniform(-0.0003, 0.0003)
    current_lon += random.uniform(-0.0005, 0.0005)
    current_lat = min(max(current_lat, BRNO_LAT_MIN), BRNO_LAT_MAX)
    current_lon = min(max(current_lon, BRNO_LON_MIN), BRNO_LON_MAX)
    return {"latitude": round(current_lat, 6), "longitude": round(current_lon, 6)}

def getPos():
    module.sendCommand("AT+QGPS=1\r\n")
    for i in range(30):
        time.sleep(2)
        res = module.sendCommand("AT+QGPSLOC=2\r\n")
        if "+QGPSLOC:" in res:
            try:
                data = res.split(": ")[1].split(",")
                lat = float(data[1])
                lon = float(data[2])
                module.sendCommand("AT+QGPSEND\r\n")
                print("REAL GPS FIX!")
                return ujson.dumps({
                    "latitude": lat,
                    "longitude": lon,
                    "fake": False
                })
            except:
                pass
        if (i % 5 == 0): print(f"Searching for satellites (attempt {i}/30)...")

    module.sendCommand("AT+QGPSEND\r\n")
    print("FIX FAILED - SENDING FAKE GPS")
    fake = get_random_gps()
    return ujson.dumps({
        "latitude": fake["latitude"],
        "longitude": fake["longitude"],
        "fake": True
    })

pon_trig = machine.Pin(9, machine.Pin.OUT)
pon_trig.value(1)
time.sleep(1)
pon_trig.value(0)
print("Powering on modem, waiting 4s...")
time.sleep(4)

bg_uart = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1), timeout=1000)
module = BG77.BG77(bg_uart, verbose=True, radio=False)
time.sleep(1)

if "+CPIN: READY" not in module.sendCommand("AT+CPIN?\r\n"):
    module.setRadio(0)
    time.sleep(1)
    module.setRadio(1)
    time.sleep(3)

module.sendCommand("AT+QURCCFG=\"urcport\",\"uart1\"\r\n")
configRadio()

for i in range(30):
    info = module.getNWInfo()
    if module.isRegistered():
        print("REGISTERED")
        break
    time.sleep(2)

module.sendCommand("AT+CGATT=1\r\n")
time.sleep(2)
module.sendCommand("AT+QIACT=1\r\n")
time.sleep(3)

result, sock = module.socket(BG77.AF_INET, BG77.SOCK_DGRAM)

if result:
    sock.settimeout(10)
    token = "kr1ze9clmww6tbmermv8"
    pos_json = getPos()
    
    print("GPS finished, stabilizing network...")
    time.sleep(5) 
    
    for _ in range(15):
        if module.isRegistered():
            print("Network restored.")
            break
        print("Still searching for network...")
        time.sleep(2)

    module.sendCommand("AT+QIACT=1\r\n")
    time.sleep(1)
    
    res, sock = module.socket(BG77.AF_INET, BG77.SOCK_DGRAM)
    if res:
        sock.connect("147.229.148.105", 5683)
        if not sendCoap(sock, token, pos_json):
            print("Sending failed even after connection restart.")
    else:
        print("Failed to restore socket.")
else:
    print("Socket creation failed.")