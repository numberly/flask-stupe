_logger = None


class Log(object):

    def _log(self, type, message, *args, **kwargs):
        global _logger
        if _logger is None:
            import logging
            _logger = logging.getLogger("stupe")
        return getattr(_logger, type)(message.rstrip(), *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self._log(*args, **kwargs)

    def __getattr__(self, attr):
        return self._proxy(attr)

    def _proxy(self, log_type):
        def __inner(*args, **kwargs):
            return self(log_type, *args, **kwargs)
        return __inner


log = Log()

__all__ = ["log"]
