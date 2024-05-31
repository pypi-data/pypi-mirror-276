import loguru

logger = loguru.logger
logger.remove(0)
logger.add("./logs/info.log", format="[{time:YYYY-MM-DD HH:mm:ss}-{level}] {message}", rotation="00:00", encoding="utf-8", level="INFO",
           filter=lambda record: record["level"].no == logger.level("INFO").no)
logger.add("./logs/warn.log", format="[{time:YYYY-MM-DD HH:mm:ss}-{level}] {message}", rotation="00:00", encoding="utf-8", level="WARNING",
           filter=lambda record: record["level"].no == logger.level("WARNING").no)
logger.add("./logs/error.log", format="[{time:YYYY-MM-DD HH:mm:ss}-{level}] {message}", rotation="00:00", encoding="utf-8", level="ERROR",
           filter=lambda record: record["level"].no >= logger.level("ERROR").no)
