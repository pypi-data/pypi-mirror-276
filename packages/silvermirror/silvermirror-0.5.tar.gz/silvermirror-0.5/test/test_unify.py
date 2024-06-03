# Requires `pytest`

import os
from silvermirror import unify

HERE = os.path.dirname(os.path.abspath(__file__))
CONF = os.path.join(HERE, 'silvermirror.ini')


def test_read_config():
    unify.read_config(CONF)

