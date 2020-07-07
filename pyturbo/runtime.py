import os
import resource
import faulthandler

try:
    '''
    Prefer Pytorch's multiprocessing module for optimized sharing of Tensor
    '''
    import torch.multiprocessing as mp
    try:
        resource.setrlimit(resource.RLIMIT_NOFILE, (1048576, 1048576))
    except:
        mp.set_sharing_strategy('file_system')
except:
    import multiprocessing as mp

mp = mp.get_context('spawn')
faulthandler.enable()
DevModes = set(os.environ.get('PYTURBO_DEV', '').split())
