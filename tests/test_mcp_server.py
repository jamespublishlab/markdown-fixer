#!/usr/bin/env python3
"""Tests for MCP server."""

from markdown_fixer.mcp_server import MarkdownFixerMCPServer


class TestServerInitialization:
    """Test server initialization."""

    def test_server_creates_successfully(self):
        """Server should initialize without errors."""
        server = MarkdownFixerMCPServer()
        assert server is not None
        assert server.fixer is not None

    def test_server_info_has_correct_fields(self):
        """Server info should have name and version."""
        server = MarkdownFixerMCPServer()
        assert "name" in server.server_info
        assert "version" in server.server_info
        assert server.server_info["name"] == "markdown-fixer"


class TestToolDefinitions:
    """Test that tool definitions are valid."""

    def test_tools_list_returns_valid_response(self):
        """tools/list should return proper JSON-RPC response."""
        server = MarkdownFixerMCPServer()
        response = server._handle_tools_list(request_id=1)

        # Should have JSON-RPC fields
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 1
        assert "result" in response

        # Result should have tools array
        result = response["result"]
        assert "tools" in result
        assert isinstance(result["tools"], list)

    def test_all_tools_have_required_fields(self):
        """Each tool should have name, description, and inputSchema."""
        server = MarkdownFixerMCPServer()
        response = server._handle_tools_list(request_id=1)
        tools = response["result"]["tools"]

        assert len(tools) == 3  # Should have 3 tools

        for tool in tools:
            assert "name" in tool
            assert "description" in tool
            assert "inputSchema" in tool
            assert isinstance(tool["name"], str)
            assert isinstance(tool["description"], str)
            assert isinstance(tool["inputSchema"], dict)

    def test_input_schemas_are_valid(self):
        """Each tool's inputSchema should be valid JSON Schema."""
        server = MarkdownFixerMCPServer()
        response = server._handle_tools_list(request_id=1)
        tools = response["result"]["tools"]

        for tool in tools:
            schema = tool["inputSchema"]
            assert schema["type"] == "object"
            assert "properties" in schema
            assert "required" in schema
            assert isinstance(schema["properties"], dict)
            assert isinstance(schema["required"], list)

    def test_tool_names_are_correct(self):
        """Should have the expected tool names."""
        server = MarkdownFixerMCPServer()
        response = server._handle_tools_list(request_id=1)
        tools = response["result"]["tools"]

        tool_names = {tool["name"] for tool in tools}
        expected_names = {"fix_markdown", "fix_markdown_file", "preview_markdown_fixes"}
        assert tool_names == expected_names


class TestFixMarkdownTool:
    """Test fix_markdown tool."""

    def test_fix_markdown_with_valid_content(self):
        """Should fix markdown content and return proper response."""
        server = MarkdownFixerMCPServer()
        arguments = {"content": "**Name:** John\n**Age:** 30"}

        response = server._fix_markdown(request_id=1, arguments=arguments)

        # Should be valid JSON-RPC response
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 1
        assert "result" in response

        # Result should have content array
        result = response["result"]
        assert "content" in result
        assert isinstance(result["content"], list)
        assert len(result["content"]) > 0

        # First content item should be text
        content_item = result["content"][0]
        assert content_item["type"] == "text"
        assert "text" in content_item

        # Should have isError flag
        assert "isError" in result
        assert result["isError"] is False

    def test_fix_markdown_with_empty_content(self):
        """Should return error for empty content."""
        server = MarkdownFixerMCPServer()
        arguments = {"content": ""}

        response = server._fix_markdown(request_id=1, arguments=arguments)

        # Should be error response
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 1
        assert "error" in response
        assert response["error"]["code"] == -32602

    def test_fix_markdown_converts_field_metadata(self):
        """Should convert consecutive field metadata to bullets."""
        server = MarkdownFixerMCPServer()
        content = "**Name:** John\n**Age:** 30"
        arguments = {"content": content}

        response = server._fix_markdown(request_id=1, arguments=arguments)
        result_text = response["result"]["content"][0]["text"]

        # Should have bullets
        assert "- **Name:** John" in result_text
        assert "- **Age:** 30" in result_text


