from functools import wraps
from inspect import get_annotations


def strict(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        var_annotations = get_annotations(func)
        return_type = var_annotations.pop("return", None)
        for i, (var, var_type) in enumerate(var_annotations.items()):
            # Позиционные аргументы всегда идут первыми как в списке args, так и в сигнатуре.
            # Также учитывается что длина сигнатуры всегда равна длине args + kwargs
            if i < len(args):
                check_val = args[i]
            else:
                check_val = kwargs[var]

            if not isinstance(check_val, var_type):
                raise TypeError(f"Argument '{var}' expected type {var_type.__name__}, got {type(check_val).__name__}")

        out = func(*args, **kwargs)
        if return_type and not isinstance(out, return_type):
            raise TypeError(f"Return value expected type {return_type.__name__}, got {type(out).__name__}")
        return out

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


try:
    print(f"Result: {sum_two(b=1, a=2)}")
except TypeError:
    print("Test failed")
else:
    print("Test passed")

try:
    print(f"Result: {sum_two(1, 2.4)}")
except TypeError:
    print("Test passed")
else:
    print("Test failed")
