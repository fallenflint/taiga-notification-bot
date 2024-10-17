import config


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