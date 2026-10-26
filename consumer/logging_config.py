import json
import logging
import sys


class JsonFormatter(logging.Formatter):

    def format(self, record):
        return json.dumps(
            {
                "timestamp":
                    self.formatTime(record),

                "level":
                    record.levelname,

                "logger":
                    record.name,

                "message":
                    record.getMessage(),
            }
        )


def configure_logging():
    handler = logging.StreamHandler(
        sys.stdout
    )

    handler.setFormatter(
        JsonFormatter()
    )

    root = logging.getLogger()

    root.handlers.clear()
    root.addHandler(handler)

    root.setLevel(
        logging.INFO
    )