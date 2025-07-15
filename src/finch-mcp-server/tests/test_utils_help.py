"""Tests for the help utility."""

from awslabs.finch_mcp_server.consts import STATUS_ERROR, STATUS_SUCCESS
from awslabs.finch_mcp_server.utils.help import get_help
from unittest.mock import MagicMock, patch


class TestHelp:
    """Tests for the help utility."""

    @patch('awslabs.finch_mcp_server.utils.help.execute_command')
    def test_get_help_success(self, mock_execute_command):
        """Test successful help retrieval."""
        # Mock the execute_command function to return a successful result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = (
            'Finch - Container management tool\n\nUsage: finch [command] [options]'
        )
        mock_execute_command.return_value = mock_result

        # Call the function
        result = get_help()

        # Verify the result
        assert result['status'] == STATUS_SUCCESS
        assert 'Successfully retrieved Finch help' in result['message']
        assert 'Finch - Container management tool' in result['help_text']

        # Verify the command was called correctly
        mock_execute_command.assert_called_once_with(['finch', '--help'])

    @patch('awslabs.finch_mcp_server.utils.help.execute_command')
    def test_get_help_with_command_success(self, mock_execute_command):
        """Test successful help retrieval for a specific command."""
        # Mock the execute_command function to return a successful result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = (
            'Finch image - Manage container images\n\nUsage: finch image [command] [options]'
        )
        mock_execute_command.return_value = mock_result

        # Call the function with a command
        result = get_help('image')

        # Verify the result
        assert result['status'] == STATUS_SUCCESS
        assert 'Successfully retrieved Finch help for image' in result['message']
        assert 'Finch image - Manage container images' in result['help_text']

        # Verify the command was called correctly
        mock_execute_command.assert_called_once_with(['finch', 'image', '--help'])

    @patch('awslabs.finch_mcp_server.utils.help.execute_command')
    def test_get_help_error(self, mock_execute_command):
        """Test help retrieval when command returns an error."""
        # Mock the execute_command function to return an error
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = 'Error: unknown command'
        mock_execute_command.return_value = mock_result

        # Call the function
        result = get_help()

        # Verify the result
        assert result['status'] == STATUS_ERROR
        assert 'Failed to get help' in result['message']

        # Verify the command was called correctly
        mock_execute_command.assert_called_once_with(['finch', '--help'])

    @patch('awslabs.finch_mcp_server.utils.help.execute_command')
    def test_get_help_with_command_error(self, mock_execute_command):
        """Test help retrieval for a specific command when command returns an error."""
        # Mock the execute_command function to return an error
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = 'Error: unknown command "invalid"'
        mock_execute_command.return_value = mock_result

        # Call the function with an invalid command
        result = get_help('invalid')

        # Verify the result
        assert result['status'] == STATUS_ERROR
        assert 'Failed to get help' in result['message']

        # Verify the command was called correctly
        mock_execute_command.assert_called_once_with(['finch', 'invalid', '--help'])

    @patch('awslabs.finch_mcp_server.utils.help.execute_command')
    def test_get_help_exception(self, mock_execute_command):
        """Test help retrieval when an exception occurs."""
        # Mock the execute_command function to raise an exception
        mock_execute_command.side_effect = Exception('Unexpected error')

        # Call the function
        result = get_help()

        # Verify the result
        assert result['status'] == STATUS_ERROR
        assert 'Error getting help: Unexpected error' in result['message']

        # Verify the command was called
        mock_execute_command.assert_called_once_with(['finch', '--help'])
