import os
import re

id_pattern = re.compile(r'^.\d+$')


token = os.environ.get("TOKEN")
app_id = int(os.environ.get("APP_ID"))
app_hash = os.environ.get("API_HASH")
allowed = [int(user) if id_pattern.search(user) else user for user in os.environ.get('AUTH_USERS', '').split()]

help_text = """
Hello I'm Terminal Bot which will Execute your Commands.

With this bot you can execute system commands on your server.

**if you not owner of this bot You can not use me because I'm private...
So you run one of these for yourself [here](https://github.com/moshe-coh/Terminal-Bot)**

**My Commands For Owner Only:**

🔹 /st - speed test
🔹 /ip - ip details
🔹 /stats - disk space
🔹 /cd - change working dir
🔹 /my_files - file manager
🔹 And All System Commands...

"""
