import os
import json

try:
    import openai
except ImportError as exc:
    raise ImportError("openai package is required to use write_narrative") from exc


def write_narrative(profile, chart_paths, forecast_path):
    """Generate a short markdown narrative from a dataset profile and figures.

    Parameters
    ----------
    profile : dict
        Summary of the dataset profile, will be serialized to JSON.
    chart_paths : list of str
        Paths to generated chart images.
    forecast_path : str
        Path to the forecast figure image.

    Returns
    -------
    str
        Narrative in markdown format limited to three paragraphs.
    """

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY not set")

    openai.api_key = api_key

    system_prompt = "You are a data analyst..."
    payload = json.dumps({
        "profile": profile,
        "figures": chart_paths + ([forecast_path] if forecast_path else [])
    })

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": payload},
        ],
    )

    text = response["choices"][0]["message"]["content"].strip()
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    return "\n\n".join(paragraphs[:3])

