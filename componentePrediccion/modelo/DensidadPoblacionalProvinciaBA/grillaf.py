from qgis.core import *
from PyQt4.QtGui import QApplication
from qgis.PyQt.QtCore import QVariant
from qgis.utils import iface

Horizontal_spacing= 10000
Vertical_spacing= 10000

app = QApplication([])
QgsApplication.setPrefixPath("/usr", True) # Adjust prefix path according to your installation (see note below)
QgsApplication.initQgis()

hspacing = Horizontal_spacing
vspacing = Vertical_spacing

# Load the layer
layer = QgsVectorLayer('/home/otto/Proyectos/inundappBackend/componentePrediccion/modelo/DensidadPoblacionalProvinciaBA/centroidesPoblacion.shp', 'teste_layer', 'ogr')

if not layer.isValid():
  print "Layer failed to load!"
 
# Add the layer to the map (comment the following line if the loading in the Layers Panel is not needed)
QgsMapLayerRegistry.instance().addMapLayer(layer)
 
# Get the Coordinate Reference System and the extent from the loaded layer
crs = layer.crs().toWkt()
ext=layer.extent()

# Set the extent of the new layer
xmin = ext.xMinimum()
xmax = ext.xMaximum()
ymin = ext.yMinimum()
ymax = ext.yMaximum()

# Create the grid layer
vector_grid = QgsVectorLayer('Polygon?crs='+ crs, 'vector_grid' , 'memory')
prov = vector_grid.dataProvider()
 
# Add ids and coordinates fields
fields = QgsFields()
fields.append(QgsField('ID', QVariant.Int, '', 10, 0))
fields.append(QgsField('XMIN', QVariant.Double, '', 24, 6))
fields.append(QgsField('XMAX', QVariant.Double, '', 24, 6))
fields.append(QgsField('YMIN', QVariant.Double, '', 24, 6))
fields.append(QgsField('YMAX', QVariant.Double, '', 24, 6))
prov.addAttributes(fields)

for feature in layer.getFeatures():
    print "sd"
    break

# Generate the features for the vector grid
id = 0
y = ymax
while y >= ymin:
    x = xmin
    while x <= xmax:
        point1 = QgsPoint(x, y)
        point2 = QgsPoint(x + hspacing, y)
        point3 = QgsPoint(x + hspacing, y - vspacing)
        point4 = QgsPoint(x, y - vspacing)
        vertices = [point1, point2, point3, point4] # Vertices of the polygon for the current id

        

        inAttr = [id, x, x + hspacing, y - vspacing, y]
        feat = QgsFeature()
        feat.setGeometry(QgsGeometry().fromPolygon([vertices])) # Set geometry for the current id
        feat.setAttributes(inAttr) # Set attributes for the current id
        prov.addFeatures([feat])
        x = x + hspacing
        id += 1
    y = y - vspacing
 
# Update fields for the vector grid
vector_grid.updateFields()
 
# Add the layer to the Layers panel
#QgsMapLayerRegistry.instance().addMapLayers([vector_grid])

vector_grid_data = vector_grid.dataProvider()

# Check mem layer
print " Mem Layer features:", vector_grid_data.featureCount()
print "fields:", len(vector_grid_data.fields())
e = vector_grid_data.extent()
print "extent:", e.xMinimum(), e.yMinimum(), e.xMaximum(), e.yMaximum()


vector_grid.commitChanges()

crs=QgsCoordinateReferenceSystem("epsg:4326")

# Save memory layer to file
error = QgsVectorFileWriter.writeAsVectorFormat(vector_grid, "outShapefile.shp", "UTF-8", crs , "ESRI Shapefile")

if error == QgsVectorFileWriter.NoError:
    print "success! writing new memory layer"

QgsApplication.exitQgis()
