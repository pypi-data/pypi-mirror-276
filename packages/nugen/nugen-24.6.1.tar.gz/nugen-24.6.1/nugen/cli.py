

import argparse
from . import __version__
from . import print_current_timestamp

def main():
    parser = argparse.ArgumentParser(description="nugen intelligence")
    parser.add_argument('action', nargs='?', default='help', choices=['timestamp', 'help'], help='Action to perform (default: help)')
    parser.add_argument('timezone', nargs='?', default='in', choices=['in', 'ng', 'eu', 'us'], help='Timezone abbreviation for timestamp (default: in)')
    parser.add_argument('--version', action='version', version='%(prog)s {version}'.format(version=__version__))

    args = parser.parse_args()
    
    if args.action == 'timestamp':
        print_current_timestamp(args.timezone)
    elif args.action == 'help':
        parser.print_help()

if __name__ == "__main__":
    main()

