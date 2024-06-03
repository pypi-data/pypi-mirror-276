#
# CMX: Common Metadata eXchange
#
# (C)opyright 2024 cKnowledge.org
#

import sys
import os
import logging

from cmeta import utils
from cmeta import repos

cmx = None
cmx_module_class_cache = {}
cmx_logger = logging.getLogger(__name__)

############################################################
class CMeta(object):
    """
    """

    ############################################################
    def __init__(self, home_path = '', cfg = {}):
        """
        """

        r = self.init(home_path, cfg)
        if r['return'] > 0: self.halt(r)


    ############################################################
    def init(self, home_path, cfg):
        """
        """

        ##########################################################################################
        # Default configuration
        self.cfg = {
          "debug": False,

          "error_prefix": "CMX error:",

          "env_venv_python": "VIRTUAL_ENV",
          "env_venv_conda": "CONDA_PREFIX",

          "env_home_path": "CMX_HOME",
          "env_internal_repo_path": "CMX_INTERNAL_REPO",
          "default_home_dir": "CMX",

          "file_repos": "cmx-repos.json",
          "dir_repos": "repos",

          "internal_repo": "internal",

          "repo_meta_file": "_cmr",
          "repo_module_dir": "category",

          "module_prefix": "cmeta_",

          "local_repo_name": "local",
          "local_repo_meta": {
              "uid": "9a3280b14a4285c9",
              "alias": "local"
          },

        }

        self.cfg.update(cfg)

        ##########################################################################################
        # Configure logger

        self._logger = cmx_logger
        logging.basicConfig(level = logging.INFO)

        self._logger.debug('initialize CMeta class')

        ##########################################################################################
        # Check the path to store repositories and internal info
        # (detect if inside venv or conda)

        self.home_path = ''

        if home_path !=None and home_path != '':
            if not os.path.isdir(home_path):
                return {'return': 1, 'error': 'home directory {} not found'.format(home_path)}

            self.home_path = home_path

        if self.home_path == '':
            # Check from env
            for key in ['env_venv_python', 'env_venv_conda']:
                home_path = os.environ.get(self.cfg[key], '').strip()
                if home_path != '' and os.path.isdir(home_path):
                    self.home_path = os.path.join(home_path, self.cfg['default_home_dir'])
                    break

        if self.home_path == '':
            home_path = os.environ.get(self.cfg['env_home_path'], '').strip()
            if home_path !='':
                self.home_path = home_path

        if self.home_path == '':
            from os.path import expanduser
            self.home_path = os.path.join(expanduser("~"), self.cfg['default_home_dir'])

        if self.home_path != '' and not os.path.isdir(self.home_path):
            os.makedirs(self.home_path)

        ##########################################################################################
        # Check if file with repos exists and load it
        self.repos = repos.Repos(self.home_path, self.cfg)

        r = self.repos.load()
        if r['return'] > 0: return r

        ##########################################################################################
        # Process paths to categories
        for path_to_module in self.repos.module_paths:
            sys.path.append(path_to_module)

        # Add to the end of system path (can be overrided from local and other repos)
        path_to_this_module = os.path.join(os.path.dirname(__file__), self.cfg['repo_module_dir'])
        sys.path.append(path_to_this_module)

        return {'return': 0}


    ############################################################
    def error(self, r):
        """
        If r['return']>0: print CM error in r['error'] 
        and raise error if in debugging mode

        Args:
           r (dict): output from CM function with "return" and "error"

        Returns:
           (dict): r

        """

        import os

        if r['return']>0:
            if self.cfg.get('debug', False):
                raise Exception(r['error'])

            x = '\n{} {}'.format(self.cfg['error_prefix'], r['error'])

            self._logger.error(x)

        return r

    ############################################################
    def halt(self, r):
        """
        If r['return']>0: print CM error in r['error'] 
        and raise error if in debugging mode or halt with r['return'] code

        Args:
           r (dict): output from CM function with "return" and "error"

        Returns:
           (dict): r
        """

        # Force console
        self.error(r)

        sys.exit(r['return'])

    ############################################################
    def access(self, category = '', action = '', flags = {}, control = {}):
        """
        """

        global cmx_module_class_cache

        import importlib
        from cmeta.category import Category

        ##########################################################################################
        # Check if Python module for a given Category exists.
        # Use default Category class otherwise.
        if category == '' or category == '-': 
             category = 'internal'

        module = self.cfg['module_prefix'] + category

        module_name = module + '.api'

        if module_name in cmx_module_class_cache:
            module_class = cmx_module_class_cache[module_name]
        else:
            try:
                module_code = importlib.import_module(module_name)
            except ModuleNotFoundError as e1:
                module_code = None
            except Exception as e2:
                return {'return':1, 'error':'problem loading module {}: {}'.format(module_name, format(e2))}

            # Initialize Category class with common and extra actions
            if module_code == None:
                module_class = Category(self)
            else:
                module_class = module_code.CMetaCategory(self)

            cmx_module_class_cache[module_name] = module_class

        ##########################################################################################
        # Check action
        if action == '':
             action = 'default'

        if not hasattr(module_class, action):
            return {'return':1, 'error':'action "{}" not found for category "{}"'.format(action, category)}

        action_addr = getattr(module_class, action)

        ##########################################################################################
        # Update class
        module_class.rt_category = category
        module_class.rt_action = action

        ##########################################################################################
        # Call action for a given category

        r = action_addr(**flags)
        return r

############################################################
def access(category = '', action = '', flags = {}, control = {}):
    """
    Automatically initialize CM and run automations 
    without the need to initialize and customize CM class.
    Useful for Python automation scripts.

    See CM.access function for more details.
    """

    global cmx

    if cmx is None:
       cmx = CMeta()

    return cmx.access(category, action, flags, control)

############################################################
def error(i):
    """
    Automatically initialize CM and print error if needed
    without the need to initialize and customize CM class.
    Useful for Python automation scripts.

    See CMeta.error function for more details.
    """

    global cmx

    if cmx is None:
       cmx = CMeta()

    return cmx.error(i)

############################################################
def halt(i):
    """
    Automatically initialize CM, print error and halt if needed
    without the need to initialize and customize CM class.
    Useful for Python automation scripts.

    See CMeta.halt function for more details.

    """

    global cmx

    if cmx is None:
       cmx = CMeta()

    return cmx.halt(i)
