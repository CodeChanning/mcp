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

"""Help utilities for the Finch MCP server.

This module provides functions to get Finch help information.
"""

from ..consts import STATUS_ERROR, STATUS_SUCCESS
from .common import execute_command, format_result
from loguru import logger
from typing import Any, Dict


def get_help(command: str = None) -> Dict[str, Any]:
    """Get Finch help information.

    Args:
        command: Optional specific command to get help for (e.g., 'image', 'container')

    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): "success" if the operation succeeded, "error" otherwise
            - message (str): A descriptive message about the result
            - help_text (str): Help information if successful

    """
    try:
        logger.info(f'Getting Finch help{f" for {command}" if command else ""}')

        # Build command
        cmd = ['finch']
        if command:
            cmd.append(command)
        cmd.append('--help')

        # Execute finch --help or finch <command> --help
        result = execute_command(cmd)

        if result.returncode != 0:
            error_msg = f'Failed to get help: {result.stderr}'
            logger.error(error_msg)
            return format_result(STATUS_ERROR, error_msg)

        help_text = result.stdout.strip()

        return {
            'status': STATUS_SUCCESS,
            'message': f'Successfully retrieved Finch help{f" for {command}" if command else ""}',
            'help_text': help_text,
        }

    except Exception as e:
        error_msg = f'Error getting help: {str(e)}'
        logger.error(error_msg)
        return format_result(STATUS_ERROR, error_msg)
