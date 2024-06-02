"""pyoload

pyoload is a little python script to incorporate some features of
annotation and typechecking in python.

"""
from typing import Any, GenericAlias, Callable
from types import UnionType
from functools import wraps, partial
from inspect import isclass

import sys


class AnnotationError(ValueError):
    """class AnnotationError(ValueError)
    base exception for most pyoload errors
    """


class AnnotationErrors(AnnotationError):
    """class AnnotationErrors(AnnotationError)
    Hosts a list of AnnotationError
    """


class InternalAnnotationError(Exception):
    """class InternalAnnotationError(Exception)
    **internam**
    raised by overloads on type mismatch
    """


class CastingError(TypeError):
    """class CastingError(TypeError)
    Error during casting
    """


class OverloadError(TypeError):
    """class OverloadError(TypeError)
    Error in or during overload
    """


class AnnotationResolutionError(AnnotationError):
    """class AnnotationResolutionError(AnnotationError)
    Annotations could not be resolved or evaluated.
    """
    _raise = False


class PyoloadAnnotation:
    """class PyoloadAnnotation
    A parent class for pyoload extra annotations
    """


class Values(PyoloadAnnotation, tuple):
    """class Values(PyoloadAnnotation, tuple)
    A tuple subclass which holds several values as possible annotations
    """

    def __call__(self: 'Values', val: Any) -> bool:
        """def __call__(self, val)
        :param self: the `Values` object
        :param val: the value to be checked

        :returns: if the value `val` is contained in `self`
        """
        return val in self

    def __str__(self):
        return 'Values(' + ', '.join(map(repr, self)) + ')'

    __repr__ = __str__


def get_name(funcOrCls: Any):
    """def get_name(funcOrCls: Any)
    Gives a class or function name, possibly unique gotten from
    it's module name and qualifier name
    """
    return funcOrCls.__module__ + '.' + funcOrCls.__qualname__


class Check:
    """class Check
    A class basicly abstract which holds registerred checks in pyoload
    """
    checks_list = {}

    def __init_subclass__(cls: Any, subclass: Any):
        """def __init_subclass__(cls, subclass)
        register's subclasses as chexks
        """
        cls.register(cls.name, cls.__call__)

    @classmethod
    def register(cls: Any, name: str) -> Any:
        """def register(cls, name)
        returns a callable which registers a new checker mathod
        :param cls: the Check class
        :param name: the name to be registerred as
        """
        if name in cls.checks_list:
            raise Check.CheckNameAlreadyExistsError(name)

        def inner(func: Callable) -> Callable:
            """def inner(func: Callable)
            :param func: The callable to register

            :returns: func
            """
            cls.checks_list[name] = func
            return func
        return inner

    @classmethod
    def check(cls: Any, name: str, params: Any, val: Any) -> None:
        """def check(cls: Any, name: str, params: Any, val: Any)
        Performs the specified check with the specified params on
        the specified value
        :param cls: pyoload.Check class
        :param name: The registerred name of the check
        :param params: The parameters to pass to the check
        :param val: The value to check
        """
        check = cls.checks_list.get(name)
        if check is None:
            raise Check.CheckDoesNotExistError(name)
        check(params, val)

    class CheckNameAlreadyExistsError(ValueError):
        """class CheckNameAlreadyExistsError(ValueError)
        The check name to be registerred already exists
        """

    class CheckDoesNotExistError(ValueError):
        """class CheckDoesNotExistError(ValueError)
        The specified check does not exist
        """

    class CheckError(Exception):
        """class CheckError(Exception)
        Error occurring during check call.
        """


@Check.register('len')
def len_check(params, val):
    if isinstance(params, int):
        if not len(val) == params:
            raise Check.CheckError(f'length of {val!r} not eq {params!r}')
    elif isinstance(params, tuple) and len(params) > 0:
        mi = ma = None
        mi, ma = params
        if mi is not None:
            if not len(val) > mi:
                raise Check.CheckError(f'length of {val!r} not gt {mi!r}')
        if ma is not None:
            if not len(val) < ma:
                raise Check.CheckError(f'length of {val!r} not lt {mi!r}')


@Check.register('lt')
def lt_check(param, val):
    if not val < param:
        raise Check.CheckError(f'{val!r} not lt {param!r}')


