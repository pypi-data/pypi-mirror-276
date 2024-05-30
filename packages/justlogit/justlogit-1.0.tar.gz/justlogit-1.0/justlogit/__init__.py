# JustLogIt
# https://github.com/watermelon46/jli

import platform
import cpuinfo
from distro import name as distrname
from psutil import virtual_memory
from time import gmtime, strftime

loggers = {} # Переменная для хранения логгеров

sysinfo = { # Получаем инфо о системе для вывода в логи
    "os": platform.system(),
    "ram": virtual_memory().total,
    "cpu": cpuinfo.get_cpu_info()['brand_raw']
}

if sysinfo['os'] == 'Linux':
    sysinfo['os'] += f' {str(distrname())}'

def getCurrentTime(): # Сервисная функция для получения времени
    """Get current time"""
    return strftime("%H:%M:%S", gmtime())

def createLogger(loggerName = 'main', fileName = 'latest.log', branding = None, printLogs = False):
    """Create a logger"""

    if loggerName in loggers.keys():
        raise Exception(f'Logger named "{loggerName}" already exist')

    logging = open(fileName, 'w') # Очищаем файл логов от предыдущей сессии

    logging.truncate(0)

    logging.close()
    class logger:

        log_file = fileName
        log_brand = branding
        log_print = printLogs

        logTemplate = "[{}]{}{}"

        logging = open(log_file, 'w')

        def log(text):
            log_brand = branding
            
            if log_brand == None:
                logRender = logger.logTemplate.format(getCurrentTime(), ' ', text)
            else:
                logRender = logger.logTemplate.format(getCurrentTime(), f'[{logger.log_brand}]', text)
            
            if logger.log_print == True:
                print(logRender)

            logger.logging.write(f'{logRender}\n')

            return True

        def warn(text):
            logger.log("".join(['[WARN] ', text])) # зачем копипастить log(), если можно использовать его?

        def info(text):
            logger.log("".join(['[INFO] ', text]))

        def error(text):
            logger.log("".join(['[ERROR] ', text]))

        def close():
            del logger.log, logger.info, logger.error
            del loggers[loggerName]
            logger.logging.close()

    loggers[loggerName] = logger

    logger.log('JLI Service started')
    logger.info(f'System information:\n    OS: {sysinfo["os"]}\n    RAM: {sysinfo["ram"]} bytes\nC    PU: {sysinfo["cpu"]}')

    return logger

def getLogger(loggerName):
    """Get created logger"""
    return loggers[loggerName]

def delLogger(loggerName):
    """Delete created logger"""
    loggers[loggerName].close()
    del loggers[loggerName]