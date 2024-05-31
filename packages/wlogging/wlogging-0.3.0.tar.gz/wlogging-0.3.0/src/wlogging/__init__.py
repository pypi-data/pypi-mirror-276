"""
Pytonic wrapper for the standard logging module
"""


from logging import *
from .loggers import *


add_level_name = addLevelName
basic_config = basicConfig
get_logger = getLogger


StreamHandler.add_filter = StreamHandler.addFilter
StreamHandler.handle_error = StreamHandler.handleError
StreamHandler.remove_filter = StreamHandler.removeFilter
StreamHandler.set_formatter = StreamHandler.setFormatter
StreamHandler.set_formatter = StreamHandler.setFormatter
StreamHandler.set_level = StreamHandler.setLevel
StreamHandler.set_stream = StreamHandler.setStream


Logger.add_filter = Logger.addFilter
Logger.add_handler = Logger.addHandler
Logger.call_handlers = Logger.callHandlers
Logger.find_caller = Logger.findCaller
Logger.get_child = Logger.getChild
Logger.get_effective_level = Logger.getEffectiveLevel
Logger.has_handlers = Logger.hasHandlers
Logger.is_enabled_for = Logger.isEnabledFor
Logger.make_record = Logger.makeRecord
Logger.remove_filter = Logger.removeFilter
Logger.remove_handler = Logger.removeHandler
Logger.set_level = Logger.setLevel


if hasattr(Logger, "getChildren"):
    Logger.get_children = Logger.getChildren


