"""
Module for loading data from a yaml file and testing it. The yaml file should contain a list of dictionaries, each
containing the following keys:
- notebook: str
    Name of the notebook.
- metadata: dict
    Metadata for the map.
- path_save: str
    Path to save the map.
- zoom: int
    Zoom level for the map.
- queries: dict
    Dictionary of queries to be executed.

Types of queries accepted as part of the list:
- polygons
    - latlons: list
        List of latlons for the polygon. (example: `55.6, -3.5, 56, -2.8`)
    - modes: list
        List of modes for the polygon. (example: `within` and `intersects`)
- coordinates: list. Provided as a list of coordinates. (example: `-4.5, 55.4`)
- lines: dict
- wfs_ids: list
- string: list

Example of a yaml file:
```yaml
- notebook: path/to/notebook.ipynb
  metadata: path/to/metadata.json
  path_save: maps
  zoom: 14
  queries:
    coordinates:
      - -4.33, 55.90
      - -3.25, 51.93
- notebook: path/to/notebook2.ipynb
  metadata: path/to/metadata.json
  path_save: maps
  zoom: 14
  queries:
    polygons:
      latlons:
        - 55.6, -3.5, 56, -2.8
      modes:
        - within
        - intersects
    coordinates:
      - -4.5, 55.4
    lines:
      latlons:
        - xy1: 56.5, -5
          xy2: 57.0, -4.5
    wfs_ids:
      - 12
      - 30
      - 37
      - 38
    string:
      - literal: "Stirling"
      - property: IMAGEURL
        literal: 74487492
"""

from yaml import load
import ast
import mapreader
from pathlib import Path

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


AUTO_PATH_SAVE = "maps"  # Automatic path for downloading maps
AUTO_ADD_NOTEBOOK = (
    True  # Automatically add notebook name before map download directory
)
VERBOSE = False


def load_data(file):
    """
    Load data from a yaml file and return it as a list of dictionaries.

    Parameters
    ----------
    file : str
        Path to the yaml file.

    Returns
    -------
    list
        List of dictionaries containing the data from the yaml file.
    """
    with open(file) as f:
        data = load(f, Loader=Loader)

    # Clear out duplicate queries
    data = list(set([str(d) for d in data]))
    data = [ast.literal_eval(d) for d in data]

    return data


def test_data(data, verbose=False):
    """
    Test the data loaded from the yaml file.

    Parameters
    ----------
    data : list
        List of dictionaries containing the data from the yaml file.
    verbose : bool, optional
        If True, print warnings and errors. Default is False.

    Returns
    -------
    tuple
        Tuple containing lists of notebooks without metadata, path_save and zoom keys.
    """
    if len([dic for dic in data if not "notebook" in dic.keys()]):
        print(
            "Fatal error: Some entries in download-examples.yaml file do not have a 'notebook' key. Please fix this."
        )
        exit(1)

    notebooks_without_metadata = [
        dic["notebook"] for dic in data if not "metadata" in dic.keys()
    ]
    if len(notebooks_without_metadata) and verbose:
        print(
            f"Error: {len(notebooks_without_metadata)} entries in download-examples.yaml file do not have a 'metadata' key. They will not be processed:"
        )
        print("- " + "\n- ".join(notebooks_without_metadata))

    notebooks_without_path_save = [
        dic["notebook"] for dic in data if not "path_save" in dic.keys()
    ]
    if len(notebooks_without_path_save) and verbose:
        print(
            f"Warning: {len(notebooks_without_path_save)} entries in download-examples.yaml file do not have a 'path_save' key. They will be saved in the automatic directory ({AUTO_PATH_SAVE}):"
        )
        print("- " + "\n- ".join(notebooks_without_path_save))

    notebooks_without_zoom = [
        dic["notebook"] for dic in data if not "zoom" in dic.keys()
    ]
    if len(notebooks_without_zoom) and verbose:
        print(
            f"Warning: {len(notebooks_without_zoom)} entries in download-examples.yaml file do not have a 'zoom' key. They will be saved with MapReader's predefined zoom value:"
        )
        print("- " + "\n- ".join(notebooks_without_zoom))

    return (
        notebooks_without_metadata,
        notebooks_without_path_save,
        notebooks_without_zoom,
    )


data = load_data("download-examples.yaml")
(
    notebooks_without_metadata,
    notebooks_without_path_save,
    notebooks_without_zoom,
) = test_data(data, verbose=VERBOSE)

# Check for missing notebooks in YAML file
missing_notebooks = set([str(x) for x in Path("notebooks").glob("**/*.ipynb")]) - set([x["notebook"] for x in data])
if len(missing_notebooks):
    print("Warning: There are notebooks in the examples that are not defined in the download-examples.yaml file:")
    print("\n".join(missing_notebooks))

for d in data:
    # Skip any notebooks that does not have metadata
    if d["notebook"] in notebooks_without_metadata:
        print(f'Skipping {d["notebook"]}...') if VERBOSE else None
        continue

    # Set up SheetDownloader for the notebook
    q = mapreader.SheetDownloader(
        metadata_path=d["metadata"],
        download_url=d["url"],
    )

    # Add queries to the SheetDownloader object
    if "coordinates" in d["queries"]:
        coordinates = d["queries"]["coordinates"]
        for coords in coordinates:
            coords = ast.literal_eval(coords)
            q.query_map_sheets_by_coordinates(coords, append=True)

    if "wfs_ids" in d["queries"]:
        wfs_ids = d["queries"]["wfs_ids"]
        q.query_map_sheets_by_wfs_ids(wfs_ids)

    if "polygons" in d["queries"]:
        polygons_latlons = d["queries"]["polygons"]["latlons"]
        polygons_modes = d["queries"]["polygons"]["modes"]

        for latlon in polygons_latlons:
            latlon = tuple(latlon.split(", "))
            for mode in polygons_modes:
                poly = mapreader.create_polygon_from_latlons(*latlon)
                q.query_map_sheets_by_polygon(poly, mode, append=True)

    if "lines" in d["queries"]:
        lines = d["queries"]["lines"]
        for latlon in lines["latlons"]:
            xy1 = tuple(latlon["xy1"].split(", "))
            xy2 = tuple(latlon["xy2"].split(", "))
            line = mapreader.create_line_from_latlons(xy1, xy2)
            q.query_map_sheets_by_line(line, append=True)

    if "string" in d["queries"]:
        for string in d["queries"]["string"]:
            if "property" in string:
                property = str(string["property"])
                literal = str(string["literal"])
            else:
                property = None
                literal = str(string["literal"])

            if property:
                keys = ["properties", property]
                q.query_map_sheets_by_string(literal, keys=keys, append=True)
            else:
                q.query_map_sheets_by_string(literal, append=True)

    # Set zoom
    if d.get("zoom"):
        q.get_grid_bb(d["zoom"])
    else:
        q.get_grid_bb()

    if q.found_queries:
        # Print out any queries found if we have verbosity on
        print(q.print_found_queries()) if VERBOSE else None

        # Download all maps into the correct path
        path_save = d.get("path_save", AUTO_PATH_SAVE)
        if d.get("path_add_notebook") or AUTO_ADD_NOTEBOOK:
            # If the name of the notebook is "pipeline", we want to use the parent directory name
            stem = Path(d["notebook"]).stem
            if stem.lower() == "pipeline":
                stem = Path(d["notebook"]).parent.stem

            path_save = f"{path_save}/{stem}"

        q.download_map_sheets_by_queries(path_save=path_save)
