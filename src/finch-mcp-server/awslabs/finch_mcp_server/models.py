# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
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

"""Pydantic models for the Finch MCP server.

This module defines the data models used for request and response validation
in the Finch MCP server tools.
"""

from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


class Result(BaseModel):
    """Base model for operation results.

    This model only includes status and message fields, regardless of what additional
    fields might be present in the input dictionary. This ensures that only these two
    fields are returned to the user.
    """

    status: str = Field(..., description="Status of the operation ('success', 'error', etc.)")
    message: str = Field(..., description='Descriptive message about the result of the operation')


class ContainerRunRequest(BaseModel):
    """Request model for running a container."""

    image: str = Field(..., description='The image to run')
    name: Optional[str] = Field(None, description='Name to assign to the container')
    detach: bool = Field(True, description='Run container in background')
    ports: Optional[List[str]] = Field(
        None, description="List of port mappings (e.g., ['8080:80'])"
    )
    volumes: Optional[List[str]] = Field(
        None, description="List of volume mappings (e.g., ['/host:/container'])"
    )
    env_vars: Optional[List[str]] = Field(
        None, description="List of environment variables (e.g., ['KEY=VALUE'])"
    )
    command: Optional[str] = Field(None, description='Command to run in the container')
    entrypoint: Optional[str] = Field(None, description='Overwrite the default entrypoint')
    network: Optional[str] = Field(None, description='Connect to a network')
    restart_policy: Optional[str] = Field(
        None, description="Restart policy (e.g., 'always', 'on-failure')"
    )
    memory: Optional[str] = Field(None, description="Memory limit (e.g., '512m', '1g')")
    cpus: Optional[str] = Field(None, description="Number of CPUs (e.g., '0.5', '2')")
    platform: Optional[str] = Field(
        None, description='Set platform if server is multi-platform capable'
    )
    user: Optional[str] = Field(None, description='Username or UID')
    workdir: Optional[str] = Field(None, description='Working directory inside the container')
    labels: Optional[List[str]] = Field(
        None, description="Set metadata on container (e.g., ['key=value'])"
    )
    rm: bool = Field(False, description='Automatically remove the container when it exits')
    privileged: bool = Field(False, description='Give extended privileges to this container')
    read_only: bool = Field(
        False, description="Mount the container's root filesystem as read only"
    )


class ContainerStopRequest(BaseModel):
    """Request model for stopping a container."""

    container_id: str = Field(..., description='The ID or name of the container to stop')
    time: Optional[int] = Field(None, description='Seconds to wait for stop before killing it')
    force: bool = Field(False, description='Force the container to stop')


class ContainerRemoveRequest(BaseModel):
    """Request model for removing a container."""

    container_id: str = Field(..., description='The ID or name of the container to remove')
    force: bool = Field(False, description='Force removal of the container')
    volumes: bool = Field(
        False, description='Remove anonymous volumes associated with the container'
    )


class ContainerInspectRequest(BaseModel):
    """Request model for inspecting a container."""

    container_id: str = Field(..., description='The ID or name of the container to inspect')
    format_str: Optional[str] = Field(
        None, description='Format the output using the given Go template'
    )


class ContainerRunResult(Result):
    """Result model for running a container."""

    container_id: Optional[str] = Field(None, description='The ID of the created container')


class ContainerInspectResult(Result):
    """Result model for inspecting a container."""

    container_info: Optional[Dict[str, Any]] = Field(
        None, description='Detailed information about the container'
    )
    raw_output: Optional[str] = Field(None, description='Raw output from the inspect command')


class ContainerLSResult(Result):
    """Result model for listing containers."""

    raw_output: Optional[str] = Field(None, description='Raw output from the command')
