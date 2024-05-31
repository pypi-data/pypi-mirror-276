"""command-line tools to configure available resources"""
import os
from virtmat.middleware.resconfig import get_resconfig_loc
from virtmat.middleware.resconfig import ResConfig, set_defaults_from_guess
from virtmat.middleware.exceptions import SlurmError, ResourceConfigurationError


def setup_resconfig():
    """setup resource configuration interactively"""
    resconfig_loc = get_resconfig_loc()
    if os.path.exists(resconfig_loc):
        return

    def _configure():
        try:
            cfg = ResConfig.from_scratch()
            set_defaults_from_guess(cfg.default_worker)
        except SlurmError as err:
            print(err)
        except ResourceConfigurationError as err:
            print(err)
        else:
            resconfig_dir = os.path.dirname(resconfig_loc)
            if not os.path.exists(resconfig_dir):
                os.makedirs(resconfig_dir, exist_ok=True)
            cfg.to_file(resconfig_loc)
    print(f'Resource configuration {resconfig_loc} not found.\n'
          'Do you want to create it?')
    while True:
        try:
            inp = input('Yes(default) | No | Ctrl+C to skip: ').strip()
        except KeyboardInterrupt:
            print('\n')
            break
        else:
            if inp.lower() in ('no', 'n'):
                break
            if inp.lower() in ('yes', ''):
                _configure()
                break
            continue
