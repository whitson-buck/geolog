"""Main module."""

import string
import random
#import ipyleaflet

#class Map(ipyleaflet.map):
#    def __init__(self, center, zoom, **kwargs): -> None:
#
#        if "scroll_wheel_zoom" not in kwargs:
#            kwargs["scroll_wheel_zoom"] = True
#        super().__init__(self, center, zoom, **kwargs)

def generate_password(length=10):
    # Define the character sets to use in the password
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_chars = string.punctuation
    
    # Combine the character sets
    all_chars = lowercase + uppercase + digits + special_chars
    
    # Generate a password with the specified length
    password = ''.join(random.choice(all_chars) for i in range(length))
    
    return password

def generate_ascii_image(width, height):
    # Define the ASCII characters to use
    ascii_chars = ['.', ',', ':', ';', '+', '*', '?', '%', 'S', '#', '@']
    
    # Generate the ASCII image
    image = ''
    for y in range(height):
        for x in range(width):
            # Choose a random ASCII character from the list
            char = random.choice(ascii_chars)
            # Add the character to the image
            image += char
        # Add a newline character at the end of each row
        image += '\n'
    
    return image

def text_adventure_game():
    # Define the game world
    world = {
        'start': {
            'description': 'You are standing at the entrance of a dark cave. There is a torch lying on the ground next to you.',
            'exits': {
                'north': 'tunnel',
                'east': 'wall',
                'west': 'cliff'
            }
        },
        'tunnel': {
            'description': 'You are in a narrow tunnel. The walls are damp and the air is musty.',
            'exits': {
                'south': 'start',
                'north': 'chamber'
            }
        },
        'chamber': {
            'description': 'You are in a large chamber. There is a treasure chest in the middle of the room.',
            'exits': {
                'south': 'tunnel'
            },
            'items': {
                'treasure': 'A shiny gold coin'
            }
        },
        'wall': {
            'description': 'You have hit a dead end. There is nothing here.',
            'exits': {
                'west': 'start'
            }
        },
        'cliff': {
            'description': 'You are standing at the edge of a cliff. The ground drops away beneath you.',
            'exits': {
                'east': 'start'
            }
        }
    }
    
    # Define the player's starting location
    current_location = 'start'
    
    # Define the player's inventory
    inventory = []
    
    # Start the game loop
    while True:
        # Print the current location description
        print(world[current_location]['description'])
        
        # Check if there are any items in the current location and prompt the player to pick them up
        if 'items' in world[current_location]:
            for item_name, item_description in world[current_location]['items'].items():
                print(f"You see a {item_name} here.")
                answer = input("Do you want to pick it up? (y/n) ")
                if answer.lower() == 'y':
                    inventory.append(item_name)
                    print(f"You pick up the {item_name}.")
        
        # Print the available exits
        print("Available exits:")
        for exit_direction, exit_location in world[current_location]['exits'].items():
            print(f"{exit_direction.capitalize()}: {exit_location}")
        
        # Prompt the player to choose an exit
        answer = input("What do you want to do? ")
        if answer in world[current_location]['exits']:
            current_location = world[current_location]['exits'][answer]
        elif answer == 'inventory':
            print("You are carrying:")
            for item in inventory:
                print(f"- {item}")
        else:
            print("You can't do that.")