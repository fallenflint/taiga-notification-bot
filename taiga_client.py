#!/usr/bin/env python

import logging
from pprint import pprint
import json

import requests

import config, exceptions


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


class SessionStorage:
    """
    Class for session handling between executions
    """
    __store_file_path = '.session'

    def __init__(self):
        with open(self.__store_file_path, 'r') as store_file:
            self.__data = json.load(store_file)
        self._validate_data()

    @property
    def token(self):
        return self.__data.get('token')

    @token.setter
    def token(self, value):
        self.__data['token'] = value

    def _validate_data(self):
        # for key in ('token'):
        for key in ():
            if key not in self.__data:
                raise exceptions.StorageException(f'Missing {key} if storage file!')

    def save(self):
        with open(self.__store_file_path, 'w') as store_file:
            json.dump(self.__data, store_file)


if __name__ == '__main__':
    urls = URLConfig(config.TAIGA_HOST)
    session = SessionStorage()

    if not session.token:
        logger.debug("Receiving new token")
        response = requests.post(
            urls.auth, json={
                "username": config.LOGIN,
                "password": config.PASSWORD,
                "type": "normal",
            })
        response.raise_for_status()
        if response.status_code == 200:
            session.token = response.json()['auth_token']
            session.save()
            logger.debug("Done")
        else:
            logger.warn(f"Can't proceed due to authentication failure ({ response.status_code=})")
            exit(0)
    else:
        logger.debug("Token taken from session")

    for milestone in config.TARGET_MILESTONES:
        project_id = milestone['project_id']
        milestone_id = milestone['milestone_id']
        logger.debug(f'Trying to retreive project {project_id}, sprint {milestone_id}')
        response = requests.get(urls.tasks(project_id, milestone_id))
        response.raise_for_status()
        # pprint(response.json())
