import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
import tqdm
from os.path import isdir, isfile, join

import numpy as np
import pandas as pd

from scripts.format_json import json_join


def get_now():
    return datetime.datetime.now().strftime('%y-%m-%d_%H%M%S')


def write_log(log_name, message, log_type='INFO'):
    with open(log_name, 'a') as f:
        f.write('[{0}] [{2}]: {1}\n'.format(get_now(), message, log_type))


def shutdown(message='Shutting down machine'):
    # sys.exit(message)
    os.system('shutdown now')


vid_dir = 'images'
json_dir = 'json'
log_dir = 'logs'
label_dir = 'labels'
script_dir = 'scripts'


# The the absolute directory path of where the python file is located
root = os.path.dirname(os.path.realpath(__file__))

# Change the relative paths to absolute paths
vid_dir = join(root, vid_dir)
json_dir = join(root, json_dir)
log_dir = join(root, log_dir)
label_dir = join(root, label_dir)
script_dir = join(root, script_dir)

try:
    log = join(log_dir, get_now() + '.txt')
    write_log(log, 'Starting logging for pid {}'.format(os.getpid()))

except BaseException as e:
    shutdown()


try:
    json_file = join(label_dir, 'train.csv')
    labels = pd.read_csv(json_file, index_col=0, sep=';', header=None)
    labels = json.loads(labels.to_json())['1']

    json_file = join(label_dir, 'validation.csv')
    validation_labels = pd.read_csv(
        json_file, index_col=0, sep=';', header=None)
    validation_labels = json.loads(validation_labels.to_json())['1']

    json_file = join(label_dir, 'test.csv')
    test_labels = pd.read_csv(json_file, index_col=0, sep=';', header=None)
    test_labels['1'] = '?'
    test_labels = json.loads(test_labels.to_json())['1']

    labels.update(validation_labels)
    labels.update(test_labels)

except BaseException as e:
    write_log(log, 'Unable to get labels: {}'.format(e), log_type='FATAL')
    shutdown()


# Get the video directories only as directory name
try:
    vid_list = [i for i in os.listdir(vid_dir) if isdir(join(vid_dir, i))]
    vid_list = np.random.permutation(vid_list)
except BaseException as e:
    write_log(log, 'Cannot get video lists', log_type='FATAL')
    shutdown()


for j, i in tqdm(enumerate(vid_list)):
    print('\r Iteration {} out of {}'.format(j + 1, len(vid_list)), end='')
    input_dir = join(vid_dir, i)
    output_dir = join(json_dir, i)
    big_json_name = output_dir + '.json'
    write_log(log, '-' * 64)
    write_log(log, 'Starting video {}'.format(i))

    # if the directory exists then we can skip it
    # In case we run need to run it twice.
    try:
        if isfile(big_json_name):
            write_log(log, 'Big json exists going to next video')
            continue
        else:
            write_log(log, 'Making json directory')
            os.makedirs(output_dir)

    except BaseException as e:
        write_log(
            log, 'Something wrong with json file/dir: {}'.format(e), log_type='ERROR')
        continue

    ### run the openpose command ###
    write_log(log, 'Extracting features using openPose')
    rc = subprocess.run(['./scripts/openpose.sh', '{}'.format(input_dir),
                         '{}'.format(output_dir)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if rc.returncode == 0:
        write_log(log, rc.stdout)
        write_log(log, 'Features extracted for video {}'.format(
            i), log_type='COMPL')
    else:
        write_log(log, 'Unable to complete openPose extraction',
                  log_type='ERROR')
        write_log(log, 'Openpose stdout: {}'.format(str(rc.stdout)))
        write_log(log, 'OpenPose stderr: {}'.format(str(rc.stderr)))
        write_log(log, 'Delete json directory of {}'.format(i))
        shutil.rmtree(output_dir)
        continue

    ### Combine the json scripts into one ###
    try:
        big_json = json_join(output_dir, labels)
        with open(big_json_name, 'w') as j:
            json.dump(big_json, j)
        write_log(log, 'Concatenating json files')
    except BaseException as e:
        if isfile(big_json_name):
            os.remove(big_json_name)
        write_log(log, 'Concat json files {}'.format(e), log_type='ERROR')
        continue

    try:
        if isfile(big_json_name):
            write_log(log, 'Removing json dir')
            shutil.rmtree(output_dir)
        else:
            write_log(log, 'No file names {}'.format(
                big_json_name), log_type='ERROR')
    except:
        write_log(log, 'Couldn\'t remove json dir')
        continue


print()
write_log(log, 'End of programm shutting down machine')
shutdown()
