# ytt-mcp: YouTube Transcript MCP Server

MCP Server to fetch transcripts for YouTube videos.

## Installing and Running
The most convenient way to install and run is to use [uv](https://docs.astral.sh/uv/) and then invoke the package using `uvx`

## Claude Desktop
Go to _Settings_ → _Developer_, and then click on _Edit Config_. This will open the claude-desktop-config.json file in your default editor. Make the following addition

```
{
  "mcpServers": {
    …<rest of the config>…
    "ytt-mcp": {
      "command": "uvx",
      "args": ["ytt-mcp"]
    }
  }
}
```

Relaunch Claude config and try out the server as shown in the screenshot below

<img width="1621" alt="image" src="https://github.com/user-attachments/assets/179e8ee0-524e-4735-a3bc-ff4f8fdb9d08" />


## Raycast
If you are using Raycast, you can install the MCP server by invoking the _Install Server_ command from the MCP extension.

<img width="754" alt="image" src="https://github.com/user-attachments/assets/6488c090-6dd5-4926-b1b5-2ae35bb349bc" />

After that you can refer to the MCP server as `@youtube-transcript` and interact with it. You can also use it in a Raycast AI Command with a prompt. For example, here is a prompt I use to extract and summarize a YouTube URL in the clipboard

```
@youtube-transcript fetch the Youtube transcript of the video: {clipboard | raw}

Comprehensively summarize the transcript with the following format:
"""
### Key Takeaways

- <EXACTLY three bullet points with the key takeaways, keep the bullet points as short as possible>
"""

### Theme Wise Breakdown
<divide the transcript into thematic sections and summarize each section comprehensively. reuse any existing section delimiters the article already has. If not add your own. keep the content of the breakdown in the same order as it appears in the webpage text.>

Some rules to follow precisely:
- ALWAYS capture the perspective and POV of the author
- NEVER come up with additional information
```

See video demo below

https://github.com/user-attachments/assets/e6530768-3483-4cb9-988a-7ec7a999d505

