#
# CMX: Common Metadata eXchange
#
# (C)opyright 2024 cKnowledge.org
#

import os
import logging

from cmind import utils

class Category:
    """
    """

    ############################################################
    def __init__(self, cmeta, self_file = '', self_name = ''):
        """
        """

        self.cmeta = cmeta
        self._version = '0.0.1'
        self._file = __file__ if self_file == '' else self_file
        self._name = __name__ if self_name == '' else self_name

        self._logger = logging.getLogger(self._name)

    ############################################################
    def default(self):
        print ('Default')
        return {'return':0}


    ############################################################
    def version(self):
        return {'return':0, 'version':self._version}
