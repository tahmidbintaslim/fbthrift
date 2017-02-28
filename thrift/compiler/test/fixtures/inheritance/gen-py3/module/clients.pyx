#
# Autogenerated by Thrift
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#  @generated
#
from libcpp.memory cimport shared_ptr, make_shared, unique_ptr, make_unique
from libcpp.string cimport string
from libcpp cimport bool as cbool
from cpython cimport bool as pbool
from libc.stdint cimport int8_t, int16_t, int32_t, int64_t
from libcpp.vector cimport vector as vector
from libcpp.set cimport set as cset
from libcpp.map cimport map as cmap
from cython.operator cimport dereference as deref
from cpython.ref cimport PyObject
from thrift.py3.client cimport EventBase, make_py3_client, py3_get_exception
from thrift.py3.client import get_event_base
from thrift.py3.folly cimport cFollyEventBase, cFollyTry, cFollyUnit, c_unit

import asyncio
import sys
import traceback

cimport module.types
import module.types

from module.clients_wrapper cimport move

from module.clients_wrapper cimport cMyRootAsyncClient, cMyRootClientWrapper
from module.clients_wrapper cimport cMyNodeAsyncClient, cMyNodeClientWrapper
from module.clients_wrapper cimport cMyLeafAsyncClient, cMyLeafClientWrapper


cdef void MyRoot_do_root_callback(
        PyObject* future,
        cFollyTry[cFollyUnit] result) with gil:
    cdef object pyfuture = <object> future
    cdef cFollyUnit citem
    if result.hasException():
        try:
            result.exception().throwException()
        except:
            pyfuture.loop.call_soon_threadsafe(pyfuture.set_exception, sys.exc_info()[1])
    else:
        citem = c_unit;
        pyfuture.loop.call_soon_threadsafe(pyfuture.set_result, None)

cdef void MyNode_do_mid_callback(
        PyObject* future,
        cFollyTry[cFollyUnit] result) with gil:
    cdef object pyfuture = <object> future
    cdef cFollyUnit citem
    if result.hasException():
        try:
            result.exception().throwException()
        except:
            pyfuture.loop.call_soon_threadsafe(pyfuture.set_exception, sys.exc_info()[1])
    else:
        citem = c_unit;
        pyfuture.loop.call_soon_threadsafe(pyfuture.set_result, None)

cdef void MyLeaf_do_leaf_callback(
        PyObject* future,
        cFollyTry[cFollyUnit] result) with gil:
    cdef object pyfuture = <object> future
    cdef cFollyUnit citem
    if result.hasException():
        try:
            result.exception().throwException()
        except:
            pyfuture.loop.call_soon_threadsafe(pyfuture.set_exception, sys.exc_info()[1])
    else:
        citem = c_unit;
        pyfuture.loop.call_soon_threadsafe(pyfuture.set_result, None)


cdef class MyRoot:

    def __init__(self, *args, **kwds):
        raise TypeError('Use MyRoot.connect() instead.')

    def __cinit__(self, loop):
        self.loop = loop

    @staticmethod
    cdef _module_MyRoot_set_client(MyRoot inst, shared_ptr[cMyRootClientWrapper] c_obj):
        """So the class hierarchy talks to the correct pointer type"""
        inst._module_MyRoot_client = c_obj

    @staticmethod
    async def connect(str host, int port, loop=None):
        loop = loop or asyncio.get_event_loop()
        future = loop.create_future()
        future.loop = loop
        eb = await get_event_base(loop)
        cdef string _host = host.encode('UTF-8')
        make_py3_client[cMyRootAsyncClient, cMyRootClientWrapper](
            (<EventBase> eb)._folly_event_base,
            _host,
            port,
            0,
            made_MyRoot_py3_client_callback,
            future)
        return await future

    def do_root(
            self):
        future = self.loop.create_future()
        future.loop = self.loop

        deref(self._module_MyRoot_client).do_root(
            MyRoot_do_root_callback,
            future)
        return future


