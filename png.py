import os
import subprocess

def license(path, license_data):
    cmd = ['exiftool']
    for tag, val in license_data.items():
        cmd.append('-{}={}'.format(tag, val))
    cmd.append('-overwrite_original')
    if isinstance(path, str):
        cmd.append(os.path.abspath(path))
    elif isinstance(path, list):
        for f in path:
            cmd.append(os.path.abspath(f))
    else:
        raise ValueError('invalid path type')
    try:
        r = subprocess.run(cmd, stdout=subprocess.DEVNULL).returncode
    except Exception as e:
        raise Exception('exiftool invocation failed: ' + str(e))
    if r:
        raise Exception('exiftool returned error code: ' + str(r))
