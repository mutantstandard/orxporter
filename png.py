import os
import subprocess

def license(path, license_data, max_batch=1000):
    cmd = ['exiftool']
    for tag, val in license_data.items():
        cmd.append('-{}={}'.format(tag, val))
    cmd.append('-overwrite_original')
    remaining = list(path)
    while remaining:
        batch, remaining = remaining[:max_batch], remaining[max_batch:]
        try:
            r = subprocess.run(cmd + batch,
                               stdout=subprocess.DEVNULL).returncode
        except Exception as e:
            raise Exception('exiftool invocation failed: ' + str(e))
        if r:
            raise Exception('exiftool returned error code: ' + str(r))
