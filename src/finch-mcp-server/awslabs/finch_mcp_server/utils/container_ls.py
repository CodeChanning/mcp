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

"""Container listing utilities for the Finch MCP server.

This module provides functions to list containers using Finch.
"""

import json
from ..consts import STATUS_ERROR, STATUS_SUCCESS
from .common import execute_command, format_result
from loguru import logger
from typing import Any, Dict, List, Optional


def list_containers(
    all_containers: bool = False,
    filter_expr: Optional[List[str]] = None,
    last: Optional[int] = None,
    latest: bool = False,
    no_trunc: bool = False,
    quiet: bool = False,
    size: bool = False,
) -> Dict[str, Any]:
    """List containers using finch container ls with various options.

    Args:
        all_containers: Show all containers (default: False, only running)
        filter_expr: Filter output based on conditions (e.g., ["status=exited", "label=app=web"])
        last: Show n last created containers (includes all states)
        latest: Show the latest created container (includes all states)
        no_trunc: Don't truncate output
        quiet: Only display container IDs
        size: Display total file sizes

    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): "success" if the operation succeeded, "error" otherwise
            - message (str): A descriptive message about the result
            - containers (List[Dict]): List of container information if successful

    """
    try:
        logger.info('Listing containers')

        # Build command with options
        cmd = ['finch', 'container', 'ls', '--format', 'json']

        if all_containers:
            cmd.append('-a')

        if filter_expr:
            for filter_item in filter_expr:
                cmd.extend(['-f', filter_item])

        if last is not None:
            cmd.extend(['-n', str(last)])

        if latest:
            cmd.append('-l')

        if no_trunc:
            cmd.append('--no-trunc')

        if quiet:
            cmd.append('-q')

        if size:
            cmd.append('-s')

        # Execute command with options
        result = execute_command(cmd)

        if result.returncode != 0:
            error_msg = f'Failed to list containers: {result.stderr}'
            logger.error(error_msg)
            return format_result(STATUS_ERROR, error_msg)

        # Parse JSON output
        containers = []
        if result.stdout.strip():
            try:
                # Each line is a separate JSON object
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        container_data = json.loads(line)
                        containers.append(container_data)
            except json.JSONDecodeError as e:
                logger.error(f'Failed to parse container list JSON: {e}')
                # Fallback to plain text output
                result_plain = execute_command(['finch', 'container', 'ls'])
                if result_plain.returncode == 0:
                    return {
                        'status': STATUS_SUCCESS,
                        'message': f'Successfully listed {len(result_plain.stdout.strip().split(chr(10))[1:])} containers (plain text format)',
                        'containers_text': result_plain.stdout,
                    }
                else:
                    return format_result(
                        STATUS_ERROR, f'Failed to list containers: {result_plain.stderr}'
                    )

        return {
            'status': STATUS_SUCCESS,
            'message': f'Successfully listed {len(containers)} containers, all continers bool: {all_containers}',
            'containers': containers,
        }

    except Exception as e:
        error_msg = f'Error listing containers: {str(e)}'
        logger.error(error_msg)
        return format_result(STATUS_ERROR, error_msg)
