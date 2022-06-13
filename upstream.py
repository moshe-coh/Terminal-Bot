from logging import error as log_error, info as log_info
from os import path as ospath, environ,
from subprocess import run as srun

UPSTREAM_REPO = environ.get('UPSTREAM_REPO')
UPSTREAM_BRANCH = environ.get('UPSTREAM_BRANCH')
try:
    if len(UPSTREAM_REPO) == 0:
       raise TypeError
except:
    UPSTREAM_REPO = "https://github.com/Frozen12/Terminal-Bot"
try:
    if len(UPSTREAM_BRANCH) == 0:
       raise TypeError
except:
    UPSTREAM_BRANCH = 'development'

if ospath.exists('.git'):
    srun(["rm", "-rf", ".git"])

update = srun([f"git init -q \
                 && git config --global user.email frozen12@gmail.com \
                 && git config --global user.name frozen12 \
                 && git add . \
                 && git commit -sm update -q \
                 && git remote add origin {UPSTREAM_REPO} \
                 && git fetch origin -q \
                 && git reset --hard origin/{UPSTREAM_BRANCH} -q"], shell=True)

if update.returncode == 0:
    log_info('Successfully updated with latest commit from UPSTREAM_REPO')
else:
    log_error('Something went wrong while updating, check UPSTREAM_REPO if valid or not!')
