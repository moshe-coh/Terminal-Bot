import httpx
import psutil
import speedtest
from datetime import datetime
from time import time


def str_uptime(secs: float):
    if secs > 217728000:  # 1 year in secs
        return datetime.fromtimestamp(secs).strftime("%YY %mM %dd | %Hh %Mm %Ss")
    elif secs > 2629746:  # 1 month in secs
        return datetime.fromtimestamp(secs).strftime("%mM %dd | %Hh %Mm %Ss")
    else:  # 1 day in secs
        return datetime.fromtimestamp(secs).strftime("%dd | %Hh %Mm %Ss")


def convert_to_GB(input_bytes):
    return round(input_bytes / (1024 * 1024 * 1024), 1)


def ip() -> str:
    url = "http://ip-api.com/json/"
    data = httpx.get(url).json()
    IP = data['query']
    ISP = data['isp']
    Organisation = data['org']
    country = data['country']
    City = data['city']
    Region = data['region']
    Longitude = data['lon']
    Latitude = data['lat']
    Timezone = data['timezone']
    zip_code = data['zip']

    text = f"""
**My IP:** {IP}
**ISP:** {ISP}
**Organisation:** {Organisation}
**Country:** {country}
**City:** {City}
**Region:** {Region}
**Longitude:** {Longitude}
**Latitude:** {Latitude}
**Time zone:** {Timezone}
**Zip code:** {zip_code}
"""
    return text


def speed_test() -> tuple:
    st = speedtest.Speedtest()
    ping = st.results.ping

    BytesPerMB = 1024 * 1024
    f_down = "%.2f MB" % (float(st.download()) / BytesPerMB)
    f_up = "%.2f MB" % (float(st.upload()) / BytesPerMB)

    return f_down, f_up, ping


def stats_server() -> str:
    stat_msg = f"""
    **Server Stats**

    CPU Used 💽: {psutil.cpu_percent(interval=0.1)}%
    RAM Used 💿: {psutil.virtual_memory().percent}%
    Disk Used 💾: {convert_to_GB(psutil.disk_usage('/').used)}GB of {convert_to_GB(psutil.disk_usage('/').total)}GB
    Uptime ⚡: {str_uptime(time() - psutil.boot_time())}
    Booted on ⏱: {datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")}
    Stats as of 🩸: {datetime.fromtimestamp(time()).strftime("%Y-%m-%d %H:%M:%S")}
    """
    return stat_msg


