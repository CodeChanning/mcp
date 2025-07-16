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

"""Tests for the inspect utility functions."""

import json
import unittest
from awslabs.finch_mcp_server.utils.inspect import inspect_image
from unittest.mock import MagicMock, patch


class TestInspectImage(unittest.TestCase):
    """Test cases for the inspect_image function."""

    @patch('awslabs.finch_mcp_server.utils.inspect.execute_command')
    def test_inspect_image_success(self, mock_execute_command):
        """Test successful image inspection."""
        # Mock the execute_command function to return a successful result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps([{'Id': 'sha256:123', 'RepoTags': ['test:latest']}])
        mock_execute_command.return_value = mock_result

        # Call the function
        result = inspect_image('test:latest')

        # Verify the result
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['message'], 'Successfully inspected image test:latest')
        self.assertEqual(result['image_info'], [{'Id': 'sha256:123', 'RepoTags': ['test:latest']}])

        # Verify the command was called correctly
        mock_execute_command.assert_called_once_with(['finch', 'image', 'inspect', 'test:latest'])

    @patch('awslabs.finch_mcp_server.utils.inspect.execute_command')
    def test_inspect_image_with_format(self, mock_execute_command):
        """Test image inspection with format flag."""
        # Mock the execute_command function to return a successful result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = 'sha256:123'
        mock_execute_command.return_value = mock_result

        # Call the function with format
        result = inspect_image('test:latest', format_str='{{.Id}}')

        # Verify the result
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['message'], 'Successfully inspected image test:latest')
        self.assertEqual(result['output'], 'sha256:123')

        # Verify the command was called correctly
        mock_execute_command.assert_called_once_with(
            ['finch', 'image', 'inspect', '--format', '{{.Id}}', 'test:latest']
        )

    @patch('awslabs.finch_mcp_server.utils.inspect.execute_command')
    def test_inspect_image_with_mode(self, mock_execute_command):
        """Test image inspection with mode flag."""
        # Mock the execute_command function to return a successful result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps([{'Id': 'sha256:123', 'RepoTags': ['test:latest']}])
        mock_execute_command.return_value = mock_result

        # Call the function with mode
        result = inspect_image('test:latest', mode='native')

        # Verify the result
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['message'], 'Successfully inspected image test:latest')
        self.assertEqual(result['image_info'], [{'Id': 'sha256:123', 'RepoTags': ['test:latest']}])

        # Verify the command was called correctly
        mock_execute_command.assert_called_once_with(
            ['finch', 'image', 'inspect', '--mode', 'native', 'test:latest']
        )

    @patch('awslabs.finch_mcp_server.utils.inspect.execute_command')
    def test_inspect_image_with_platform(self, mock_execute_command):
        """Test image inspection with platform flag."""
        # Mock the execute_command function to return a successful result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps([{'Id': 'sha256:123', 'RepoTags': ['test:latest']}])
        mock_execute_command.return_value = mock_result

        # Call the function with platform
        result = inspect_image('test:latest', platform='linux/amd64')

        # Verify the result
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['message'], 'Successfully inspected image test:latest')
        self.assertEqual(result['image_info'], [{'Id': 'sha256:123', 'RepoTags': ['test:latest']}])

        # Verify the command was called correctly
        mock_execute_command.assert_called_once_with(
            ['finch', 'image', 'inspect', '--platform', 'linux/amd64', 'test:latest']
        )

    @patch('awslabs.finch_mcp_server.utils.inspect.execute_command')
    def test_inspect_image_error(self, mock_execute_command):
        """Test image inspection with error."""
        # Mock the execute_command function to return an error result
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = 'Error: No such image: test:latest'
        mock_execute_command.return_value = mock_result

        # Call the function
        result = inspect_image('test:latest')

        # Verify the result
        self.assertEqual(result['status'], 'error')
        self.assertEqual(
            result['message'], 'Failed to inspect image: Error: No such image: test:latest'
        )

        # Verify the command was called correctly
        mock_execute_command.assert_called_once_with(['finch', 'image', 'inspect', 'test:latest'])

    @patch('awslabs.finch_mcp_server.utils.inspect.execute_command')
    def test_inspect_image_json_error(self, mock_execute_command):
        """Test image inspection with JSON parsing error."""
        # Mock the execute_command function to return an invalid JSON result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = 'Invalid JSON'
        mock_execute_command.return_value = mock_result

        # Call the function
        result = inspect_image('test:latest')

        # Verify the result
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['message'], 'Successfully inspected image test:latest')
        self.assertEqual(result['output'], 'Invalid JSON')

        # Verify the command was called correctly
        mock_execute_command.assert_called_once_with(['finch', 'image', 'inspect', 'test:latest'])

    @patch('awslabs.finch_mcp_server.utils.inspect.execute_command')
    def test_inspect_image_exception(self, mock_execute_command):
        """Test image inspection with exception."""
        # Mock the execute_command function to raise an exception
        mock_execute_command.side_effect = Exception('Test exception')

        # Call the function
        result = inspect_image('test:latest')

        # Verify the result
        self.assertEqual(result['status'], 'error')
        self.assertEqual(result['message'], 'Error inspecting image: Test exception')

        # Verify the command was called correctly
        mock_execute_command.assert_called_once_with(['finch', 'image', 'inspect', 'test:latest'])


if __name__ == '__main__':
    unittest.main()
