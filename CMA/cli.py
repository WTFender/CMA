from CMA.api import Handler
import argparse
import json


verbose = argparse.ArgumentParser(add_help=False)
verbose.add_argument('--verbose', dest='verbose', action='store_true')
verbose.add_argument('--limit', dest='limit', type=int, default=100, help='Limit for number of JSON results. Default: 100')
verbose.add_argument('--indent', dest='indent', type=int, default=4, help='Number of spaces to indent JSON response. Default: 4')
parser = argparse.ArgumentParser(description='Cleveland Museum of Art API Wrapper.', parents=[verbose])

# Commands
command = parser.add_subparsers(dest='command')
command.required = True
cmd_artwork = command.add_parser('artwork', parents=[verbose])
cmd_creator = command.add_parser('creators', parents=[verbose])
cmd_exhibit = command.add_parser('exhibits', parents=[verbose])

# Subcommands
sub_artwork = cmd_artwork.add_subparsers(dest='subcommand')
sub_creator = cmd_creator.add_subparsers(dest='subcommand')
sub_exhibit = cmd_exhibit.add_subparsers(dest='subcommand')
for sub in [sub_artwork, sub_creator, sub_exhibit]:
    sub.required = True

# artwork get
sub_artwork_get = sub_artwork.add_parser('get', parents=[verbose])
sub_artwork_get.add_argument('--id', dest='resource', type=str, help='resource ID to retrieve', required=True)
sub_artwork_get.add_argument('--preview', dest='preview', action='store_true', help='generate preview')
sub_artwork_get.add_argument('--preview_cols', dest='preview_cols', type=int, help='generate preview')
sub_artwork_get.add_argument('--preview_scale', dest='preview_scale', type=float, help='generate preview')
sub_artwork_get.add_argument('--preview_levels', dest='preview_levels', action='store_true', help='generate preview')

