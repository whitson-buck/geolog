"""Main module."""

import string
import random
import ipyleaflet
from ipyleaflet import GeoData, LayersControl, GeoJSON
import folium

import geopandas
from geopandas import GeoDataFrame, GeoSeries

class Map(ipyleaflet.Map):
    def __init__(self, center=[35,-90], zoom=5, **kwargs) -> None:

        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True

        super().__init__(center=center, zoom=zoom, **kwargs)

        if "layers_control" not in kwargs:
            kwargs["layers_control"]=True

        if kwargs["layers_control"]:
            self.add_layers_control()

        if "fullscreen_control" not in kwargs:
            kwargs["fullscreen_control"]=True  

        if kwargs["fullscreen_control"]:
            self.add_fullscreen_control()  
        
        if "add_search_control" not in kwargs:
            kwargs["add_search_control"]=True

        if kwargs["add_search_control"]:
            self.add_search_control()

    def add_layers_control(self,**kwargs):
        """Layers control functionality
        
        """
        layers_control = ipyleaflet.LayersControl(**kwargs)
        self.add_control(layers_control)
    
    def add_fullscreen_control(self,position="topleft"):
        """Adds fullscreen control capability to the map.
        
        Args: 
            position - where you want controls located.
        """
        fullscreen_control = ipyleaflet.FullScreenControl(position=position)
        self.add_control(fullscreen_control)
    
    def add_search_control(self,position="bottomleft",**kwargs):
        """Adds search control to the map.
        
        Args: 
            position - Where you would like the search control box to be
            located. Eg: topleft, bottomright.
            Kwargs - Keyword arguments to pass to search control
        """
        if "url" not in kwargs:
            kwargs["url"] = 'https://nominatim.openstreetmap.org/search?format=json&q={s}'
        search_control = ipyleaflet.SearchControl(position=position,**kwargs)
        self.add_control(search_control)

    def add_draw_control(self,**kwargs):
        """Adds drawing control to the map, like lines and polygons.
        
        Args: 
            Kwargs - Keyword arguments to pass to search control
        """
    
        draw_control = ipyleaflet.DrawControl(**kwargs)
        draw_control.polyline =  {
            "shapeOptions": {
                "color": "#6bc2e5",
                "weight": 8,
                "opacity": 1.0
            }
        }
        draw_control.polygon = {
            "shapeOptions": {
                "fillColor": "#6be5c3",
                "color": "#6be5c3",
                "fillOpacity": 1.0
            },
            "drawError": {
                "color": "#dd253b",
                "message": "Oups!"
            },
            "allowIntersection": False
        }
        draw_control.circle = {
            "shapeOptions": {
                "fillColor": "#efed69",
                "color": "#efed69",
                "fillOpacity": 1.0
            }
        }
        draw_control.rectangle = {
            "shapeOptions": {
                "fillColor": "#fca45d",
                "color": "#fca45d",
                "fillOpacity": 1.0
            }
        }

        self.add_control(draw_control)

    def add_tile_layer(self, url, name, attribution="",**kwargs):
        """
        Adds tile layer to the map.

        Args:
            url - URL of tile layer
            name - name of the tile layer
            attribution - optional, adds attribution to map
        """
        tile_layer = ipyleaflet.TileLayer(
            url=url,
            name=name,
            attribution=attribution,
            **kwargs
        )
        self.add_layer(tile_layer)

    def add_basemap(self, basemap, **kwargs):
        """
        More user-friendly way to specify basemap.

        Args:
            basemap (must be string)- basemap of user choice.
        """
        import xyzservices.providers as xyz

        if basemap.lower()=="roadmap":
            url = 'https://mt1.google.com/vt/lyrs=h&x={x}&y={y}&z={z}'
            self.add_tile_layer(url,name=basemap,**kwargs)
        elif basemap.lower()=="satellite":
            url = 'https://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}'
            self.add_tile_layer(url,name=basemap,**kwargs)
        else:
            try:
                basemap=eval(f"xyz.{basemap}")
                url = basemap.build_url()
                attribution = basemap.attribution
                self.add_tile_layer(url,name=basemap.name,attribution=attribution, **kwargs)
            except:
                raise ValueError(f"Basemap '{basemap}' not found.")
            
    def add_shp(self, data, name='Shapefile', **kwargs):
        """Adds a Shapefile layer to the map.
        Args:
            data (must be string): The path to the Shapefile.
        """
        import geopandas as gpd
        gdf = gpd.read_file(data)
        geojson = gdf.__geo_interface__
        self.add_geojson(geojson, name=name, **kwargs)


    def add_geojson(self, data, **kwargs):
        """Adds a GeoJSON layer to the map.
        Args:
            data (must be dict): The GeoJSON data.
            kwargs: Keyword arguments to pass to the GeoJSON layer.
        """
        import json

        if isinstance(data, str):
            with open(data, "r") as f:
                data = json.load(f)

        geojson = ipyleaflet.GeoJSON(data=data, **kwargs)
        self.add_layer(geojson)

    def add_vector(self,data,**kwargs):
        """Accepts shp file, checks if GeoPandas.
        
        Args:
            data: geopandas shapefile
        """

        try:
            self.add_shp(data)
        except:

            try:
                self.add_layer(GeoData(data,name="Vector Data"))
                self.add_layer(GeoSeries(data,name="Vector Data"))
                self.add_layer(GeoDataFrame(data,name="Vector Data"))
            except:
                return "Not supported filetype"
            
    def add_raster(self, url, name="raster",fit_bounds = True, **kwargs):
        """Adds raster to Geolog map
        
        Args:
            url: user-selected url to add raster
            name: Optional argument for raster name
            fit_bound: optional argument for whether bound of map should be fit"""
        
        import httpx
        titiler_endpoint = "https://titiler.xyz"

        r1 = httpx.get(f"{titiler_endpoint}/cog/info",params = {'url': url,}).json()
        bounds = r1["bounds"]

        r1 = httpx.get(f"{titiler_endpoint}/cog/tilejson.json",params = {'url': url,}).json()
        tile = r1["tiles"][0]

        bbox = [[bounds[1],bounds[0]],[bounds[3],bounds[2]]]
        self.fit_bounds(bbox)
        self.add_tile_layer(url=tile, name=name, **kwargs)

    def add_image(self, url, **kwargs):
        """Adds image to Geolog map
        
        Args:
            url: user-selected url to add image
        """
        import ipywidgets
        from ipyleaflet import WidgetControl
        from IPython import display
        
        logo = ipywidgets.HTML(
            value='<img src="http://www.freshmap.co.nz/images/enlarge2.jpg" width="200" height="200">'
        )
        output_widget = ipywidgets.Output(layout={'border': '1px solid black'})
        output_widget.clear_output()
        output_control = WidgetControl(widget=output_widget, position='bottomright')
        self.add_control(output_control)
        with output_widget:
            display(logo)
