import os
import json
import requests

########## CONFIG START ##########
#infrastructure / scoreboard config
TEAM_IP_PREFIX = '10.60.' #This is the first two "blocks" of the vulnboxes ip. Do not forget the dot at the end. Probably won't need to be changed
TEAM_IP_SUFFIX = '.1' #This is the last "block" of the vulnboxes ip. Do not forget the dot at the beginning. Probably won't need to be changed
SCOREBOARD_IP = '10.10.0.1' #This is the ip of the scoreboard. It probably won't need to be changed

#Flag config
FLAG_SUBMIT_URL = "http://10.10.0.1:8080/flags" #this is the url to send the flags to with a post requests. It probably won't need to be changed.
FLAG_REGEX = r'[A-Z0-9]{31}=' #This is the regex for the flags. It probably won't need to be changed

#S4D config
S4D_PASSWORD = 'supersafesupercazzola' #This is the password for the S4D web interface, needs to be changed

#Team config
TEAM_TOKEN = '0c67e3441daeb12317c243dcc84070c8' #This is the team token, make sure it is correct if you want points for your flags
TEAM_NAME = 'Brescia' #This is the name of the team. It won't need to be changed
########## CONFIG END ##########


get_ip = lambda id: TEAM_IP_PREFIX + str(id) + TEAM_IP_SUFFIX


CONFIG = {
    # Don't forget to remove the old database (flags.sqlite) before each competition.
    'DEBUG': os.getenv('DEBUG') == '1',

    'TEAMS': {},
    'FLAG_FORMAT': FLAG_REGEX,
    'FLAG_SUBMIT_URL': FLAG_SUBMIT_URL,

    'SYSTEM_PROTOCOL': 'ccit_http',
    'SYSTEM_HOST': SCOREBOARD_IP,
    'TEAM_TOKEN': TEAM_TOKEN,

    # The server will submit not more than SUBMIT_FLAG_LIMIT flags
    # every SUBMIT_PERIOD seconds. Flags received more than
    # FLAG_LIFETIME seconds ago will be skipped.
    'SUBMIT_FLAG_LIMIT': 500,
    'SUBMIT_PERIOD': 58,
    'FLAG_LIFETIME': 10 * 60,

    # Password for the web interface. This key will be excluded from config
    # before sending it to farm clients.
    'SERVER_PASSWORD': S4D_PASSWORD,

    # For all time-related operations
    'TIMEZONE': 'Europe/Rome',
}

try:
    CONFIG['TEAMS'].update({team["logo"]: get_ip(id) for (id, team) in enumerate(json.loads(requests.get(f"http://{SCOREBOARD_IP}/api/game.json", timeout=3).text)["teams"]) if "nop" not in team and TEAM_NAME not in team["name"]})
except Exception as e:
    CONFIG['TEAMS'].update({f"team{id:02}": get_ip(id) for id in range(1, 44) if id != 15})
