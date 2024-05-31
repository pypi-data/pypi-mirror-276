# -*- coding: utf-8 -*-
###############################################################################
# author       # TecDroiD
# date         # 2022-12-02
# ---------------------------------------------------------------------------
# description  # configuration file management
#              #
#              #
##############################################################################
import json
import os
import logging
from datetime import date

BASECONFIG = {
    'pattern': {
        'current_date': date.today().isoformat(),
        'current_year': str(date.today().year)
    },
    'template_path': 'templates'
}


def synchronize(config, overlay):
    """ TODO: synchronize config with overlay recursively
    """
    for k, v in overlay.items():
        if k not in config or not isinstance(v, dict):
            config[k] = v
        else:
            synchronize(config[k], v)

    return config


def load(files=None):
    """ load configuration files
    """
    if files is None:
        files = ['./.cfg']
    cfg = dict(BASECONFIG)

    for file in files:
        logging.debug(f'trying config file {file}')
        fn = os.path.expanduser(file)
        if os.path.exists(fn):
            with open(fn) as fp:
                logging.debug(f'reading config {file}')

                cfg = synchronize(cfg, json.load(fp))

    logging.debug(f'{cfg}')

    return cfg
