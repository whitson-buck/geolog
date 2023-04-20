import folium

class Map(folium.Map):
    def __init__(self, center=[35,-90], zoom=5, **kwargs) -> None:
        super().__init__(location=center,zoom_start=zoom, **kwargs)

    def add_tile_layer(self, url, name, attribution="",**kwargs):
        tile_layer = folium.TileLayer(
            tiles=url,
            name=name,
            attr=attribution,
            **kwargs
        )
        self.add_child(tile_layer)