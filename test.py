import ezdxf
from ezdxf.addons import geo
from shapely.geometry import *

# DEFINE WHICH INFORMATIONS YOU WANT FROM YOUR DXF ELEMENTS
# this would later be the columns of the GeoPanda you can create using the dictonaries
dic_col = {'dxf_type': "typ", 'layer': "layer", 
                                'linetype': "linetype", 'color': "color",'geometry': "geometry"}
 
def get_coordinates_vertices(e):
    """Obtain the coordinates from a a tuple of Vec3s.

    Args:
        e : dxf_entitiy of type HATCH

    Returns:
        shapely.geometry: Coordinates in the original goemetry type
    """
    dic = list(geo.proxy(e))[0]
    type_ = dic['type']
    coord = dic['coordinates']
    # print(type_, coord)
    # print(type(coord))
    if isinstance(coord[0][0],ezdxf.acc.vector.Vec3):
        # most DXF I have worked with do not hold height information,
        # if yours does please skip this part
        coord = [np.delete(x, 2, axis = 0) for x in coord[0]]
    if type_ == "Polygon":
        geom_ = Polygon(coord)
    elif type_ == "LineString":
        geom_ = LineString(coord)
    else:
        raise ValueError("Unkown Type: " + str(type_))
    del type_,coord
    return geom_
                                
def read_hatch(dxf_entety,dic_col):
    col = dic_col.keys()
    geo = get_coordinates_vertices(dxf_entety)
    val = [dxf_entety.dxftype(), dxf_entety.dxf.layer, dxf_entety.dxf.linetype, dxf_entety.dxf.color, geo]
    return dict(zip(col, val))
    
 # TEST
doc = ezdxf.new("R2000")
msp = doc.modelspace()
hatch = msp.add_hatch(
     color=1,
     dxfattribs={
         "hatch_style": ezdxf.const.HATCH_STYLE_NESTED,
         # 0 = nested: ezdxf.const.HATCH_STYLE_NESTED
         # 1 = outer: ezdxf.const.HATCH_STYLE_OUTERMOST
         # 2 = ignore: ezdxf.const.HATCH_STYLE_IGNORE
     },
 )
hatch.paths.add_polyline_path(
     [(0, 0), (10, 0), (10, 10), (0, 10)],
     is_closed=True,
     flags=ezdxf.const.BOUNDARY_PATH_EXTERNAL,
 )
hatch_ = msp.query('HATCH')[0] 
hatch_info = read_hatch(hatch_, dic_col)