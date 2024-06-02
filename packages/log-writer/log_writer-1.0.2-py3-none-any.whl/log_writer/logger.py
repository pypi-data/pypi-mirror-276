import os
from datetime import datetime


class WriteLogger:
    __instance = None

    __LOGS = "logs"
    __INFO = "info.log"
    __ERROR = "error.log"
    __NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __new__(cls, base_dir):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls.__instance.base_dir = base_dir
            cls.__instance.__log_dir = os.path.join(base_dir, cls.__LOGS)
            cls.__instance.__make_dir()
        return cls.__instance

    @classmethod
    def __make_dir(cls):
        os.makedirs(cls.__instance.__log_dir, exist_ok=True)
        cls.__make_files(cls.__INFO)
        cls.__make_files(cls.__ERROR)

    @classmethod
    def __make_files(cls, file_name):
        file = os.path.join(cls.__instance.__log_dir, file_name)
        if not os.path.exists(file):
            with open(file, "w", encoding="utf-8") as f:
                f.write(f"File made at " + cls.__NOW)

    @classmethod
    def __write_messages(cls, status, message):
        file = cls.__INFO if status == "info" else cls.__ERROR
        with open(os.path.join(cls.__instance.__log_dir, file), "a") as f:
            f.write(f"\n{message} at {cls.__NOW}")

    @classmethod
    def info(cls, message):
        cls.__write_messages("info", message)

    @classmethod
    def error(cls, message):
        cls.__write_messages("error", message)
