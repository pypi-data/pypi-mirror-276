"""Main module."""


import ipyleaflet
from ipyleaflet import basemaps, WidgetControl
import ipywidgets as widgets

class Map(ipyleaflet.Map):

    """This is the map class that inherits from ipyleaflet.Map.

    Args:
        ipyleaflet (Map): The ipyleaflet.Map class.
    """
    def __init__(self, center=[20, 0], zoom=2, **kwargs):
        """Initialize the map.

        Args:
            center (list, optional): Set the center of the map. Defaults to [20, 0].
            zoom (int, optional): Set the zoom level of the map. Defaults to 2.
        """
        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True

        super().__init__(center=center, zoom=zoom, **kwargs)
        self.add_control(ipyleaflet.LayersControl(position='topright'))

        self.add_toolbar()
     
    def add_tile_layer(self, url, name, **kwargs):
        layer = ipyleaflet.TileLayer(url=url, name=name, **kwargs)
        self.add_layer(layer)

    def add_basemap(self, name):
        """Adds a basemap to the map.

        Args:
            name (str): The name of the basemap to add to the map. Check ipyleaflet website for possible names
        """
        if isinstance(name, str):
            url = eval(f"basemaps.{name}").build_url()
            self.add_tile_layer(url, name)
        else:
            self.add(name)

    def add_geojson(self, data, name = "geojson", **kwargs):
        """Adds a GeoJSON layer to the map.

        Args:
            data (str | dict): The GeoJSON data as a string or a dictionary.
            name (str, optional): The name of the layer. Defaults to "geojson".
        """
        import json
        
        if isinstance(data, str):
                with open(data) as f:
                    data = json.load(f)


        if "style" not in kwargs:
            kwargs["style"] = {"color": "blue", "weight": 1, "fillOpacity": 0}
        
        if "hover_style" not in kwargs:
            kwargs["hover_style"] = {"fillColor": "red", "fillOpacity": 0.3}

        layer = ipyleaflet.GeoJSON(data=data, name=name, **kwargs)
        self.add(layer)

    def add_shp(self, data, name = "shp", **kwargs):
        """Adds a shapefile to the current map.

        Args:
            data (str or dict): The path to the shapefile as a string or a dictionary representing a shapefile.
            name (str, optional): Name of the layer. Defaults to "shp".
        """

        import shapefile
        import json
        """_summary_
        """
        if isinstance(data, str):
            with shapefile.Reader(data) as shp:
                data = shp.__geo_interface__
        self.add_geojson(data, name, **kwargs)
   
    def add_image(self, url, bounds,  name = "image", **kwargs):
        """_summary_

        Args:
            url (_type_): _description_
            bounds (_type_): _description_
            name (str, optional): _description_. Defaults to "image".
        """

        layer = ipyleaflet.ImageOverlay(url=url, bounds=bounds, name=name, **kwargs)
        self.add(layer)

    def add_raster(self, data, name="raster",zoom_to_layer=True, **kwargs):
        """Adds a raster layer to the map.

        Args:
            data (str): The path to the raster file.
            name (str, optional): The name of the layer. Defaults to "raster".
        """
        try:
            from localtileserver import TileClient, get_leaflet_tile_layer
        except ImportError:
            raise ImportError("Please install the localtileserver package.")
        
        client = TileClient(data)
        layer = get_leaflet_tile_layer(client, name=name, **kwargs)
        self.add(layer)
        if zoom_to_layer:
            self.center = client.center()
            self.zoom = client.default_zoom

    def add_zoom_slider(self, description="Zoom level", min=0, max=15, value=10, position='topright'):
        """_summary_

        Args:
            description (str, optional): _description_. Defaults to "Zoom level".
            min (int, optional): _description_. Defaults to 0.
            max (int, optional): _description_. Defaults to 15.
            value (int, optional): _description_. Defaults to 10.
            position (str, optional): _description_. Defaults to 'topright'.
        """
        zoom_slider = widgets.IntSlider(
            description=description, min=min, max=max, value=value                                      
                )
        control = ipyleaflet.WidgetControl(widget=zoom_slider, position=position,)
        self.add(control)
        widgets.jslink((zoom_slider, "value"), (self, "zoom"))

    def add_toolbar(self, position="topright"):
        """_summary_

        Args:
            position (str, optional): _description_. Defaults to "topright".
        """        

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
        toolbar = widgets.VBox([toolbar_button])

        def close_click(change):
            if change["new"]:
                toolbar_button.close()
                close_button.close()
                toolbar.close()


        close_button.observe(close_click, "value")
        
        rows = 2
        cols = 2
        grid = widgets.GridspecLayout(
            rows, cols, grid_gap="0px", layout=widgets.Layout(width="65px")
        )

        icons = ["folder-open", "map", "info", "question"]

        for i in range(rows):
            for j in range(cols):
                grid[i, j] = widgets.Button(
                    description="",
                    button_style="primary",
                    icon=icons[i * rows + j],
                    layout=widgets.Layout(width="28px", padding="0px"),
                )

        def toolbar_click(change):
            if change["new"]:
                toolbar.children = [widgets.HBox([close_button, toolbar_button]), grid]
            else:
                toolbar.children = [toolbar_button]

        toolbar_button.observe(toolbar_click, "value")
        toolbar_ctrl = WidgetControl(widget=toolbar, position="topright")
        self.add(toolbar_ctrl)

        output = widgets.Output()
        output_control = WidgetControl(widget=output, position="bottomright")
        self.add(output_control)

        def toolbar_callback(change):
            if change.icon == "folder-open":
                with output:
                    output.clear_output()
                    print(f"You can open a file")
            elif change.icon == "map":
                with output:
                    output.clear_output()
                    print(f"You can add a layer")
            else:
                with output:
                    output.clear_output()
                    print(f"Icon: {change.icon}")

        for tool in grid.children:
            tool.on_click(toolbar_callback)

        with output:
            print("Toolbar is ready")
