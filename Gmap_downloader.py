import urllib.request
from PIL import ImageTk, Image
import os
import math


class GoogleMapDownloader:


    def __init__(self, lat, lng, zoom=12):

        self._lat = lat
        self._lng = lng
        self._zoom = zoom

    def getXY(self):

        tile_size = 256

        # Use a left shift to get the power of 2
        # i.e. a zoom level of 2 will have 2^2 = 4 tiles
        numTiles = 1 << self._zoom

        # Find the x_point given the longitude
        point_x = (tile_size / 2 + self._lng * tile_size / 360.0) * numTiles // tile_size

        # Convert the latitude to radians and take the sine
        sin_y = math.sin(self._lat * (math.pi / 180.0))

        # Calulate the y coorindate
        point_y = ((tile_size / 2) + 0.5 * math.log((1 + sin_y) / (1 - sin_y)) * -(
                    tile_size / (2 * math.pi))) * numTiles // tile_size

        return int(point_x), int(point_y)

    def generateImage(self, **kwargs):

        start_x = kwargs.get('start_x', None)
        start_y = kwargs.get('start_y', None)
        tile_width = kwargs.get('tile_width', 5)
        tile_height = kwargs.get('tile_height', 5)

        # Check that we have x and y tile coordinates
        if start_x == None or start_y == None:
            start_x, start_y = self.getXY()

        # Determine the size of the image
        width, height = 256 * tile_width, 256 * tile_height

        # Create a new image of the size require
        map_img = Image.new('RGB', (width, height))

        for x in range(0, tile_width):
            for y in range(0, tile_height):
                url = 'https://mt0.google.com/vt?x=' + str(start_x + x) + '&y=' + str(start_y + y) + '&z=' + str(
                    self._zoom)

                current_tile = str(x) + '-' + str(y)
                urllib.request.urlretrieve(url, current_tile)

                im = Image.open(current_tile)
                map_img.paste(im, (x * 256, y * 256))

                os.remove(current_tile)

        return map_img


def main_l():

    print("Launching Google map downloader")
   # x_cordinate = float(input("Input latitude(43.2406):\n"))
   # y_cordinate = float(input("Input longitude(76.9105):\n"))

    gmd = GoogleMapDownloader(43.2406, 76.9105, 15)
    #gmd = GoogleMapDownloader(x_cordinate, y_cordinate, 16)

    print("The tile coorindates are {}".format(gmd.getXY()))

    try:
        # Get the high resolution image
        img = gmd.generateImage()
    except IOError:
        print("Could not generate the image")
    else:
        img.save("mymap.jpg")
        print("The map has successfully been created")


if __name__ == '__main__':  main_l()