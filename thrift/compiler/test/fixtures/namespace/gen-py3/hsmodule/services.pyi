#
# Autogenerated by Thrift
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#  @generated
#

import typing as _typing
from thrift.py3.server import RequestContext, ServiceInterface

import hsmodule.types as _hsmodule_types



class HsTestServiceInterface(
    ServiceInterface
):
    @_typing.overload
    async def init(
        self,
        ctx: RequestContext,
        int1: int
    ) -> int: ...

    async def init(
        self,
        int1: int
    ) -> int: ...

