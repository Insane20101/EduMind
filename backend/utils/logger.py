import logging
import json
import sys

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module
        }
        
        # Add any extra attributes passed in via 'extra' dictionary
        for k, v in record.__dict__.items():
            if k not in ["args", "asctime", "created", "exc_info", "exc_text", "filename", "funcName", 
                         "id", "levelname", "levelno", "lineno", "module", "msecs", "message", "msg", 
                         "name", "pathname", "process", "processName", "relativeCreated", "stack_info", "thread", "threadName"]:
                log_obj[k] = v
                
        return json.dumps(log_obj)

def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
        # Prevent log messages from being propagated to the root logger and printed multiple times
        logger.propagate = False
    return logger
