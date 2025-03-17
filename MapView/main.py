import asyncio
from kivy.app import App
from kivy_garden.mapview import MapMarker, MapView
from kivy.clock import Clock
from lineMapLayer import LineMapLayer
from datasource import Datasource


class MapViewApp(App):
    def __init__(self, **kwargs):
        super().__init__()
        # додати необхідні змінні
        self.user_id : int = 1
        self.mapview = MapView(zoom = 11)
        self.map_layer = LineMapLayer()
        self.datasource : Datasource = Datasource(self.user_id)
        self.car_marker = MapMarker(source = 'images/car.png')
        self.first_point_received : bool = False

    def on_start(self):
        """
        Встановлює необхідні маркери, викликає функцію для оновлення мапи
        """
        self.mapview.add_marker(self.car_marker)
        Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        """
        Викликається регулярно для оновлення мапи
        """
        points = self.datasource.get_new_points()
        if not points:
            return
        for point in points:
            coordinates = point.get_coordinates()

            #Centering map for first point`s coordinates
            if not self.first_point_received:
                self.mapview.center_on(*coordinates)
                self.first_point_received = True

            self.map_layer.add_point(coordinates)
            self.update_car_marker(coordinates)

            if point.is_bump():
                self.set_pothole_marker(coordinates)
            elif point.is_pothole():
                self.set_bump_marker(coordinates)

    def update_car_marker(self, point):
        """
        Оновлює відображення маркера машини на мапі
        :param point: GPS координати
        """
        self.car_marker.lat = point[0]
        self.car_marker.lon = point[1]

        self.mapview.remove_marker(self.car_marker)
        self.mapview.add_marker(self.car_marker)


    def set_pothole_marker(self, point):
        """
        Встановлює маркер для ями
        :param point: GPS координати
        """
        marker = MapMarker(lat=point[0],
                           lon = point[1],
                           source = "images/pothole.png")
        self.mapview.add_marker(marker)

    def set_bump_marker(self, point):
        """
        Встановлює маркер для лежачого поліцейського
        :param point: GPS координати
        """
        marker = MapMarker(lat=point[0],
                           lon = point[1],
                           source = "images/bump.png")
        self.mapview.add_marker(marker)

    def build(self):
        """
        Ініціалізує мапу MapView(zoom, lat, lon)
        :return: мапу
        """
        self.mapview.add_layer(self.map_layer, mode="scatter")
        return self.mapview


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(MapViewApp().async_run(async_lib="asyncio"))
    loop.close()
