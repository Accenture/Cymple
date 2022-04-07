"""Package entrypoint when the package is run with -m option"""

from .version import __version__

if __name__ == '__main__':
    print('Welcome to Cymple version ' + __version__)