cdef void made_MyRoot_py3_client_callback(
        PyObject* future,
        cFollyTry[shared_ptr[cMyRootClientWrapper]] result) with gil:
    cdef object pyfuture = <object> future
    if result.hasException():
        try:
            result.exception().throwException()
        except:
            pyfuture.loop.call_soon_threadsafe(pyfuture.set_exception, sys.exc_info()[1])
    else:
        pyclient = <MyRoot> MyRoot.__new__(MyRoot, pyfuture.loop)
        MyRoot._module_MyRoot_set_client(pyclient, result.value())
        pyfuture.loop.call_soon_threadsafe(pyfuture.set_result, pyclient)

cdef class MyNode(MyRoot):

    def __init__(self, *args, **kwds):
        raise TypeError('Use MyNode.connect() instead.')

    def __cinit__(self, loop):
        self.loop = loop

    @staticmethod
    cdef _module_MyNode_set_client(MyNode inst, shared_ptr[cMyNodeClientWrapper] c_obj):
        """So the class hierarchy talks to the correct pointer type"""
        inst._module_MyNode_client = c_obj
        MyRoot._module_MyRoot_set_client(inst, <shared_ptr[cMyRootClientWrapper]>c_obj)

    @staticmethod
    async def connect(str host, int port, loop=None):
        loop = loop or asyncio.get_event_loop()
        future = loop.create_future()
        future.loop = loop
        eb = await get_event_base(loop)
        cdef string _host = host.encode('UTF-8')
        make_py3_client[cMyNodeAsyncClient, cMyNodeClientWrapper](
            (<EventBase> eb)._folly_event_base,
            _host,
            port,
            0,
            made_MyNode_py3_client_callback,
            future)
        return await future

    def do_mid(
            self):
        future = self.loop.create_future()
        future.loop = self.loop

        deref(self._module_MyNode_client).do_mid(
            MyNode_do_mid_callback,
            future)
        return future


cdef void made_MyNode_py3_client_callback(
        PyObject* future,
        cFollyTry[shared_ptr[cMyNodeClientWrapper]] result) with gil:
    cdef object pyfuture = <object> future
    if result.hasException():
        try:
            result.exception().throwException()
        except:
            pyfuture.loop.call_soon_threadsafe(pyfuture.set_exception, sys.exc_info()[1])
    else:
        pyclient = <MyNode> MyNode.__new__(MyNode, pyfuture.loop)
        MyNode._module_MyNode_set_client(pyclient, result.value())
        pyfuture.loop.call_soon_threadsafe(pyfuture.set_result, pyclient)

cdef class MyLeaf(MyNode):

    def __init__(self, *args, **kwds):
        raise TypeError('Use MyLeaf.connect() instead.')

    def __cinit__(self, loop):
        self.loop = loop

    @staticmethod
    cdef _module_MyLeaf_set_client(MyLeaf inst, shared_ptr[cMyLeafClientWrapper] c_obj):
        """So the class hierarchy talks to the correct pointer type"""
        inst._module_MyLeaf_client = c_obj
        MyNode._module_MyNode_set_client(inst, <shared_ptr[cMyNodeClientWrapper]>c_obj)

    @staticmethod
    async def connect(str host, int port, loop=None):
        loop = loop or asyncio.get_event_loop()
        future = loop.create_future()
        future.loop = loop
        eb = await get_event_base(loop)
        cdef string _host = host.encode('UTF-8')
        make_py3_client[cMyLeafAsyncClient, cMyLeafClientWrapper](
            (<EventBase> eb)._folly_event_base,
            _host,
            port,
            0,
            made_MyLeaf_py3_client_callback,
            future)
        return await future

    def do_leaf(
            self):
        future = self.loop.create_future()
        future.loop = self.loop

        deref(self._module_MyLeaf_client).do_leaf(
            MyLeaf_do_leaf_callback,
            future)
        return future


cdef void made_MyLeaf_py3_client_callback(
        PyObject* future,
        cFollyTry[shared_ptr[cMyLeafClientWrapper]] result) with gil:
    cdef object pyfuture = <object> future
    if result.hasException():
        try:
            result.exception().throwException()
        except:
            pyfuture.loop.call_soon_threadsafe(pyfuture.set_exception, sys.exc_info()[1])
    else:
        pyclient = <MyLeaf> MyLeaf.__new__(MyLeaf, pyfuture.loop)
        MyLeaf._module_MyLeaf_set_client(pyclient, result.value())
        pyfuture.loop.call_soon_threadsafe(pyfuture.set_result, pyclient)

