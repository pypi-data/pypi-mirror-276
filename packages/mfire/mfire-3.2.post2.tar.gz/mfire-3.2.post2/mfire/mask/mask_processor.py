import re
from pathlib import Path
from typing import Dict, List, Optional

from geojson import Feature
from shapely import geometry as shp_geom

import mfire.utils.hash as hashmod
import mfire.utils.mfxarray as xr
from mfire.mask.cardinal_mask import CardinalMasks
from mfire.mask.gridage import GeoDraw, Shape
from mfire.mask.mask_merge import MaskMerge, MergeArea
from mfire.settings import Settings, get_logger
from mfire.utils.xr import (
    ArrayLoader,
    from_0_360_to_center,
    from_center_to_0_360,
    grid_info,
)
from mfire.utils.string import _

# Logging
LOGGER = get_logger(name="mask_processor", bind="mask")


class MaskFile:
    """
    Class to write masks to disk, in netcdf format.

    Args:
        data: Dictionary containing the data to be written to disk.
        grid_names: List of grid names to be written.

    Attributes:
        output_path: Path to the output file.

    """

    def __init__(self, data: Dict, grid_names: List[str]):
        self.data = data
        self.grid_names = grid_names

        # Check if the output file is defined
        if "file" not in data:
            raise ValueError(
                "You should have in the file something to name the output."
            )

        self.output_path = Path(data["file"])

        # Create the output directory if it does not exist
        output_dir = self.output_path.parent
        output_dir.mkdir(parents=True, exist_ok=True)

    def to_file(self, mask_merge: MaskMerge):
        """Writes masks to disk, in netcdf format.

        Args:
            mask_merge (MaskMerge): List of masks to be written.

        """
        # Create a netcdf dataset from the mask merge
        mask_ds = mask_merge.get_merge()

        # Reduce the size of the netcdf file by converting the mask variables to
        # boolean.
        for grid_name in self.grid_names:
            mask_ds[grid_name] = mask_ds[grid_name].mask.bool
        mask_ds = mask_ds.drop_vars("is_point")

        # Add the md5sum of the masks to the netcdf attributes
        md5sum = self.data.get("mask_hash") or hashmod.MD5(self.data["geos"]).hash
        mask_ds.attrs["md5sum"] = md5sum

        # Write the netcdf file to disk
        mask_ds.to_netcdf(self.output_path)


