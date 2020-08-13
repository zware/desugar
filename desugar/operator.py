"""A pure Python implementation of the operator module that pertains to syntax.

1. `a + b` ➠ `operator.add(a, b)`
2. `a - b` ➠ `operator.sub(a, b)`
3. `a * b` ➠ `operator.mul(a, b)`
4. `a @ b` ➠ `operator.matmul(a, b)`
5. `a / b` ➠ `operator.truediv(a, b)`
6. `a // b` ➠ `operator.floordiv(a, b)`
7. `a % b` ➠ `operator.mod(a, b)`
8. `a ** b` ➠ `operator.pow(a, b)`
9. `a << b` ➠ `operator.lshift(a, b)`
10. `a >> b` ➠ `operator.rshift(a, b)`
11. `a & b` ➠ `operator.and_(a, b)`
12. `a ^ b` ➠ `operator.xor(a, b)`
13. `a | b` ➠ `operator.or_(a, b)`

"""
# https://docs.python.org/3.8/reference/datamodel.html#emulating-numeric-types
# https://docs.python.org/3.8/library/operator.html#mapping-operators-to-functions
# https://docs.python.org/3.8/library/operator.html#in-place-operators
from __future__ import annotations

import typing
from typing import Callable

from . import builtins as debuiltins

if typing.TYPE_CHECKING:
    from typing import Any


def _create_binary_op(name: str, operator: str) -> Callable[[Any, Any], Any]:
    """Create a binary operation function.

    The `name` parameter specifies the name of the special method used for the
    binary operation (e.g. `sub` for `__sub__`). The `operator` name is the
    token representing the binary operation (e.g. `-` for subtraction).

    """

    def binary_op(lhs: Any, rhs: Any, /) -> Any:
        """A closure implementing a binary operation in Python."""
        rhs_type = type(rhs)
        lhs_type = type(lhs)
        if rhs_type is not lhs_type and issubclass(rhs_type, lhs_type):
            call_first = (rhs, rhs_type), f"__r{name}__", lhs
            call_second = (lhs, lhs_type), f"__{name}__", rhs
        else:
            call_first = (lhs, lhs_type), f"__{name}__", rhs
            call_second = (rhs, rhs_type), f"__r{name}__", lhs

        for first, meth, second_obj in (call_first, call_second):
            first_obj, first_type = first
            try:
                meth = debuiltins._mro_getattr(first_type, meth)
            except AttributeError:
                continue
            value = meth(first_obj, second_obj)
            if value is not NotImplemented:
                return value
        else:
            raise TypeError(
                f"unsupported operand type(s) for {operator}: {lhs_type!r} and {rhs_type!r}"
            )

    binary_op.__name__ = binary_op.__qualname__ = name
    binary_op.__doc__ = f"""Implement the binary operation `a {operator} b`."""
    return binary_op


add = __add__ = _create_binary_op("add", "+")
sub = __sub__ = _create_binary_op("sub", "-")
mul = __mul__ = _create_binary_op("mul", "*")
matmul = __matmul__ = _create_binary_op("matmul", "@")
truediv = __truediv__ = _create_binary_op("truediv", "/")
floordiv = __floordiv__ = _create_binary_op("floordiv", "//")
mod = __mod__ = _create_binary_op("mod", "%")
pow = __pow__ = _create_binary_op("pow", "**")
lshift = __lshift__ = _create_binary_op("lshift", "<<")
rshift = __rshift__ = _create_binary_op("rshift", ">>")
and_ = __and__ = _create_binary_op("and", "&")
xor = __xor__ = _create_binary_op("xor", "^")
or_ = __or__ = _create_binary_op("or", "|")
