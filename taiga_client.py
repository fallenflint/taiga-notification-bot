#!/usr/bin/env python

import logging

import requests

import config


logger = logging.getLogger(__name__)


if __name__ == '__main__':
    token = None
    logger.info("hi")
    logger.info(config.TAIGA_HOST, config.TARGET_MILESTONES)
    response = requests.post(
        config.TAIGA_HOST + '/api/v1/auth', json={
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
        logger.debug(f'Trying to retreive project {milestone["project_id"]}, sprint {milestone["milestone_id"]}')