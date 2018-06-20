from qgis.core import *
from PyQt4.QtGui import QApplication

app = QApplication([])
QgsApplication.setPrefixPath("/usr", True) # Adjust prefix path according to your installation (see note below)
QgsApplication.initQgis()
 
# Set the spacing
spacing = 1999
# Set the inset
inset = 50

# Load the layer
layer = QgsVectorLayer('/home/otto/Proyectos/inundappBackend/componentePrediccion/modelo/DensidadPoblacionalProvinciaBA/Buenos_Aires_con_datos.shp', 'teste_layer', 'ogr')

if not layer.isValid():
  print "Layer failed to load!"
 
# Add the layer to the map (comment the following line if the loading in the Layers Panel is not needed)
QgsMapLayerRegistry.instance().addMapLayer(layer)
 
# Get the Coordinate Reference System and the extent from the loaded layer
crs = layer.crs().toWkt()
ext=layer.extent()
 
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
#QgsMapLayerRegistry.instance().addMapLayer(points_layer)

points_layer_data = points_layer.dataProvider()


# Check mem layer
print " Mem Layer features:", points_layer_data.featureCount()
print "fields:", len(points_layer_data.fields())
e = points_layer_data.extent()
print "extent:", e.xMinimum(), e.yMinimum(), e.xMaximum(), e.yMaximum()


points_layer.commitChanges()

crs=QgsCoordinateReferenceSystem("epsg:4326")

# Save memory layer to file
error = QgsVectorFileWriter.writeAsVectorFormat(points_layer, "outShapefile.shp", "UTF-8", crs , "ESRI Shapefile")

if error == QgsVectorFileWriter.NoError:
    print "success! writing new memory layer"

QgsApplication.exitQgis()
