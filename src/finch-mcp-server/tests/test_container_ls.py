"""Tests for the container_ls functionality."""

import json
import pytest
from awslabs.finch_mcp_server.consts import STATUS_ERROR, STATUS_SUCCESS
from awslabs.finch_mcp_server.server import finch_container_ls
from unittest.mock import patch


class TestContainerLs:
    """Tests for the container_ls functionality."""

    @pytest.mark.asyncio
    async def test_finch_container_ls_success(self):
        """Test successful finch_container_ls resource."""
        with patch('awslabs.finch_mcp_server.server.list_containers') as mock_list_containers:
            mock_list_containers.return_value = {
                'status': STATUS_SUCCESS,
                'message': 'Successfully listed 2 containers',
                'containers': [
                    {
                        'ID': 'test-container-1',
                        'Image': 'python:3.9-alpine',
                        'Command': 'python app.py',
                        'Created': '2023-01-01 12:00:00',
                        'Status': 'Up 2 hours',
                        'Ports': '8080/tcp',
                        'Names': 'my-python-app',
                    },
                    {
                        'ID': 'test-container-2',
                        'Image': 'nginx:latest',
                        'Command': 'nginx -g daemon off;',
                        'Created': '2023-01-02 12:00:00',
                        'Status': 'Up 1 hour',
                        'Ports': '80/tcp, 443/tcp',
                        'Names': 'my-nginx',
                    },
                ],
            }

            result = await finch_container_ls()
            result_json = json.loads(result)

            assert result_json['status'] == STATUS_SUCCESS
            assert 'Successfully listed 2 containers' in result_json['message']
            assert len(result_json['containers']) == 2
            assert result_json['containers'][0]['Image'] == 'python:3.9-alpine'
            assert result_json['containers'][1]['Image'] == 'nginx:latest'

            # Verify that all_containers=True was passed to list_containers
            mock_list_containers.assert_called_once_with(all_containers=True)

    @pytest.mark.asyncio
    async def test_finch_container_ls_error(self):
        """Test finch_container_ls resource when an error occurs."""
        with patch('awslabs.finch_mcp_server.server.list_containers') as mock_list_containers:
            mock_list_containers.return_value = {
                'status': STATUS_ERROR,
                'message': 'Failed to list containers',
            }

            result = await finch_container_ls()
            result_json = json.loads(result)

            assert result_json['status'] == STATUS_ERROR
            assert 'Failed to list containers' in result_json['message']

            mock_list_containers.assert_called_once_with(all_containers=True)

    @pytest.mark.asyncio
    async def test_finch_container_ls_exception(self):
        """Test finch_container_ls resource when an exception occurs."""
        with patch('awslabs.finch_mcp_server.server.list_containers') as mock_list_containers:
            mock_list_containers.side_effect = Exception('Unexpected error')

            result = await finch_container_ls()
            result_json = json.loads(result)

            assert result_json['status'] == STATUS_ERROR
            assert 'Error listing containers' in result_json['message']

            mock_list_containers.assert_called_once_with(all_containers=True)
