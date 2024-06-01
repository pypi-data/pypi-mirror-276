﻿from typing import Optional

import mfire.utils.mfxarray as xr
from mfire.settings import get_logger

# Logging
LOGGER = get_logger(name="mask_processor", bind="mask")

# Pour la création de masques netcdf
# options pour la génération.
xr.set_options(keep_attrs=True)


def generate_mask_by_altitude(
    domain: xr.DataArray, altitude: xr.DataArray, area_id: str
) -> Optional[xr.Dataset]:
    """Genere des zones par tranche d'altitudes

    Args:
        domain (dataArray): Un dataArray contenant de 1 et des nans
        altitude (dataArray): Sur la même grille, contient des altitudes
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
        grid_name=altitude.name,
        func="generate_mask_by_altitude",
    )
    PERCENT = 5
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
    if int(domain.count()) == 0:
        LOGGER.warning(
            "Le domaine n'est pas couvert par la grille d'altitude de ce modele"
        )
        return None
    domain = domain.squeeze("id").reset_coords("id", drop=True)
    LOGGER.debug(
        f"max = {altitude.min().values} et min = {altitude.max().values}",
        area_id=area_id,
        grid_name=altitude.name,
        func="generate_mask_by_altitude",
    )

    try:
        ds_alt = domain * altitude.rename(
            {
                "longitude": f"longitude_{altitude.name}",
                "latitude": f"latitude_{altitude.name}",
            }
        )
    except Exception as e:
        LOGGER.error(
            f"Failed to calculate domain * altitude with domain={domain}"
            f" and altitude={altitude}.",
            func="generate_mask_by_altitude",
        )
        raise (e)

    alt_min = ds_alt.min().values
    alt_max = ds_alt.max().values
    nb_pt = int(ds_alt.count())
    if alt_min == alt_max and nb_pt > 1:
        LOGGER.warning(
            "Le fichier d'altitude ne semble pas correct. "
            f"Altitude min = {alt_min}; Altitude max = {alt_max}",
            alt_min=float(alt_min),
            alt_max=float(alt_max),
            area_id=area_id,
            grid_name=altitude.name,
            nb_points=nb_pt,
            func="generate_mask_by_altitude",
        )
    # Creation des inferieurs
    l_temp = []
    for alt in [alt for alt in MIN_ALT if alt_min <= alt <= alt_max]:
        dtemp = (ds_alt < alt) * domain
        dtemp = dtemp.wheretype.f32(dtemp > 0)
        nb_current = int(dtemp.count())
        if (1 - PERCENT / 100) > nb_current / nb_pt > (PERCENT / 100):
            name = f"en dessous de {alt} m"
            dtemp = dtemp.expand_dims(dim="id").assign_coords(
                id=[f"{area_id}_inf_{alt}"]
            )
            dtemp["areaName"] = (("id"), [name])
            dtemp["areaType"] = (("id"), ["Altitude"])
            l_temp.append(dtemp)

    # Et là des supérieurs
    for alt in [alt for alt in MAX_ALT if alt_min <= alt <= alt_max]:
        dtemp = (ds_alt > alt) * domain
        dtemp = dtemp.wheretype.f32(dtemp > 0)
        nb_current = int(dtemp.count())
        if (1 - PERCENT / 100) > nb_current / nb_pt > (PERCENT / 100):
            name = f"au-dessus de {alt} m"
            dtemp = dtemp.expand_dims(dim="id").assign_coords(
                id=[f"{area_id}_sup_{alt}"]
            )
            dtemp["areaName"] = (("id"), [name])
            dtemp["areaType"] = (("id"), ["Altitude"])
            l_temp.append(dtemp)

    if l_temp:
        dmerged = xr.merge(l_temp)
        return dmerged.reset_coords(["areaName", "areaType"])
    else:
        LOGGER.debug(
            "Not enought area.",
            area_id=area_id,
            grid_name=altitude.name,
            func="generate_mask_by_altitude",
        )
        return None