# artwork list
sub_artwork_list = sub_artwork.add_parser('list', parents=[verbose])
sub_artwork_list.add_argument('--query', '-q', dest='q', type=str, help='Any keyword or phrase that searches against title, creator, artwork description, and several other meaningful fields related to the artwork.')
sub_artwork_list.add_argument('--department', dest='department', type=str, help='Filter by department. List of valid departments in Appendix B.')
sub_artwork_list.add_argument('--type', dest='type', type=str, help='Filter by artwork types. List of valid types in Appendix C.')
sub_artwork_list.add_argument('--has_image', dest='has_image', type=int, help='0 or 1. Filter to return only artworks that have a web image asset. (synonymous with the deprecated field web_image)')
sub_artwork_list.add_argument('--skip', dest='skip', type=int, help='Offset index for results.')
sub_artwork_list.add_argument('--artists', dest='artists', type=str, help='Filter by name of artist.')
sub_artwork_list.add_argument('--title', dest='title', type=str, help='Filter by title of artwork.')
sub_artwork_list.add_argument('--medium', dest='medium', type=str, help='Filter by artwork medium.')
sub_artwork_list.add_argument('--dimensions', dest='dimensions', type=str, help='Filter artworks by dimensions with the unit of measurement being meters. This filter is somewhat tricky, as the terminolgy for describing object dimensions varies from object to object (for example coins have diameters, swords have lengths, and necklaces have heights). An object\'s most descriptive dimension (whatever you think is the best way to describe it in meters) is generally put in the first part of the comma seperated list of dimensions. A default value of 20cm will be used if no value is provided for a dimension in the list. The second and third dimensions places are interchangable and describe a square that an object\'s remaining dimensions could fit inside. The dimensions filter returns objects with a fault tolerance of 20cm on all dimensions.')
sub_artwork_list.add_argument('--dimensions_max', dest='dimensions_max', type=str, help='Filter artworks to return all works that can fit inside a box defined by provided 3 values with the unit of measurement being meters. Place the most descriptive dimension in the first value, and any remaining dimensions in the second two values. If no value is provided for a dimension, a default value of 20cm is used. The dimensions_max filter has a fault tolerance of 0 on all dimensions, and will not return objects that cannot fit in the described box.')
sub_artwork_list.add_argument('--dimensions_min', dest='dimensions_min', type=str, help='Filter artworks to return all works that cannot fit inside a box defined by provided 3 values with the unit of measurement being meters. Place the most descriptive dimension in the first value, and any remaining dimensions in the second two values. If no value is provided for a dimension, a default value of 20cm is used. The dimensions_min filter has a fault tolerance of 0 on all dimensions, and will not return objects that can fit in the described box.')
sub_artwork_list.add_argument('--credit', dest='credit', type=str, help='Filter by credit line.')
sub_artwork_list.add_argument('--catalogue_raisonne', dest='catalogue_raisonne', type=str, help='Filter by catalogue raisonne.')
sub_artwork_list.add_argument('--provenance', dest='provenance', type=str, help='Filter by provenance of artwork')
sub_artwork_list.add_argument('--citations', dest='citations', type=str, help='Keyword search against the citations field.')
sub_artwork_list.add_argument('--exhibition_history', dest='exhibition_history', type=str, help='Filter by exhibition history of artwork.')
sub_artwork_list.add_argument('--created_before', dest='created_before', type=int, help='Returns artworks created before the year specified. Negative years are BCE.')
sub_artwork_list.add_argument('--created_after', dest='created_after', type=int, help='Returns artworks created after the year specified. Negative years are BCE.')
sub_artwork_list.add_argument('--created_after_age', dest='created_after_age', type=int, help='Filters by artworks that were created by artists older than the provided value in years at time of creation.')
sub_artwork_list.add_argument('--created_before_age', dest='created_before_age', type=int, help='Filters by artworks that were created by artists younger than the provided value in years at time of creation.')
sub_artwork_list.add_argument('--cc0', dest='cc0', action='store_true', help='Filters by works that have share license cc0.')
sub_artwork_list.add_argument('--copyrighted', dest='copyrighted', action='store_true', help='Filters by works that have some sort of copyright.')
sub_artwork_list.add_argument('--currently_on_view', dest='currently_on_view', action='store_true', help='Filters by works that are currently on view at CMA.')
sub_artwork_list.add_argument('--currently_on_loan', dest='currently_on_loan', action='store_true', help='Filters by works that are currently on loan.')
sub_artwork_list.add_argument('--african_american_artists', dest='african_american_artists', action='store_true', help='Filters by works created by African American artists.')
sub_artwork_list.add_argument('--cia_alumni_artists', dest='cia_alumni_artists', action='store_true', help='Filters by works created by Cleveland Institute of Art alumni.')
sub_artwork_list.add_argument('--may_show_artists', dest='may_show_artists', action='store_true', help='Filters by works exhibited in Cleveland Museum of Art May Shows')
sub_artwork_list.add_argument('--female_artists', dest='female_artists', action='store_true', help='Filters by artworks created by female artists.')
sub_artwork_list.add_argument('--recently_acquired', dest='recently_acquired', action='store_true', help='Filters by artworks acquired by the museum in the last three years.')
sub_artwork_list.add_argument('--nazi_era_provenance', dest='nazi_era_provenance', action='store_true', help='Filters by nazi-era provenance.')
sub_artwork_list.add_argument('--count', dest='count', action='store_true', help='Only display number of results.')

# creator get
sub_creator_get = sub_creator.add_parser('get', parents=[verbose])
sub_creator_get.add_argument('--id', dest='resource', type=str, help='resource ID to retrieve', required=True)

# creator list
sub_creator_list = sub_creator.add_parser('list', parents=[verbose])
sub_creator_list.add_argument('--name', dest='name', type=str, help='Filter by matches or partial matches to the name of any creator.')
sub_creator_list.add_argument('--biography', dest='biography', type=str, help='Filter by a keyword in creator biography.')
sub_creator_list.add_argument('--nationality', dest='nationality', type=str, help='Filter by a keyword in creator nationality, e.g. French.')
sub_creator_list.add_argument('--birth_year', dest='birth_year', type=int, help='Filter by exact match on creator\'s birth year.')
sub_creator_list.add_argument('--birth_year_after', dest='birth_year_after', type=int, help='Filter by creators born after a certain year.')
sub_creator_list.add_argument('--birth_year_before', dest='birth_year_before', type=int, help='Filter by creators born before a certain year.')
sub_creator_list.add_argument('--death_year', dest='death_year', type=int, help='Filter by exact match on creator\'s death year.')
sub_creator_list.add_argument('--death_year_after', dest='death_year_after', type=int, help='Filter by creators who have died after a certain year.')
sub_creator_list.add_argument('--death_year_before', dest='death_year_before', type=int, help='Filter by creators who have died before a certain year.')
sub_creator_list.add_argument('--skip', dest='skip', type=int, help='Offset index for results.')
sub_creator_list.add_argument('--count', dest='count', action='store_true', help='Only display number of results.')

