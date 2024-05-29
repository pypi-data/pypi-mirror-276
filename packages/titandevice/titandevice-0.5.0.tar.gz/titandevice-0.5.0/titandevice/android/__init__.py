from titandevice.utils.logger_utils import DailyRotatingLogger

log_directory = "./log/"
log_filename = "titan_device.log"
logger = DailyRotatingLogger(log_directory, log_filename,'debug').get_logger()
