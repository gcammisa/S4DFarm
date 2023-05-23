import requests

from flask import current_app as app
from models import FlagStatus, SubmitResult


RESPONSES = {
    FlagStatus.QUEUED: [],
    FlagStatus.ACCEPTED: ['accepted'],
    FlagStatus.REJECTED: ['own', 'too old', 'nop', 'invalid'],
}


TIMEOUT = 5


def submit_flags(flags, config):
    r = requests.put(config['SYSTEM_URL'],
                     headers={'X-Team-Token': config['TEAM_TOKEN']},
                     json=[item.flag for item in flags], timeout=TIMEOUT)

    unknown_responses = set()
    for item in r.json():
        response = item['msg'].strip()
        response = response.replace('[{}] '.format(item['flag']), '')

        response_lower = response.lower()
        for status, substrings in RESPONSES.items():
            if any(s in response_lower for s in substrings):
                found_status = status
                break
        else:
            found_status = FlagStatus.QUEUED
            if response not in unknown_responses:
                unknown_responses.add(response)
                app.logger.warning('Unknown checksystem response (flag will be resent): %s', response)

        yield SubmitResult(item['flag'], found_status, response)