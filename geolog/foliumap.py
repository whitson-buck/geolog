import folium

class Map(folium.Map):
    """The Map class inherits folium.Map. By default, the Map will add OpenStreetMap as the basemap.
    Returns:
        object: folium map object.
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.baseclass = "folium"

        if "layers_control" not in kwargs:
            self.options["layersControl"] = True
        else:
            self.options["layersControl"] = kwargs["layers_control"]

    def add_layer(self, layer):
        """Adds a layer to the map.
        Args:
            layer (TileLayer): A TileLayer instance.
        """
        layer.add_to(self)

    def add_layer_control(self):
        """Adds layer control to the map."""
        layer_ctrl = False
        for item in self.to_dict()["children"]:
            if item.startswith("layer_control"):
                layer_ctrl = True
                break
        if not layer_ctrl:
            folium.LayerControl().add_to(self)

    

    # def add_raster(
    #     self,
    #     source,
    #     band=None,
    #     palette=None,
    #     vmin=None,
    #     vmax=None,
    #     nodata=None,
    #     attribution=None,
    #     layer_name="Local COG",
    #     **kwargs,
    # ):
    #     """Add a local raster dataset to the map.
    #         If you are using this function in JupyterHub on a remote server (e.g., Binder, Microsoft Planetary Computer) and
    #         if the raster does not render properly, try running the following code before calling this function:
    #         import os
    #         os.environ['LOCALTILESERVER_CLIENT_PREFIX'] = 'proxy/{port}'
    #     Args:
    #         source (str): The path to the GeoTIFF file or the URL of the Cloud Optimized GeoTIFF.
    #         band (int, optional): The band to use. Band indexing starts at 1. Defaults to None.
    #         palette (str, optional): The name of the color palette from `palettable` to use when plotting a single band. See https://jiffyclub.github.io/palettable. Default is greyscale
    #         vmin (float, optional): The minimum value to use when colormapping the palette when plotting a single band. Defaults to None.
    #         vmax (float, optional): The maximum value to use when colormapping the palette when plotting a single band. Defaults to None.
    #         nodata (float, optional): The value from the band to use to interpret as not valid data. Defaults to None.
    #         attribution (str, optional): Attribution for the source raster. This defaults to a message about it being a local file.. Defaults to None.
    #         layer_name (str, optional): The layer name to use. Defaults to 'Local COG'.
    #     """

    #     tile_layer, tile_client = get_local_tile_layer(
    #         source,
    #         band=band,
    #         palette=palette,
    #         vmin=vmin,
    #         vmax=vmax,
    #         nodata=nodata,
    #         attribution=attribution,
    #         tile_format="folium",
    #         layer_name=layer_name,
    #         return_client=True,
    #         **kwargs,
    #     )
    #     self.add_layer(tile_layer)

    #     bounds = tile_client.bounds()  # [ymin, ymax, xmin, xmax]
    #     bounds = (
    #         bounds[2],
    #         bounds[0],
    #         bounds[3],
    #         bounds[1],
    #     )  # [minx, miny, maxx, maxy]
    #     self.zoom_to_bounds(bounds)

    #     arc_add_layer(tile_layer.tiles, layer_name, True, 1.0)
    #     arc_zoom_to_extent(bounds[2], bounds[0], bounds[3], bounds[1])

    # add_local_tile = add_raster
    
    # def add_basemap(self, basemap="HYBRID", show=True, **kwargs):
    #     """Adds a basemap to the map.
    #     Args:
    #         basemap (str, optional): Can be one of string from ee_basemaps. Defaults to 'HYBRID'.
    #         show (bool, optional): Whether to show the basemap. Defaults to True.
    #         **kwargs: Additional keyword arguments to pass to folium.TileLayer.
    #     """
    #     import xyzservices

    #     try:
    #         if isinstance(basemap, xyzservices.TileProvider):
    #             name = basemap.name
    #             url = basemap.build_url()
    #             attribution = basemap.attribution
    #             if "max_zoom" in basemap.keys():
    #                 max_zoom = basemap["max_zoom"]
    #             else:
    #                 max_zoom = 22
    #             layer = folium.TileLayer(
    #                 tiles=url,
    #                 attr=attribution,
    #                 name=name,
    #                 max_zoom=max_zoom,
    #                 overlay=True,
    #                 control=True,
    #                 show=show,
    #                 **kwargs,
    #             )

    #             self.add_layer(layer)

    #             arc_add_layer(url, name)

    #         elif basemap in basemaps:
    #             bmap = basemaps[basemap]
    #             bmap.show = show
    #             bmap.add_to(self)
    #             if isinstance(basemaps[basemap], folium.TileLayer):
    #                 url = basemaps[basemap].tiles
    #             elif isinstance(basemaps[basemap], folium.WmsTileLayer):
    #                 url = basemaps[basemap].url
    #             arc_add_layer(url, basemap)
    #         else:
    #             print(
    #                 "Basemap can only be one of the following: {}".format(
    #                     ", ".join(basemaps.keys())
    #                 )
    #             )

    #     except Exception:
    #         raise Exception(
    #             "Basemap can only be one of the following: {}".format(
    #                 ", ".join(basemaps.keys())
    #             )
    #         )



