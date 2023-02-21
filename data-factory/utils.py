class logger:
    def __init__(self):
        self.log_str = "[{}]: {}"

    def default(self, process, message):
        print(self.log_str.format(process), message)

    def error(self, process, message):
        print(self.log_str.format(process, "ERROR"), message)

    def warning(self, process, message):
        print(self.log_str.format(process, "WARNING"), message)

    def info(self, process, message):
        print(self.log_str.format(process, "INFO"), message)
