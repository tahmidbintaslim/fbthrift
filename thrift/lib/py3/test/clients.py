#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import sys
import traceback
import types
import unittest

from testing.clients import TestingService
from testing.types import Color, I32List, easy
from thrift.py3 import Priority, RpcOptions, TransportError, get_client
from thrift.py3.client import get_proxy_factory, install_proxy_factory
from thrift.py3.common import WriteHeaders
from thrift.py3.test.client_event_handler.helper import (
    TestHelper as ClientEventHandlerTestHelper,
)


async def bad_client_connect() -> None:
    async with get_client(TestingService, port=1) as client:
        await client.complex_action("foo", "bar", 9, "baz")


class ThriftClientTestProxy:  # noqa: B903
    def __init__(self, inner) -> None:  # type: ignore
        # pyre-fixme[4]: Attribute must be annotated.
        self.inner = inner


class ClientTests(unittest.TestCase):
    def test_annotations(self) -> None:
        annotations = TestingService.annotations
        self.assertIsInstance(annotations, types.MappingProxyType)
        self.assertTrue(annotations.get("py3.pass_context"))
        self.assertFalse(annotations.get("NotAnAnnotation"))
        self.assertEqual(annotations["fun_times"], "yes")
        with self.assertRaises(TypeError):
            # You can't set attributes on builtin/extension types
            TestingService.annotations = {}

    def test_client_keyword_arguments(self) -> None:
        # Create a broken client
        client = TestingService()
        # This should not raise an exception
        with self.assertRaises(asyncio.InvalidStateError):
            client.complex_action(first="foo", second="bar", third=9, fourth="baz")

        with self.assertRaises(asyncio.InvalidStateError):
            client.complex_action("foo", "bar", 9, "baz")

    def test_none_arguments(self) -> None:
        client = TestingService()
        with self.assertRaises(TypeError):
            # missing argument
            client.take_it_easy(9)  # type: ignore
        with self.assertRaises(TypeError):
            # Should be an easy type
            client.take_it_easy(9, None)  # type: ignore
        with self.assertRaises(TypeError):
            # Should not be None
            client.takes_a_list(None)  # type: ignore
        with self.assertRaises(TypeError):
            # Should be a bool
            client.invert(None)  # type: ignore
        with self.assertRaises(TypeError):
            # None is not a Color
            client.pick_a_color(None)  # type: ignore
        with self.assertRaises(TypeError):
            # None is not an int
            client.take_it_easy(None, easy())  # type: ignore

    def test_TransportError(self) -> None:
        """
        Are C++ TTransportException converting properly to py TransportError
        """
        loop = asyncio.get_event_loop()
        with self.assertRaises(TransportError):
            loop.run_until_complete(bad_client_connect())

        try:
            loop.run_until_complete(bad_client_connect())
        except TransportError as ex:
            # Test that we can get the errno
            self.assertEqual(ex.errno, 0)
            # The traceback should be short since it raises inside
            # the rpc call not down inside the guts of thrift-py3
            self.assertEqual(len(traceback.extract_tb(sys.exc_info()[2])), 3)

    def test_set_persistent_header(self) -> None:
        """
        This was causing a nullptr dereference and thus a segfault
        """
        loop = asyncio.get_event_loop()

        async def test() -> None:
            async with get_client(TestingService, port=1, headers={"foo": "bar"}):
                pass

        loop.run_until_complete(test())

    def test_rpc_container_autoboxing(self) -> None:
        client = TestingService()

        with self.assertRaises(asyncio.InvalidStateError):
            client.takes_a_list([1, 2, 3])

        with self.assertRaises(asyncio.InvalidStateError):
            client.takes_a_list(I32List([1, 2, 3]))

        loop = asyncio.get_event_loop()
        with self.assertRaises(TypeError):
            # This is safe because we do type checks before we touch
            # state checks
            loop.run_until_complete(
                client.takes_a_list([1, "b", "three"])  # type: ignore
            )

    def test_rpc_non_container_types(self) -> None:
        client = TestingService()
        with self.assertRaises(TypeError):
            client.complex_action(b"foo", "bar", "nine", fourth="baz")  # type: ignore

    def test_rpc_enum_args(self) -> None:
        client = TestingService()
        loop = asyncio.get_event_loop()
        with self.assertRaises(TypeError):
            loop.run_until_complete(client.pick_a_color(0))  # type: ignore

        with self.assertRaises(asyncio.InvalidStateError):
            loop.run_until_complete(client.pick_a_color(Color.red))

    def test_rpc_int_sizes(self) -> None:
        one = 2 ** 7 - 1
        two = 2 ** 15 - 1
        three = 2 ** 31 - 1
        four = 2 ** 63 - 1
        client = TestingService()
        loop = asyncio.get_event_loop()
        with self.assertRaises(asyncio.InvalidStateError):
            # means we passed type checks
            loop.run_until_complete(client.int_sizes(one, two, three, four))

        with self.assertRaises(OverflowError):
            loop.run_until_complete(client.int_sizes(two, two, three, four))

        with self.assertRaises(OverflowError):
            loop.run_until_complete(client.int_sizes(one, three, three, four))

        with self.assertRaises(OverflowError):
            loop.run_until_complete(client.int_sizes(one, two, four, four))

        with self.assertRaises(OverflowError):
            loop.run_until_complete(client.int_sizes(one, two, three, four * 10))

    def test_proxy_get_set(self) -> None:
        # Should be empty before we assign it
        self.assertEqual(get_proxy_factory(), None)

        # Should be able to assign/get a test factory
        install_proxy_factory(ThriftClientTestProxy)  # type: ignore
        self.assertEqual(get_proxy_factory(), ThriftClientTestProxy)

        # Should be able to unhook a factory
        install_proxy_factory(None)
        self.assertEqual(get_proxy_factory(), None)

    def test_client_event_handler(self) -> None:
        loop = asyncio.get_event_loop()
        test_helper = ClientEventHandlerTestHelper()

        # pyre-fixme[53]: Captured variable `test_helper` is not annotated.
        async def test() -> None:
            self.assertFalse(test_helper.is_handler_called())
            async with test_helper.get_client(TestingService, port=1) as cli:
                try:
                    await cli.getName()
                except TransportError:
                    pass
                self.assertTrue(test_helper.is_handler_called())

        loop.run_until_complete(test())


