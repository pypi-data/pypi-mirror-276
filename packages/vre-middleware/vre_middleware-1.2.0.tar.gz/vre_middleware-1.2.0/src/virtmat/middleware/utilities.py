"""various utilities for the VRE middleware"""
import os
import logging
import time
import json
import subprocess as sp
from virtmat.middleware.exceptions import SlurmError


def get_logger(name, default_level=logging.ERROR):
    """return a custom logger object"""
    fstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fstr))
    logger.addHandler(handler)
    logger.setLevel(default_level)
    return logger


def get_slurm_job_state(*args, method='parse', **kwargs):
    """select the method to get the SLURM job state"""
    if method == 'parse':
        return get_slurm_job_state_parse(*args, **kwargs)
    if method == 'json':
        return get_slurm_job_state_json(*args, **kwargs)
    raise ValueError(f'unknown method {method}')


def get_slurm_job_state_json(res_id, max_trials=3, trial_delay=3, trial=0):
    """extract the SLURM job state using the sacct command"""
    if trial > max_trials:
        msg = f'cannot get SLURM job state after {max_trials} trials'
        raise SlurmError(msg)
    command = f'sacct -j {res_id} --json'
    sacct_out = json.loads(sp.getoutput(command))  # nosec B605
    if len(sacct_out['jobs']) == 0:
        time.sleep(trial_delay)
        return get_slurm_job_state(res_id, max_trials, trial_delay, trial+1)
    assert sacct_out['jobs'][0]['job_id'] == int(res_id)
    return sacct_out['jobs'][0]['state']['current']


def get_slurm_job_state_parse(res_id, max_trials=10, trial_delay=3, trial=0):
    """extract the SLURM job state using the sacct command"""
    if trial > max_trials:
        msg = f'cannot get SLURM job state after {max_trials} trials'
        raise SlurmError(msg)
    command = f'sacct -j {res_id}.batch -n -o state'
    state = sp.getoutput(command).strip()  # nosec B605
    if len(state) == 0:
        time.sleep(trial_delay)
        return get_slurm_job_state(res_id, max_trials, trial_delay, trial+1)
    return state


def await_slurm_job_state(res_id, state, sleep_time=10):
    """return when a specified SLURM job state has been reached"""
    while get_slurm_job_state(res_id) != state:
        time.sleep(sleep_time)


def lmod_env_module(command):
    """Process lmod modules list and spider commands and return modules

    Due to ambiguous format of provided input it is assumed that the last
    division is the module version in the case of more than one division.

    Args:
        command (str): either 'list' or 'spider'

    Returns:
        (dict): {prefix/.../name: [version1, ...]} in case of more divisions
                {'name': []} in case of one division

    """
    assert isinstance(command, str) and command in ('list', 'spider')
    lmod_cmd = os.environ.get('LMOD_CMD')
    if lmod_cmd is None:
        return None
    full_command = [lmod_cmd, 'bash', '-t', command]
    with sp.Popen(full_command, stdout=sp.DEVNULL, stderr=sp.PIPE) as proc:  # nosec B603
        string = proc.stderr.read().decode()
    if string.strip() == 'No modules loaded':
        return None
    mods_lst = string.strip().split('\n')
    mods_dct = {}
    for mod in mods_lst:
        divisions = mod.split('/')
        name = '/'.join(divisions[:-1]) if len(divisions) > 1 else divisions[0]
        mods_dct[name] = []
    for mod in mods_lst:
        divisions = mod.split('/')
        if len(divisions) > 1:
            version = divisions[-1]
            if version:
                mods_dct['/'.join(divisions[:-1])].append(version)
    return mods_dct