# def generate_password(length=10):
#     # Define the character sets to use in the password
#     lowercase = string.ascii_lowercase
#     uppercase = string.ascii_uppercase
#     digits = string.digits
#     special_chars = string.punctuation
    
#     # Combine the character sets
#     all_chars = lowercase + uppercase + digits + special_chars
    
#     # Generate a password with the specified length
#     password = ''.join(random.choice(all_chars) for i in range(length))
    
#     return password

# def generate_ascii_image(width, height):
#     # Define the ASCII characters to use
#     ascii_chars = ['.', ',', ':', ';', '+', '*', '?', '%', 'S', '#', '@']
    
#     # Generate the ASCII image
#     image = ''
#     for y in range(height):
#         for x in range(width):
#             # Choose a random ASCII character from the list
#             char = random.choice(ascii_chars)
#             # Add the character to the image
#             image += char
#         # Add a newline character at the end of each row
#         image += '\n'
    
#     return image

# class Text_Adventure():
#     world = {
#         'start': {
#             'description': 'You are standing at the entrance of a dark cave. There is a torch lying on the ground next to you.',
#             'exits': {
#                 'north': 'tunnel',
#                 'east': 'wall',
#                 'west': 'cliff'
#             }
#         },
#         'tunnel': {
#             'description': 'You are in a narrow tunnel. The walls are damp and the air is musty.',
#             'exits': {
#                 'south': 'start',
#                 'north': 'chamber'
#             }
#         },
#         'chamber': {
#             'description': 'You are in a large chamber. There is a treasure chest in the middle of the room.',
#             'exits': {
#                 'south': 'tunnel'
#             },
#             'items': {
#                 'treasure': 'A shiny gold coin'
#             }
#         },
#         'wall': {
#             'description': 'You have hit a dead end. There is nothing here.',
#             'exits': {
#                 'west': 'start'
#             }
#         },
#         'cliff': {
#             'description': 'You are standing at the edge of a cliff. The ground drops away beneath you.',
#             'exits': {
#                 'east': 'start'
#             }
#         }
#     }
    
#     # Define the player's starting location
#     current_location = 'start'
    
#     # Define the player's inventory
#     inventory = []
    
#     # Start the game loop
#     while True:
#         # Print the current location description
#         print(world[current_location]['description'])
        
#         # Check if there are any items in the current location and prompt the player to pick them up
#         if 'items' in world[current_location]:
#             for item_name, item_description in world[current_location]['items'].items():
#                 print(f"You see a {item_name} here.")
#                 answer = input("Do you want to pick it up? (y/n) ")
#                 if answer.lower() == 'y':
#                     inventory.append(item_name)
#                     print(f"You pick up the {item_name}.")
        
#         # Print the available exits
#         print("Available exits:")
#         for exit_direction, exit_location in world[current_location]['exits'].items():
#             print(f"{exit_direction.capitalize()}: {exit_location}")
        
#         # Prompt the player to choose an exit
#         answer = input("What do you want to do? ")
#         if answer in world[current_location]['exits']:
#             current_location = world[current_location]['exits'][answer]
#         elif answer == 'inventory':
#             print("You are carrying:")
#             for item in inventory:
#                 print(f"- {item}")
#         else:
#             print("You can't do that.")