@Check.register('le')
def le_check(param, val):
    if not val <= param:
        raise Check.CheckError(f'{val!r} not gt {param!r}')


@Check.register('ge')
def ge_check(param, val):
    if not val >= param:
        raise Check.CheckError(f'{val!r} not ge {param!r}')


@Check.register('gt')
def gt_check(param, val):
    if not val > param:
        raise Check.CheckError(f'{val!r} not gt {param!r}')


@Check.register('eq')
def eq_check(param, val):
    if not val == param:
        raise Check.CheckError(f'{val!r} not eq {param!r}')


@Check.register('func')
def func_check(param, val):
    if not param(val):
        raise Check.CheckError(f'{param!r} call returned false on {val!r}')


@Check.register('type')
def matches_check(param, val):
    if not typeMatch(val, param):
        raise Check.CheckError(f'{val!r} foes not match type {param!r}')


@Check.register('isinstance')
def instance_check(param, val):
    if not isinstance(val, param):
        raise Check.CheckError(f'{val!r} not instance of {param!r}')


class Checks(PyoloadAnnotation):
    """class Checks(Annotation)
    Pyoload annotation holding several checks
    """

    def __init__(self: PyoloadAnnotation, **checks):
        """def __init__(self: PyoloadAnnotation, **checks)
        crates the check object,e.g

        class foo:
            bar = pyoload.Checks(gt=4)
        """
        self.checks = checks

    def __call__(self: PyoloadAnnotation, val: Any) -> None:
        """def __call__(self: PyoloadAnnotation, val: Any) -> None
        Performs the several checks contained in `self.checks`
        """
        for name, params in self.checks.items():
            Check.check(name, params, val)

    def __str__(self: Any) -> str:
        ret = '<Checks('
        for k, v in self.checks.items():
            ret += f'{k}={v!r}, '
        ret = ret[:-2] + ')>'
        return ret

    __repr__ = __str__


class CheckedAttr(Checks):
    """class CheckedAttr(Checks)
    A descriptor class providing attributes which are checked on assignment
    """

    name: str
    value: Any

    def __set_name__(self: Any, obj: Any, name: str, typo: Any = None):
        """def __set_name__(self: Any, obj: Any, name: str, typo: Any = None)
        setd the name of the attribute
        """
        self.name = name
        self.value = None

    def __get__(self: Any, obj: Any, type: Any):
        """def __get__(self: Any, obj: Any, type: Any)
        returns the value in `self.value`
        """
        return self.value

    def __set__(self: Any, obj: Any, value: Any):
        """def __set__(self: Any, obj: Any, value: Any)
        Performs checks then assigns the new value
        """
        self(value)
        self.value = value


class Cast(PyoloadAnnotation):
    """class Cast(PyoloadAnnotation)
    Holds a cast object which describes the casts to be performed
    """
    @staticmethod
    def cast(val: Any, totype: Any) -> Any:
        """def cast(val: Any, totype: Any) -> Any
        The gratest deal.
        Recursively casts the given value to the specified structure or type
        e.g
        Cast.cast({ 1: 2}, dict[str, float])

        returns: {'1': 2.0}
        """
        if isinstance(totype, GenericAlias):
            if totype.__origin__ == dict:
                if len(totype.__args__) == 2:
                    kt, vt = totype.__args__
                elif len(totype.__args__) == 1:
                    kt, vt = Any, totype.__args__[1]
                return {
                    Cast.cast(k, kt): Cast.cast(v, vt) for k, v in val.items()
                }
            else:
                sub = totype.__args__[0]
                return totype.__origin__([
                    Cast.cast(v, sub) for v in val
                ])
        if isinstance(totype, UnionType):
            errors = []
            for subtype in totype.__args__:
                try:
                    return Cast.cast(val, subtype)
                except Exception as e:
                    errors.append(e)
            else:
                raise errors
        else:
            return totype(val) if not isinstance(val, totype) else val

    def __init__(self: PyoloadAnnotation, type: Any):
        """
        creates a casting object for the specified type
        """
        self.type = type

    def __call__(self: PyoloadAnnotation, val: Any):
        """
        Calls to the type specified in the object `.type` attribute
        :param self: The cast onject
        :param val: the value to be casted

        :return: The casted value
        """
        try:
            return Cast.cast(val, self.type)
        except Exception as e:
            raise CastingError(
                f'Exception({e}) while casting: {val!r} to {self.type}',
            ) from e

    def __str__(self):
        return f'pyoload.Cast({self.type!s})'