class RpcOptionsTests(unittest.TestCase):
    def test_write_headers(self) -> None:
        options = RpcOptions()
        headers = options.write_headers
        self.assertIsInstance(headers, WriteHeaders)
        options.set_header("test", "test")
        self.assertTrue(options.write_headers is headers)
        self.assertIn("test", headers)
        self.assertEqual(headers["test"], "test")
        with self.assertRaises(TypeError):
            options.set_header("count", 1)  # type: ignore

    def test_timeout(self) -> None:
        options = RpcOptions()
        self.assertEqual(0, options.timeout)
        options.timeout = 0.05
        self.assertEqual(0.05, options.timeout)
        options.chunk_timeout = options.queue_timeout = options.timeout
        self.assertEqual(options.chunk_timeout, options.queue_timeout)
        with self.assertRaises(TypeError):
            options.timeout = "1"  # type: ignore

    def test_priority(self) -> None:
        options = RpcOptions()
        self.assertIsInstance(options.priority, Priority)
        options.priority = Priority.HIGH
        self.assertEquals(options.priority, Priority.HIGH)
        with self.assertRaises(TypeError):
            options.priority = 1  # type: ignore

    def test_chunk_buffer_size(self) -> None:
        options = RpcOptions()
        self.assertEquals(options.chunk_buffer_size, 100)  # default value
        options.chunk_buffer_size = 200
        self.assertEquals(options.chunk_buffer_size, 200)
        with self.assertRaises(TypeError):
            options.chunk_buffer_size = "1"  # type: ignore
