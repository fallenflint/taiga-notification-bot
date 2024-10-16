#!/usr/bin/env python

import logging
from pprint import pprint

import requests

import config


logger = logging.getLogger(__name__)


class URLConfig:
    """
    Container for unified URL generation based on a given hostname
    """
    def __init__(self, hostname:str=config.TAIGA_HOST):
        self.__hostname = hostname

    @property
    def auth(self):
        return f"{self.__hostname}/api/v1/auth"

    def tasks(self, project_id:int=None, milestone_id:int=None):
        base_url = f"{self.__hostname}/api/v1/tasks"
        if project_id or milestone_id:
            base_url += "?{project_id=}&{milestone_id=}"
        return base_url


if __name__ == '__main__':
    token = None
    urls = URLConfig(config.TAIGA_HOST)

    response = requests.post(
        urls.auth, json={
            "username": config.LOGIN,
            "password": config.PASSWORD,
            "type": "normal",
        })
    response.raise_for_status()
    if response.status_code == 200:
        token = response.json()['auth_token']
    else:
        logger.warn(f"Can't proceed due to authentication failure ({ response.status_code=})")
        exit(0)

    for milestone in config.TARGET_MILESTONES:
        project_id = milestone['project_id']
        milestone_id = milestone['milestone_id']
        logger.debug(f'Trying to retreive project {project_id}, sprint {milestone_id}')
        response = requests.get(urls.tasks(project_id, milestone_id))
        response.raise_for_status()
        pprint(response.json())
