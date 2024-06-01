"""Command-line script to generate manifest 0.

Usage:
    manifest_0.py --canonical-bucket=<cb> --manifest-out-path=<mop> 

Options:

--canonical-bucket=<cb>  S3 bucket to use to compute the statistics and to upload the manifest to.
--manifest-out-path=<mop>  Path in local file-system where to write the manifest.
"""

import json
from docopt import docopt
from time import strftime
import copy
from typing import Any

import dask.bag as db

from impresso_commons.utils.s3 import (
    upload,
)
from impresso_commons.path.path_s3 import fetch_files
from impresso_commons.versioning.data_statistics import (
    NewspaperStatistics,
)


# adapted from https://github.com/impresso/impresso-data-sanitycheck/blob/master/sanity_check/contents/stats.py#L241
def compute_canonical_stats_for_manifest(
    s3_canonical_issues: db.core.Bag,
) -> list[dict[str, Any]]:
    """Computes some statistics on issues and pages in provided issue files

    Args:
        s3_canonical_issues (db.core.Bag): Dask.bag containing the issues to compute
            the statistics on.

    Returns:
        list[dict[str, Any]]: Canonical statistics as a list of dicts.
    """

    print("Fetched all issues, gathering desired information.")
    pages_count_df = (
        s3_canonical_issues.map(
            lambda i: {
                "np_id": i["id"].split("-")[0],
                "year": i["id"].split("-")[1],
                "id": i["id"],
                "issue_id": i["id"],
                "n_pages": len(set(i["pp"])),
                "n_content_items": len(i["i"]),
                "n_images": len(
                    [item for item in i["i"] if item["m"]["tp"] == "image"]
                ),
            }
        )
        .to_dataframe(
            meta={
                "np_id": str,
                "year": str,
                "id": str,
                "issue_id": str,
                "n_pages": int,
                "n_images": int,
                "n_content_items": int,
            }
        )
        .set_index("id")
        .persist()
    )

    # cum the counts for all values collected
    aggregated_df = (
        pages_count_df.groupby(by=["np_id", "year"])
        .agg(
            {
                "n_pages": sum,
                "issue_id": "count",
                "n_content_items": sum,
                "n_images": sum,
            }
        )
        .rename(
            columns={
                "issue_id": "issues",
                "n_pages": "pages",
                "n_content_items": "content_items_out",
                "n_images": "images",
            }
        )
        .reset_index()
    )

    print("Finished grouping and aggregating by title and year.")
    # return as a list of dicts
    return aggregated_df.to_bag(format="dict").compute()


def pretty_print(np_stats: NewspaperStatistics) -> dict[str, Any]:
    stats_dict = {
        "stage": np_stats.format.value,
        "granularity": np_stats.granularity,
        "element": np_stats.element,
        "nps_stats": {k: v for k, v in np_stats.counts.items() if v > 0},
    }
    if stats_dict["granularity"] == "corpus":
        del stats_dict["element"]
    return stats_dict


def new_np_stats(stats: dict[str, int]) -> NewspaperStatistics:
    element = f"{stats['np_id']}-{stats['year']}"
    del stats["np_id"]
    del stats["year"]
    return NewspaperStatistics("canonical", "year", element, counts=stats)


def new_media(stats: dict[str, int], manifest_data: dict[str, Any]) -> dict[str, Any]:
    title = stats["np_id"]
    print(f"Creating new media dict for {title}.")
    new_media_stats = new_np_stats(stats)
    return {
        "media_title": title,
        "last_modification_date": manifest_data["mft_generation_date"],
        "update_type": None,
        "update_level": "title",
        "update_targets": [],
        "code_git_commit": None,
        "media_statistics": [new_media_stats],
    }


def aggregate_stats_for_title(title: str, media_dict: dict[str, Any]):
    print(f"Inside aggregate_stats_for_title for {title}.")
    # instantiate a NewspaperStatistics object for the title
    title_cumm_stats = NewspaperStatistics("canonical", "title", title)
    # instantiate the list of counts for display
    pretty_counts = []
    for np_year_stat in media_dict["media_statistics"]:
        # add the title yearly counts
        title_cumm_stats.add_counts(np_year_stat.counts)
        pretty_counts.append(pretty_print(np_year_stat))
    # insert the title-level statistics at the top of the statistics
    pretty_counts.insert(0, pretty_print(title_cumm_stats))
    media_dict["media_statistics"] = pretty_counts

    return media_dict, title_cumm_stats


def main():
    arguments = docopt(__doc__)
    s3_canonical_bucket = arguments["--canonical-bucket"]
    manifest_out_path = arguments["--manifest-out-path"]

    version = "v0.0.1"
    manifest_out_name = f"canonical_{version.replace('.','-')}.json"

    print(
        f"Generating manifest {manifest_out_name} using the s3 bucket {s3_canonical_bucket}."
    )

    manifest_data = {
        "mft_version": version,
        "mft_generation_date": strftime("%Y-%m-%d %H:%M:%S"),
        "mft_s3_path": f"s3://{s3_canonical_bucket}/{manifest_out_name}",
        "input_mft_s3_path": None,
        "input_mft_git_path": None,
        "code_git_commit": None,
        "media_list": [],
        "overall_statistics": [],
        "notes": f"Initial Manifest computed retroactively on the canonical data present in the bucket s3://{s3_canonical_bucket}.",
    }

    s3_canonical_issues, _ = fetch_files(s3_canonical_bucket, compute=False)

    canonical_stats = compute_canonical_stats_for_manifest(s3_canonical_issues)
    canonical_counts = copy.deepcopy(canonical_stats)

    print(
        "Finished gathering and aggregating all counts. Start populating the manifests."
    )

    # instantiate the media list with NewspaperStatistics ojects
    canonical_media_list = {}
    for d in canonical_counts:
        title = d["np_id"]
        if title in canonical_media_list:
            # if the title is already present in the media list, append new statistics
            canonical_media_list[title]["media_statistics"].append(new_np_stats(d))
        else:
            # if the title is not in the media list, initialize a new "media" object
            canonical_media_list[title] = new_media(d, manifest_data)

    # aggregate the statistics per title
    full_title_stats = []
    for title, media in canonical_media_list.items():
        media_dict, title_cumm_stats = aggregate_stats_for_title(title, media)
        # update the canonical_media_list with the new media_dict
        canonical_media_list[title] = media_dict
        # save the title level statistics for the overall statistics
        full_title_stats.append(title_cumm_stats)

    # set the final media list (only the values)
    manifest_data["media_list"] = list(canonical_media_list.values())

    print("Now computing the overall statistics")
    # compute the overall statistics
    corpus_stats = NewspaperStatistics("canonical", "corpus", "")
    for np_stats in full_title_stats:
        corpus_stats.add_counts(np_stats.counts)
    # add the number of titles present in corpus
    corpus_stats.add_counts({"titles": len(full_title_stats)})
    # set the final overall counts
    manifest_data["overall_statistics"] = [pretty_print(corpus_stats)]

    f_path = f"{manifest_out_path}/{manifest_out_name}"

    print(f"Finished creating the manifest. Writing to fs and S3: {f_path}.")

    with open(f_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, ensure_ascii=False, indent=4)

    # upload to s3
    upload(f_path, bucket_name=s3_canonical_bucket)


if __name__ == "__main__":
    main()
