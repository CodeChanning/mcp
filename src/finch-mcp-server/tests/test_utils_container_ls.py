"""Tests for the container_ls utility."""

from awslabs.finch_mcp_server.consts import STATUS_ERROR, STATUS_SUCCESS
from awslabs.finch_mcp_server.utils.container_ls import list_containers
from unittest.mock import MagicMock, patch


class TestContainerLs:
    """Tests for the container_ls utility."""

    @patch('awslabs.finch_mcp_server.utils.container_ls.execute_command')
    def test_list_containers_success(self, mock_execute_command):
        """Test successful container listing."""
        # Mock the execute_command function to return a successful result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = '{"ID":"test-container-1","Image":"python:3.9-alpine","Command":"python app.py","Created":"2023-01-01 12:00:00","Status":"Up 2 hours","Ports":"8080/tcp","Names":"my-python-app"}\n{"ID":"test-container-2","Image":"nginx:latest","Command":"nginx -g daemon off;","Created":"2023-01-02 12:00:00","Status":"Up 1 hour","Ports":"80/tcp, 443/tcp","Names":"my-nginx"}'
        mock_execute_command.return_value = mock_result

        # Call the function
        result = list_containers()

        # Verify the result
        assert result['status'] == STATUS_SUCCESS
        assert 'Successfully listed 2 containers' in result['message']
        assert len(result['containers']) == 2
        assert result['containers'][0]['Image'] == 'python:3.9-alpine'
        assert result['containers'][1]['Image'] == 'nginx:latest'

        # Verify the command was called correctly
        mock_execute_command.assert_called_once_with(
            ['finch', 'container', 'ls', '--format', 'json']
        )

    @patch('awslabs.finch_mcp_server.utils.container_ls.execute_command')
    def test_list_containers_all(self, mock_execute_command):
        """Test container listing with all_containers=True."""
        # Mock the execute_command function to return a successful result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = '{"ID":"test-container-1","Image":"python:3.9-alpine","Command":"python app.py","Created":"2023-01-01 12:00:00","Status":"Up 2 hours","Ports":"8080/tcp","Names":"my-python-app"}\n{"ID":"test-container-2","Image":"nginx:latest","Command":"nginx -g daemon off;","Created":"2023-01-02 12:00:00","Status":"Exited (0) 1 hour ago","Ports":"80/tcp, 443/tcp","Names":"my-nginx"}'
        mock_execute_command.return_value = mock_result

        # Call the function with all_containers=True
        result = list_containers(all_containers=True)

        # Verify the result
        assert result['status'] == STATUS_SUCCESS
        assert 'Successfully listed 2 containers' in result['message']
        assert len(result['containers']) == 2
        assert result['containers'][0]['Status'] == 'Up 2 hours'
        assert result['containers'][1]['Status'] == 'Exited (0) 1 hour ago'

        # Verify the command was called correctly with -a flag
        mock_execute_command.assert_called_once_with(
            ['finch', 'container', 'ls', '--format', 'json', '-a']
        )

    @patch('awslabs.finch_mcp_server.utils.container_ls.execute_command')
    def test_list_containers_filter(self, mock_execute_command):
        """Test container listing with filter_expr."""
        # Mock the execute_command function to return a successful result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = '{"ID":"test-container-1","Image":"python:3.9-alpine","Command":"python app.py","Created":"2023-01-01 12:00:00","Status":"Up 2 hours","Ports":"8080/tcp","Names":"my-python-app"}'
        mock_execute_command.return_value = mock_result

        # Call the function with filter_expr
        result = list_containers(filter_expr=['status=running', 'label=app=web'])

        # Verify the result
        assert result['status'] == STATUS_SUCCESS
        assert 'Successfully listed 1 containers' in result['message']
        assert len(result['containers']) == 1
        assert result['containers'][0]['Image'] == 'python:3.9-alpine'

        # Verify the command was called correctly with -f flags
        mock_execute_command.assert_called_once_with(
            [
                'finch',
                'container',
                'ls',
                '--format',
                'json',
                '-f',
                'status=running',
                '-f',
                'label=app=web',
            ]
        )

    @patch('awslabs.finch_mcp_server.utils.container_ls.execute_command')
    def test_list_containers_last(self, mock_execute_command):
        """Test container listing with last parameter."""
        # Mock the execute_command function to return a successful result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = '{"ID":"test-container-2","Image":"nginx:latest","Command":"nginx -g daemon off;","Created":"2023-01-02 12:00:00","Status":"Up 1 hour","Ports":"80/tcp, 443/tcp","Names":"my-nginx"}'
        mock_execute_command.return_value = mock_result

        # Call the function with last=1
        result = list_containers(last=1)

        # Verify the result
        assert result['status'] == STATUS_SUCCESS
        assert 'Successfully listed 1 containers' in result['message']
        assert len(result['containers']) == 1
        assert result['containers'][0]['Image'] == 'nginx:latest'

        # Verify the command was called correctly with -n flag
        mock_execute_command.assert_called_once_with(
            ['finch', 'container', 'ls', '--format', 'json', '-n', '1']
        )

    @patch('awslabs.finch_mcp_server.utils.container_ls.execute_command')
    def test_list_containers_latest(self, mock_execute_command):
        """Test container listing with latest=True."""
        # Mock the execute_command function to return a successful result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = '{"ID":"test-container-2","Image":"nginx:latest","Command":"nginx -g daemon off;","Created":"2023-01-02 12:00:00","Status":"Up 1 hour","Ports":"80/tcp, 443/tcp","Names":"my-nginx"}'
        mock_execute_command.return_value = mock_result

        # Call the function with latest=True
        result = list_containers(latest=True)

        # Verify the result
        assert result['status'] == STATUS_SUCCESS
        assert 'Successfully listed 1 containers' in result['message']
        assert len(result['containers']) == 1
        assert result['containers'][0]['Image'] == 'nginx:latest'

        # Verify the command was called correctly with -l flag
        mock_execute_command.assert_called_once_with(
            ['finch', 'container', 'ls', '--format', 'json', '-l']
        )

    @patch('awslabs.finch_mcp_server.utils.container_ls.execute_command')
    def test_list_containers_no_trunc(self, mock_execute_command):
        """Test container listing with no_trunc=True."""
        # Mock the execute_command function to return a successful result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = '{"ID":"test-container-full-id","Image":"python:3.9-alpine","Command":"python app.py","Created":"2023-01-01 12:00:00","Status":"Up 2 hours","Ports":"8080/tcp","Names":"my-python-app"}'
        mock_execute_command.return_value = mock_result

        # Call the function with no_trunc=True
        result = list_containers(no_trunc=True)

        # Verify the result
        assert result['status'] == STATUS_SUCCESS
        assert 'Successfully listed 1 containers' in result['message']
        assert len(result['containers']) == 1
        assert result['containers'][0]['ID'] == 'test-container-full-id'

        # Verify the command was called correctly with --no-trunc flag
        mock_execute_command.assert_called_once_with(
            ['finch', 'container', 'ls', '--format', 'json', '--no-trunc']
        )

    @patch('awslabs.finch_mcp_server.utils.container_ls.execute_command')
    def test_list_containers_quiet(self, mock_execute_command):
        """Test container listing with quiet=True."""
        # Mock the execute_command function to return a successful result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = '{"ID":"test-container-1"}\n{"ID":"test-container-2"}'
        mock_execute_command.return_value = mock_result

        # Call the function with quiet=True
        result = list_containers(quiet=True)

        # Verify the result
        assert result['status'] == STATUS_SUCCESS
        assert 'Successfully listed 2 containers' in result['message']
        assert len(result['containers']) == 2
        assert 'ID' in result['containers'][0]
        assert 'Image' not in result['containers'][0]

        # Verify the command was called correctly with -q flag
        mock_execute_command.assert_called_once_with(
            ['finch', 'container', 'ls', '--format', 'json', '-q']
        )

    @patch('awslabs.finch_mcp_server.utils.container_ls.execute_command')
    def test_list_containers_size(self, mock_execute_command):
        """Test container listing with size=True."""
        # Mock the execute_command function to return a successful result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = '{"ID":"test-container-1","Image":"python:3.9-alpine","Command":"python app.py","Created":"2023-01-01 12:00:00","Status":"Up 2 hours","Ports":"8080/tcp","Names":"my-python-app","Size":"10MB"}'
        mock_execute_command.return_value = mock_result

        # Call the function with size=True
        result = list_containers(size=True)

        # Verify the result
        assert result['status'] == STATUS_SUCCESS
        assert 'Successfully listed 1 containers' in result['message']
        assert len(result['containers']) == 1
        assert result['containers'][0]['Size'] == '10MB'

        # Verify the command was called correctly with -s flag
        mock_execute_command.assert_called_once_with(
            ['finch', 'container', 'ls', '--format', 'json', '-s']
        )

    @patch('awslabs.finch_mcp_server.utils.container_ls.execute_command')
    def test_list_containers_multiple_options(self, mock_execute_command):
        """Test container listing with multiple options."""
        # Mock the execute_command function to return a successful result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = '{"ID":"test-container-1","Image":"python:3.9-alpine","Command":"python app.py","Created":"2023-01-01 12:00:00","Status":"Up 2 hours","Ports":"8080/tcp","Names":"my-python-app","Size":"10MB"}'
        mock_execute_command.return_value = mock_result

        # Call the function with multiple options
        result = list_containers(all_containers=True, size=True, no_trunc=True)

        # Verify the result
        assert result['status'] == STATUS_SUCCESS
        assert 'Successfully listed 1 containers' in result['message']
        assert len(result['containers']) == 1

        # Verify the command was called correctly with all flags
        mock_execute_command.assert_called_once_with(
            ['finch', 'container', 'ls', '--format', 'json', '-a', '--no-trunc', '-s']
        )

    @patch('awslabs.finch_mcp_server.utils.container_ls.execute_command')
    def test_list_containers_error(self, mock_execute_command):
        """Test container listing when command returns an error."""
        # Mock the execute_command function to return an error
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = 'Error: failed to list containers'
        mock_execute_command.return_value = mock_result

        # Call the function
        result = list_containers()

        # Verify the result
        assert result['status'] == STATUS_ERROR
        assert 'Failed to list containers' in result['message']

        # Verify the command was called correctly
        mock_execute_command.assert_called_once_with(
            ['finch', 'container', 'ls', '--format', 'json']
        )

    @patch('awslabs.finch_mcp_server.utils.container_ls.execute_command')
    def test_list_containers_json_decode_error(self, mock_execute_command):
        """Test container listing when JSON parsing fails."""
        # Mock the execute_command function to return invalid JSON
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = 'Invalid JSON'
        mock_execute_command.return_value = mock_result

        # Mock the fallback command
        mock_fallback_result = MagicMock()
        mock_fallback_result.returncode = 0
        mock_fallback_result.stdout = 'CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES\ntest-container-1   python:3.9-alpine   python app.py   2023-01-01 12:00:00   Up 2 hours   8080/tcp   my-python-app'
        mock_execute_command.side_effect = [mock_result, mock_fallback_result]

        # Call the function
        result = list_containers()

        # Verify the result
        assert result['status'] == STATUS_SUCCESS
        assert 'Successfully listed 1 containers (plain text format)' in result['message']
        assert 'containers_text' in result

        # Verify both commands were called
        assert mock_execute_command.call_count == 2
        mock_execute_command.assert_any_call(['finch', 'container', 'ls', '--format', 'json'])
        mock_execute_command.assert_any_call(['finch', 'container', 'ls'])

    @patch('awslabs.finch_mcp_server.utils.container_ls.execute_command')
    def test_list_containers_json_decode_error_fallback_error(self, mock_execute_command):
        """Test container listing when JSON parsing fails and fallback also fails."""
        # Mock the execute_command function to return invalid JSON
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = 'Invalid JSON'

        # Mock the fallback command to also fail
        mock_fallback_result = MagicMock()
        mock_fallback_result.returncode = 1
        mock_fallback_result.stderr = 'Error: failed to list containers'

        mock_execute_command.side_effect = [mock_result, mock_fallback_result]

        # Call the function
        result = list_containers()

        # Verify the result
        assert result['status'] == STATUS_ERROR
        assert 'Failed to list containers' in result['message']

        # Verify both commands were called
        assert mock_execute_command.call_count == 2
        mock_execute_command.assert_any_call(['finch', 'container', 'ls', '--format', 'json'])
        mock_execute_command.assert_any_call(['finch', 'container', 'ls'])

    @patch('awslabs.finch_mcp_server.utils.container_ls.execute_command')
    def test_list_containers_exception(self, mock_execute_command):
        """Test container listing when an exception occurs."""
        # Mock the execute_command function to raise an exception
        mock_execute_command.side_effect = Exception('Unexpected error')

        # Call the function
        result = list_containers()

        # Verify the result
        assert result['status'] == STATUS_ERROR
        assert 'Error listing containers: Unexpected error' in result['message']

        # Verify the command was called
        mock_execute_command.assert_called_once_with(
            ['finch', 'container', 'ls', '--format', 'json']
        )
