"""Tests for YouTube Transcript MCP Server."""

import pytest
from unittest.mock import patch, AsyncMock
from fastmcp import Client
from ytt_mcp import mcp, extract_video_id


class TestExtractVideoId:
    """Test video ID extraction."""

    def test_extract_from_watch_url(self) -> None:
        """Test extracting ID from watch URL."""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        assert extract_video_id(url) == "dQw4w9WgXcQ"

    def test_extract_from_short_url(self) -> None:
        """Test extracting ID from short URL."""
        url = "https://youtu.be/dQw4w9WgXcQ"
        assert extract_video_id(url) == "dQw4w9WgXcQ"

    def test_extract_from_embed_url(self) -> None:
        """Test extracting ID from embed URL."""
        url = "https://www.youtube.com/embed/dQw4w9WgXcQ"
        assert extract_video_id(url) == "dQw4w9WgXcQ"

    def test_return_video_id_directly(self) -> None:
        """Test returning video ID when already provided."""
        video_id = "dQw4w9WgXcQ"
        assert extract_video_id(video_id) == video_id

    def test_invalid_url_raises_error(self) -> None:
        """Test that invalid URL raises ValueError."""
        with pytest.raises(ValueError, match="Invalid YouTube URL"):
            extract_video_id("not-a-valid-url")


async def test_youtube_transcript_mcp_server():
    """Test the get_youtube_transcript function with a mocked transcript fetch."""
    mock_transcript = "This is a test transcript"

    with patch(
        "ytt_mcp.fetch_youtube_transcript", new_callable=AsyncMock
    ) as mock_fetch:
        mock_fetch.return_value = mock_transcript

        async with Client(mcp) as client:
            tools = await client.list_tools()
            assert len(tools) == 1
            assert tools[0].name == "get_youtube_transcript"

            result = await client.call_tool(
                "get_youtube_transcript",
                {"url": "https://youtube.com/watch?v=dQw4w9WgXcQ"},
            )
            print(result)
            assert result[0].text == mock_transcript
            mock_fetch.assert_called_once_with("dQw4w9WgXcQ", "en")


async def test_youtube_transcript_mcp_server_with_french():
    """Test the get_youtube_transcript function with French language parameter."""
    mock_transcript_french = "Ceci est une transcription de test en français"

    with patch(
        "ytt_mcp.fetch_youtube_transcript", new_callable=AsyncMock
    ) as mock_fetch:
        mock_fetch.return_value = mock_transcript_french

        async with Client(mcp) as client:
            result = await client.call_tool(
                "get_youtube_transcript",
                {"url": "https://youtube.com/watch?v=dQw4w9WgXcQ", "lang": "fr"},
            )
            assert result[0].text == mock_transcript_french
            mock_fetch.assert_called_once_with("dQw4w9WgXcQ", "fr")


async def test_youtube_transcript_invalid_language():
    """Test that invalid language codes are rejected by Pydantic validation."""
    async with Client(mcp) as client:
        with pytest.raises(Exception, match="validation error"):
            await client.call_tool(
                "get_youtube_transcript",
                {
                    "url": "https://youtube.com/watch?v=dQw4w9WgXcQ",
                    "lang": "invalid-lang",
                },
            )
