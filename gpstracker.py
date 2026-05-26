import machine
import time
import BG77
import random
import ujson
import re

sleep_interval = 1800
msg_id = 100
force_wakeup = False
pending_time_log = None
TOKEN = "kr1ze9clmww6tbmermv8"
SERVER_IP = "147.229.148.105"
SERVER_PORT = 5683
BRNO_LAT_MIN = 49.17
BRNO_LAT_MAX = 49.23
BRNO_LON_MIN = 16.55
BRNO_LON_MAX = 16.68
current_lat = 49.1951
current_lon = 16.6068

def configRadio():
    time.sleep(0.2)
    bg77.sendCommand('AT+CGDCONT=1,"IP","lpwa.vodafone.iot"\r\n')
    time.sleep(0.3)
    bg77.sendCommand('AT+QCFG="iotopmode",0,1\r\n')
    time.sleep(0.3)
    bg77.sendCommand('AT+QPTWEDRXS=2,4,"0011","0110"\r\n')
    time.sleep(0.5)
    bg77.sendCommand("AT+QPSMS=0\r\n")
    time.sleep(0.5)
    bg77.setRadio(1)

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

def createAttrRequest(token):
    global msg_id
    msg_id += 1
    header = bytes([0x40, 0x01, (msg_id >> 8) & 0xFF, msg_id & 0xFF])
    opt = b''
    opt += b'\xb3api'
    opt += b'\x02v1'
    t = token.encode()
    opt += bytes([0x0D, len(t) - 13]) + t
    opt += b'\x0aattributes'
    query = "sharedKeys=sleepInterval,forceTrigger"
    q = query.encode()
    opt += bytes([0x4D, len(q) - 13])
    opt += q
    return header + opt

def decode_coap_payload(hex_data):
    try:
        if len(hex_data) % 2 != 0:
            return None
        data = bytes.fromhex(hex_data)
        marker = data.find(b'\xFF')
        if marker == -1:
            return None
        payload = data[marker + 1:]
        decoded = payload.decode()
        print("received:", decoded)
        return decoded
    except Exception as e:
        print("decode error:", e)
        return None

def parse_raw_data(resp_str):
    global sleep_interval, force_wakeup, pending_time_log
    try:
        clean_str = resp_str.lower()
        print("server data:", clean_str)
        if "sleepinterval" in clean_str:
            idx = clean_str.find("sleepinterval")
            sub_str = clean_str[idx:]
            start_idx = sub_str.find(":")
            if start_idx != -1:
                end_idx = sub_str.find(",")
                if end_idx == -1:
                    end_idx = sub_str.find("}")
                if end_idx != -1:
                    val_str = sub_str[start_idx + 1:end_idx].replace('"', '').strip()
                    try:
                        new_minutes = int(val_str)
                        if 1 <= new_minutes <= 120:
                            if (new_minutes * 60) != sleep_interval:
                                sleep_interval = new_minutes * 60
                                pending_time_log = "sleep changed to: {} min".format(new_minutes)
                                print("new sleep interval:", new_minutes, "minutes")
                    except:
                        pass
        if '"method":"forcetrigger"' in clean_str or '"forcetrigger":true' in clean_str:
            print("got force trigger!")
            force_wakeup = True
            return True
    except Exception as e:
        print("parse error:", e)
    return False

def processQirdResponse(resp):
    lines = resp.splitlines()
    for line in lines:
        line = line.strip()
        if len(line) > 20 and all(c in "0123456789ABCDEFabcdef" for c in line):
            decoded = decode_coap_payload(line)
            if decoded:
                print("decoded:", decoded)
                parse_raw_data(decoded)

def pollQird():
    try:
        bg_uart.write(b"AT+QIRD=1,200\r\n")
        time.sleep(0.5)
        if bg_uart.any():
            raw = bg_uart.read()
            if raw:
                resp = raw.decode('utf-8', 'ignore')
                print("raw response:", resp.strip())
                processQirdResponse(resp)
    except Exception as e:
        print("qird error:", e)

def sendCoap(sock, token, payload):
    packet = createPacket(token, payload)
    print("sending telemetry:", payload)
    if not sock.sendBytes(packet):
        print("send failed")
        return False
    sock.setDataFormats(BG77.FORMAT_PLAIN_TEXT, BG77.FORMAT_HEX)
    return True

