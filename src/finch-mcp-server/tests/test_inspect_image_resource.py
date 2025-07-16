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

"""Tests for the finch_inspect_image resource."""

import asyncio
import json
import unittest
from awslabs.finch_mcp_server.server import finch_inspect_image
from unittest.mock import patch


class TestFinchInspectImageResource(unittest.TestCase):
    """Test cases for the finch_inspect_image resource."""

    def run_async(self, coro):
        """Run an async function in the event loop."""
        return asyncio.get_event_loop().run_until_complete(coro)

    @patch('awslabs.finch_mcp_server.server.check_finch_installation')
    @patch('awslabs.finch_mcp_server.server.ensure_vm_running')
    @patch('awslabs.finch_mcp_server.utils.inspect.inspect_image')
    def test_finch_inspect_image_success(
        self, mock_inspect_image, mock_ensure_vm_running, mock_check_finch_installation
    ):
        """Test successful image inspection resource."""
        # Mock the dependencies
        mock_check_finch_installation.return_value = {
            'status': 'success',
            'message': 'Finch is installed',
        }
        mock_ensure_vm_running.return_value = {'status': 'success', 'message': 'VM is running'}
        mock_inspect_image.return_value = {
            'status': 'success',
            'message': 'Successfully inspected image test:latest',
            'image_info': [{'Id': 'sha256:123', 'RepoTags': ['test:latest']}],
        }

        # Call the resource function
        result = self.run_async(finch_inspect_image('test:latest'))

        # Parse the JSON result
        result_dict = json.loads(result)

        # Verify the result
        self.assertEqual(result_dict['status'], 'success')
        self.assertEqual(result_dict['message'], 'Successfully inspected image test:latest')
        self.assertEqual(
            result_dict['image_info'], [{'Id': 'sha256:123', 'RepoTags': ['test:latest']}]
        )

        # Verify the mocks were called correctly
        mock_check_finch_installation.assert_called_once()
        mock_ensure_vm_running.assert_called_once()
        mock_inspect_image.assert_called_once_with('test:latest')

    @patch('awslabs.finch_mcp_server.server.check_finch_installation')
    def test_finch_inspect_image_finch_not_installed(self, mock_check_finch_installation):
        """Test image inspection resource when Finch is not installed."""
        # Mock the dependencies
        mock_check_finch_installation.return_value = {
            'status': 'error',
            'message': 'Finch is not installed',
        }

        # Call the resource function
        result = self.run_async(finch_inspect_image('test:latest'))

        # Parse the JSON result
        result_dict = json.loads(result)

        # Verify the result
        self.assertEqual(result_dict['status'], 'error')
        self.assertEqual(result_dict['message'], 'Finch is not installed')

        # Verify the mocks were called correctly
        mock_check_finch_installation.assert_called_once()

    @patch('awslabs.finch_mcp_server.server.check_finch_installation')
    @patch('awslabs.finch_mcp_server.server.ensure_vm_running')
    def test_finch_inspect_image_vm_not_running(
        self, mock_ensure_vm_running, mock_check_finch_installation
    ):
        """Test image inspection resource when VM is not running."""
        # Mock the dependencies
        mock_check_finch_installation.return_value = {
            'status': 'success',
            'message': 'Finch is installed',
        }
        mock_ensure_vm_running.return_value = {'status': 'error', 'message': 'VM is not running'}

        # Call the resource function
        result = self.run_async(finch_inspect_image('test:latest'))

        # Parse the JSON result
        result_dict = json.loads(result)

        # Verify the result
        self.assertEqual(result_dict['status'], 'error')
        self.assertEqual(result_dict['message'], 'VM is not running')

        # Verify the mocks were called correctly
        mock_check_finch_installation.assert_called_once()
        mock_ensure_vm_running.assert_called_once()

    @patch('awslabs.finch_mcp_server.server.check_finch_installation')
    @patch('awslabs.finch_mcp_server.server.ensure_vm_running')
    @patch('awslabs.finch_mcp_server.utils.inspect.inspect_image')
    def test_finch_inspect_image_error(
        self, mock_inspect_image, mock_ensure_vm_running, mock_check_finch_installation
    ):
        """Test image inspection resource with error."""
        # Mock the dependencies
        mock_check_finch_installation.return_value = {
            'status': 'success',
            'message': 'Finch is installed',
        }
        mock_ensure_vm_running.return_value = {'status': 'success', 'message': 'VM is running'}
        mock_inspect_image.return_value = {
            'status': 'error',
            'message': 'Failed to inspect image: Error: No such image: test:latest',
        }

        # Call the resource function
        result = self.run_async(finch_inspect_image('test:latest'))

        # Parse the JSON result
        result_dict = json.loads(result)

        # Verify the result
        self.assertEqual(result_dict['status'], 'error')
        self.assertEqual(
            result_dict['message'], 'Failed to inspect image: Error: No such image: test:latest'
        )

        # Verify the mocks were called correctly
        mock_check_finch_installation.assert_called_once()
        mock_ensure_vm_running.assert_called_once()
        mock_inspect_image.assert_called_once_with('test:latest')

    @patch('awslabs.finch_mcp_server.server.check_finch_installation')
    @patch('awslabs.finch_mcp_server.server.ensure_vm_running')
    @patch('awslabs.finch_mcp_server.utils.inspect.inspect_image')
    def test_finch_inspect_image_exception(
        self, mock_inspect_image, mock_ensure_vm_running, mock_check_finch_installation
    ):
        """Test image inspection resource with exception."""
        # Mock the dependencies
        mock_check_finch_installation.return_value = {
            'status': 'success',
            'message': 'Finch is installed',
        }
        mock_ensure_vm_running.return_value = {'status': 'success', 'message': 'VM is running'}
        mock_inspect_image.side_effect = Exception('Test exception')

        # Call the resource function
        result = self.run_async(finch_inspect_image('test:latest'))

        # Parse the JSON result
        result_dict = json.loads(result)

        # Verify the result
        self.assertEqual(result_dict['status'], 'error')
        self.assertEqual(result_dict['message'], 'Error inspecting image: Test exception')

        # Verify the mocks were called correctly
        mock_check_finch_installation.assert_called_once()
        mock_ensure_vm_running.assert_called_once()
        mock_inspect_image.assert_called_once_with('test:latest')


if __name__ == '__main__':
    unittest.main()
