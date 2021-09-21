import shutil
import psutil as p
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


def get_server_details():

    dtotal, dused, dfree = shutil.disk_usage(".")
    mem = p.virtual_memory()
    tram, aram, uram, fram, fpercent = mem.total, mem.available, mem.used, mem.free, mem.percent

    cpuf = p.cpu_freq()
    ccpu, mcpu = cpuf.current, cpuf.max

    lcore, pcore = p.cpu_count(logical=True), p.cpu_count(logical=False)

    text = f""" **System Details **

__Storage__
  Total: {human_readable_speed(dtotal)}
  Used: {human_readable_speed(dused)}
  Free: {human_readable_speed(dfree)}

__Core & Cpu Info__
  CPU Frequency: {ccpu} Mhz 
  Max: {mcpu}
  PCore: {pcore} LCore: {lcore}

__Ram Info__
  Total: {human_readable_speed(tram)}
  Available: {human_readable_speed(aram)}
  Used: {human_readable_speed(uram)}
  Free: {human_readable_speed(fram)}
  Usage: {fpercent}%

  Uptime: {str_uptime(time() - psutil.boot_time())}
  Booted on: {datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")}
  Stats as of: {datetime.fromtimestamp(time()).strftime("%Y-%m-%d %H:%M:%S")}
 """

    return text


def get_server_speedtest():
    speedy = speedtest.Speedtest()
    speedy.get_best_server()
    speedy.download()
    speedy.upload()
    speedy.results.share()
    speedresult = speedy.results.dict()
    image_url = (speedresult['share'])
    speedstring = f"""__Server SpeedTest Result__
**Server Details**

__Name__:**{speedresult['server']['name']}**
__Country__:**{speedresult['server']['country']}**,**{speedresult['server']['cc']}**
__Sponser__:**{speedresult['server']['sponsor']}**

__**Speed Results**__
__Ping__:**{speedresult['ping']}**
__Upload__:**{human_readable_speed(speedresult['upload'] / 8)}/s**
__Download__:**{human_readable_speed(speedresult['download'] / 8)}/s**
__ISP__:**{speedresult['client']['isp']}**
"""
    return speedstring, image_url


def human_readable_speed(size):
    power = 2 ** 10
    zero = 0
    units = {0: "", 1: "Kb", 2: "MB", 3: "Gb", 4: "Tb"}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"

