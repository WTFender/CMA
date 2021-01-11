import requests

class Handler:

    def __init__(self, baseurl='https://openaccess-api.clevelandart.org/api', key=''):
        self.baseurl = baseurl
        self.key = key # unimplemented

    def _api(self, method, path, payload):
        if payload:
            resp = requests.request(method, self.baseurl+path, json=payload)
        else:
            resp = requests.request(method, self.baseurl+path)
        if resp.status_code != 200:
            raise Exception(resp.content)
        else:
            return resp.json()['data']

    def get_artworks(self):
        return self._api('GET', '/artworks', None)

    def get_artwork(self, rid, preview=False):
        rid = str(rid)
        if '.' in rid:
            rid = float(rid)
        else:
            rid = int(rid)
        resp = self._api('GET', '/artworks/' + str(rid), None)
        if preview:
            resp['preview'] = self._get_artwork_preview(resp)
        return resp

    def _get_artwork_preview(self, artwork, cols=80, scale=.43, moreLevels=False):
        from .utils import covertImageToAscii
        try:
            img = requests.get(artwork['images']['web']['url'])
        except KeyError:
            return None
        if img.status_code != 200:
            raise Exception(img.content)
        return covertImageToAscii(img, cols, scale, moreLevels)
        
    def get_curators(self):
        pass

    def get_exhibitions(self):
        pass

