from .params import GraphObject, Function
from .param_impl import capture_kwargs


def isnamedtupleinstance(x):
    t = type(x)
    b = t.__bases__
    if len(b) != 1 or b[0] != tuple:
        return False
    f = getattr(t, "_fields", None)
    if not isinstance(f, tuple):
        return False
    return all(type(n) == str for n in f)


def _is_supported_container(in_obj):
    if isnamedtupleinstance(in_obj):
        return True
    if isinstance(in_obj, dict):
        return True
    return False


def expand_nested_graphobjs(in_obj, is_root=True):
    isnt = isnamedtupleinstance(in_obj)
    orig_class = in_obj.__class__

    if isnt:
        in_obj = in_obj._asdict()

        def capture_nt(*args, **kwargs):
            return orig_class(**kwargs)

        capture_func = capture_nt

    else:
        capture_func = capture_kwargs

    out_obj = {}
    has_go = False
    for k, v in in_obj.items():
        if _is_supported_container(v):
            out_obj[k], _sub_has_go = expand_nested_graphobjs(v, False)  # type: ignore
            if _sub_has_go:
                has_go = True
        else:
            out_obj[k] = v
            if isinstance(v, GraphObject):
                has_go = True

    out_kwargs = out_obj
    if isnt:
        out_obj = orig_class(**out_obj)

    if has_go:
        if is_root:
            return Function(capture_func, kwargs=out_kwargs)
        else:
            return Function(capture_func, kwargs=out_kwargs), has_go
    else:
        if is_root:
            return out_obj
        else:
            return out_obj, has_go
