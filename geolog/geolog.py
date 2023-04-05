"""Main module."""

import string
import random
import ipyleaflet

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
        layers_control = ipyleaflet.LayersControl(**kwargs)
        self.add_control(layers_control)

    def add_tile_layer(self,url,name,attribution="",**kwargs):

        tile_layer = ipyleaflet.TileLayer(
            url=url,
            name=name,
            ttribution=attribution
            **kwargs
        )
        self.add_layer(tile_layer)
    
    def add_fullscreen_control(self,position="topleft"):
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
            basemap - basemap of user choice.
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