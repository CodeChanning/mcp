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

"""Utility functions for inspecting container images using Finch."""

import json
from awslabs.finch_mcp_server.utils.common import execute_command, format_result
from typing import Any, Dict, Optional


def inspect_image(
    image_name: str,
    format_str: Optional[str] = None,
    mode: Optional[str] = None,
    platform: Optional[str] = None,
) -> Dict[str, Any]:
    """Inspect a container image using Finch.

    This function executes the 'finch image inspect' command to retrieve detailed
    information about a container image, including its configuration, layers, and metadata.

    Args:
        image_name: Name of the image to inspect
        format_str: Format the output using the given Go template, e.g, '{{json .}}'
        mode: Inspect mode, "dockercompat" for Docker-compatible output, "native" for containerd-native output
        platform: Inspect a specific platform

    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): "success" if the operation succeeded, "error" otherwise
            - message (str): A descriptive message about the result of the operation
            - image_info (Dict[str, Any]): Image information if successful

    """
    try:
        # Build command with flags
        command = ['finch', 'image', 'inspect']

        if format_str:
            command.extend(['--format', format_str])

        if mode:
            command.extend(['--mode', mode])

        if platform:
            command.extend(['--platform', platform])

        # Add image name
        command.append(image_name)

        # Execute finch image inspect command
        result = execute_command(command)

        if result.returncode != 0:
            return format_result('error', f'Failed to inspect image: {result.stderr}')

        # Parse JSON output
        try:
            # If format is specified, we might not get JSON output
            if format_str:
                return {
                    'status': 'success',
                    'message': f'Successfully inspected image {image_name}',
                    'output': result.stdout,
                }
            else:
                image_info = json.loads(result.stdout)

                # TODO: Implement sensitive data filtering for environment variables and other
                # potentially sensitive fields (e.g., Config.Env entries containing PASSWORD, SECRET, etc.)

                return {
                    'status': 'success',
                    'message': f'Successfully inspected image {image_name}',
                    'image_info': image_info,
                }
        except json.JSONDecodeError:
            # If we can't parse as JSON, return the raw output
            return {
                'status': 'success',
                'message': f'Successfully inspected image {image_name}',
                'output': result.stdout,
            }
    except Exception as e:
        return format_result('error', f'Error inspecting image: {str(e)}')
