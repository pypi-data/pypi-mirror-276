from astropy.io import fits
import logging, os, sys
from logging.handlers import TimedRotatingFileHandler


def print_time(seconds: float):

    us = 1e-6
    ms = 1e-3
    s = 1
    minute = 60
    hour = 3600
    day = 86400

    asec = abs(seconds)

    if asec < ms:
        ss = f'{seconds/us:.2f} us'

    elif asec < s:
        ss = f'{seconds/ms:.2f} ms'

    elif asec < minute:
        ss = f'{seconds/s:.2f} s'

    elif asec < hour:
        ss = f'{seconds/minute:.2f} min'

    elif asec < day:
        ss = f'{seconds/hour:.2f} h'
    
    else:
        ss = f'{seconds/day:.2f} d'

    return ss


def update_hdr_file(hdr_file_name, key, value, comment=''):

    with fits.open(hdr_file_name) as hdul:
        hdr = hdul[0].header

    update_hdr_card(hdr, key, value, comment)

    hdr.tofile(hdr_file_name, overwrite=True)


def update_hdr_card(hdr: fits.Header, key: str, value, comment: str):

    if key.upper() == 'END': key = 'END_'
    if len(key) > 8: key = 'HIERARCH '+key
    hdr[key] = (value, comment)


def init_logger(name, loglevel=logging.INFO, fileloglevel=None):

    # Initialize logger
    logger = logging.getLogger(name)

    # global logging level
    logger.setLevel(logging.DEBUG)

    # do not add handlers if a root logger is configured
    if logger.hasHandlers(): 
        logger.addHandler(logging.NullHandler())
        return logger

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)-25s - %(levelname)-8s - %(message)s')

    # create console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(loglevel)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # create file handler if requested
    if fileloglevel:
        # file log directory
        logdir = ("log")
        if not os.path.isdir(logdir):
            os.makedirs(logdir)

        # create file handler
        fh = TimedRotatingFileHandler(
            os.path.join(logdir, name+'.log'), when='midnight', utc=True, delay=True)
        fh.setLevel(fileloglevel)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
