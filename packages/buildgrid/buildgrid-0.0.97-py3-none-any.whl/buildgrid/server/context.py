# Copyright (C) 2022 Bloomberg LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  <http://www.apache.org/licenses/LICENSE-2.0>
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import functools
from contextvars import ContextVar
from typing import Any, Callable, Optional, Tuple, TypeVar, Union, cast

import grpc

from buildgrid._protos.build.bazel.remote.execution.v2.remote_execution_pb2 import RequestMetadata
from buildgrid.server.request_metadata_utils import extract_request_metadata
from buildgrid.settings import REQUEST_METADATA_HEADER_NAME, REQUEST_METADATA_TOOL_NAME, REQUEST_METADATA_TOOL_VERSION


def get_empty() -> RequestMetadata:
    """Function to create an empty request metadata structure, to use as
    the deafult for the ContextVar
    """
    empty_metadata = RequestMetadata()
    empty_metadata.tool_details.tool_name = REQUEST_METADATA_TOOL_NAME
    empty_metadata.tool_details.tool_version = REQUEST_METADATA_TOOL_VERSION
    return empty_metadata


# ContextVar for request metadata
ctx_request_metadata: ContextVar[RequestMetadata] = ContextVar("ctx_request_metadata", default=get_empty())


Func = TypeVar("Func", bound=Callable)  # type: ignore[type-arg]


def metadatacontext() -> Callable[[Func], Func]:
    """Helper function to obtain metadata and set request metadata ContextVar,
    and then reset it on completion of method.

    Note:
        args[2] of the method must be of type grpc.ServicerContext

    This returns a decorator that extracts the invocation_metadata from the
    context argument and sets the ContextVar variable with it. Resetting the
    ContextVar variable after the method has completed.
    """

    def context_decorator(func: Func) -> Func:
        @functools.wraps(func)
        def context_wrapper(*args: Any, **kwargs: Any) -> Any:
            context = args[2]
            assert isinstance(context, grpc.ServicerContext)
            metadata = extract_request_metadata(context.invocation_metadata())
            token = ctx_request_metadata.set(metadata)
            try:
                retval = func(*args, **kwargs)
                return retval
            finally:
                ctx_request_metadata.reset(token)

        return cast(Func, context_wrapper)

    return context_decorator


def metadata_list() -> Tuple[Tuple[str, Union[str, bytes]], ...]:
    """Helper function to construct the metadata list from the ContextVar."""
    metadata = ctx_request_metadata.get()
    return ((REQUEST_METADATA_HEADER_NAME, metadata.SerializeToString()),)


ctx_grpc_request_id: ContextVar[Optional[str]] = ContextVar("grpc_request_id", default=None)
