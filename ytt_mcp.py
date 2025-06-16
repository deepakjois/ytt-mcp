"""YouTube Transcript MCP Server.

A Model Context Protocol server that provides YouTube transcript extraction.
"""

import asyncio
import logging
import re

from mcp.server.fastmcp import FastMCP
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("youtube-transcript-server")

# Create server instance
mcp = FastMCP("YouTube Transcript Server")


def extract_video_id(url_or_id: str) -> str:
    """Extract YouTube video ID from URL or return ID if already provided.

    Args:
        url_or_id: YouTube URL or video ID

    Returns:
        YouTube video ID

    Raises:
        ValueError: If video ID cannot be extracted
    """
    # Extract video ID from URL if it's a full URL
    video_id_match = re.search(r"(?:v=|/)([a-zA-Z0-9_-]{11})", url_or_id)
    if video_id_match:
        return video_id_match.group(1)

    # Check if it's already a valid video ID format
    if re.match(r"^[a-zA-Z0-9_-]{11}$", url_or_id):
        return url_or_id

    raise ValueError(f"Invalid YouTube URL or video ID: {url_or_id}")


async def fetch_youtube_transcript(video_id: str) -> str:
    """Get YouTube transcript for a video ID.

    Args:
        video_id: YouTube video ID

    Returns:
        Formatted transcript text

    Raises:
        Exception: If transcript cannot be retrieved
    """
    try:
        # Run the blocking API call in a thread pool
        loop = asyncio.get_event_loop()
        transcript = await loop.run_in_executor(
            None, YouTubeTranscriptApi().fetch, video_id
        )

        formatter = TextFormatter()
        return formatter.format_transcript(transcript)
    except Exception as e:
        logger.error(f"Failed to get transcript for video {video_id}: {e}")
        raise


@mcp.tool(description="Get the transcript of a YouTube video")
async def get_youtube_transcript(url: str) -> str:
    """Get the transcript of a YouTube video.

    Args:
        url: YouTube URL or video ID

    Returns:
        The transcript text

    Raises:
        ValueError: If the URL is invalid or transcript cannot be retrieved
    """
    try:
        video_id = extract_video_id(url)
        transcript = await fetch_youtube_transcript(video_id)
        return transcript
    except ValueError as e:
        raise ValueError(f"Error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error getting transcript: {e}")
        raise ValueError(f"Error retrieving transcript: {e}")


if __name__ == "__main__":
    mcp.run()
