class no_vnodes(object):
    def __call__(self, f):
        def wrapped(obj):
            if ENABLE_VNODES:
                obj.skip("Test disabled for vnodes")
            f(obj)
        wrapped.__name__ = f.__name__
        wrapped.__doc__ = f.__doc__
        return wrapped
