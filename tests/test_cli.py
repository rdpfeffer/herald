import herald.cli as cli
import herald.config as config

from .fixtures import basic_config


def test_main(basic_config):
    cli.main([], basic_config)
