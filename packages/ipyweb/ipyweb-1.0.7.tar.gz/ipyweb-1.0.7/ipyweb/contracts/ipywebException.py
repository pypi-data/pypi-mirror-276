
from ipyweb.logger import logger


class ipywebException(Exception):
    key = ''
    message = ''
    code = 1

    def __init__(self, message, key='', code=1):
        self.message = message
        self.key = key
        self.code = code
        super().__init__(self.message)
        logger.file.error(f'ipywebException [{code}] :{message}')

    def __str__(self):
        return self.message



