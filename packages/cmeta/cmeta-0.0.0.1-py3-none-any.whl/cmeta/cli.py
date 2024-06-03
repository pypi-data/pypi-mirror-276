#
# CMX: Common Metadata eXchange
#
# (C)opyright 2024 cKnowledge.org
#

import sys

cmx = None

############################################################
def cli(cmd = None):

    global cmx

    # First parse command line (some flags may control CM init)
    r = parse(cmd)
    if r['return'] >0: return r

    category = r.get('category', '')
    action = r.get('action', '')
    flags = r.get('flags', {})
    control = r.get('control', {})

    # Init or reuse CM
    if cmx == None:
        from cmeta.core import CMeta
        cmx = CMeta()

    # Access CMX function
    r = cmx.access(category, action, flags, control)
    return r

############################################################
def parse(cmd):
    """
    Parse command line into access dictionary.

    Args:
        cmd (str | list) : arguments as a string or list

    Returns:
        (CM return dict):

        * return (int): return code == 0 if no error and >0 if error
        * (error) (str): error string if return>0

        * category (str): category
        * action (str): action
        * args (list of str)
        * flags (dict): flags for category
        * control (dict): flags for CMX framework

    """

    # If input is string, convert to argv
    # We use shlex to properly convert values with spaces wrapped with ""

    if cmd is None:
        argv = sys.argv[1:]

    elif type(cmd) == str:
        import shlex
        argv = shlex.split(cmd)

    else:
        argv = cmd

    # Main arguments
    category = ''
    action = ''

    # Positional arguments
    args = []

    # Main flags to category (starts with --)
    flags = {}

    # Control flags for CMeta (starts with -)
    control = {}

    for a in argv:
        if a.startswith('@'):
            # Load JSON or YAML file
            from xk import utils
            r = utils.load_json_or_yaml(file_name = a[1:], check_if_exists=True)
            if r['return'] >0 : return r

            meta = r['meta']

            flags.update(meta)

        elif not a.startswith('-'):
            if category == '':
                category = a
            elif action == '':
                action = a
            else:
                # append arguments
                args.append(a)

        else:
            # flags
            where = flags if a.startswith('--') else control

            j = a.find('=') # find first =
            if j>0:
               key = a[:j].strip()
               value = a[j+1:].strip()
            else:
               key=a
               value=True

            if key.startswith('-'): key=key[1:]
            if key.startswith('-'): key=key[1:]

            if key.endswith(','): 
               key = key[:-1]
               value = value.split(',') if value!="" else []

            if '.' in key:
               keys = key.split('.')
               new_where = where

               first = True

               for key in keys[:-1]:
                   if first:
                       first = False

                   if key not in new_where:
                      new_where[key] = {}
                   new_where = new_where[key]

               new_where[keys[-1]] = value
            else:
               where[key] = value

    if len(args)>0:
        flags['args'] = args

    return {'return':0, 'category':category, 'action':action, 'flags':flags, 'control':control}


############################################################
if __name__ == "__main__":
    cli()
