"""Command-line script to generate manifest 0.

Usage:
    rebuilt_manifest_0.py --output-bucekt=<ob> --temp-dir=<td> 

Options:

--output-bucekt=<ob>  Outout s3 bucket for the manifest.
--temp-dir=<td>  Path in local file-system where to write the manifest.
"""

import os
import json
import pandas as pd
import git
from dask import bag as db
from dask import dataframe as dd
from dask.distributed import Client
import numpy as np
from pathlib import Path
from time import strftime
import copy
from typing import Any
from docopt import docopt
from impresso_commons.utils.s3 import (
    fixed_s3fs_glob,
    alternative_read_text,
    upload,
    get_storage_options,
    get_boto3_bucket,
    IMPRESSO_STORAGEOPT,
)
from impresso_commons.versioning.helpers import (
    DataStage,
    read_manifest_from_s3,
    validate_stage,
    clone_git_repo,
    write_and_push_to_git,
    write_dump_to_fs,
)
from impresso_commons.path import parse_canonical_filename
from impresso_commons.path.path_fs import IssueDir
from impresso_commons.path.path_s3 import read_s3_issues, list_newspapers
from impresso_commons.versioning.data_statistics import (
    NewspaperStatistics,
    POSSIBLE_GRANULARITIES,
)
from impresso_commons.versioning.data_manifest import DataManifest
from collections import defaultdict


def chunk(s):
    """
    The function applied to the
    individual partition (map)
    """
    return s.apply(lambda x: list(set(x)))


def agg(s):
    """
    The function whic will aggrgate
    the result from all the partitions(reduce)
    """
    s = s._selected_obj
    return s.groupby(level=list(range(s.index.nlevels))).sum()


def finalize(s):
    """
    The optional functional that will be
    applied to the result of the agg_tu functions
    """
    return s.apply(lambda x: len(set(x)))


# aggregating function implementing np.nunique()
tunique = dd.Aggregation("tunique", chunk, agg, finalize)


def main():
    arguments = docopt(__doc__)
    mft_s3_output_bucket = arguments["--output-bucekt"]
    temp_dir = arguments["--temp-dir"]

    s3_rebuilt_bucket = "rebuilt-data"

    pycommons_repo = git.Repo("/home/piconti/impresso-pycommons")
    # bucket corresponding to the input data of the data currently in 'rebuilt-data'
    mft_s3_input_bucket = "canonical-data"

    rebuilt_mft_0 = DataManifest(
        data_stage="rebuilt",  # DataStage.REBUILT also works
        s3_output_bucket=mft_s3_output_bucket,
        s3_input_bucket=mft_s3_input_bucket,
        git_repo=pycommons_repo,
        temp_dir=temp_dir,
        staging=True,
    )

    client = Client(n_workers=16, threads_per_worker=2)
    print(client)

    print(f"Fetching the rebuilt files from the bucket s3://{s3_rebuilt_bucket}")

    rebuilt_files = fixed_s3fs_glob(os.path.join(s3_rebuilt_bucket, "*.jsonl.bz2"))

    print(f"Reading the contents of the {len(rebuilt_files)} fetched files...")
    # lazy object, to comput once reduced
    rebuilt_bag = db.read_text(rebuilt_files, storage_options=IMPRESSO_STORAGEOPT).map(
        json.loads
    )

    # for each rebuilt content-item, fetch the information necessary to compute the statistics we seek
    rebuilt_count_df = (
        rebuilt_bag.map(
            lambda ci: {
                "np_id": ci["id"].split("-")[0],
                "year": ci["id"].split("-")[1],
                "issue_id": "-".join(
                    ci["id"].split("-")[:-1]
                ),  # count the issues represented
                "n_content_items": 1,  # each element of the bag corresponds to one content-item
                "n_tokens": (
                    len(ci["ft"].split()) if "ft" in ci else 0
                ),  # split on spaces to count tokens
            }
        )
        .to_dataframe(
            meta={
                "np_id": str,
                "year": str,
                "issue_id": str,
                "n_content_items": int,
                "n_tokens": int,
            }
        )
        .persist()
    )

    # agggregate them at the scale of the entire corpus
    # first groupby title, year and issue to also count the individual issues present
    aggregated_df = (
        rebuilt_count_df
        # .groupby(by=['np_id', 'year', 'issue_id'])
        # .agg({'n_content_items': sum, 'n_tokens': sum})
        # .reset_index()
        # .groupby(by=['np_id', 'year'])
        # .agg({'issue_id': 'count', 'n_content_items': sum, 'n_tokens': sum})
        .groupby(by=["np_id", "year"])
        .agg({"issue_id": tunique, "n_content_items": sum, "n_tokens": sum})
        .rename(
            columns={
                "issue_id": "issues",
                "n_content_items": "content_items_out",
                "n_tokens": "ft_tokens",
            }
        )
        .reset_index()
    )

    print("Obtaining the yearly rebuilt statistics for the entire corpus")
    # return as a list of dicts
    stats_as_dict = aggregated_df.to_bag(format="dict").compute()

    rebuilt_stats = copy.deepcopy(stats_as_dict)

    print("Populating the manifest with the resulting yearly statistics...")
    # populate the manifest with these statistics
    for stats in rebuilt_stats:
        title = stats["np_id"]
        year = stats["year"]
        del stats["np_id"]
        del stats["year"]
        rebuilt_mft_0.add_by_title_year(title, year, stats)

    print("Finalizing the manifest, and computing the result...")

    note = f"Initial Manifest computed retroactively on the rebuilt data present in the bucket s3://{s3_rebuilt_bucket}."
    rebuilt_mft_0.append_to_notes(note)
    rebuilt_mft_0.compute(export_to_git_and_s3=False)
    rebuilt_mft_0.validate_and_export_manifest(push_to_git=False)


if __name__ == "__main__":
    main()
