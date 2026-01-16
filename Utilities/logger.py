import logging
import colorlog

# Define custom log level TEST
TEST_LEVEL = 25  # Between INFO (20) and WARNING (30)
logging.addLevelName(TEST_LEVEL, 'TEST')

def test(self, message, *args, **kws):
    if self.isEnabledFor(TEST_LEVEL):
        self._log(TEST_LEVEL, message, args, **kws)

logging.Logger.test = test

def get_logger(name):
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)s: %(message)s",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'TEST': 'blue',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    ))

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.propagate = False  # Prevent duplicate logs
    return logger

