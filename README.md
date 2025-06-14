# InsightPress

This project contains a placeholder CLI that simulates generating reports from a dataset.

## Docker Usage

1. **Build the image**

```bash
docker build -t insightpress .
```

2. **Prepare data**

Place your input file inside a `data/` directory relative to the repository. The compose file expects `input.csv` in this folder and writes results to `data/report`.

3. **Run the container**

```bash
docker-compose run --rm app
```

The command mounts the local `data/` folder inside the container at `/data`. Adjust the `command` in `docker-compose.yml` if your input or output paths differ.

You can also run the image directly:

```bash
docker run --rm -v $(pwd)/data:/data insightpress python -m insight /data/input.csv /data/report
```
