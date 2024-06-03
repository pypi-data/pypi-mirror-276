from pathlib import Path

import mfire.mask.mask_processor as mpr
import mfire.utils.mfxarray as xr
from mfire.settings import get_logger
from mfire.settings.settings import Settings
from mfire.tasks.CLI import CLI
from mfire.utils import MD5, Tasks
from mfire.utils.json import JsonFile

LOGGER = get_logger(name="process_mask.mod", bind="process_mask")


def main_function(mask_configuration: dict):
    """Main function for mask creation.

    Args:
        mask_configuration (dict): Single mask configuration.
    """
    output_file = Path(mask_configuration.get("file", ""))

    if output_file.exists():
        current_hash = mask_configuration.get(
            "mask_hash", MD5(mask_configuration["geos"]).hash
        )

        with xr.open_dataset(output_file) as ds:
            if ds.attrs.get("md5sum", "") == current_hash:
                LOGGER.info(
                    "Mask already exists and has the same md5sum. Mask creation is "
                    "skipped."
                )
                return

    LOGGER.info("Launching mask creation")
    mask_handler = mpr.MaskProcessor(mask_configuration)
    mask_handler.create_masks()

    LOGGER.info(f"Mask {output_file} has been created")


if __name__ == "__main__":
    # Argument parsing
    args = CLI().parse_args()
    print(args)

    parallel = Tasks(processes=args.nproc)
    sorted_dict_config = dict(
        sorted(
            JsonFile(Settings().mask_config_filename).load().items(),
            key=lambda ele: len(ele[1]["geos"]["features"]),
            reverse=True,
        )
    )
    for name, conf in sorted_dict_config.items():
        parallel.apply(main_function, task_name=name, args=(conf,))
    parallel.run(timeout=Settings().timeout)
