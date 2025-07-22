"""Tests for the container_inspect utility."""

from awslabs.finch_mcp_server.utils.container_inspect import inspect_container
from unittest.mock import MagicMock, patch


class TestContainerInspect:
    """Tests for the container_inspect utility."""

    @patch('awslabs.finch_mcp_server.utils.container_inspect.execute_command')
    def test_inspect_container_success(self, mock_execute_command):
        """Test successful container inspection."""
        # Mock the execute_command function to return a successful result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = '[{"Id":"test-container-id-1","Name":"/test-container","State":{"Status":"running","Running":true},"Config":{"Image":"python:3.9-alpine"}}]'
        mock_execute_command.return_value = mock_result

        # Call the function
        result = inspect_container('test-container')

        # Verify the result
        assert result['status'] == 'success'
        assert 'Successfully inspected container test-container' in result['message']
        assert 'raw_output' in result
        assert result['raw_output'] == mock_result.stdout

        # Verify the command was called correctly
        mock_execute_command.assert_called_once_with(
            ['finch', 'container', 'inspect', '--format', 'json', 'test-container']
        )

    @patch('awslabs.finch_mcp_server.utils.container_inspect.execute_command')
    def test_inspect_container_with_format(self, mock_execute_command):
        """Test container inspection with custom format."""
        # Mock the execute_command function to return a successful result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = 'running'
        mock_execute_command.return_value = mock_result

        # Call the function with custom format
        result = inspect_container('test-container', format_str='{{.State.Status}}')

        # Verify the result
        assert result['status'] == 'success'
        assert 'Successfully inspected container test-container' in result['message']
        assert 'raw_output' in result
        assert result['raw_output'] == 'running'

        # Verify the command was called correctly with custom format
        mock_execute_command.assert_called_once_with(
            ['finch', 'container', 'inspect', '--format', '{{.State.Status}}', 'test-container']
        )

    @patch('awslabs.finch_mcp_server.utils.container_inspect.execute_command')
    def test_inspect_container_by_id(self, mock_execute_command):
        """Test container inspection by container ID."""
        # Mock the execute_command function to return a successful result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = '[{"Id":"test-container-id-1","Name":"/test-container","State":{"Status":"running","Running":true}}]'
        mock_execute_command.return_value = mock_result

        # Call the function with container ID
        result = inspect_container('test-container-id-1')

        # Verify the result
        assert result['status'] == 'success'
        assert 'Successfully inspected container test-container-id-1' in result['message']
        assert 'raw_output' in result
        assert result['raw_output'] == mock_result.stdout

        # Verify the command was called correctly
        mock_execute_command.assert_called_once_with(
            ['finch', 'container', 'inspect', '--format', 'json', 'test-container-id-1']
        )

    @patch('awslabs.finch_mcp_server.utils.container_inspect.execute_command')
    def test_inspect_container_error(self, mock_execute_command):
        """Test container inspection when command returns an error."""
        # Mock the execute_command function to return an error
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = 'Error: No such container: nonexistent-container'
        mock_execute_command.return_value = mock_result

        # Call the function
        result = inspect_container('nonexistent-container')

        # Verify the result
        assert result['status'] == 'error'
        assert 'Failed to inspect container' in result['message']
        assert 'No such container' in result['message']

        # Verify the command was called correctly
        mock_execute_command.assert_called_once_with(
            ['finch', 'container', 'inspect', '--format', 'json', 'nonexistent-container']
        )

    @patch('awslabs.finch_mcp_server.utils.container_inspect.execute_command')
    def test_inspect_container_exception(self, mock_execute_command):
        """Test container inspection when an exception occurs."""
        # Mock the execute_command function to raise an exception
        mock_execute_command.side_effect = Exception('Unexpected error')

        # Call the function
        result = inspect_container('test-container')

        # Verify the result
        assert result['status'] == 'error'
        assert 'Error inspecting container: Unexpected error' in result['message']

        # Verify the command was called
        mock_execute_command.assert_called_once_with(
            ['finch', 'container', 'inspect', '--format', 'json', 'test-container']
        )

    @patch('awslabs.finch_mcp_server.utils.container_inspect.execute_command')
    def test_inspect_container_empty_output(self, mock_execute_command):
        """Test container inspection with empty output."""
        # Mock the execute_command function to return empty output
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ''
        mock_execute_command.return_value = mock_result

        # Call the function
        result = inspect_container('test-container')

        # Verify the result
        assert result['status'] == 'success'
        assert 'Successfully inspected container test-container' in result['message']
        assert 'raw_output' in result
        assert result['raw_output'] == ''

        # Verify the command was called correctly
        mock_execute_command.assert_called_once_with(
            ['finch', 'container', 'inspect', '--format', 'json', 'test-container']
        )
