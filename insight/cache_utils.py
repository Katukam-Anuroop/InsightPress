import functools
import importlib.metadata
from joblib import Memory

# Shared joblib cache
memory = Memory('.cache', verbose=0)

# Packages whose versions we include in the cache key
DEFAULT_PACKAGES = [
    'numpy',
    'pandas',
    'matplotlib',
    'seaborn',
    'scipy',
    'statsmodels',
    'joblib',
]

def _library_versions(packages=DEFAULT_PACKAGES):
    """Return a tuple of (package, version) for hashing."""
    versions = []
    for pkg in packages:
        try:
            ver = importlib.metadata.version(pkg)
        except importlib.metadata.PackageNotFoundError:  # pragma: no cover - optional deps
            ver = None
        versions.append((pkg, ver))
    return tuple(versions)

def cache_with_versions(func):
    """Wrap function with joblib.Memory cache including library versions."""
    cached_func = memory.cache(func)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        kwargs['_lib_versions'] = _library_versions()
        return cached_func(*args, **kwargs)

    return wrapper


def clear_cache():
    """Remove all cached results."""
    memory.clear(warn=False)
