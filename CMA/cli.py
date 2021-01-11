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
    flags = cmd.add_mutually_exclusive_group(required=True)
    flags.add_argument('--search', dest='search', type=str, help='search terms for resource')
    flags.add_argument('--id', dest='resource', type=str, help='resource ID to retrieve')

# Add api options
artwork_cmd.add_argument('--query', '-q', dest='q', type=str, help='Any keyword or phrase that searches against title, creator, artwork description, and several other meaningful fields related to the artwork.')
artwork_cmd.add_argument('--department', dest='department', type=str, help='Filter by department. List of valid departments in Appendix B.')
artwork_cmd.add_argument('--type', dest='type', type=str, help='Filter by artwork types. List of valid types in Appendix C.')
artwork_cmd.add_argument('--has_image', dest='has_image', type=int, help='0 or 1. Filter to return only artworks that have a web image asset. (synonymous with the deprecated field web_image)')
artwork_cmd.add_argument('--indent', dest='indent', type=int, help='Number of spaces to indent JSON content if "pretty" formatting is desired.')
artwork_cmd.add_argument('--skip', dest='skip', type=int, help='Offset index for results.')
artwork_cmd.add_argument('--limit', dest='limit', type=int, help='Limit for number of results. If no limit provided, API will return the maximum (1000) number of records.')
artwork_cmd.add_argument('--artists', dest='artists', type=str, help='Filter by name of artist.')
artwork_cmd.add_argument('--title', dest='title', type=str, help='Filter by title of artwork.')
artwork_cmd.add_argument('--medium', dest='medium', type=str, help='Filter by artwork medium.')
artwork_cmd.add_argument('--dimensions', dest='dimensions', type=str, help='Filter artworks by dimensions with the unit of measurement being meters. This filter is somewhat tricky, as the terminolgy for describing object dimensions varies from object to object (for example coins have diameters, swords have lengths, and necklaces have heights). An object\'s most descriptive dimension (whatever you think is the best way to describe it in meters) is generally put in the first part of the comma seperated list of dimensions. A default value of 20cm will be used if no value is provided for a dimension in the list. The second and third dimensions places are interchangable and describe a square that an object\'s remaining dimensions could fit inside. The dimensions filter returns objects with a fault tolerance of 20cm on all dimensions.')
artwork_cmd.add_argument('--dimensions_max', dest='dimensions_max', type=str, help='Filter artworks to return all works that can fit inside a box defined by provided 3 values with the unit of measurement being meters. Place the most descriptive dimension in the first value, and any remaining dimensions in the second two values. If no value is provided for a dimension, a default value of 20cm is used. The dimensions_max filter has a fault tolerance of 0 on all dimensions, and will not return objects that cannot fit in the described box.')
artwork_cmd.add_argument('--dimensions_min', dest='dimensions_min', type=str, help='Filter artworks to return all works that cannot fit inside a box defined by provided 3 values with the unit of measurement being meters. Place the most descriptive dimension in the first value, and any remaining dimensions in the second two values. If no value is provided for a dimension, a default value of 20cm is used. The dimensions_min filter has a fault tolerance of 0 on all dimensions, and will not return objects that can fit in the described box.')
artwork_cmd.add_argument('--credit', dest='credit', type=str, help='Filter by credit line.')
artwork_cmd.add_argument('--catalogue_raisonne', dest='catalogue_raisonne', type=str, help='Filter by catalogue raisonne.')
artwork_cmd.add_argument('--provenance', dest='provenance', type=str, help='Filter by provenance of artwork')
artwork_cmd.add_argument('--citations', dest='citations', type=str, help='Keyword search against the citations field.')
artwork_cmd.add_argument('--exhibition_history', dest='exhibition_history', type=str, help='Filter by exhibition history of artwork.')
artwork_cmd.add_argument('--created_before', dest='created_before', type=int, help='Returns artworks created before the year specified. Negative years are BCE.')
artwork_cmd.add_argument('--created_after', dest='created_after', type=int, help='Returns artworks created after the year specified. Negative years are BCE.')
artwork_cmd.add_argument('--created_after_age', dest='created_after_age', type=int, help='Filters by artworks that were created by artists older than the provided value in years at time of creation.')
artwork_cmd.add_argument('--created_before_age', dest='created_before_age', type=int, help='Filters by artworks that were created by artists younger than the provided value in years at time of creation.')
artwork_cmd.add_argument('--cc0', dest='cc0', action='store_true', help='Filters by works that have share license cc0.')
artwork_cmd.add_argument('--copyrighted', dest='copyrighted', action='store_true', help='Filters by works that have some sort of copyright.')
artwork_cmd.add_argument('--currently_on_view', dest='currently_on_view', action='store_true', help='Filters by works that are currently on view at CMA.')
artwork_cmd.add_argument('--currently_on_loan', dest='currently_on_loan', action='store_true', help='Filters by works that are currently on loan.')
artwork_cmd.add_argument('--african_american_artists', dest='african_american_artists', action='store_true', help='Filters by works created by African American artists.')
artwork_cmd.add_argument('--cia_alumni_artists', dest='cia_alumni_artists', action='store_true', help='Filters by works created by Cleveland Institute of Art alumni.')
artwork_cmd.add_argument('--may_show_artists', dest='may_show_artists', action='store_true', help='Filters by works exhibited in Cleveland Museum of Art May Shows')
artwork_cmd.add_argument('--female_artists', dest='female_artists', action='store_true', help='Filters by artworks created by female artists.')
artwork_cmd.add_argument('--recently_acquired', dest='recently_acquired', action='store_true', help='Filters by artworks acquired by the museum in the last three years.')
artwork_cmd.add_argument('--nazi_era_provenance', dest='nazi_era_provenance', action='store_true', help='Filters by nazi-era provenance.')

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

            if args.preview:
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
            output = cma.get_artworks(**args.__dict__)

            if args.preview:
                print('No. Results: ' + str(len(output)))

    elif args.command == 'curator':
        output = 'curator not yet implemented'

    elif args.command == 'exhibition':
        output = 'exhibition not yet implemented'

    else:
        raise Exception('Unknown subcommand.')
    
    if not args.preview:
        print(json.dumps(output, indent=4))
