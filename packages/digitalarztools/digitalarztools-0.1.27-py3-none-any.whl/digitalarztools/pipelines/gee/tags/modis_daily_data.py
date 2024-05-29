from datetime import datetime, timedelta

import ee

from digitalarztools.pipelines.gee.core.region import GEERegion


class MODISDailyData:
    @staticmethod
    def get_latest_dates(delta_in_days=10) -> (str, str):
        # Calculate the date range for the latest 10 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=delta_in_days)

        # Convert dates to strings formatted as required by the Earth Engine API
        return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

    @staticmethod
    def get_temperature_vis_param():
        # Define visualization parameters
        return {
            'min': 13000.0,
            'max': 16500.0,
            'palette': [
                '040274', '040281', '0502a3', '0502b8', '0502ce', '0502e6',
                '0602ff', '235cb1', '307ef3', '269db1', '30c8e2', '32d3ef',
                '3be285', '3ff38f', '86e26f', '3ae237', 'b5e22e', 'd6e21f',
                'fff705', 'ffd611', 'ffb613', 'ff8b13', 'ff6e08', 'ff500d',
                'ff0000', 'de0101', 'c21301', 'a71001', '911003'
            ],
        }

    @staticmethod
    def convert_modis_lst_to_celsius(dn_value):
        """
        Converts a MODIS LST digital number (DN) to degrees Celsius.

        Parameters:
        - dn_value: The MODIS LST DN value to convert.

        Returns:
        - The temperature in degrees Celsius.
        """
        # Constants
        scale_factor = 0.02
        kelvin_to_celsius_offset = 273.15

        # Convert DN to Kelvin
        kelvin_value = dn_value * scale_factor

        # Convert Kelvin to Celsius
        celsius_value = kelvin_value - kelvin_to_celsius_offset

        return celsius_value

    @classmethod
    def get_temperature_image_collection(cls, delta_in_days=10, region: GEERegion=None) -> ee.ImageCollection:
        start_date_str, end_date_str = cls.get_latest_dates(delta_in_days)
        # Define the dataset with the updated date range
        dataset = ee.ImageCollection('MODIS/061/MOD11A1') \
            .filter(ee.Filter.date(start_date_str, end_date_str))
        if region is not None:
            dataset = dataset.filterBounds(region.bounds)

        # Select the Land Surface Temperature band
        landSurfaceTemperature = dataset.select('LST_Day_1km')
        return landSurfaceTemperature

    @classmethod
    def get_temperature_data_url(cls, delta_in_days=10, region: GEERegion=None) -> str:
        landSurfaceTemperature = cls.get_temperature_image_collection(delta_in_days, region)
        # Generate a URL for visualization
        landSurfaceTemperatureVis = cls.get_temperature_vis_param()
        url = landSurfaceTemperature.getMapId(landSurfaceTemperatureVis)
        return url['tile_fetcher'].url_format

    @classmethod
    def get_snow_cover_url(cls, delta_in_days=10):
        start_date_str, end_date_str = cls.get_latest_dates(delta_in_days)
        # Define your dataset, filtering by the last 15 days.
        dataset = ee.ImageCollection('MODIS/061/MOD10A1') \
            .filter(ee.Filter.date(start_date_str, end_date_str))
        snowCover = dataset.select('NDSI_Snow_Cover')

        # Mask areas with no snow cover.
        maskedSnowCover = snowCover.map(lambda image: image.updateMask(image.gt(0)))

        # Composite the images if needed. For simplicity, here we just take the median.
        composite = maskedSnowCover.median()

        # Define visualization parameters.
        snowCoverVis = {
            'min': 0.0,
            'max': 100.0,
            'palette': ['0dffff', '0524ff', 'ffffff'],
        }

        # Generate the map ID and token.
        map_id_dict = composite.getMapId(snowCoverVis)

        # Construct the tile layer URL template.
        tile_url_template = "https://earthengine.googleapis.com/v1alpha/projects/earthengine-legacy/maps/{map_id}/tiles/{{z}}/{{x}}/{{y}}".format(
            map_id=map_id_dict['mapid'])

        print("Tile layer URL:", tile_url_template)
