import inspect
import joblib
from .parallel_tqdm import parallel_tqdm
from .no_context import no_context


def map(function, iterable, num_jobs=8, loading_bar=True, **kwargs):
    """
    Quite like functools.map, but works in parallel.
    Will show a loading bar using tqdm unless you pass loading_bar=False.
    You can pass extra arguments to tqdm using keyword arguments.
    """
    if num_jobs <= 0:
        raise ValueError("Number of jobs must be positive")
    arg_spec = inspect.getfullargspec(function)
    if (
        len(arg_spec.args) != 1
        or arg_spec.varargs is not None
        or arg_spec.varkw is not None
        or len(arg_spec.kwonlyargs) != 0
    ):
        raise ValueError("The function must take exactly one positional argument")
    context = (
        parallel_tqdm(iterable, tqdm_kwargs=kwargs) if loading_bar else no_context()
    )
    with context:
        pool = joblib.Parallel(n_jobs=num_jobs)
        return pool(joblib.delayed(function)(item) for item in iterable)
