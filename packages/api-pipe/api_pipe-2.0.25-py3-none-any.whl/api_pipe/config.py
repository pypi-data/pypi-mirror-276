# Copyright (C) 2024 RomanLabs, Rafael Roman Otero
# This file is part of API Pipe.
#
# API Pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# API Pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with API Pipe. If not, see <http://www.gnu.org/licenses/>.

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
