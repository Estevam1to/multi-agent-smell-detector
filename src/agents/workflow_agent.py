from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph_supervisor import create_supervisor

from src.config.settings import Settings

from .security_agent import security_agent
from .static_analizer_agent import static_agent

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    google_api_key=Settings().API_KEY,
)


supervisor = create_supervisor(
    agents=[static_agent, security_agent],
    model=llm,
    tools=[],
    prompt="""You are the Agent Supervisor. Your role is to monitor and validate the output of static and security agents, ensuring:

    1. **Functionality**: Verify that each agent correctly fulfilled its task.
    2. **Security**: Identify and remediate security vulnerabilities in the code.
    3. **Quality**: Detect and fix code smells and poor practices.
    4. **Feedback**: For each agent:
    - If correct, confirm success and move to the next task.
    - If there is a failure or risk, present:
        a) Problem diagnosis.
        b) Adjusted code or clear instructions for correction.

    **Response format**:
    - List the verified points (Functionality, Security, Quality).
    - Include, when necessary, corrected code snippets.
    - End with next steps instructions or recommendations.

    Be objective, structured, and maintain a collaborative tone.
    """,
)

supervisor = supervisor.compile()