class TestFixMarkdownFileTool:
    """Test fix_markdown_file tool."""

    def test_fix_markdown_file_with_missing_file(self):
        """Should return error for non-existent file."""
        server = MarkdownFixerMCPServer()
        arguments = {"filepath": "/nonexistent/file.md"}

        response = server._fix_markdown_file(request_id=1, arguments=arguments)

        # Should be error response
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 1
        assert "error" in response
        assert response["error"]["code"] == -32602

    def test_fix_markdown_file_with_empty_filepath(self):
        """Should return error for empty filepath."""
        server = MarkdownFixerMCPServer()
        arguments = {"filepath": ""}

        response = server._fix_markdown_file(request_id=1, arguments=arguments)

        # Should be error response
        assert "error" in response
        assert response["error"]["code"] == -32602

    def test_fix_markdown_file_with_valid_file(self, tmp_path):
        """Should fix markdown file and return success response."""
        # Create temp markdown file
        test_file = tmp_path / "test.md"
        test_file.write_text("**Name:** John\n**Age:** 30")

        server = MarkdownFixerMCPServer()
        arguments = {"filepath": str(test_file), "in_place": True}

        response = server._fix_markdown_file(request_id=1, arguments=arguments)

        # Should be success response
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 1
        assert "result" in response

        result = response["result"]
        assert "content" in result
        assert result["isError"] is False

        # File should be modified
        fixed_content = test_file.read_text()
        assert "- **Name:** John" in fixed_content


class TestPreviewMarkdownFixesTool:
    """Test preview_markdown_fixes tool."""

    def test_preview_with_valid_content(self):
        """Should preview fixes and return proper response."""
        server = MarkdownFixerMCPServer()
        arguments = {"content": "**Name:** John\n**Age:** 30"}

        response = server._preview_fixes(request_id=1, arguments=arguments)

        # Should be valid response
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 1
        assert "result" in response

        result = response["result"]
        assert "content" in result
        assert result["isError"] is False

        # Should show preview info
        preview_text = result["content"][0]["text"]
        assert "Preview" in preview_text or "Fixed content" in preview_text

    def test_preview_with_no_changes_needed(self):
        """Should indicate when no changes are needed."""
        server = MarkdownFixerMCPServer()
        # Already properly formatted markdown
        arguments = {"content": "# Test\n\n- Item 1\n- Item 2"}

        response = server._preview_fixes(request_id=1, arguments=arguments)

        result = response["result"]
        preview_text = result["content"][0]["text"]
        assert "No formatting changes needed" in preview_text

    def test_preview_with_empty_content(self):
        """Should return error for empty content."""
        server = MarkdownFixerMCPServer()
        arguments = {"content": ""}

        response = server._preview_fixes(request_id=1, arguments=arguments)

        assert "error" in response
        assert response["error"]["code"] == -32602


class TestRequestHandling:
    """Test request handling."""

    def test_handle_initialize_request(self):
        """Should handle initialize request."""
        server = MarkdownFixerMCPServer()
        request = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}

        response = server.handle_request(request)

        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 1
        assert "result" in response
        assert "capabilities" in response["result"]
        assert "serverInfo" in response["result"]

    def test_handle_tools_list_request(self):
        """Should handle tools/list request."""
        server = MarkdownFixerMCPServer()
        request = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}

        response = server.handle_request(request)

        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 2
        assert "result" in response
        assert "tools" in response["result"]

    def test_handle_tools_call_request(self):
        """Should handle tools/call request."""
        server = MarkdownFixerMCPServer()
        request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "fix_markdown", "arguments": {"content": "**Test:** value"}},
        }

        response = server.handle_request(request)

        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 3
        assert "result" in response

    def test_handle_unknown_method(self):
        """Should return error for unknown method."""
        server = MarkdownFixerMCPServer()
        request = {"jsonrpc": "2.0", "id": 4, "method": "unknown_method", "params": {}}

        response = server.handle_request(request)

        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 4
        assert "error" in response
        assert response["error"]["code"] == -32601  # Method not found

    def test_handle_notification_without_id(self):
        """Should return None for notifications (no id)."""
        server = MarkdownFixerMCPServer()
        request = {"jsonrpc": "2.0", "method": "some_notification", "params": {}}

        response = server.handle_request(request)

        # Notifications should not get a response
        assert response is None


class TestErrorHandling:
    """Test error handling."""

    def test_error_response_format(self):
        """Error responses should have correct format."""
        server = MarkdownFixerMCPServer()
        error = server._error_response(request_id=1, code=-32602, message="Invalid params")

        assert error["jsonrpc"] == "2.0"
        assert error["id"] == 1
        assert "error" in error
        assert error["error"]["code"] == -32602
        assert error["error"]["message"] == "Invalid params"

    def test_handle_request_exception(self):
        """Should handle exceptions gracefully."""
        server = MarkdownFixerMCPServer()
        # Request with invalid structure
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "nonexistent_tool", "arguments": {}},
        }

        response = server.handle_request(request)

        # Should return error response, not crash
        assert "error" in response
