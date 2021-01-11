from CMA.api import Handler

artwork_id = 1953.424

cma = Handler()

artwork = cma.get_artwork(rid=artwork_id, preview=True)

print(artwork)