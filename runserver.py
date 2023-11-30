"""module runserver: server of luxapp
"""
import argparse
from sys import exit, stderr
from luxapp import app
import os

def parse_args():
    """$ python runserver.py -h
usage: runserver.py [-h] port

The YUAG search application

positional arguments:
  port        the port at which the server should listen

optional arguments:
  -h, --help  show this help message and exit
    """
    parser = argparse.ArgumentParser(description="The YUAG search application",
                                     prog='runserver.py', allow_abbrev=False,
                                     usage='%(prog) s' + '[-h] port')
    parser.add_argument("port", help="the port at which the server should listen")
    return parser.parse_args()

def main():
    """main function
    """

    args = parse_args()

    try:
        port = int(args.port)
        if port <= 0:
            raise ValueError()
    except ValueError:
        print('Error: Port must be a positive integer.', file=stderr)
        exit(1)

    # Check if the database file exists
    if not os.path.exists('lux.sqlite'):
        print('Error: The database file lux.sqlite does not exist.', file=stderr)
        exit(1)

    try:
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

if __name__ == '__main__':
    main()