def get_random_gps():
    global current_lat, current_lon
    current_lat += random.uniform(-0.005, 0.005)
    current_lon += random.uniform(-0.005, 0.005)
    current_lat = min(max(current_lat, BRNO_LAT_MIN), BRNO_LAT_MAX)
    current_lon = min(max(current_lon, BRNO_LON_MIN), BRNO_LON_MAX)
    return {"latitude": round(current_lat, 6), "longitude": round(current_lon, 6)}

def getTime():
    res = bg77.sendCommand("AT+CCLK?\r\n")
    if "+CCLK:" in res:
        try:
            full_time = res.split('"')[1]
            time_part = full_time.split(',')[1].split('+')[0]
            h, m, s = map(int, time_part.split(':'))
            h = (h + 2) % 24
            return "{:02d}:{:02d}:{:02d}".format(h, m, s)
        except:
            pass
    return "00:00:00"

def getPos():
    bg77.sendCommand("AT+QGPSEND\r\n")
    time.sleep(1)
    bg77.sendCommand("AT+QGPS=1\r\n")
    for i in range(15):
        time.sleep(1)
        res = bg77.sendCommand("AT+QGPSLOC=2\r\n")
        if "+QGPSLOC:" in res:
            try:
                data = res.split(": ")[1].split(",")
                lat = float(data[1])
                lon = float(data[2])
                ts = getTime()
                bg77.sendCommand("AT+QGPSEND\r\n")
                print("gps fix ok!")
                return ujson.dumps({"fake": False, "latitude": lat, "longitude": lon, "time": ts})
            except:
                pass
        print("searching satellites (try {}/15)...".format(i + 1))
    ts = getTime()
    bg77.sendCommand("AT+QGPSEND\r\n")
    print("gps failed, using fake coords")
    fake = get_random_gps()
    return ujson.dumps({"fake": True, "latitude": fake["latitude"], "longitude": fake["longitude"], "time": ts})

bg_uart = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1), timeout=2000)
pon_trig = machine.Pin(9, machine.Pin.OUT)
print("hw init...")
pon_trig.value(1)
time.sleep(1)
pon_trig.value(0)
time.sleep(4)
while bg_uart.any():
    bg_uart.read()
bg77 = BG77.BG77(bg_uart, verbose=True, radio=False)
configRadio()

while True:
    sock_link = None
    print("\n--- loop start ---")
    print("current interval:", sleep_interval, "s")
    registered = False
    for i in range(20):
        status = bg77.sendCommand("AT+CEREG?\r\n")
        if (",1" in status or ",5" in status or "0,1" in status or "0,5" in status or "4,5" in status):
            print("connected to network.")
            registered = True
            break
        time.sleep(1)
    if not registered:
        print("network error, resetting...")
        bg77.sendCommand("AT+CFUN=0\r\n")
        time.sleep(2)
        configRadio()
        time.sleep(5)
        continue
    status = bg77.sendCommand("AT+CEREG?\r\n")
    if (",1" in status or ",5" in status or "0,1" in status or "0,5" in status):
        res, sock_link = bg77.socket(BG77.AF_INET, BG77.SOCK_DGRAM)
        if res:
            sock_link.connect(SERVER_IP, SERVER_PORT)
            time.sleep(0.2)
    if sock_link:
        attr_packet = createAttrRequest(TOKEN)
        sock_link.sendBytes(attr_packet)
        print("getting config...")
        for _ in range(4):
            pollQird()
            time.sleep(0.5)
    print("getting position...")
    pos_json = getPos()
    if sock_link:
        print("sending data to server...")
        sendCoap(sock_link, TOKEN, pos_json)
        for _ in range(3):
            pollQird()
            time.sleep(0.5)
    if pending_time_log:
        print(pending_time_log)
        pending_time_log = None
    print("sleeping for:", sleep_interval, "seconds")
    for seconds_passed in range(sleep_interval):
        time.sleep(1)
        if sock_link and seconds_passed % 3 == 0:
            attr_packet = createAttrRequest(TOKEN)
            sock_link.sendBytes(attr_packet)
            time.sleep(0.5)
            pollQird()
        if force_wakeup:
            print("manual wake up!")
            force_wakeup = False
            break
    if sock_link:
        try:
            sock_link.close()
            print("socket closed.")
        except:
            pass
