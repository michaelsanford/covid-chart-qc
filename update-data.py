#!/usr/bin/env python3

import urllib.request, json

QC = "https://kustom.radio-canada.ca/coronavirus/canada_quebec"

REGIONS = [
    None,
    'montreal',
    'monteregie',
    'laval',
    'laurentides',
    'lanaudiere',
    'outaouais',
    'capitale-nationale',
    
    'nunavik',
    'nord-du-quebec',
    'abitibi-temiscamingue',
    'estrie',
    'mauricie-centre-du-quebec',
    'chaudiere-appalaches',
    'bas-saint-laurent',
    'gaspesie-iles-de-la-madeleine',
    'cote-nord',
    'saguenay-lac-saint-jean'
]

for r in REGIONS:
    name = r if r is not None else "quebec"
    try:
        print("Fetching %s . . . " % name, end='')
        urllib.request.urlretrieve(
            url="%s_%s" % (QC, r) if r is not None else QC,
            filename="data/%s.json" % name
        )
        print("done!")
    except Exception as e:
        print("[ERROR] Raised %s fetching %s !" % e, name)