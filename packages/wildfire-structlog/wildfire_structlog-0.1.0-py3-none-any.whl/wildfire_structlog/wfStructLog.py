import inspect
import logging
import structlog
import orjson


# Use a class to make thread safe
class StructLogger:
    def __init__(self):
        self.initialized = False
        self.log_level_map = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
        }

    def add_context_from_cfg(self, log_context: dict, logger):
        if self.initialized:
            for k, v in log_context.items():
                logger = logger.bind(k=v)
            return logger
        else:
            raise ValueError("logger is not initialized")

    def initialize(self, logger_name: str, worker_id: str, log_level=None, factory=None):

        if self.initialized:
            return

        ll = logging.DEBUG if self.log_level_map.get(log_level) is None else self.log_level_map.get(log_level)
        factory = structlog.BytesLoggerFactory() if factory is None else factory

        structlog.configure(
            processors=[
                # Sets up a context
                structlog.contextvars.merge_contextvars,
                # Include loglevel
                structlog.processors.add_log_level,
                # Add line number, function name, and filename
                # Custom implementation for panBaseApp to get real caller info
                structlog.processors.CallsiteParameterAdder(
                    {
                        structlog.processors.CallsiteParameter.FILENAME,
                        structlog.processors.CallsiteParameter.FUNC_NAME,
                        structlog.processors.CallsiteParameter.LINENO,
                    }
                ),
                # Format tracebacks as strings
                structlog.processors.format_exc_info,
                # renames _event to msg
                structlog.processors.EventRenamer("msg", "_event"),
                # Add structured timestamps
                structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
                # Render log in JSON format with orjson
                structlog.processors.JSONRenderer(serializer=orjson.dumps),
            ],
            # filter to debug and higher - we can filter further at the cloud router
            wrapper_class=structlog.make_filtering_bound_logger(ll),
            # Produces byte-logger - this is the most performant option available out of the box
            logger_factory=factory,
            # get_logger method will always return a proxy to this logger
            cache_logger_on_first_use=True,
        )
        logger = structlog.get_logger().bind(configured=True, log_source="wf_structlog")
        logger.info("initialized structured logger")

        return_logger = structlog.get_logger(logger_name=logger_name, log_mode="wf_structlog", worker_id=worker_id)
        self.initialized = True

        return return_logger
