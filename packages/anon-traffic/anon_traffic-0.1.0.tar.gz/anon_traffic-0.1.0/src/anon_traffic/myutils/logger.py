from anon_traffic.myutils import project_path
import logging
import logging.handlers
import os


# 配置日志基本设置
def setup_logging(filename="defult.log"):
    # 创建一个logger
    logger = logging.getLogger(filename.split(".")[0])
    logger.setLevel(logging.DEBUG)  # 可以根据需要设置不同的日志级别

    # 创建一个handler，用于写入日志文件
    log_file = os.path.join(project_path, "logs", filename)


    # 用于写入日志文件，当文件大小超过500MB时进行滚动
    file_handler = logging.handlers.RotatingFileHandler(log_file,
                                                        maxBytes=50 * 1024 *
                                                        1024,
                                                        backupCount=3)
    file_handler.setLevel(logging.DEBUG)

    # 创建一个handler，用于将日志输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 定义handler的输出格式
    # formatter = logging.Formatter
    # ('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 给logger添加handler
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

logger = setup_logging()