# exhibition get
sub_exhibit_get = sub_exhibit.add_parser('get', parents=[verbose])
sub_exhibit_get.add_argument('--id', dest='resource', type=str, help='resource ID to retrieve', required=True)

# exhibition list
sub_exhibit_list = sub_exhibit.add_parser('list', parents=[verbose])
sub_exhibit_list.add_argument('--title', dest='title', type=str, help='Filter by matches or partial matches to the title of an exhibition.')
sub_exhibit_list.add_argument('--organizer', dest='organizer', type=str, help='Filter by exhibition organizer.')
sub_exhibit_list.add_argument('--opened_after', dest='opened_after', type=str, help='Filter exhibitions opened after a certain data. (date in YYYY-MM-DD format, e.g. 1974-01-01)')
sub_exhibit_list.add_argument('--opened_before', dest='opened_before', type=str, help='Filter exhibitions opened before a certain data. (date in YYYY-MM-DD format, e.g. 1974-01-01)')
sub_exhibit_list.add_argument('--closed_after', dest='closed_after', type=str, help='Filter exhibitions closed after a certain data. (date in YYYY-MM-DD format, e.g. 1974-01-01)')
sub_exhibit_list.add_argument('--closed_before', dest='closed_before', type=str, help='Filter exhibitions closed before a certain data. (date in YYYY-MM-DD format, e.g. 1974-01-01)')
sub_exhibit_list.add_argument('--venue', dest='venue', type=str, help='Filter by exhibitioned opened in certain venues.')
sub_exhibit_list.add_argument('--skip', dest='skip', type=int, help='Offset index for results.')
sub_exhibit_list.add_argument('--count', dest='count', action='store_true', help='Only display number of results.')


def preview_artwork(output):
    print('Title: ' + output['title'])
    print('Type: ' + output['type'])
    creators = ', '.join([c['description'] for c in output['creators']])
    print('Creator: ' + creators)
    print('Culture: ' + ', '.join(output['culture']))
    if 'preview' in output:
        print('Link: ' + output['images']['web']['url'])
        print('Preview: ')
        print(output['preview'])
    else:
        print('No image preview.')


def pprint(s, indent):
    print(json.dumps(s, indent=indent))


def main():
    cma = Handler()
    args = parser.parse_args()
    
    if args.verbose:
        print(args)

    if args.command == 'artwork':

        if args.subcommand == 'get':
            output = cma.get_artwork(rid=args.resource, **args.__dict__)

            if args.preview:
                preview_artwork(output)
            else:
                pprint(output, indent=args.indent)

        elif args.subcommand == 'list':
            output = cma.list_artworks(**args.__dict__)

            if args.count:
                print(str(len(output)))
            else:
                pprint(output, indent=args.indent)

    elif args.command == 'creators':

        if args.subcommand == 'get':
            output = cma.get_creator(rid=args.resource)
            pprint(output, indent=args.indent)

        elif args.subcommand == 'list':
            output = cma.list_creators(**args.__dict__)

            if args.count:
                print(str(len(output)))
            else:
                pprint(output, indent=args.indent)

    elif args.command == 'exhibits':

        if args.subcommand == 'get':
            output = cma.get_exhibition(rid=args.resource)
            pprint(output, indent=args.indent)

        elif args.subcommand == 'list':
            output = cma.list_exhibitions(**args.__dict__)

            if args.count:
                print(str(len(output)))
            else:
                pprint(output, indent=args.indent)
