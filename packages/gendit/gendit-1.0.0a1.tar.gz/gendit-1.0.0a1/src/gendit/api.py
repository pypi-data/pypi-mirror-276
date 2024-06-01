import csv
import json
from typing import List, Callable

from gendit import core

AUTO=core.Format.AUTO
CSV=core.Format.CSV
JSON=core.Format.JSON


def generate_file(
    data_generator: Callable[[], dict],
    output: str, row: int,
    sorting: Callable[[List[dict]], List[dict]] | None = None,
    options: dict | None = None,
    format: str = AUTO
):
    """
    Generates a file from a data generator
    """
    if options is None:
        options = {}

    if format == core.Format.AUTO:
        format = core.detect_format(output)
        if format is None:
            raise ValueError(f"Output format detection failed for `{output}`, use format argument to specify the output format")

    if sorting is not None:
        generator = iter(sorting([data_generator() for _ in range(row)]))
    else:
        generator = (data_generator() for _ in range(row))

    if format == core.Format.CSV:
        with open(output, 'w') as filep:
            firstrow = next(generator)
            writer = csv.DictWriter(filep, fieldnames=firstrow.keys(), delimiter=options.get('delimiter', ','))
            if options.get('header', False):
                writer.writeheader()

            writer.writerow(firstrow)
            for i in range(row - 1):
                writer.writerow(next(generator))

    if format == core.Format.JSON:
        indent = options.get('indent', None)
        with open(output, 'w') as filep:
            json.dump([
                next(generator) for _ in range(row)
            ], filep, indent=indent)
