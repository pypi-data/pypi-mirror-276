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
    URL
'''
class Url:
    '''
        URL
    '''
    def __init__(self, value: str) -> None:
        '''
            Init
        '''
        self.value = value

    def __truediv__(self, other) -> "Url":
        '''
            Truediv.
        '''
        _other = other.value if isinstance(other, Url) else other
        return Url(f"{self.value}/{_other}")

    def __str__(self):
        '''
            Str
        '''
        return self.value

    def __eq__(self, other):
       '''
           Eq
       '''
       if isinstance(other, str):
           return self.value == other
       elif isinstance(other, Url):
           return self.value == other.value
       else:
           return NotImplemented
