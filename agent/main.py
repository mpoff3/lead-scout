from dotenv import load_dotenv
load_dotenv()

import os
import sys

# Get project URL from sys.argv; exit if not provided
if len(sys.argv) > 1:
    project_url = sys.argv[1]
else:
    print("Usage: python main.py <project_url>")
    print("Example: python main.py https://www.sundai.club/api/projects/a3d5c057-837e-4a87-b4f4-0af74c1db801")
    sys.exit(1)


from crewai import Agent, Crew, Task, LLM
from crewai_tools import ScrapeWebsiteTool

from mcp import StdioServerParameters
from mcpadapt.core import MCPAdapt
from mcpadapt.crewai_adapter import CrewAIAdapter



# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
llm = LLM(
    model=f"gemini/{os.getenv("GEMINI_MODEL")}",
    # model=f"mistral/{os.getenv("MISTRAL_MODEL")}",
    # api_key=os.getenv("MISTRAL_API_KEY"),
    temperature=0.3
)

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

project_summarizer_agent = Agent(
    role="Project Summarizer",
    goal="Summarize the project in a concise paragraph",
    backstory="You are an expert at reading project documentation and summarizing the essence of the project for new team members or stakeholders.",
    verbose=True,
    tools=[ScrapeWebsiteTool()],
    llm=llm,
)
marketing_agent = Agent(
    role="VP of Marketing and Sales",
    goal="Define the problem the project solves",
    backstory="You get a project description, then define the problem it solves for the market, so it can be marketed.",
    verbose=True,
    tools=[],
    llm=llm,
)
reddit_reseach_agent = Agent(
    role="Reddit Researcher",
    goal="Find recent posts where we can promote the project",
    backstory="You help find recent posts where we can promote the project",
    verbose=True,
    tools=tools,
    llm=llm,
)
content_marketing_agent = Agent(
    role="Content Marketing Specialist (Reddit)",
    goal="Draft a Reddit-native comment that subtly promotes our project in a helpful, authentic way, blending into the conversation.",
    backstory="You are a savvy Redditor with a knack for writing comments that add value and gently highlight useful projects without coming off as spammy or corporate. You reference personal experience, curiosity, or practical value, never using overt marketing language.",
    verbose=True,
    tools=[],
    llm=llm,
)

project_summary_task = Task(
    description=f"Summarize the project at the URL '{project_url}' in a concise paragraph.",
    agent=project_summarizer_agent,
    expected_output="A concise summary of the project.",
)
marketing_task = Task(
    description=f"Given the project, define the problem it solves",
    agent=marketing_agent,
    expected_output="The problem this project solves.",
)
reddit_research_task = Task(
    description="Find 1 recent Reddit post where we can promote this project. Return the post's URL and its full text content.",
    agent=reddit_reseach_agent,
    expected_output="A single Reddit post (URL and full text content) where we can promote this project.",
)
content_marketing_task = Task(
    description=f"Given the following Reddit post, draft a native, helpful comment that subtly promotes our project. Don't use any special formatting. Mention the project by name and url {project_url}.",
    agent=content_marketing_agent,
    expected_output="URL of the Reddit post, and a Reddit-native comment that subtly promotes the project.",
)

crew = Crew(
    agents=[project_summarizer_agent, marketing_agent, reddit_reseach_agent, content_marketing_agent],
    tasks=[project_summary_task, marketing_task, reddit_research_task, content_marketing_task],
    verbose=1
)
crew.kickoff()

# Output final answers for each task
output = None
for task in crew.tasks:
    print(f"\n\nTASK: {task.description}")
    print(f"AGENT: {task.agent.role}")
    print(f"FINAL ANSWER:\n{task.output if hasattr(task, 'output') else 'No output available'}")
    output = task.output

adapter.close()

# 

task = "Post this comment to this Reddit post, use https://old.reddit.com UI instead of new UI:\n " + str(output)

from langchain_google_genai import ChatGoogleGenerativeAI

from browser_use import Agent, BrowserConfig, Browser
import asyncio

async def post_comment_to_reddit(task: str):
    llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash-preview-04-17', google_api_key=os.getenv("GEMINI_API_KEY"))

    chrome_instance_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    config = BrowserConfig(
        chrome_instance_path=chrome_instance_path
    )
    browser = Browser(config=config)

    agent = Agent(
        task=task,
        llm=llm,
        browser=browser
    )
    result = await agent.run()
    print(result)


asyncio.run(post_comment_to_reddit(task))