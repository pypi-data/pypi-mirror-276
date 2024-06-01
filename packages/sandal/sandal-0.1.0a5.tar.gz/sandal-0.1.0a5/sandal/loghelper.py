import json
import logging
from logging import Formatter, LogRecord
from typing import TypeAlias

Verbosity: TypeAlias = int | bool | None


def vrb_to_level(verbose: Verbosity) -> int:
    if verbose is None:
        verbose = 0
    if verbose is True:
        verbose = 1

    level = logging.INFO
    if verbose < 0:
        level = logging.WARN
    elif verbose > 0:
        level = logging.DEBUG
    return level


class BunyanFormatter(Formatter):
    def format(self, record: LogRecord) -> str:
        if not hasattr(record, "message"):
            record.message = record.getMessage()

        obj = {
            "v": 0,
            "time": self.formatTime(record),
            "level": record.levelno + 10,
            "name": record.name,
            "pid": record.process,
            "msg": record.message,
        }
        return json.dumps(obj)
