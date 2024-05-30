'''
    Config

    This file is used to configure the module
'''
import logging

#logger
logger_level = logging.ERROR
logger_words_to_highlight = [
    "fetching",
    "Keys",
    "mapping",
    "filtering",
    "converting",
    "importing",
    "exporting",
    "validating",
    "deleting",
    "parsing",
    "getting",
    "writing",
    "reading",
    "found",
    "making",
    "removing",
    "selecting",
    "multiplexing",
    "emptying",
    "creating",
    "initializing",
    "logging",
    "checking",
    "requesting",
    "imported",
    "exported",
    "Step"
]
logger_show_time = False
logger_formatter_stdout = "%(message)s"                                     # Rich has this built in
logger_formatter_stdout_in_file = "%(levelname)s - %(message)s %(name)s"    # We don't use Rich to logs stdout to files
