#!/usr/bin/env python

import logging
import json

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

    def tasks(self, project_id:int|None=None, milestone_id:int|None=None):
        base_url = f"{self.__hostname}/api/v1/tasks"
        if project_id or milestone_id:
            base_url += "?{project=}&{milestone=}"
        return base_url


class SessionStorage:
    """
    Class for session handling between executions
    """
    __store_file_path = '.session'

    def __init__(self):
        with open(self.__store_file_path, 'r') as store_file:
            self.__data = json.load(store_file)

    @property
    def token(self):
        return self.__data.get('token')

    @token.setter
    def token(self, value):
        self.__data['token'] = value

    @property
    def tasks(self):
        return self.__data.get('tasks', list())

    @tasks.setter
    def tasks(self, value):
        self.__data['tasks'] = value

    @property
    def task_ids(self):
        return set(self.__data.get('task_ids', set()))

    @task_ids.setter
    def task_ids(self, value):
        self.__data['task_ids'] = list(value)

    def save(self):
        with open(self.__store_file_path, 'w') as store_file:
            data_copy = self.__data

            json.dump(data_copy, store_file)


class TaigaClient:
    """
    User-level abstraction interface to Taiga
    """

    def __init__(self, session:SessionStorage, urls:URLConfig):
        self._session = session
        self._urls = urls

    def login(self):
        if not self._session.token:
            logger.debug("Receiving new token")
            response = requests.post(
                self._urls.auth, json={
                    "username": config.LOGIN,
                    "password": config.PASSWORD,
                    "type": "normal",
                })
            response.raise_for_status()
            if response.status_code == 200:
                self._session.token = response.json()['auth_token']
                self._session.save()
                logger.debug("Done")
            else:
                logger.warn(f"Can't proceed due to authentication failure ({ response.status_code=})")
                exit(0)
        else:
            logger.debug("Token taken from session")


    def update_tasks(self) -> set[int]:
        if not self._session.task_ids:
            self._session.task_ids = self._retreive_task_ids()
            self._session.save()
            return {}
        else:
            all_ids = self._retreive_task_ids()
            new_ids = all_ids - self._session.task_ids
            self._session.task_ids = all_ids
            self._session.save()
            return new_ids

    def _retreive_task_ids(self) -> set[int]:
        result = set()
        for milestone in config.TARGET_MILESTONES:
            project_id = milestone['project_id']
            milestone_id = milestone['milestone_id']
            logger.debug(f'Trying to retreive project {project_id}, sprint {milestone_id}')
            response = requests.get(
                urls.tasks(project_id, milestone_id),
                headers={'Authorization': f'Bearer {session.token}'}
            )
            response.raise_for_status()
            result.update(set(map(lambda x: int(x['id']), response.json())))
        return result

if __name__ == '__main__':
    urls = URLConfig(config.TAIGA_HOST)
    session = SessionStorage()
    client = TaigaClient(session, urls)

    client.login()
    new_ids = client.update_tasks()
    print("New ids:", new_ids)
