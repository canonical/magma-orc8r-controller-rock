#!/usr/bin/env python3

"""Setups Build Context.

build_context.py creates the build context for the orc8r rock build.
It first creates a tmp directory, and then copies the cloud directories
for all modules into it.
"""

import glob
import os
import shutil

HOST_BUILD_CONTEXT = '/tmp/magma_orc8r_build'
HOST_MAGMA_ROOT = '../../../.'
IMAGE_MAGMA_ROOT = os.path.join('src', 'magma')


def main():
    modules = [
        'orc8r',
        'lte',
        'feg',
    ]
    for module_name in modules:
        module_host_path = os.path.abspath(os.path.join(HOST_MAGMA_ROOT, module_name))
        build_context = os.path.join(HOST_BUILD_CONTEXT, IMAGE_MAGMA_ROOT, module_name)
        shutil.copytree(
            src=os.path.join(module_host_path, 'cloud'),
            dst=os.path.join(build_context, 'cloud'),
        )
        if module_name == 'orc8r':
            shutil.copytree(
                src=os.path.join(module_host_path, 'lib'),
                dst=os.path.join(build_context, 'lib'),
            )
            shutil.copytree(
                src=os.path.join(module_host_path, 'gateway'),
                dst=os.path.join(build_context, 'gateway'),
            )

        if os.path.isdir(os.path.join(module_host_path, 'cloud', 'configs')):
            shutil.copytree(
                os.path.join(module_host_path, 'cloud', 'configs'),
                os.path.join(HOST_BUILD_CONTEXT, 'configs', module_name),
            )

        for f in glob.iglob(build_context + '/**/go.mod', recursive=True):
            gomod = f.replace(HOST_BUILD_CONTEXT, os.path.join(HOST_BUILD_CONTEXT, 'gomod'),)
            os.makedirs(os.path.dirname(gomod))
            shutil.copyfile(f, gomod)


if __name__ == '__main__':
    main()
