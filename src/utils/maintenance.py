import functools


def deprecated(message):
    """ This is a decorator which can be used to mark functions as deprecated. It will result in a
        warning being emmitted when the function is used.
        https://stackoverflow.com/questions/2536307/decorators-in-the-python-standard-lib-deprecated-specifically

        # Examples

        @deprecated
        def some_old_function(x,y):
            return x + y

        class SomeClass:
            @deprecated
            def some_old_method(self, x,y):
                return x + y
    """
    def decorator(func):
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            print("WARNING: Call to deprecated function '{}'. {}".format(func.__name__, message))
            return func(*args, **kwargs)
        return new_func

    return decorator
