import  ellipsis as el
import json
import math
import pandas as pd
import  numpy as np

def parseAsSparkDataFrame(r, sparkSession):
    sh = r['result']
    pageStart = r['nextPageStart']

    bounds = sh.bounds
    sh['x1'] = bounds['minx']
    sh['y1'] = bounds['miny']
    sh['x2'] = bounds['maxx']
    sh['y2'] = bounds['maxy']
    features_json = sh.to_json(na='drop')

    sh['geometry'] = [f['geometry'] for f in json.loads(features_json)['features']]


    df_ps = sparkSession.createDataFrame(sh)
    return df_ps, pageStart


def readVector(sparkSession, pathId, timestampId, token=None):
    r = el.path.vector.timestamp.listFeatures(pathId=pathId, timestampId=timestampId, listAll=False, token = token, pageStart=None)
    df_ps, pageStart = parseAsSparkDataFrame(r, sparkSession)

    while type(pageStart) != type(None):
        r = el.path.vector.timestamp.listFeatures(pathId=pathId, timestampId=timestampId, listAll=False, token=token, pageStart=pageStart)
        df_ps_new, pageStart = parseAsSparkDataFrame(r, sparkSession)
        df_ps.unionByName(df_ps_new, allowMissingColumns=True)
    return df_ps


def readRaster(sparkSession, pathId, timestampId, token=None, extent = None):
    info = el.path.get(pathId=pathId, token=token)
    bands = info['raster']['bands']

    t = [t for t in info['raster']['timestamps'] if t['id'] == timestampId]
    if len(t) == 0:
        raise ValueError('timestampId not found in the given layer')
    resolution = t[0]['resolution']
    if type(extent) ==type(None):
        extent = t[0]['extent']


    xMin, yMin = el.util.transformPoint( (extent['xMin'], extent['yMin']), 4326, 3857 )
    xMax, yMax = el.util.transformPoint( (extent['xMax'], extent['yMax']), 4326, 3857 )


    dx = 4000
    dy = 4000

    steps_x = math.ceil((xMax - xMin)/(resolution * dx))
    steps_y = math.ceil((yMax - yMin)/(resolution * dy))

    Dx = (xMax - xMin )/steps_x
    Dy = (xMax - xMin )/steps_y

    df = None

    for x in range(steps_x):
        for y in range(steps_y):
            x1 = xMin + x *Dx
            x2 = xMin + (x+1) *Dx
            y1 = yMin + x *Dy
            y2 =yMin + (x+1) *Dy
            temp_extent = {'xMin':x1, 'yMin':y1, 'xMax': x2, 'yMax':y2}
            r = el.path.raster.timestamp.getRaster(pathId=pathId, timestampId=timestampId, extent=temp_extent, token = token, epsg = 3857)['raster']

            Nx = r.shape[1]
            d = (x2 - x1) / (Nx - 1)
            xSteps = [x1 + d * i for i in range(Nx)]
            Ny = r.shape[2]
            d = (y2 - y1) / (Ny - 1)
            ySteps = [y1 + d * i for i in range(Ny)]
            xCoords, yCoords = np.meshgrid(xSteps, ySteps, indexing='ij')
            xCoords = np.expand_dims(xCoords, axis=0)
            yCoords = np.expand_dims(yCoords, axis=0)
            r = np.concatenate([r, xCoords, yCoords], axis=0)
            df_new = pd.DataFrame()
            df_new['x'] = r[-2,].flatten()
            df_new['y'] = r[-1,].flatten()

            for i in range(len(bands)):
                df_new[bands[i]['name'] ] = r[i,  ].flatten()
            del r
            if type(df) == type(None):
                df = sparkSession.createDataFrame(df_new)
            else:
                df_new = sparkSession.createDataFrame(df_new)
                df.unionByName(df_new, allowMissingColumns=True)
                del df_new
    return df
