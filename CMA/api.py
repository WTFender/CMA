from .utils import covertImageToAscii
import requests
import urllib


# https://openaccess-api.clevelandart.org/


class Handler:

    def __init__(self, baseurl='https://openaccess-api.clevelandart.org/api'):
        self.baseurl = baseurl

    def _api(self, method, path, params):
        if params:
            resp = requests.request(method, self.baseurl+path, params=params)
        else:
            resp = requests.request(method, self.baseurl+path)
        if resp.status_code != 200:
            raise Exception(resp.content)
        else:
            return resp.json()['data']

    def list_artworks(self, **kwargs):
        '''
        q	string	Any keyword or phrase that searches against title, creator, artwork description, and several other meaningful fields related to the artwork.
        department	string	Filter by department. List of valid departments in Appendix B.
        type	string	Filter by artwork types. List of valid types in Appendix C.
        has_image	integer	0 or 1. Filter to return only artworks that have a web image asset. (synonymous with the deprecated field web_image)
        indent	integer	Number of spaces to indent JSON content if "pretty" formatting is desired.
        skip	integer	Offset index for results.
        limit	integer	Limit for number of results. If no limit provided, API will return the maximum (1000) number of records.
        artists	string	Filter by name of artist.
        title	string	Filter by title of artwork.
        medium	string	Filter by artwork medium.
        dimensions	float,float,float	Filter artworks by dimensions with the unit of measurement being meters. This filter is somewhat tricky, as the terminolgy for describing object dimensions varies from object to object (for example coins have diameters, swords have lengths, and necklaces have heights). An object's most descriptive dimension (whatever you think is the best way to describe it in meters) is generally put in the first part of the comma seperated list of dimensions. A default value of 20cm will be used if no value is provided for a dimension in the list. The second and third dimensions places are interchangable and describe a square that an object's remaining dimensions could fit inside. The dimensions filter returns objects with a fault tolerance of 20cm on all dimensions.
        dimensions_max	float,float,float	Filter artworks to return all works that can fit inside a box defined by provided 3 values with the unit of measurement being meters. Place the most descriptive dimension in the first value, and any remaining dimensions in the second two values. If no value is provided for a dimension, a default value of 20cm is used. The dimensions_max filter has a fault tolerance of 0 on all dimensions, and will not return objects that cannot fit in the described box.
        dimensions_min	float,float,float	Filter artworks to return all works that cannot fit inside a box defined by provided 3 values with the unit of measurement being meters. Place the most descriptive dimension in the first value, and any remaining dimensions in the second two values. If no value is provided for a dimension, a default value of 20cm is used. The dimensions_min filter has a fault tolerance of 0 on all dimensions, and will not return objects that can fit in the described box.
        credit	string	Filter by credit line.
        catalogue_raisonne	string	Filter by catalogue raisonne.
        provenance	string	Filter by provenance of artwork
        citations	string	Keyword search against the citations field.
        exhibition_history	string	Filter by exhibition history of artwork.
        created_before	integer	Returns artworks created before the year specified. Negative years are BCE.
        created_after	integer	Returns artworks created after the year specified. Negative years are BCE.
        created_after_age	integer	Filters by artworks that were created by artists older than the provided value in years at time of creation.
        created_before_age	integer	Filters by artworks that were created by artists younger than the provided value in years at time of creation.      
        cc0	none	Filters by works that have share license cc0.
        copyrighted	none	Filters by works that have some sort of copyright.
        currently_on_view	none	Filters by works that are currently on view at CMA.
        currently_on_loan	none	Filters by works that are currently on loan.
        african_american_artists	none	Filters by works created by African American artists.
        cia_alumni_artists	none	Filters by works created by Cleveland Institute of Art alumni.
        may_show_artists	none	Filters by works exhibited in Cleveland Museum of Art May Shows
        female_artists	none	Filters by artworks created by female artists.
        recently_acquired	none	Filters by artworks acquired by the museum in the last three years.
        nazi_era_provenance	none	Filters by nazi-era provenance.
        '''
        params = {}
        if kwargs['q']:
            params['q'] = str(kwargs['q'])
        if kwargs['department']:
            params['department'] = str(kwargs['department'])
        if kwargs['type']:
            params['type'] = str(kwargs['type'])
        if kwargs['has_image']:
            params['has_image'] = int(kwargs['has_image'])
        if kwargs['indent']:
            params['indent'] = int(kwargs['indent'])
        if kwargs['skip']:
            params['skip'] = int(kwargs['skip'])
        if kwargs['limit']:
            params['limit'] = int(kwargs['limit'])
        if kwargs['artists']:
            params['artists'] = str(kwargs['artists'])
        if kwargs['title']:
            params['title'] = str(kwargs['title'])
        if kwargs['medium']:
            params['medium'] = str(kwargs['medium'])
        if kwargs['dimensions']:
            params['dimensions'] = str(kwargs['dimensions'])
        if kwargs['dimensions_max']:
            params['dimensions_max'] = str(kwargs['dimensions_max'])
        if kwargs['dimensions_min']:
            params['dimensions_min'] = str(kwargs['dimensions_min'])
        if kwargs['credit']:
            params['credit'] = str(kwargs['credit'])
        if kwargs['catalogue_raisonne']:
            params['catalogue_raisonne'] = str(kwargs['catalogue_raisonne'])
        if kwargs['provenance']:
            params['provenance'] = str(kwargs['provenance'])
        if kwargs['citations']:
            params['citations'] = str(kwargs['citations'])
        if kwargs['exhibition_history']:
            params['exhibition_history'] = str(kwargs['exhibition_history'])
        if kwargs['created_before']:
            params['created_before'] = int(kwargs['created_before'])
        if kwargs['created_after']:
            params['created_after'] = int(kwargs['created_after'])
        if kwargs['created_after_age']:
            params['created_after_age'] = int(kwargs['created_after_age'])
        if kwargs['created_before_age']:
            params['created_before_age'] = int(kwargs['created_before_age'])

        path = ''
        for k in ['cc0','copyrighted','currently_on_view','currently_on_loan',
                'african_american_artists','cia_alumni_artists','may_show_artists',
                'female_artists','recently_acquired','nazi_era_provenance']:
            if k in kwargs:
                if kwargs[k]:
                    path += k + '&'

        path = path[:-1] # remove trailing &

        return self._api('GET', '/artworks/?' + path, params)

    def get_artwork(self, rid, preview=False, **kwargs):
        if '.' in str(rid):
            rid = float(rid)
        else:
            rid = int(rid)
        resp = self._api('GET', '/artworks/' + str(rid), None)
        if preview:
            resp['preview'] = self._gen_artwork_preview(resp, **kwargs)
        return resp

    def _gen_artwork_preview(self, artwork, cols=80, scale=.43, moreLevels=False, **kwargs):
        if kwargs['preview_cols']:
            cols = int(kwargs['preview_cols'])
        if kwargs['preview_scale']:
            scale = float(kwargs['preview_scale'])
        if kwargs['preview_levels']:
            moreLevels = bool(kwargs['preview_levels'])
        try:
            img = requests.get(artwork['images']['web']['url'])
        except KeyError:
            return None
        if img.status_code != 200:
            raise Exception(img.content)
        return covertImageToAscii(img, cols, scale, moreLevels)

    def list_creators(self, **kwargs):
        '''
        name	string	Filter by matches or partial matches to the name of any creator.
        biography	string	Filter by a keyword in creator biography.
        nationality	string	Filter by a keyword in creator nationality, e.g. 'French'.
        birth_year	integer	Filter by exact match on creator's birth year.
        birth_year_after	integer	Filter by creators born after a certain year.
        birth_year_before	integer	Filter by creators born before a certain year.
        death_year	integer	Filter by exact match on creator's death year.
        death_year_after	integer	Filter by creators who have died after a certain year.
        death_year_before	integer	Filter by creators who have died before a certain year.
        indent	integer	Number of spaces to indent JSON content if "pretty" formatting is desired.
        skip	integer	Offset index for results.
        limit	integer	Limit for number of results. If no limit provided, API will return the maximum (100) number of records.
        '''
        params = {}
        if kwargs['name']:
            params['name'] = str(kwargs['name'])
        if kwargs['biography']:
            params['biography'] = str(kwargs['biography'])
        if kwargs['nationality']:
            params['nationality'] = str(kwargs['nationality'])
        if kwargs['birth_year']:
            params['birth_year'] = int(kwargs['birth_year'])
        if kwargs['birth_year_after']:
            params['birth_year_after'] = int(kwargs['birth_year_after'])
        if kwargs['birth_year_before']:
            params['birth_year_before'] = int(kwargs['birth_year_before'])
        if kwargs['death_year']:
            params['death_year'] = int(kwargs['death_year'])
        if kwargs['death_year_after']:
            params['death_year_after'] = int(kwargs['death_year_after'])
        if kwargs['death_year_before']:
            params['death_year_before'] = int(kwargs['death_year_before'])
        if kwargs['indent']:
            params['indent'] = int(kwargs['indent'])
        if kwargs['skip']:
            params['skip'] = int(kwargs['skip'])
        if kwargs['limit']:
            params['limit'] = int(kwargs['limit'])
        return self._api('GET', '/creators/?', params=params)

    def get_creator(self, rid):
        rid = int(rid)
        return self._api('GET', '/creators/' + str(rid), None)

    def list_exhibitions(self, **kwargs):
        '''
        title	string	Filter by matches or partial matches to the title of an exhibition.
        organizer	string	Filter by exhibition organizer.
        opened_after	date	Filter exhibitions opened after a certain data. (date in YYYY-MM-DD format, e.g. 1974-01-01)
        opened_before	date	Filter exhibitions opened before a certain data. (date in YYYY-MM-DD format, e.g. 1974-01-01)
        closed_after	date	Filter exhibitions closed after a certain data. (date in YYYY-MM-DD format, e.g. 1974-01-01)
        closed_before	date	Filter exhibitions closed before a certain data. (date in YYYY-MM-DD format, e.g. 1974-01-01)
        venue	string	Filter by exhibitioned opened in certain venues.
        indent	integer	Number of spaces to indent JSON content if "pretty" formatting is desired.
        skip	integer	Offset index for results.
        limit	integer	Limit for number of results. If no limit provided, API will return the maximum (100) number of records.
        '''
        class d(str): # yyyy-mm-dd date string
            def __new__(cls, s):
                if re.match(r"\d{4}\-\d{2}\-\d{2}", s):
                    return str.__new__(cls, s)
                else:
                    raise Exception('yyyy-mm-dd required, %s' % s)
        params = {}
        if kwargs['title']:
            params['title'] = str(kwargs['title'])
        if kwargs['organizer']:
            params['organizer'] = str(kwargs['organizer'])
        if kwargs['opened_after']:
            params['opened_after'] = d(kwargs['opened_after'])
        if kwargs['opened_before']:
            params['opened_before'] = d(kwargs['opened_before'])
        if kwargs['closed_after']:
            params['closed_after'] = d(kwargs['closed_after'])
        if kwargs['closed_before']:
            params['closed_before'] = d(kwargs['closed_before'])
        if kwargs['venue']:
            params['venue'] = str(kwargs['venue'])
        if kwargs['indent']:
            params['indent'] = int(kwargs['indent'])
        if kwargs['skip']:
            params['skip'] = int(kwargs['skip'])
        if kwargs['limit']:
            params['limit'] = int(kwargs['limit'])
        return self._api('GET', '/exhibitions/?', params=params)

    def get_exhibition(self, rid):
        rid = int(rid)
        return self._api('GET', '/exhibitions/' + str(rid), None)
