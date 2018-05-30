from qgis.core import *
from qgis.utils import iface
import processing

QgsApplication.showSettings() 

# Set the spacing
spacing = 10
# Set the inset
inset = 5
#layer = QgsVectorLayer('//home//otto/Proyectos//inundappBackend//componentePrediccion//modelo//DensidadPoblacionalProvinciaBA//Buenos_Aires_con_datos.shp', 'Densidad Poblacional', 'ogr')

#QgsMapLayerRegistry.instance().addMapLayer(layer)
#layer = iface.activeLayer()

#layer = processing.getObject('/home/otto/Proyectos/inundappBackend/componentePrediccion/modelo/DensidadPoblacionalProvinciaBA/Buenos_Aires_con_datos.shp')

layer = iface.addVectorLayer("Buenos_Aires_con_datos.shp", "layer name you like", "ogr")
if not layer:
	print "Layer failed to load!"
# Get the Coordinate Reference System and the extent from the loaded layer
crs = layer.crs().toWkt()
ext= layer.extent()
 
# Create a new vector point layer
points_layer = QgsVectorLayer('Point?crs=' + crs, 'grid', "memory")
prov = points_layer.dataProvider()
 
# Set the extent of the new layer
xmin = ext.xMinimum() + inset
xmax = ext.xMaximum()
ymin = ext.yMinimum()
ymax = ext.yMaximum() - inset
 
# Create the coordinates of the points in the grid
points = []
y = ymax
while y >= ymin:
    x = xmin
    while x <= xmax:
        geom = QgsGeometry().fromPoint(QgsPoint(x, y))
        feat = QgsFeature()
        point = QgsPoint(x,y)
        feat.setGeometry(QgsGeometry.fromPoint(point))
        points.append(feat)
        x += spacing
    y = y - spacing
 
prov.addFeatures(points)
points_layer.updateExtents()
 
# Add the layer to the map
QgsMapLayerRegistry.instance().addMapLayer(points_layer)