file = True
version = 1
formatters = {
    'console': {
        'format': '%(asctime)s - %(levelname)s[%(name)s] - %(message)s - at[%(pathname)s  => %(funcName)s():%(lineno)d]'
    },
    'file': {
        'format': '%(asctime)s - %(levelname)s[%(name)s] - %(message)s'
    }
}
handlers = {
    'console': {
        'class': 'logging.StreamHandler',
        'level': 'DEBUG',
        'formatter': 'console'
    },
    'file': {
        'class': 'logging.FileHandler',
        'filename': 'log.log',
        'level': 'ERROR',
        'formatter': 'file',
        'encoding': 'utf-8',
    },
    'timFile': {
        'class': 'logging.handlers.TimedRotatingFileHandler',
        'filename': 'log.log',
        'level': 'ERROR',
        'formatter': 'file',
        'encoding': 'utf-8',
        'when': 'H',
        'interval': 1,
        'backupCount': 0,
    }
}

loggers = {
    'consoleLogger': {
        'level': 'DEBUG',
        'handlers': ['console']
    },
    'fileLogger': {
        'level': 'DEBUG',
        'handlers': ['console', 'file'],
        'propagate': 'no'
    }
}