class CastedAttr(Cast):
    """class CastedAttr(Cast)
    A descriptor class providing attributes which are checked on assignment
    """

    name: str
    value: Any

    def __set_name__(self: Any, obj: Any, name: str, typo: Any = None):
        """def __set_name__(self: Any, obj: Any, name: str, typo: Any = None)
        setd the name of the attribute
        """
        self.name = name
        self.value = None

    def __get__(self: Any, obj: Any, type: Any):
        """def __get__(self: Any, obj: Any, type: Any)
        returns the value in `self.value`
        """
        return self.value

    def __set__(self: Any, obj: Any, value: Any):
        """def __set__(self: Any, obj: Any, value: Any)
        Performs checks then assigns the new value
        """
        self.value = self(value)


def typeMatch(val: Any, spec: type) -> bool:
    """
    recursively checks if type matches
    :param val: The value to typecheck
    :param spec: The type specifier

    :return: A boolean
    """
    if spec == any:
        raise TypeError('May be have you confused `Any` and `any`')

    if spec == Any or spec is None or val is None:
        return True
    if isinstance(spec, Values):
        return spec(val)
    elif isinstance(spec, Checks):
        try:
            spec(val)
        except Check.CheckError:
            return False
        else:
            return True
    elif isinstance(spec, GenericAlias):
        if not isinstance(val, spec.__origin__):
            return False

        if spec.__origin__ == dict:
            if len(spec.__args__) == 2:
                kt, vt = spec.__args__
            elif len(spec.__args__) == 1:
                kt, vt = Any, spec.__args__[1]
            else:
                return True

            for k, v in val.items():
                if not typeMatch(k, kt) or not typeMatch(v, vt):
                    return False
            else:
                return True
        else:
            sub = spec.__args__[0]
            for val in val:
                if not typeMatch(val, sub):
                    return False
            else:
                return True
    else:
        return isinstance(val, spec)


def get_module(obj: Any):
    """
    gets the module to which an object, function or class belongs
    :param obj: the object
    :returns: the module
    """
    return sys.modules[obj.__module__]


def resolveAnnotations(obj: Any) -> None:
    """
    Evaluates all the stringized annotations of the argument

    :param obj: The object
    :returns: None
    """
    if isclass(obj) or hasattr(obj, '__class__'):
        for k, v in obj.__annotations__.items():
            if isinstance(v, str):
                try:
                    obj.__annotations__[k] = eval(
                        v,
                        dict(vars(get_module(obj))), dict(vars(obj)),
                    )
                except Exception as e:
                    raise AnnotationResolutionError(
                        (
                            f'Exception: {e!s} while resolving'
                            f' annotation {e}={v!r} of object {obj!r}'
                        ),
                    ) from e
    elif callable(obj):
        for k, v in obj.__annotations__.items():
            if isinstance(v, str):
                try:
                    obj.__annotations__[k] = eval(v, obj.__globals__)
                except Exception as e:
                    raise AnnotationResolutionError(
                        f'Exception: {k!s} while resolving'
                        f' annotation {v!r} of function {obj!r}',
                        f'globals: {obj.__globals__}',
                    ) from e
    else:
        raise AnnotationError(f'unknown resolution method for {obj}')


