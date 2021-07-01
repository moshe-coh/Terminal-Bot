import shutil
import httpx
import psutil
import speedtest


def disk_space() -> tuple:
    BytesPerGB = 1024 * 1024 * 1024
    total, used, free = shutil.disk_usage(".")
    total_ram = psutil.virtual_memory().total
    ram_used = psutil.virtual_memory().percent
    f_total = "%.2f GB" % (float(total) / BytesPerGB)
    f_used = "%.2f GB" % (float(used) / BytesPerGB)
    f_free = "%.2f GB" % (float(free) / BytesPerGB)
    f_total_ram = "%.2f GB" % (float(total_ram) / BytesPerGB)
    return f_total, f_used, f_free, f_total_ram, ram_used


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
