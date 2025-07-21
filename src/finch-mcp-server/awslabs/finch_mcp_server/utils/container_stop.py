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

"""Utility functions for stopping containers using Finch.

This module provides functions for stopping and removing containers.
"""

import logging
from awslabs.finch_mcp_server.consts import SERVER_NAME
from awslabs.finch_mcp_server.utils.common import execute_command, format_result
from typing import Any, Dict, Optional


logger = logging.getLogger(SERVER_NAME)


def stop_container(
    container_id: str, time: Optional[int] = None, force: bool = False
) -> Dict[str, Any]:
    """Stop a running container.

    Args:
        container_id (str): The ID or name of the container to stop
        time (int, optional): Seconds to wait for stop before killing it
        force (bool, optional): Force the container to stop

    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): "success" if the operation succeeded, "error" otherwise
            - message (str): A descriptive message about the result of the operation

    """
    logger.info(f'Stopping container: {container_id}')

    # Build the command
    cmd = ['finch', 'container', 'stop']

    if time is not None:
        cmd.extend(['--time', str(time)])

    if force:
        cmd.append('--force')

    cmd.append(container_id)

    try:
        result = execute_command(cmd)
        if result.returncode == 0:
            return {
                'status': 'success',
                'message': f'Successfully stopped container {container_id}',
            }
        else:
            return format_result('error', f'Failed to stop container: {result.stderr}')
    except Exception as e:
        return format_result('error', f'Error stopping container: {str(e)}')


def remove_container(
    container_id: str, force: bool = False, volumes: bool = False
) -> Dict[str, Any]:
    """Remove a container.

    Args:
        container_id (str): The ID or name of the container to remove
        force (bool, optional): Force removal of the container
        volumes (bool, optional): Remove anonymous volumes associated with the container

    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): "success" if the operation succeeded, "error" otherwise
            - message (str): A descriptive message about the result of the operation

    """
    logger.info(f'Removing container: {container_id}')

    # Build the command
    cmd = ['finch', 'container', 'rm']

    if force:
        cmd.append('--force')

    if volumes:
        cmd.append('--volumes')

    cmd.append(container_id)

    try:
        result = execute_command(cmd)
        if result.returncode == 0:
            return {
                'status': 'success',
                'message': f'Successfully removed container {container_id}',
            }
        else:
            return format_result('error', f'Failed to remove container: {result.stderr}')
    except Exception as e:
        return format_result('error', f'Error removing container: {str(e)}')
