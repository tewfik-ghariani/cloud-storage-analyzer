import sys
import os
import subprocess


bindir = os.path.dirname(os.path.realpath( __file__ ))
prefix = os.path.dirname(bindir)

def run(args):
    subenv = os.environ.copy()
    subenv['S3LIB_HOME'] = prefix

    java_args = ['java', '-jar', prefix + '/lib/static/cloud-store/lib/java/s3lib-0.2.jar']
    java_args.extend(args)

    subprocess.call(java_args)

def main(cmd):
    if not isinstance(cmd, list):
        cmd = cmd.strip().split()
    run(cmd)