def annotate(func: Callable, oload: bool = False) -> Callable:
    """
    returns a wrapper over the passed function
    which typechecks arguments on each call
    :param func: the function to annotate
    :param oload: internal

    :returns: the wrapper function
    """
    if isclass(func):
        return annotateClass(func)
    if len(func.__annotations__) == 0:
        raise Warning(f'function {get_name(func)} is not annotated')
        return func

    @wraps(func)
    def wrapper(*args, **kw):
        i = 0
        while str in map(type, func.__annotations__.values()) and i < 10:
            resolveAnnotations(func)
            i += 1
        else:
            if i == 10:
                raise AnnotationResolutionError(func.__annotations__)
        anno = func.__annotations__.copy()
        if 'return' in anno:
            anno.pop('return')
        names = list(anno.keys())
        vals = {}
        try:
            if func.__defaults__:
                for i, v in enumerate(reversed(func.__defaults__)):
                    vals[names[-1 - i]] = v
            for i, v in enumerate(args):
                vals[names[i]] = v
            vals.update(kw)
        except IndexError as e:
            raise AnnotationError(
                f'Was function {get_name(func)} properly annotated?, has'
                f' {len(anno)} annotations but {len(args)} arguments passed',
            ) from e

        errors = []
        for k, v in vals.items():
            if isinstance(anno[k], Cast):
                vals[k] = anno[k](v)
                continue
            if not typeMatch(v, anno[k]):
                if oload:
                    raise InternalAnnotationError()
                errors.append(
                    AnnotationError(
                        f'Value: {v!r} does not match annotation: {anno[k]!r}'
                        f' for argument {k!r} of function {get_name(func)}',
                    ),
                )
        if len(errors) > 0:
            raise AnnotationErrors(errors)

        ret = func(**vals)
        if 'return' in func.__annotations__:
            ann = func.__annotations__['return']
            if not typeMatch(ret, ann):
                raise AnnotationError(
                    f'return value {ret!r} does not match annotation: '
                    f'{ann} of function {get_name(func)}',
                )
        return ret
    wrapper.__pyod_annotate__ = func
    return wrapper


__overloads__: dict[str, list[Callable]] = {}


def overload(func: callable, name: str | None = None):
    """
    returns a wrapper over the passed function
    which typechecks arguments on each call
    and finds the function instance with same name which does not raise
    an `InternalAnnotationError` exception
    :param func: the function to annotate
    :param oload: internal

    :return: the wrapper function
    """
    if isinstance(func, str):
        return partial(overload, name=func)
    if name is None or not isinstance(name, str):
        name = get_name(func)
    if name not in __overloads__:
        __overloads__[name] = []
    __overloads__[name].append(annotate(func, True))

    @wraps(func)
    def wrapper(*args, **kw):
        for f in __overloads__[name]:
            try:
                val = f(*args, **kw)
            except InternalAnnotationError:
                continue
            else:
                break
        else:
            raise OverloadError(
                f'No overload of function: {get_name(func)}'
                f' matches types of arguments: {args}, {kw}',
            )
        return val

    wrapper.__pyod_overloads__ = __overloads__[name]
    wrapper.__pyod_overloads_name__ = name
    wrapper.overload = partial(overload, name=name)

    return wrapper


def annotateClass(cls):
    """
    Annotates a class object, wrapping and replacing over it's __setattr__
    and typechecking over each attribute assignment.
    If no annotation for the passed object found it sets it to `type(val)`
    """
    if not hasattr(cls, '__annotations__'):
        cls.__annotations__ = {}
    if isinstance(cls, bool):
        return partial(annotate, recur=cls)
    recur = not hasattr(cls, '__annotate_norecur__')
    setter = cls.__setattr__
    if recur:
        for x in dir(cls):
            if hasattr(getattr(cls, x), '__annotations__'):
                setattr(
                    cls,
                    x,
                    annotate(
                        getattr(
                            cls,
                            x,
                        ),
                    ),
                )

    @wraps(cls.__setattr__)
    def new_setter(self: Any, name: str, value: Any) -> Any:
        """def new_setter(self: Any, name: str, value: Any) -> Any
        """
        if any(isinstance(x, str) for x in self.__annotations__.values()):
            resolveAnnotations(self)

        if name not in self.__annotations__:
            if value is not None:
                self.__annotations__[name] = type(value)
        elif isinstance(self.__annotations__[name], Cast):
            return setter(self, name, self.__annotations__[name](value))
        elif not typeMatch(value, self.__annotations__[name]):
            raise AnnotationError(
                f'value {value!r} does not match annotation'
                f'of attribute: {name!r}:{self.__annotations__[name]!r}'
                f' of object of class {get_name(cls)}',
            )
        return setter(self, name, value)
    cls.__setattr__ = new_setter
    return cls


__version__ = '1.1.1'
__author__ = 'ken-morel'
