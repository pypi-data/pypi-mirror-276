import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter('%(message)s'))

logger.addHandler(stream_handler)

def configure(filepath=None, graylog_host=None, graylog_port=None):
    
    formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s || %(message)s",
                datefmt="%d-%m-%Y %I:%M:%S")

    def setup_file_handler(file_path):
        file_handler = logging.FileHandler(file_path, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    def setup_graylog_handler(host, port):
        from graypy import GELFUDPHandler
        graylog_handler = GELFUDPHandler(host, port)
        graylog_handler.setFormatter(formatter)
        logger.addHandler(graylog_handler)
    
    if filepath:
        setup_file_handler(filepath)
    
    if graylog_host and graylog_port:
        setup_graylog_handler(graylog_host, graylog_port)
