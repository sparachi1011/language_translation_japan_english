import multiprocessing
from deep_translator import GoogleTranslator
from googletrans import Translator
import math
import os
import pdb
import re
import json
from datetime import datetime, timedelta
import time
import logging
import warnings
import pytz
warnings.filterwarnings("ignore", category=Warning)

if os.name == 'nt':
    working_directory = os.getcwd() + "/"
    syslog_file_path = working_directory + 'syslog_local_5k.log'
if os.name == 'posix':
    working_directory = "/home/yokogawa/mhi_syslog_translation_script/"
    syslog_file_path = "/var/log/soc/" + 'syslog.log'  # syslog.log

# print("Current working directory:", working_directory)


mhi_log_directory_name = 'mhi_script_execution_logs/'
mhi_log_file_path = working_directory + 'mhi_script_execution_logs_' + \
    str(datetime.now().strftime("%b_%d_%y")) + '.log'
now = datetime.now(tz=pytz.timezone('Asia/Tokyo')).strftime('%b %d %H:%M:%S')
day = datetime.now(tz=pytz.timezone('Asia/Tokyo')) - timedelta(days=15)
day_ago = day.strftime('%b %d %H:%M:%S')


def generate_logger():
    """
    This Function will check the mhi_script_execution_logs is available if not, it will create the new mhi_script_execution_logs file path.

    Parameters
    ----------
    Returns
    -------
    Logger object.

    """
    try:
        log_file_path = working_directory + 'mhi_script_execution_logs/mhi_script_execution_logs_' + \
            str(datetime.now().strftime("%Y_%m_%d")) + '.log'
        if os.path.exists(log_file_path.rsplit("/", 1)[0]):
            if os.path.exists(log_file_path):
                log_file_name = log_file_path
            else:
                log_file = open(log_file_path, 'a')
                log_file.close()
                log_file_name = log_file_path
        else:
            try:
                os.mkdir(log_file_path.rsplit("/", 1)[0])
                log_file = open(log_file_path, 'a')
                log_file.close()
                log_file_name = log_file_path
            except Exception as e:
                print("Error while creating log file from imports.py\n", e)
        if log_file_name:
            try:
                log_process_activities(
                    'mhi_script_execution_logs', log_file_name)
                logger = logging.getLogger('mhi_script_execution_logs')
            except Exception as e:
                log_process_activities(
                    'mhi_script_execution_logs', log_file_path)
                logger = logging.getLogger('mhi_script_execution_logs')
        return logger
    except Exception as e:
        print("Got Error in generate_logger function as:\n", e)


def log_process_activities(logger_name, log_file, level=logging.INFO):
    """
    This Function will create a logger object.

    Parameters
    ----------
    logger_name : String
        DESCRIPTION: name of the logger object.
    log_file : String
        DESCRIPTION: Path to log file.
    logger_level : String
        DESCRIPTION: Level of logging to be tracked.

    Returns
    -------
    Logger object.

    """
    try:
        logger = logging.getLogger(logger_name)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        fileHandler = logging.FileHandler(log_file, mode='a')
        fileHandler.setFormatter(formatter)
        logger.setLevel(level)
        logger.addHandler(fileHandler)

        return logger
    except FileNotFoundError as error:
        logger.error(
            "FileNotFoundError at log_process_activities " + str(error))
    except Exception as error:
        logger.error("Error at log_process_activities " + str(error))


logger = generate_logger()