class MaskProcessor:
    """
    Class to create geographical masks on data arrays.

    Attributes:
        config_dict (dict): Configuration dictionary for the production, containing
            at least the key 'geos'.

    """

    # Numbre of pre-configured zones after which we don't create merged zones
    MERGED_ZONES_THRESHOLD = 50

    PERCENT = 1
    MIN_ALT = [200, 300, 400, 500]
    MAX_ALT = [
        300,
        400,
        500,
        600,
        700,
        800,
        900,
        1000,
        1200,
        1400,
        1600,
        1800,
        2000,
        2300,
        2600,
        2900,
        3200,
        3500,
    ]

    def __init__(self, config_dict: dict):
        self.data = config_dict
        self.change_geometry()

        self.grid_names = Settings().grid_names()

    def change_geometry(self):
        """
        smooths line by rounding borders
        """
        for i, area in enumerate(self.data["geos"]["features"]):
            if shp_geom.shape(area["geometry"]).geom_type in [
                "Polygon",
                "MultiPolygon",
            ]:
                x = shp_geom.shape(area["geometry"]).buffer(1e-5)
                y = x.simplify(tolerance=0, preserve_topology=False)
                self.data["geos"]["features"][i]["geometry"] = Feature(geometry=y)[
                    "geometry"
                ]
            if shp_geom.shape(area["geometry"]).geom_type in [
                "LineString",
                "MultiLineString",
            ]:
                x = shp_geom.shape(area["geometry"])
                y = x.simplify(tolerance=0, preserve_topology=False)
                self.data["geos"]["features"][i]["geometry"] = Feature(geometry=y)[
                    "geometry"
                ]

    @staticmethod
    def extract_area_name(properties: dict) -> str:
        """Extracts the area name from a dictionary of properties.

        Searches for the area name in the provided `properties` dictionary using a
        predefined order of keys. Returns the first valid area name found, or raises a
        `ValueError` if no name is found.

        Args:
            properties (dict): A dictionary containing potential keys for the area name.
                - "name" (preferred)
                - "label"
                - "alt_label" (alternative label)
                - "areaName" (explicit area name)
                - "area_name" (alternative explicit area name)

        Returns:
            str: The extracted area name.

        Raises:
            ValueError: If no valid area name is found in the `properties` dictionary.
        """
        for key in ("name", "label", "alt_label", "areaName", "area_name"):
            if area_name := properties.get(key):
                return area_name
        raise ValueError("Area name not found in properties dictionary")

    @staticmethod
    def extract_alt_area_name(properties: dict) -> str:
        if (alt_label := properties.get("alt_label")) and (
            search := re.search(r"^.*_\((.*)\)$", alt_label)
        ):
            return search.group(1)
        return _("sur la zone")

    def get_mask(self, grid_name: str, shape: Shape) -> xr.Dataset:
        """get_mask

        Args:
            grid_name (str): The grid name.
            shape (shapely.geometry.shape): The shape to transform in netcdf.

        Returns:
            xr.Dataset: The mask dataset.
        """
        grid_da = ArrayLoader.load_altitude(grid_name)
        change_longitude = False
        if grid_da.longitude.max() > 180:
            change_longitude = True
            grid_da = from_0_360_to_center(grid_da)
        dout = GeoDraw(grid_info(grid_da)).create_mask_PIL(shape)
        if change_longitude:
            dout = from_center_to_0_360(dout)
        return dout.rename(
            {"latitude": f"latitude_{grid_name}", "longitude": f"longitude_{grid_name}"}
        )

    @staticmethod
    def is_axe(feature: dict) -> bool:
        """checks if mask's geojson description represents an axis.

        Args:
            feature (_type_): the geojson feature

        Returns:
            Bool: True if its an Axis, False otherwise
        """
        return feature["properties"].get("is_axe", False)

    @classmethod
    def generate_mask_by_altitude(
        cls, domain: xr.DataArray, altitude_da: xr.DataArray, area_id: str
    ) -> Optional[xr.Dataset]:
        """Genere des zones par tranche d'altitudes

        Args:
            domain (dataArray): Un dataArray contenant de 1 et des nans
            altitude_da (dataArray): Sur la même grille, contient des altitudes
            area_id (str): L'id du domaine à découper

        To Do : rajouter une option pour filtrer si les zones si les champs
            sont 'trop égaux'.
            Par exemple, si l'altitude max = 200, on crée <200 < 250  < 300  < 400
            qui sont identiques.

        Returns:
            dataArray:
              Contient les différentes découpes.
              Besoin d'avoir quelque chose de merger.
        """

        LOGGER.debug(
            "Entering generate mask by altitude",
            area_id=area_id,
            grid_name=altitude_da.name,
            func="generate_mask_by_altitude",
        )
        if domain.count() == 0:
            LOGGER.warning(
                "Le domaine n'est pas couvert par la grille d'altitude de ce modele"
            )
            return None
        domain = domain.squeeze("id").reset_coords("id", drop=True)
        LOGGER.debug(
            f"max = {altitude_da.min().values} et min = {altitude_da.max().values}",
            area_id=area_id,
            grid_name=altitude_da.name,
            func="generate_mask_by_altitude",
        )

        ds_alt = domain * altitude_da.rename(
            {
                "longitude": f"longitude_{altitude_da.name}",
                "latitude": f"latitude_{altitude_da.name}",
            }
        )

        alt_min = ds_alt.min().values
        alt_max = ds_alt.max().values
        nb_pt = int(ds_alt.count())

        # Creation des inferieurs
        l_temp = []
        for alt in [alt for alt in cls.MIN_ALT if alt_min <= alt <= alt_max]:
            dtemp = ((ds_alt < alt) * domain).mask.f32
            nb_current = int(dtemp.count())
            if (1 - cls.PERCENT / 100) > nb_current / nb_pt > (cls.PERCENT / 100):
                name = f"en dessous de {alt} m"
                dtemp = dtemp.expand_dims(dim="id").assign_coords(
                    id=[f"{area_id}_inf_{alt}"]
                )
                dtemp["areaName"] = (("id"), [name])
                dtemp["altAreaName"] = (("id"), [name])
                dtemp["areaType"] = (("id"), ["Altitude"])
                l_temp.append(dtemp)

        # Et là des supérieurs
        for alt in [alt for alt in cls.MAX_ALT if alt_min <= alt <= alt_max]:
            dtemp = ((ds_alt > alt) * domain).mask.f32
            nb_current = int(dtemp.count())
            if (1 - cls.PERCENT / 100) > nb_current / nb_pt > (cls.PERCENT / 100):
                name = f"au-dessus de {alt} m"
                dtemp = dtemp.expand_dims(dim="id").assign_coords(
                    id=[f"{area_id}_sup_{alt}"]
                )
                dtemp["areaName"] = (("id"), [name])
                dtemp["altAreaName"] = (("id"), [name])
                dtemp["areaType"] = (("id"), ["Altitude"])
                l_temp.append(dtemp)

        if l_temp:
            dmerged = xr.merge(l_temp)
            return dmerged.reset_coords(["areaName", "altAreaName", "areaType"])
        LOGGER.debug(
            "Not enought area.",
            area_id=area_id,
            grid_name=altitude_da.name,
            func="generate_mask_by_altitude",
        )
        return None

    def area_mask(self, area):
        """
        operation to be done for each area
        """
        area_id = area["id"]
        # Introduire ici le truc sur le hash
        poly = shp_geom.shape(area["geometry"])
        poly = poly.simplify(tolerance=0, preserve_topology=False)
        dmask = xr.Dataset()
        for grid_name in self.grid_names:
            dtemp = self.get_mask_on_grid(grid_name, poly, area_id, area["properties"])
            dmask = xr.merge([dmask, dtemp])
        return poly, dmask

    def generate_alticompas(self, area_id, poly, managemask, dtemp):
        """
        generate altitude and cardinal zones
        """
        for grid_name in self.grid_names:
            LOGGER.debug(
                "Creating altitude and geographical mask",
                area_id=area_id,
                grid_name=grid_name,
                func="create_masks",
            )
            ds_mask_compass = self.get_compass_area(grid_name, poly, area_id)
            altitude_da = ArrayLoader.load_altitude(grid_name)
            ds_mask_alti = self.generate_mask_by_altitude(
                dtemp[grid_name], altitude_da, area_id + "_alt_"
            )

            if ds_mask_compass and ds_mask_compass.id.size > 1:
                managemask.merge(ds_mask_compass)
            if ds_mask_alti is not None:
                managemask.merge(ds_mask_alti)

    def generate_fusion(self, managemask, merged_list):
        """
        doing the actual creation and merging
        of already prepared fusionned zones
        """
        for grid_name in self.grid_names:
            dgrid = managemask.get_merge()[grid_name]

            mask_merge = MaskMerge()
            merge_area = MergeArea(dgrid, mask_merge)

            for new_zone in merged_list:
                merge_area.compute(new_zone)

            dout = mask_merge.get_merge()

            if len(dout.data_vars) > 0:
                dout = dout.reset_coords(["areaName", "altAreaName", "areaType"])
                managemask.merge(dout)

    def create_masks(self):
        """
        create_masks
        This function create all the mask from a geojson dictionary.
        The creation is performed only if the output file is not present.
        """

        filemask = MaskFile(self.data, self.grid_names)
        # On tri les zones pour mettre les axes en dernier
        self.data["geos"]["features"].sort(key=self.is_axe)

        mask_merge = MaskMerge()  # to store all areas
        mask_merge_alticompas = MaskMerge()

        for area in self.data["geos"]["features"]:
            poly, dtemp = self.area_mask(area)
            mask_merge.merge(dtemp)

            # On recupere les infos qui nous interessent
            area_id = area["id"]
            if self.is_axe(area) and not dtemp["is_point"]:
                # operation only for polygonal axis

                # adding altitude and cardinal zones
                self.generate_alticompas(area_id, poly, mask_merge_alticompas, dtemp)

        mask_merge.merge(mask_merge_alticompas.get_merge())

        # save to disk
        filemask.to_file(mask_merge)

    def get_compass_area(self, grid_name: str, poly: Shape, area_id: str) -> xr.Dataset:
        """Effectue la découpe selon les points cardinaux

        Args:
            grid_name (str): Nom de la grille sur laquelle on veut projeter le JSON
            poly (shape): Le shape de la zone a découper
            area_id (str): L'identifiant original de la zone

        Returns:
            Dataset : Un dataset de la découpe
        """
        dmask = xr.Dataset()
        geo_B = CardinalMasks(poly, area_id=f"{area_id}_compass_").all_masks

        for area in geo_B["features"]:
            compass_poly = shp_geom.shape(area["geometry"])
            compass_poly = compass_poly.simplify(tolerance=0, preserve_topology=False)
            compass_id = area["id"]
            area["properties"]["type"] = "compass"
            dtemp = self.get_mask_on_grid(
                grid_name, compass_poly, compass_id, area["properties"]
            )

            dmask = xr.merge([dmask, dtemp])
        return dmask

    def get_mask_on_grid(
        self, grid_name: str, shape: Shape, area_id: str, properties: dict
    ) -> xr.Dataset:
        """
        This function creates a mask Dataset on a specified grid for a given geometric
        object (point or polygon) and assigns it properties from a dictionary.

        Args:
            grid_name (str): The name of the grid to create the mask on.
            shape (Shape): The shape object (point or polygon) defining the mask area.
            area_id (str): The ID to assign to the mask area.
            properties (dict): A dictionary containing properties for the mask area.

        Returns:
            xr.Dataset: A new xr.Dataset containing the mask and associated properties.
        """

        # Extract area type considering "is_axe" property
        area_type = properties.get("type", "")
        if properties.get("is_axe"):
            area_type = "Axis"

        # Get mask data from grid and add dimensions and coordinates
        mask_data = self.get_mask(grid_name, shape)
        mask_data = mask_data.expand_dims(dim="id").assign_coords(id=[area_id])

        # Add properties as data variables with appropriate dimensions
        mask_data["areaName"] = (("id",), [self.extract_area_name(properties)])
        mask_data["altAreaName"] = (("id",), [self.extract_alt_area_name(properties)])
        mask_data["areaType"] = (("id",), [area_type])

        # Create temporary variable for point/multipoint handling during fusion
        mask_data["is_point"] = (("id",), [shape.geom_type in ["Point", "MultiPoint"]])

        return mask_data
