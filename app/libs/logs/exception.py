import logging


class Exc:
    def create_exception():

        # create a logger object
        logger = logging.getLogger('exc_logger')
        logger.setLevel(logging.INFO)

        # logged exceptions
        logfile = logging.FileHandler('tmp/exc_logger.log')

        fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(fmt)

        logfile.setFormatter(formatter)
        logger.addHandler(logfile)

        return logger