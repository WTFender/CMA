from CMA.api import Handler
import argparse
import json

parser = argparse.ArgumentParser(description='Cleveland Museum of Art API Wrapper.')
parser.add_argument('--verbose', dest='verbose', action='store_true')

# Subcommands
subparsers = parser.add_subparsers(dest='command')
subparsers.required = True
artwork_cmd = subparsers.add_parser("artwork")
curator_cmd = subparsers.add_parser("curator")
exhibit_cmd = subparsers.add_parser("exhibition")

# Require --id or --search for each subcommand
for cmd in [artwork_cmd, curator_cmd, exhibit_cmd]:
    cmd.add_argument('--pretty', dest='pretty', action='store_true', help='pretty print summary')
    flags = cmd.add_mutually_exclusive_group(required=True)
    flags.add_argument('--search', dest='search', type=str, help='search terms for resource')
    flags.add_argument('--id', dest='resource', type=str, help='resource ID to retrieve')

# Add ascii preview flag
artwork_cmd.add_argument('--preview', dest='preview', action='store_true', help='generate ascii preview')

def main():
    cma = Handler()
    args = parser.parse_args()
    
    if args.verbose:
        print(args)

    if args.command == 'artwork':

        if args.resource:
            output = cma.get_artwork(rid=args.resource, preview=args.preview)

            if args.pretty:
                print()

            if args.pretty:
                print('Title: ' + output['title'])
                print('Type: ' + output['type'])
                creators = ", ".join([c['description'] for c in output['creators']])
                print('Creator: ' + creators)
                print('Culture: ' + ", ".join(output['culture']))
                if 'preview' in output:
                    print('Link: ' + output['images']['web']['url'])
                    print('Preview: ')
                    print(output['preview'])

        elif args.search:
            output = 'search not yet implemented'

    elif args.command == 'curator':
        output = 'curator not yet implemented'

    elif args.command == 'exhibition':
        output = 'exhibition not yet implemented'

    else:
        raise Exception('Unknown subcommand.')
    
    if not args.pretty:
        print(json.dumps(output, indent=4))
