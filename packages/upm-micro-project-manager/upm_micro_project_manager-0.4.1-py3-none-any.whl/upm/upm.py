##############################################################################
# author       # TecDroiD
# date         # 2022-12-02
# ---------------------------------------------------------------------------
# description  # simple python project management tool
#              #
#
#
##############################################################################
from upm.template import Template
import os
import logging


def get_template_file(cfg, filename):
    base = ''
    if 'template_path' in cfg:
        base = os.path.expanduser(cfg['template_path'])

    return os.path.join(base, f'{filename}.tmpl')


def get_values(plist):
    """ get values from parameter list (-p)
    """
    retval = {}
    if isinstance(plist, list):
        for item in plist:
            k, v = item.split('=', maxsplit=1)
            retval[k] = v
    return retval


def scan(cfg, args):
    """ scan directory
    """
    basedir = args.basedir
    name = args.name
    desc = args.description
    tmpl = Template.scan(name, basedir, desc)
    filename = get_template_file(cfg, name)

    if args.no_write:
        print(f'would write file {filename}:')
        print(tmpl.json)
    else:
        print(f'Writing file {filename}.')
        with open(filename, 'w') as fp:
            fp.write(tmpl.json)


def create(cfg, args):
    """ create a filestructure from pattern
    """
    item = args.item
    dest = args.destination

    # create destination directory if not existent
    if not os.path.exists(dest):
        os.makedirs(dest)

    # replace pattern or not.. that's the question
    rpl = True
    if args.no_replace is True:
        rpl = False

    pattern = cfg['pattern']
    pattern.update(get_values(args.parameter))

    tpath = get_template_file(cfg, item)
    template = Template.from_file(tpath)
    template.apply_parameters(pattern)
    template.create(dest, pattern, _replace=rpl)


def do_list(cfg, args):
    """ list known templates
    """
    print('Known templates:\n')
    for file in os.listdir(os.path.expanduser(cfg['template_path'])):
        if file.endswith('.tmpl'):
            print(file.replace('.tmpl', ''))
    print('\nuse upm describe <template> for more info on a template')


def describe(cfg, args):
    """ describe a single template
    """
    item = args.item
    tpath = get_template_file(cfg, item)
    template = Template.from_file(tpath)
    print(template)


def run(cfg, args):
    """ run the upm command
    """
    logging.debug(f'Running action {args.action}')
    actions = {
        'scan': scan,
        'init': create,
        'list': do_list,
        'desc': describe,
    }
    actions[args.action](cfg, args)
