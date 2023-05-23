import os
import json
import requests

# import validators.volgactf

get_ip = lambda id: os.environ["TEAM_IP_PREFIX"] + str(id) + os.environ["TEAM_IP_SUFFIX"]

CONFIG = {
    # Don't forget to remove the old database (flags.sqlite) before each competition.
    'DEBUG': os.getenv('DEBUG') == '1',

    'TEAMS': {},
    # 'FLAG_FORMAT': r'CTF\.Moscow\{[a-zA-Z\.0-9_-]+\}',
    # 'FLAG_FORMAT': r'VolgaCTF{[\w-]*\.[\w-]*\.[\w-]*}',
    'FLAG_FORMAT': os.environ['FLAG_REGEX'],

    # 'SYSTEM_PROTOCOL': 'ructf_http',
    # 'SYSTEM_URL': 'http://monitor.ructfe.org/flags',
    # 'SYSTEM_TOKEN': '275_17fc104dd58d429ec11b4a5e82041cd2',

    'SYSTEM_PROTOCOL': 'ccit_http',
    'SYSTEM_HOST': os.environ['SCOREBOARD_IP'],
    'SYSTEM_PORT': os.environ['SCOREBOARD_PORT'],
    'TEAM_TOKEN': os.environ['TEAM_TOKEN'],
    # 'SYSTEM_PROTOCOL': 'volgactf',
    # 'SYSTEM_VALIDATOR': 'volgactf',
    # 'SYSTEM_HOST': 'final.volgactf.ru',
    # 'SYSTEM_SERVER_KEY': validators.volgactf.get_public_key('https://final.volgactf.ru'),

    # The server will submit not more than SUBMIT_FLAG_LIMIT flags
    # every SUBMIT_PERIOD seconds. Flags received more than
    # FLAG_LIFETIME seconds ago will be skipped.
    'SUBMIT_FLAG_LIMIT': 100,
    'SUBMIT_PERIOD': 1,
    'FLAG_LIFETIME': 10 * 60,

    # VOLGA: Don't make more than INFO_FLAG_LIMIT requests to get flag info,
    # usually should be more than SUBMIT_FLAG_LIMIT
    # 'INFO_FLAG_LIMIT': 10,

    # Password for the web interface. This key will be excluded from config
    # before sending it to farm clients.
    # ########## DO NOT FORGET TO CHANGE IT ##########
    'SERVER_PASSWORD': os.environ['DESTRUCTIVEFARM_PASSWORD'],

    # For all time-related operations
    'TIMEZONE': 'Europe/Rome',
}

try:
    CONFIG['TEAMS'].update({team["logo"]: get_ip(id) for (id, team) in enumerate(json.loads(requests.get(f"http://{os.environ['SCOREBOARD_IP']}/api/game.json", timeout=1).text)["teams"]) if "nop" not in team and "Brescia" not in team["name"]})
except Exception as e:
    CONFIG['TEAMS'].update({f"team{id:02}": get_ip(id) for id in range(1, 40)})