import typing
import collections.abc
import bpy.types

GenericType1 = typing.TypeVar("GenericType1")
GenericType2 = typing.TypeVar("GenericType2")

def preset_add(
    override_context: dict[str, typing.Any] | bpy.types.Context | None = None,
    execution_context: str | int | None = None,
    undo: bool | None = None,
    *,
    name: str | typing.Any = "",
    remove_name: bool | typing.Any | None = False,
    remove_active: bool | typing.Any | None = False,
):
    """Add or remove a Cloth Preset

    :type override_context: dict[str, typing.Any] | bpy.types.Context | None
    :type execution_context: str | int | None
    :type undo: bool | None
    :param name: Name, Name of the preset, used to make the path name
    :type name: str | typing.Any
    :param remove_name: remove_name
    :type remove_name: bool | typing.Any | None
    :param remove_active: remove_active
    :type remove_active: bool | typing.Any | None
    """

    ...
