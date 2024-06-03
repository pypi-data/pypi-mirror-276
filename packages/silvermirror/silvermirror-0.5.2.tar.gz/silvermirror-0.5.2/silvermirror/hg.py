#!/usr/bin/env python

"""
stub for the hg backend of silvermirror
"""

# imports
import argparse
import hglib # http://mercurial.selenic.com/wiki/PythonHglib
import lxml.html
import os
import subprocess
import sys
from hglib.error import ServerError
from urllib.parse import urlparse

def clone(source, path):
    print ('Cloning {} -> {}'.format(source, path))
    return hglib.clone(source, path)


def pull(source, path):
    """
    pull changes from host on path
    """

    if not os.path.isdir(path):
        raise OSError('Not a directory: {}'.format(path))
    command = ['hg', 'pull', source]
    subprocess.check_call(command, cwd=path)


def update(source, path):
    """
    get changes from host on path
    """

    if not os.path.exists(path):
        return clone(source, path)

    try:
        repo = hglib.open(path)
        print ('Updating {}'.format(path))
        try:
            repo.pull(source, update=True, insecure=True)
        except TypeError:
            # Traceback (most recent call last):
            #   File "/home/jhammel/k0s/bin/mirror-hg", line 33, in <module>
            #     sys.exit(load_entry_point('silvermirror', 'console_scripts', 'mirror-hg')())
            #   File "/home/jhammel/k0s/src/silvermirror/silvermirror/hg.py", line 116, in main
            #     update(source, dest)
            #   File "/home/jhammel/k0s/src/silvermirror/silvermirror/hg.py", line 33, in update
            #     repo.pull(source, update=True, insecure=True)
            #   File "/home/jhammel/k0s/lib/python3.10/site-packages/hglib/client.py", line 1318, in pull
            #     self.rawcommand(args, eh=eh)
            #   File "/home/jhammel/k0s/lib/python3.10/site-packages/hglib/client.py", line 258, in rawcommand
            #     ret = self.runcommand(args, inchannels, outchannels)
            #   File "/home/jhammel/k0s/lib/python3.10/site-packages/hglib/client.py", line 186, in runcommand
            #     if any(b('\0') in a for a in args):
            #   File "/home/jhammel/k0s/lib/python3.10/site-packages/hglib/client.py", line 186, in <genexpr>
            #     if any(b('\0') in a for a in args):
            # TypeError: 'in <string>' requires string as left operand, not bytes
            pull(source, path)
    except ServerError:
        repo = hglib.clone(source, path)
    return repo


def repositories_http(url):
    """
    returns the list of repositories under a URL of an hg server
    """
    element = lxml.html.parse(url)
    tds = element.xpath('//tr[position() > 1]/td[1]')
    repos = [i.text_content() for i in tds]
    return repos

def repositories_ssh(url):
    """
    returns the list of repositories under a URL via ssh
    """
    # This does require that ssh be able to run non-interactively
    # ssh k0s.org ls -1 ~/hg
    # This also requires that all contents in the directory
    # are repositories

    # parse the URL
    parsed = urlparse(url)
    assert parsed.scheme.lower() == 'ssh'
    host = parsed.netloc
    path = parsed.path.strip('/')

    # Run ssh command
    # TODO: support user@host
    command = ['ssh', host, 'ls', '-1', path]
    output = subprocess.check_output(command)
    return output.decode().strip().splitlines()


def repositories(url):
    """
    returns the list of hg repositories of a supported URL
    (HTTP, TODO SSH)
    """
    parsed = urlparse(url)
    scheme = parsed.scheme.lower()
    if parsed.scheme in ('http', 'https'):
        return repositories_http(url)
    elif parsed.scheme == 'ssh':
        return repositories_ssh(url)
    else:
        raise ValueError('unsupported scheme: {}'.format(scheme))

def main(args=sys.argv[1:]):
    """CLI"""

    # parse command line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('host',
                        help="URL of mercurial repository index page")
    parser.add_argument('-d', '--directory', dest='directory',
                        default=os.path.join(os.environ['HOME'], 'hg'),
                        help="base directory to clone/update to [DEFAULT: %(default)s]")
    parser.add_argument('-r', '--repo', dest='repositories', nargs='+',
                        help="repositories")  # TODO: stub
    parser.add_argument('--list', dest='list',
                        action='store_true', default=False,
                        help="list repositories and exit")
    options = parser.parse_args(args)

    # kill trailing slash
    options.host = options.host.rstrip('/')

    # get repositories
    repos = repositories(options.host)
    if options.list:
        for repo in repos:
            print(repo)
        return

    # clone/update repos to directory
    os.makedirs(options.directory, exist_ok=True)
    for repo in repos:
        source = '{}/{}'.format(options.host, repo)
        dest = os.path.join(options.directory, repo)
        update(source, dest)


if __name__ == '__main__':
    sys.exit(main() or 0)
