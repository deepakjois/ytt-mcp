"""YouTube Transcript MCP Server.

A Model Context Protocol server that provides YouTube transcript extraction.
"""

import logging
import re
from typing import Annotated
from urllib.parse import urlparse, parse_qs

from fastmcp import FastMCP
from pydantic import Field
from youtube_transcript_api import (
    YouTubeTranscriptApi,  # pyright: ignore reportPrivateUsage
)
from youtube_transcript_api.formatters import TextFormatter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("youtube-transcript-mcp-server")

# Create server instance
mcp = FastMCP(
    "YouTube Transcript MCP Server",
    instructions="This server provides the transcript of a YouTube video.",
)

# Valid YouTube hostnames
VALID_HOSTNAMES = {
    "www.youtube.com",
    "youtube.com",
    "m.youtube.com",
    "youtu.be",
}

def extract_video_id(url_or_id: str) -> str:
    """Extract YouTube video ID from URL or return ID if already provided.

    Args:
        url_or_id: YouTube URL or video ID

    Returns:
        YouTube video ID

    Raises:
        ValueError: If video ID cannot be extracted or URL is invalid
    """
    # Check if it's already a valid video ID format
    if re.match(r"^[a-zA-Z0-9_-]{11}$", url_or_id):
        return url_or_id

    try:
        parsed = urlparse(url_or_id)
        
        # Validate hostname
        if parsed.netloc not in VALID_HOSTNAMES:
            raise ValueError(f"Invalid YouTube hostname: {parsed.netloc}")

        # Handle different URL patterns
        if parsed.netloc == "youtu.be":
            # Short URL format: youtu.be/VIDEO_ID
            video_id = parsed.path.lstrip("/")
        elif parsed.path.startswith("/shorts/"):
            # Shorts format: youtube.com/shorts/VIDEO_ID
            video_id = parsed.path.split("/")[2]
        elif parsed.path.startswith("/embed/"):
            # Embed format: youtube.com/embed/VIDEO_ID
            video_id = parsed.path.split("/")[2]
        else:
            # Standard watch URL format
            query_params = parse_qs(parsed.query)
            video_id = query_params.get("v", [None])[0]

        # Validate video ID format
        if not video_id or not re.match(r"^[a-zA-Z0-9_-]{11}$", video_id):
            raise ValueError(f"Invalid video ID format in URL: {url_or_id}")

        return video_id

    except Exception as e:
        raise ValueError(f"Invalid YouTube URL or video ID: {url_or_id}") from e


async def fetch_youtube_transcript(video_id: str, lang: str = "en") -> str:
    """Get YouTube transcript for a video ID.

    Args:
        video_id: YouTube video ID
        lang: Language code for transcript (defaults to 'en', e.g., 'en', 'fr', 'de')

    Returns:
        Formatted transcript text

    Raises:
        Exception: If transcript cannot be retrieved
    """
    try:
        transcript = YouTubeTranscriptApi().fetch(video_id, languages=[lang])
        formatter = TextFormatter()
        return formatter.format_transcript(transcript)
    except Exception as e:
        logger.error(f"Failed to get transcript for video {video_id}: {e}")
        raise


@mcp.tool(description="Get the transcript of a YouTube video")
async def get_youtube_transcript(
    url: Annotated[
        str,
        Field(
            description="YouTube URL or video ID",
            examples=["https://youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"],
        ),
    ],
    lang: Annotated[
        str,
        Field(
            default="en",
            description="Language code for transcript (e.g., 'en', 'fr', 'de', 'es')",
            pattern=r"^[a-z]{2}(-[A-Z]{2})?$",
            examples=["en", "fr", "de", "es", "en-US"],
        ),
    ] = "en",
) -> str:
    """Get the transcript of a YouTube video.

    Args:
        url: YouTube URL or video ID
        lang: Language code for transcript (defaults to 'en', e.g., 'en', 'fr', 'de')

    Returns:
        The transcript text

    Raises:
        ValueError: If the URL is invalid or transcript cannot be retrieved
    """
    try:
        video_id = extract_video_id(url)
        transcript = await fetch_youtube_transcript(video_id, lang)
        return transcript
    except ValueError as e:
        raise ValueError(f"Error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error getting transcript: {e}")
        raise ValueError(f"Error retrieving transcript: {e}")


def main():
    mcp.run()


if __name__ == "__main__":
    main()
