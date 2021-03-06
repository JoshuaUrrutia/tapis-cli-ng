"""Functions for inspecting Git repository details at runtime"""
import subprocess
# Portable and does not introduce any dependencies

__all__ = [
    'get_git_revision_hash', 'get_git_revision_short_hash', 'get_git_remote'
]


def get_git_revision_hash():
    return subprocess.check_output(['git', 'rev-parse',
                                    'HEAD']).decode().strip()


def get_git_revision_short_hash():
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'],
                                   stderr=subprocess.DEVNULL).decode().strip()


def get_git_remote(name='origin'):
    return subprocess.check_output(['git', 'remote', 'get-url', name],
                                   stderr=subprocess.DEVNULL).decode().strip()
