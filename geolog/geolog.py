"""Main module."""

# import string
# import random
import ipyleaflet
from ipyleaflet import Map, basemaps, TileLayer, LayersControl, WMSLayer, ImageOverlay, basemap_to_tiles, MarkerCluster, Marker
# import folium
import ipywidgets as widgets
from ipywidgets import Button
from ipywidgets import ToggleButtons
import pandas as pd
from shapely.geometry import Point, shape
import geopandas as gpd
from IPython import display
# from geopandas import GeoDataFrame, GeoSeries

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
            kwargs["fullscreen_control"] = True

        if kwargs["fullscreen_control"]:
            self.add_fullscreen_control()
        
        if "add_search_control" not in kwargs:
            kwargs["add_search_control"]=True

        if kwargs["add_search_control"]:
            self.add_search_control()

        # self.toolbar = widgets.VBox()
        # self.load_button = widgets.Button(description='Load CSV')
        # self.load_button.on_click(self._on_load_button_clicked)
        # self.toolbar.children = [self.load_button]
        # self.add_control(ipyleaflet.WidgetControl(widget=self.toolbar, position='topright'))

        # self.marker_cluster = ipyleaflet.MarkerCluster()
        # self.add_layer(self.marker_cluster)
        # self.marker_layer = ipyleaflet.LayerGroup()
        # self.add_layer(self.marker_layer)
        # self.markers = []
        # self.marker_popup = widgets.HTML()
        
        # # Add a mouse click event listener to the map
        # # self.on_interaction(self.handle_interaction)
        
        # # Add a Save Markers button
        # self.save_markers_button = widgets.Button(description='Save Markers')
        # self.save_markers_button.on_click(self.save_markers_to_csv)
        # self.add_control(widgets.VBox([self.save_markers_button]))

    def add_contour_map(self):
        options = ToggleButtons(
            options=['Elevation', 'Contour'],
            value='Elevation',
            description='Map Type:',
            disabled=False,
            button_style='', 
            layout={'width': 'max-content'}
        )
        options.observe(self.change_contour_map)
        display(options)

    def change_contour_map(self, change):
        if change.new == 'Elevation':
            url = "https://cyberjapandata.gsi.go.jp/xyz/dem_png/{z}/{x}/{y}.png"
        elif change.new == 'Contour':
            url = "https://cyberjapandata.gsi.go.jp/xyz/gm_tif/{z}/{x}/{y}.tif"
        layer = TileLayer(url=url)
        self.map.substitute_layer(self.layers['basemap'], layer)
        self.layers['basemap'] = layer

    def show(self):
        control = LayersControl(position='topright')
        self.map.add_control(control)
        display(self.map)

    def add_layers_control(self,**kwargs):
        """Layers control functionality
        
        """
        layers_control = ipyleaflet.LayersControl(**kwargs)
        self.add_control(layers_control)
    
    def add_fullscreen_control(self,position="bottomright"):
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

        self.add_control(draw_control)

    # def handle_interaction(self, event, **kwargs):
    #     if event['type'] == 'click':
    #         lat, lon = event['coordinates']
    #         marker = Marker(location=(lat, lon))
    #         self.marker_cluster.add_layer(marker)
    #         self.markers.append(marker)
                
    #         # Update the marker popup to display latitude and longitude
    #         self.marker_popup.value = f'Latitude: {lat}, Longitude: {lon}'
    #         marker.popup = self.marker_popup
    #         self.marker_layer.add_layer(marker)

    # def save_markers_to_csv(self, button):
    #     data = {'latitude': [], 'longitude': []}
    #     for marker in self.markers:
    #             location = marker.location
    #             data['latitude'].append(location[0])
    #             data['longitude'].append(location[1])
    #     df = pd.DataFrame(data)
    #     df.to_csv('markers.csv', index=False)

    # def clear_markers(self):
    #     for marker in self.markers:
    #         self.marker_cluster.remove_layer(marker)
    #         self.marker_layer.remove_layer(marker)
    #     self.markers = []

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

    # def add_basemap(m, basemap_name='OpenStreetMap', **kwargs):
    #     """Add a basemap to a map object."""
        
    #     if isinstance(basemap_name, str):
    #         try:
    #             basemap = basemaps[basemap_name]
    #         except KeyError:
    #             raise ValueError(f'Invalid basemap name: {basemap_name}')
    #     else:
    #         basemap = basemap_name
        
    #     tiles = basemap_to_tiles(basemap, **kwargs)
    #     m.add_layer(tiles)
        
    #     return tiles
            
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

    def add_image(self, url, width, height, position = 'bottomright',**kwargs):
        """Adds image to Geolog map
        
        Args:
            url: user-selected url to add image
        """
        import ipywidgets
        from ipyleaflet import WidgetControl
        output_widget = ipywidgets.Output(layout={'border': '1px solid black'})
        output_widget.clear_output()
        widget = ipywidgets.HTML(value = f'<img src="{url}" width="{width}" height="{height}">')
        control = WidgetControl(widget=widget, position=position)
        self.add(control)
    
    def add_toolbar(self, position="topright"):
        """Adds toolbar capability to map"""

        widget_width = "250px"
        padding = "0px 0px 0px 5px"  # upper, right, bottom, left

        toolbar_button = widgets.ToggleButton(
            value=False,
            tooltip="Toolbar",
            icon="wrench",
            layout=widgets.Layout(width="28px", height="28px", padding=padding),
        )

        close_button = widgets.ToggleButton(
            value=False,
            tooltip="Close the tool",
            icon="times",
            button_style="primary",
            layout=widgets.Layout(height="28px", width="28px", padding=padding),
        )

        toolbar = widgets.HBox([toolbar_button])

        def toolbar_click(change):
            if change["new"]:
                toolbar.children = [toolbar_button, close_button]
            else:
                toolbar.children = [toolbar_button]

        toolbar_button.observe(toolbar_click, "value")

        def close_click(change):
            if change["new"]:
                toolbar_button.close()
                close_button.close()
                toolbar.close()

        close_button.observe(close_click, "value")

        rows = 2
        cols = 2
        grid = widgets.GridspecLayout(rows, cols, grid_gap="0px", layout=widgets.Layout(width="65px"))

        icons = ["folder-open", "map", "bluetooth", "area-chart"]
        button_descs = ["Load CSV", "Add Marker", "Toggle Heatmap", "Toggle Fullscreen"]
        button_funcs = [self.load_csv, self.add_marker, self.toggle_heatmap, self.toggle_fullscreen]

        for i in range(rows):
            for j in range(cols):
                button = widgets.Button(description=button_descs[i*rows+j], button_style="primary", icon=icons[i*rows+j], 
                                            layout=widgets.Layout(width="28px", padding="0px"))
                button.on_click(button_funcs[i*rows+j])
                grid[i, j] = button

        toolbar = widgets.VBox([toolbar_button])

        def toolbar_click(change):
            if change["new"]:
                toolbar.children = [widgets.HBox([close_button, toolbar_button]), grid]
            else:
                toolbar.children = [toolbar_button]

        toolbar_button.observe(toolbar_click, "value")

        toolbar_ctrl = ipyleaflet.WidgetControl(widget=toolbar, position=position)

        self.map.add_control(toolbar_ctrl)
        
    # def _on_load_button_clicked(self, b):
    #     # Create a file picker widget
    #     input_csv_file_picker = widgets.FileUpload(
    #         accept='.csv',
    #         description='Select CSV',
    #         multiple=False
    #     )

    #     # Create a handler for when a file is uploaded
    #     def handle_upload(change):
    #         # Get the uploaded file
    #         uploaded_file = list(change['new'].values())[0]
    #         file_content = uploaded_file['content']

    #         # Read the CSV data into a pandas dataframe
    #         csv_data = pd.read_csv(io.StringIO(file_content.decode('utf-8')))

    #         # Convert the dataframe into markers and add them to the map
    #         markers = []
    #         for i, row in csv_data.iterrows():
    #             lat = row['latitude']
    #             lon = row['longitude']
    #             popup = row['name']
    #             marker = ipyleaflet.Marker(location=(lat, lon), title=popup)
    #             markers.append(marker)
    #         self.marker_layer.markers = markers

    #         # Remove the file picker widget
    #         self.toolbar.children = [self.load_button]

    #     # Attach the handler to the file picker
    #     input_csv_file_picker.observe(handle_upload, names='value')

    #     # Replace the toolbar with the file picker widget
    #     self.toolbar.children = [input_csv_file_picker]

    def add_markers_from_csv(map_obj, csv_file):
    # Read the CSV data into a pandas DataFrame
        data = pd.read_csv(csv_file, usecols=["name", "sov_a3", "latitude", "longitude", "pop_max"])
    
    # Iterate over the rows of the DataFrame and create markers for each location
        for _, row in data.iterrows():
            location = (row["latitude"], row["longitude"])
            title = f"{row['name']} ({row['sov_a3']}) - Population: {row['pop_max']}"
            marker = Marker(location=location, title=title)
            map_obj.add_layer(marker)


    # def to_streamlit(
    #     self,
    #     width=None,
    #     height=600,
    #     scrolling=False,
    #     add_layer_control=True,
    #     bidirectional=False,
    #     **kwargs,
    # ):
    #     """Renders `folium.Figure` or `folium.Map` in a Streamlit app. This method is a static Streamlit Component, meaning, no information is passed back from Leaflet on browser interaction.

    #     Args:
    #         width (int, optional): Width of the map. Defaults to None.
    #         height (int, optional): Height of the map. Defaults to 600.
    #         scrolling (bool, optional): Whether to allow the map to scroll. Defaults to False.
    #         add_layer_control (bool, optional): Whether to add the layer control. Defaults to True.
    #         bidirectional (bool, optional): Whether to add bidirectional functionality to the map. The streamlit-folium package is required to use the bidirectional functionality. Defaults to False.

    #     Raises:
    #         ImportError: If streamlit is not installed.

    #     Returns:
    #         streamlit.components: components.html object.
    #     """

    #     try:
    #         import streamlit.components.v1 as components

    #         if add_layer_control:
    #             self.add_layer_control()

    #         if bidirectional:
    #             from streamlit_folium import st_folium

    #             output = st_folium(self, width=width, height=height)
    #             return output
    #         else:
    #             # if responsive:
    #             #     make_map_responsive = """
    #             #     <style>
    #             #     [title~="st.iframe"] { width: 100%}
    #             #     </style>
    #             #     """
    #             #     st.markdown(make_map_responsive, unsafe_allow_html=True)
    #             return components.html(
    #                 self.to_html(), width=width, height=height, scrolling=scrolling
    #             )

    #     except Exception as e:
    #         raise Exception(e)

    # #     # widget_width = "250px"
    # #     # padding = "0px 0px 0px 5px"

    # #     toolbar_button = widgets.ToggleButton(
    # #         value=False,
    # #         tooltip="Toolbar",
    # #         icon="wrench",
    # #         layout=widgets.Layout(width="28px", height="28px", padding=padding),
    # #     )

    #     # close_button = widgets.ToggleButton(
    #     #     value=False,
    #     #     tooltip="Close the tool",
    #     #     icon="times",
    #     #     button_style="primary",
    #     #     layout=widgets.Layout(height="28px", width="28px", padding=padding),
    #     # )

    #     # toolbar = widgets.HBox([toolbar_button])

    #     # def toolbar_click(change):
    #     #     if change["new"]:
    #     #         toolbar.children = [toolbar_button, close_button]
    #     #     else:
    #     #         toolbar.children = [toolbar_button]
                
    #     # toolbar_button.observe(toolbar_click, "value")

    #     # def close_click(change):
    #     #     if change["new"]:
    #     #         toolbar_button.close()
    #     #         close_button.close()
    #     #         toolbar.close()
    #     #         basemap.close()
                
    #     # close_button.observe(close_click, "value")

    #     # rows = 2
    #     # cols = 2
    #     # grid = widgets.GridspecLayout(rows, cols, grid_gap="0px", layout=widgets.Layout(width="65px"))

    #     # icons = ["folder-open", "map", "bluetooth", "area-chart"]

    #     # for i in range(rows):
    #     #     for j in range(cols):
    #     #         grid[i, j] = widgets.Button(description="", button_style="primary", icon=icons[i*rows+j], 
    #     #                                     layout=widgets.Layout(width="28px", padding="0px"))
                
    #     # toolbar = widgets.VBox([toolbar_button])

    #     basemap = widgets.Dropdown(
    #         options=['OpenStreetmap','roadmap','satellite'],
    #         value=None,
    #         description="Basemap",
    #         style={'description_width': 'initial'},
    #         layout=widgets.Layout(width='250px')
    #     )

    #     basemap_control = ipyleaflet.WidgetControl(widget=basemap, position='topright')

    #     def change_basemap(change):
    #         if change['new']:
    #             self.add_basemap(basemap.value)

    #     basemap.observe(change_basemap, names='value')

    #     # self.add_control(ipyleaflet.WidgetControl(widget=widgets.Output(),position="bottomright"))
    #     self.add_control(basemap_control)

    #     # def toolbar_click(b):
    #     #     with b:
    #     #         b.clear_output()

    #     #         if b.icon == 'map':
    #     #             self.add_control(basemap_control)

