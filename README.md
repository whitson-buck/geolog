# Geolog

**Geolog** is a Python package developed for geospatial analysis and map creation using `ipyleaflet`. It includes tools for adding drawing controls and other geospatial functionalities.

## Features
- `add_draw_controls()`: Enables drawing shapes on maps.
- More features planned for future updates.

## Installation
```sh
pip install geolog
```

## Usage
### Basic Example
```python
from geolog import add_draw_controls
add_draw_controls()
```

### Advanced Example
```python
from geolog import add_draw_controls
import ipyleaflet

# Create a map
m = ipyleaflet.Map(center=(34.05, -118.25), zoom=10)

# Add drawing controls to the map
add_draw_controls(m)

# Display the map
m
```

## License
This project is licensed under the MIT License.

For more information, visit the [Geolog documentation](https://whitson-buck.github.io/geolog).

## Credits
Created using [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [giswqs/pypackage](https://github.com/giswqs/pypackage) template.
