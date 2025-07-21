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

"""Utility functions for inspecting containers using Finch.

This module provides functions for retrieving detailed information about containers.
"""

import json
import logging
from awslabs.finch_mcp_server.consts import SERVER_NAME
from awslabs.finch_mcp_server.utils.common import execute_command, format_result
from typing import Any, Dict, Optional


logger = logging.getLogger(SERVER_NAME)


def inspect_container(container_id: str, format_str: Optional[str] = None) -> Dict[str, Any]:
    """Inspect a container to get detailed information.

    Args:
        container_id (str): The ID or name of the container to inspect
        format_str (str, optional): Format the output using the given Go template

    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): "success" if the operation succeeded, "error" otherwise
            - message (str): A descriptive message about the result of the operation
            - container_info (Dict): Detailed information about the container (if successful)
            - raw_output (str): Raw output from the inspect command (if successful)

    """
    logger.info(f'Inspecting container: {container_id}')

    # Build the command
    cmd = ['finch', 'container', 'inspect']

    if format_str:
        cmd.extend(['--format', format_str])
    else:
        # Default to JSON format for structured data
        cmd.extend(['--format', 'json'])

    cmd.append(container_id)

    try:
        result = execute_command(cmd)
        if result.returncode == 0:
            try:
                # Parse the JSON output
                container_info = json.loads(result.stdout)
                return {
                    'status': 'success',
                    'message': f'Successfully inspected container {container_id}',
                    'container_info': container_info,
                    'raw_output': result.stdout,
                }
            except json.JSONDecodeError:
                # If not JSON format, return the raw output
                return {
                    'status': 'success',
                    'message': f'Successfully inspected container {container_id}',
                    'container_info': None,
                    'raw_output': result.stdout,
                }
        else:
            return format_result('error', f'Failed to inspect container: {result.stderr}')
    except Exception as e:
        return format_result('error', f'Error inspecting container: {str(e)}')
