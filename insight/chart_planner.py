"""Chart planning utilities."""

from typing import List, Dict


def plan_charts(profile: Dict) -> List[Dict[str, object]]:
    """Generate chart specifications based on a profile description.

    Parameters
    ----------
    profile : dict
        Profile information about the dataset. Expected keys:

        ``categorical`` : list of categorical column names.
        ``numeric`` : list of numeric column names.
        ``datetime_index`` : bool indicating if the DataFrame index is datetime.

    Returns
    -------
    List[dict]
        A list of chart specification dictionaries. Each dictionary contains
        the chart ``type`` and the ``cols`` involved.
    """

    categorical = profile.get("categorical", []) or []
    numeric = profile.get("numeric", []) or []
    datetime_index = bool(profile.get("datetime_index"))

    charts: List[Dict[str, object]] = []

    # Datetime index with a single numeric column -> line chart
    if datetime_index and len(numeric) == 1:
        charts.append({"type": "line", "cols": numeric})
        return charts

    # Bar charts for categorical columns when count is small
    if len(categorical) <= 4:
        for col in categorical:
            charts.append({"type": "bar", "cols": [col]})

    # Histograms for numeric columns when there are many
    if len(numeric) > 4:
        for col in numeric:
            charts.append({"type": "hist", "cols": [col]})

    return charts

