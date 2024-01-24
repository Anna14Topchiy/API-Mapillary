import requests
import json
import os
from vt2geojson.tools import vt_bytes_to_geojson

import math
def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
  return (xtile, ytile)

MAP_ACCESS_TOKEN = "MLY|5792454307476942|a048d65f7031d0bde6ce1ded4d33a4a4" ##Change this
outputfolder = "D:\kasko\source_preparation_for_each_country\Poland"  ##Change this

#set zoom levels and corner coordinates

z = 14
ll_lat = 49.99
ll_lon = 14.07
ur_lat = 54.27
ur_lon = 16.07
llx,lly = deg2num (ll_lat, ll_lon, z)
urx,ury = deg2num (ur_lat, ur_lon, z)
#uncomment the one layer you wish to use

#type="mly1_computed_public"
type="mly_map_feature_point"
#type="mly_map_feature_traffic_sign"
#type="mly1_computed_public"
#type="mly1_public"

#types = ["mly1_computed_public","mly_map_feature_point","mly_map_feature_traffic_sign","mly1_computed_public","mly1_public"]
types = ["mly_map_feature_point"]
for type in types:
    output = {"type":"FeatureCollection","features":[]}
    for x in range(min(llx,urx),max(llx,urx),1):
        for y in range(min(lly,ury),max(lly,ury),1):
            print (type,x,y)
            url = f"https://tiles.mapillary.com/maps/vtp/{type}/2/{z}/{x}/{y}?access_token={MAP_ACCESS_TOKEN}"
            r = requests.get(url)
            assert r.status_code == 200, r.content
            vt_content = r.content
            features = vt_bytes_to_geojson(vt_content, x, y, z)
            for f in features["features"]:
                try:
                    if f['properties']['value'] == 'object--traffic-light--cyclists' or f['properties']['value'] == 'object--traffic-light--general-horizontal' or f['properties']['value'] == 'object--traffic-light--general-single' or f['properties']['value'] == 'object--traffic-light--general-upright' or f['properties']['value'] == 'object--traffic-light--other' or f['properties']['value'] == 'object--traffic-light--pedestrians':
                        output['features'].append(f)
                except:
                    pass

    with open(outputfolder + os.path.sep + type + "_" + str(z) + "_" + str(llx) + "_" + str(urx) + "_" + str(lly) + "_" + str(ury) + ".geojson", "w") as ftl_map_p1:
        json.dump(output, ftl_map_p1)
