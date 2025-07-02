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

"""Image listing utilities for the Finch MCP server.

This module provides functions to list container images using Finch.
"""

import json
from ..consts import STATUS_ERROR, STATUS_SUCCESS
from .common import execute_command, format_result
from loguru import logger
from typing import Any, Dict


def list_images() -> Dict[str, Any]:
    """List all container images using finch image ls.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): "success" if the operation succeeded, "error" otherwise
            - message (str): A descriptive message about the result
            - images (List[Dict]): List of image information if successful

    """
    try:
        logger.info('Listing container images')

        # Execute finch image ls --format json to get structured output
        result = execute_command(['finch', 'image', 'ls', '--format', 'json'])

        if result.returncode != 0:
            error_msg = f'Failed to list images: {result.stderr}'
            logger.error(error_msg)
            return format_result(STATUS_ERROR, error_msg)

        # Parse JSON output
        images = []
        if result.stdout.strip():
            try:
                # Each line is a separate JSON object
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        image_data = json.loads(line)
                        images.append(image_data)
            except json.JSONDecodeError as e:
                logger.error(f'Failed to parse image list JSON: {e}')
                # Fallback to plain text output
                result_plain = execute_command(['finch', 'image', 'ls'])
                if result_plain.returncode == 0:
                    return {
                        'status': STATUS_SUCCESS,
                        'message': f'Successfully listed {len(result_plain.stdout.strip().split(chr(10))[1:])} images (plain text format)',
                        'images_text': result_plain.stdout,
                    }
                else:
                    return format_result(
                        STATUS_ERROR, f'Failed to list images: {result_plain.stderr}'
                    )

        return {
            'status': STATUS_SUCCESS,
            'message': f'Successfully listed {len(images)} images',
            'images': images,
        }

    except Exception as e:
        error_msg = f'Error listing images: {str(e)}'
        logger.error(error_msg)
        return format_result(STATUS_ERROR, error_msg)
