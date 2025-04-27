from dotenv import load_dotenv
import os
import praw
import logging
from mcp import StdioServerParameters
from mcpadapt.core import MCPAdapt
from mcpadapt.crewai_adapter import CrewAIAdapter

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_direct_praw():
    logger.info("Testing direct PRAW authentication...")
    
    # Get credentials from environment variables
    client_id = os.getenv('REDDIT_CLIENT_ID')
    client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    
    logger.debug(f"Found client_id: {'Yes' if client_id else 'No'}")
    logger.debug(f"Found client_secret: {'Yes' if client_secret else 'No'}")
    
    try:
        # Initialize the Reddit instance
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent='test_script/1.0'
        )
        
        # Try to make a simple API call
        logger.info("Testing PRAW connection...")
        subreddit = reddit.subreddit('python')
        logger.info(f"Subreddit title: {subreddit.title}")
        print("✅ Direct PRAW authentication successful!")
        
    except Exception as e:
        logger.error("Direct PRAW authentication failed!")
        logger.error(f"Error: {str(e)}")

def test_mcp_adapter():
    logger.info("Testing MCP adapter authentication...")
    try:
        # Initialize adapter
        adapter = MCPAdapt(
            [
                StdioServerParameters(
                    command="uvx",
                    args=["reddit-mcp"],
                    env={"UV_PYTHON": "3.12", **os.environ},
                )
            ],
            CrewAIAdapter(),
        )
        tools = adapter.__enter__()
        
        # Try to use the search_subreddits tool
        logger.info("Testing search_subreddits tool...")
        for tool in tools:
            logger.debug(f"Available tool: {tool.__name__ if hasattr(tool, '__name__') else tool}")
            if hasattr(tool, '__name__') and 'search_subreddits' in tool.__name__.lower():
                search_params = {
                    "by": {
                        "type": "name",
                        "query": "python",
                        "include_nsfw": False,
                        "exact_match": False
                    }
                }
                result = tool(search_params)  # Search for python subreddit as a test
                logger.info(f"Search result: {result}")
                print("✅ MCP adapter authentication successful!")
                break
        
        adapter.close()
        
    except Exception as e:
        logger.error("MCP adapter authentication failed!")
        logger.error(f"Error: {str(e)}")

if __name__ == "__main__":
    load_dotenv()
    print("\n=== Testing Direct PRAW Authentication ===")
    test_direct_praw()
    print("\n=== Testing MCP Adapter Authentication ===")
    test_mcp_adapter() 