"""Tests for YouTube Transcript MCP Server."""

import pytest

from server import (
    extract_video_id,
)


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
