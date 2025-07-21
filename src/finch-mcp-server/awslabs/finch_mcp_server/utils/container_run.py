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

"""Utility functions for running containers using Finch.

This module provides functions for running containers with various options.
"""

import logging
from awslabs.finch_mcp_server.consts import SERVER_NAME
from awslabs.finch_mcp_server.utils.common import execute_command, format_result
from typing import Any, Dict, List, Optional


logger = logging.getLogger(SERVER_NAME)


def run_container(
    image: str,
    name: Optional[str] = None,
    detach: bool = True,
    ports: Optional[List[str]] = None,
    volumes: Optional[List[str]] = None,
    env_vars: Optional[List[str]] = None,
    command: Optional[str] = None,
    entrypoint: Optional[str] = None,
    network: Optional[str] = None,
    restart_policy: Optional[str] = None,
    memory: Optional[str] = None,
    cpus: Optional[str] = None,
    platform: Optional[str] = None,
    user: Optional[str] = None,
    workdir: Optional[str] = None,
    labels: Optional[List[str]] = None,
    rm: bool = False,
    privileged: bool = False,
    read_only: bool = False,
) -> Dict[str, Any]:
    """Run a container using Finch.

    Args:
        image (str): The image to run
        name (str, optional): Name to assign to the container
        detach (bool, optional): Run container in background. Defaults to True.
        ports (List[str], optional): List of port mappings (e.g., ["8080:80"])
        volumes (List[str], optional): List of volume mappings (e.g., ["/host:/container"])
        env_vars (List[str], optional): List of environment variables (e.g., ["KEY=VALUE"])
        command (str, optional): Command to run in the container
        entrypoint (str, optional): Overwrite the default entrypoint
        network (str, optional): Connect to a network
        restart_policy (str, optional): Restart policy (e.g., "always", "on-failure")
        memory (str, optional): Memory limit (e.g., "512m", "1g")
        cpus (str, optional): Number of CPUs (e.g., "0.5", "2")
        platform (str, optional): Set platform if server is multi-platform capable
        user (str, optional): Username or UID
        workdir (str, optional): Working directory inside the container
        labels (List[str], optional): Set metadata on container (e.g., ["key=value"])
        rm (bool, optional): Automatically remove the container when it exits
        privileged (bool, optional): Give extended privileges to this container
        read_only (bool, optional): Mount the container's root filesystem as read only

    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): "success" if the operation succeeded, "error" otherwise
            - message (str): A descriptive message about the result of the operation
            - container_id (str): The ID of the created container (if successful)

    """
    logger.info(f'Running container from image: {image}')

    # Build the command
    cmd = ['finch', 'container', 'run']

    # Add options
    if name:
        cmd.extend(['--name', name])

    if detach:
        cmd.append('-d')

    if ports:
        for port in ports:
            cmd.extend(['-p', port])

    if volumes:
        for volume in volumes:
            cmd.extend(['-v', volume])

    if env_vars:
        for env_var in env_vars:
            cmd.extend(['-e', env_var])

    if network:
        cmd.extend(['--network', network])

    if restart_policy:
        cmd.extend(['--restart', restart_policy])

    if memory:
        cmd.extend(['--memory', memory])

    if cpus:
        cmd.extend(['--cpus', cpus])

    if platform:
        cmd.extend(['--platform', platform])

    if user:
        cmd.extend(['--user', user])

    if workdir:
        cmd.extend(['--workdir', workdir])

    if labels:
        for label in labels:
            cmd.extend(['--label', label])

    if rm:
        cmd.append('--rm')

    if privileged:
        cmd.append('--privileged')

    if read_only:
        cmd.append('--read-only')

    if entrypoint:
        cmd.extend(['--entrypoint', entrypoint])

    # Add image name
    cmd.append(image)

    # Add command if provided
    if command:
        cmd.extend(command.split())

    try:
        result = execute_command(cmd)
        if result.returncode == 0:
            container_id = result.stdout.strip()
            return {
                'status': 'success',
                'message': f'Successfully started container from image {image}',
                'container_id': container_id,
            }
        else:
            return format_result('error', f'Failed to run container: {result.stderr}')
    except Exception as e:
        return format_result('error', f'Error running container: {str(e)}')
