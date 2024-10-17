import json


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

    @token.deleter
    def token(self):
        del self.__data['token']

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

    @task_ids.deleter
    def task_ids(self):
        del self.__data['task_ids']

    @property
    def jokes_available(self) -> list[int]:
        return list(self.__data.get('jokes_available', list()))


    @jokes_available.setter
    def jokes_available(self, value):
        self.__data['jokes_available'] = list(value)

    @jokes_available.deleter
    def jokes_available(self):
        del self.__data['jokes_available']
    

    def save(self):
        with open(self.__store_file_path, 'w') as store_file:
            data_copy = self.__data
            json.dump(data_copy, store_file)