import machine, time, BG77, random, ujson

sleep_interval = 1800
msg_id = 100
pending_time_log = None

TOKEN = "kr1ze9clmww6tbmermv8"
SERVER_IP = "147.229.148.105"
SERVER_PORT = 5683

BRNO_LAT_MIN, BRNO_LAT_MAX = 49.17, 49.23
BRNO_LON_MIN, BRNO_LON_MAX = 16.55, 16.68
current_lat, current_lon = 49.1951, 16.6068

def configRadio():
    time.sleep(0.2)
    bg77.sendCommand('AT+CGDCONT=1,"IP","lpwa.vodafone.iot"\r\n')
    time.sleep(0.3)
    bg77.sendCommand('AT+QCFG="iotopmode",2,1\r\n')
    time.sleep(0.5)
    bg77.sendCommand("AT+QPTWEDRXS=0\r\n")
    time.sleep(0.5)
    bg77.sendCommand("AT+QPSMS=0\r\n")
    time.sleep(0.5)
    bg77.sendCommand("AT+CFUN=1\r\n")
    time.sleep(3)

def createPacket(token, payload):
    global msg_id
    msg_id += 1
    header = bytes([0x40, 0x02, (msg_id >> 8) & 0xFF, msg_id & 0xFF])
    opt = b'\xb3api\x02v1'
    t = token.encode()
    opt += bytes([0x0D, len(t) - 13]) + t
    opt += b'\x09telemetry\x11\x32'
    return header + opt + b'\xFF' + payload.encode()

def createAttrRequest(token):
    global msg_id
    msg_id += 1
    header = bytes([0x40, 0x01, (msg_id >> 8) & 0xFF, msg_id & 0xFF])
    opt = b'\xb3api\x02v1'
    t = token.encode()
    opt += bytes([0x0D, len(t) - 13]) + t
    opt += b'\x0aattributes'
    query = "sharedKeys=sleepInterval"
    q = query.encode()
    opt += bytes([0x4D, len(q) - 13]) + q
    return header + opt

def decode_coap_payload(hex_data):
    try:
        if len(hex_data) % 2 != 0: return None
        data = bytes.fromhex(hex_data)
        marker = data.find(b'\xFF')
        if marker == -1: return None
        payload = data[marker + 1:]
        return payload.decode()
    except:
        return None

def parse_raw_data(resp_str):
    global sleep_interval, pending_time_log
    try:
        clean_str = resp_str.lower()
        if "sleepinterval" in clean_str:
            idx = clean_str.find("sleepinterval")
            sub_str = clean_str[idx:]
            start_idx = sub_str.find(":")
            if start_idx == -1: return
            end_idx = sub_str.find(",")
            if end_idx == -1:
                end_idx = sub_str.find("}")
            val_str = sub_str[start_idx + 1:end_idx].replace('"', '').strip()
            new_minutes = int(val_str)
            if 1 <= new_minutes <= 120:
                if (new_minutes * 60) != sleep_interval:
                    sleep_interval = new_minutes * 60
                    pending_time_log = "sleep changed to: {} min".format(new_minutes)
                    print("new interval:", new_minutes, "min")
    except Exception as e:
        print("parse error:", e)

def processQirdResponse(resp):
    if "pdpdeact" in resp.lower():
        raise Exception("PDP LOST")
    for line in resp.splitlines():
        line = line.strip()
        if len(line) > 20 and all(c in "0123456789ABCDEFabcdef" for c in line):
            decoded = decode_coap_payload(line)
            if decoded:
                print("rx:", decoded)
                parse_raw_data(decoded)

def pollQird():
    bg_uart.write(b"AT+QIRD=1,200\r\n")
    time.sleep(0.5)
    if bg_uart.any():
        raw = bg_uart.read()
        if raw:
            resp = raw.decode('utf-8', 'ignore')
            processQirdResponse(resp)

def sendCoap(sock, token, payload):
    packet = createPacket(token, payload)
    print("tx:", payload)
    if not sock.sendBytes(packet):
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
    for i in range(8):
        time.sleep(1)
        res = bg77.sendCommand("AT+QGPSLOC=2\r\n")
        if "+QGPSLOC:" in res:
            try:
                data = res.split(": ")[1].split(",")
                lat = float(data[1])
                lon = float(data[2])
                ts = getTime()
                bg77.sendCommand("AT+QGPSEND\r\n")
                return ujson.dumps({"fake": False, "latitude": lat, "longitude": lon, "time": ts})
            except:
                pass
    ts = getTime()
    bg77.sendCommand("AT+QGPSEND\r\n")
    fake = get_random_gps()
    return ujson.dumps({"fake": True, "latitude": fake["latitude"], "longitude": fake["longitude"], "time": ts})

# Hardware inicializace
bg_uart = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1), timeout=2000)
pon_trig = machine.Pin(9, machine.Pin.OUT)
pon_trig.value(1)
time.sleep(1)
pon_trig.value(0)
time.sleep(4)

while bg_uart.any():
    bg_uart.read()

bg77 = BG77.BG77(bg_uart, verbose=True, radio=False)
configRadio()

# Hlavní smyčka
while True:
    sock_link = None
    print("\ncycle start")
    print("interval:", sleep_interval)
    registered = False

    for i in range(30):
        status = bg77.sendCommand("AT+CEREG?\r\n")
        if ",5" in status or ",1" in status:
            registered = True
            break
        time.sleep(1)

    if not registered:
        print("network reconnect")
        bg77.sendCommand("AT+CFUN=0\r\n")
        time.sleep(3)
        configRadio()
        continue

    try:
        res, sock_link = bg77.socket(BG77.AF_INET, BG77.SOCK_DGRAM)
        if not res:
            raise Exception("socket fail")

        sock_link.connect(SERVER_IP, SERVER_PORT)
        time.sleep(1)

        attr_packet = createAttrRequest(TOKEN)
        sock_link.sendBytes(attr_packet)

        for _ in range(3):
            pollQird()
            time.sleep(1)

        pos_json = getPos()
        sendCoap(sock_link, TOKEN, pos_json)

        if pending_time_log:
            print(pending_time_log)
            pending_time_log = None

        print("sleep:", sleep_interval)
        for seconds_passed in range(sleep_interval):
            time.sleep(1)
            if seconds_passed % 15 == 0:
                try:
                    attr_packet = createAttrRequest(TOKEN)
                    sock_link.sendBytes(attr_packet)
                    time.sleep(0.5)
                    pollQird()
                except:
                    print("socket reconnect")
                    break
    except Exception as e:
        print("runtime error:", e)

    try:
        sock_link.close()
    except:
        pass
