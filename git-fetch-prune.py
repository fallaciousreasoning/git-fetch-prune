#!/usr/bin/python3

import subprocess

def git_output(args):
    result = subprocess.run(['git', *args], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')

def get_master_branch():
    possible_masters = [ 'develop' ]

    for possible in possible_masters:
        output = git_output(['branch', '--list'])
        if output:
            return possible

    return 'master'

def get_merged_branches(master_branch):
    output = git_output([
        'for-each-ref',
        '--merged',
        f'origin/{master_branch}',
        '--format',
        '%(refname:short)',
        'refs/heads'])
    branches = output.split('\n')

    for branch in branches:
        if not branch:
            continue

        yield branch

def delete_branch(branch):
    git_output(['branch', '-D', branch])
    
def run(dry_run=True):
    master_branch = get_master_branch()
    merged_branches = get_merged_branches(master_branch)

    for branch in merged_branches:
        if not dry_run:
            delete_branch(branch)
        print(f'Deleted {branch}')

run()