def csv_to_shp(in_csv, out_shp, x="longitude", y="latitude"):
    """
    Convert a CSV file with lat/lon information to a shapefile.
        
    Parameters:
        in_csv (str): Path to the input CSV file.
        out_shp (str): Path to the output shapefile.
        x (str): Name of the column in the CSV file containing the longitude values (default="longitude").
        y (str): Name of the column in the CSV file containing the latitude values (default="latitude").
    """
    # Read in the CSV file and convert the lat/lon columns to a geometry column
    df = pd.read_csv(in_csv)
    geometry = [Point(xy) for xy in zip(df[x], df[y])]
    crs = "epsg:4326" # Assume WGS84 coordinate reference system
    gdf = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)

    # Write the GeoDataFrame to a shapefile
    gdf.to_file(out_shp, driver="ESRI Shapefile")

import numpy as np

def display_polygon(shp_file, heady=0,color="Red"):
    """
    Displays your shp file in ipyleaflet map

    Args:
        - shp_file is the location of the shp file
    """
    data = gpd.read_file(shp_file)

    if heady == 0:
        pass
    else:
        data = data.head(heady)
        data.plot(facecolor=color)
        return data

def calculate_circularity_index(shp_file):
    """
    Calculates the circularity of a shapfile as defined by sqrt(4*pi*area)/perimeter

    Args:
        - shp_file is the location of the shp file
    """
    # Read in the shapefile using pyshp
    sf = gpd.read_file(shp_file)

    area = shape(sf.loc[0,'geometry']).area

    for i in range(len(sf)):
        sf.loc[i,'CI'] = np.sqrt(4 * np.pi * shape(sf.loc[i,'geometry']).area) / shape(sf.loc[i,'geometry']).length
    
    # Get the shapefile's shape records
    # shapes = sf.shapes()

    
    return sf

def elongation_ratio(shp_file):
    """
    Calculates the elongation ratio of a shapfile as defined by 1 - shortaxis/longaxis

    Args:
        - shp_file is the location of the shp file
    """
    # Read in the shapefile using pyshp
    sf = gpd.read_file(shp_file)

    area = shape(sf.loc[0,'geometry']).area

    for i in range(len(sf)):
        sf.loc[i,'CI'] = np.sqrt(4 * np.pi * shape(sf.loc[i,'geometry']).area) / shape(sf.loc[i,'geometry']).length
    
    # Get the shapefile's shape records
    # shapes = sf.shapes()

    
    return sf