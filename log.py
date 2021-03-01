import logging


class log:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level=logging.DEBUG)
        handler = logging.FileHandler("training_log.txt",encoding='GBK')
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s  - %(message)s')
        handler.setFormatter(formatter)

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)

        self.logger.addHandler(handler)
        self.logger.addHandler(console)

    def loginfo(self,data):
        self.logger.info(data)

    def logdebug(self,data):
        self.logger.debug(data)
    
    def logwarning(self,data):
        self.logger.warning(data)

    def logerror(self,data):
        self.logger.error(data, exc_info=True)