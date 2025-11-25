"""
Streamlit AWS Documentation Agent

A web application that uses the AWS Documentation MCP Server to answer
questions about AWS services and documentation.
"""

import os
import streamlit as st
from mcp import StdioServerParameters, stdio_client
from strands import Agent
from strands.tools.mcp import MCPClient

# Load AWS credentials from Streamlit secrets
if "aws_access_key_id" in st.secrets:
    os.environ["AWS_ACCESS_KEY_ID"] = st.secrets["aws_access_key_id"]
if "aws_secret_access_key" in st.secrets:
    os.environ["AWS_SECRET_ACCESS_KEY"] = st.secrets["aws_secret_access_key"]
if "aws_default_region" in st.secrets:
    os.environ["AWS_DEFAULT_REGION"] = st.secrets["aws_default_region"]
else:
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="AWS Documentation Agent",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM STYLING
# ============================================================================

st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# INITIALIZE SESSION STATE
# ============================================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    st.session_state.agent = None
    st.session_state.agent_ready = False

# ============================================================================
# INITIALIZE MCP CLIENT AND AGENT
# ============================================================================

def initialize_agent():
    """Initialize the AWS Documentation agent with MCP tools."""
    try:
        # Create MCP client
        aws_docs_mcp_client = MCPClient(
            lambda: stdio_client(
                StdioServerParameters(
                    command="uvx",
                    args=["awslabs.aws-documentation-mcp-server@latest"]
                )
            )
        )
        
        with aws_docs_mcp_client:
            # Get tools from MCP server
            tools = aws_docs_mcp_client.list_tools_sync()
            
            # Create agent with MCP tools
            agent = Agent(
                model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
                system_prompt="""You are a helpful AWS documentation assistant.

Your capabilities:
1. Search AWS documentation for information
2. Read and summarize AWS documentation pages
3. Get recommendations for related AWS documentation
4. Answer questions about AWS services

When answering questions:
- Use the available tools to search and retrieve AWS documentation
- Provide accurate information based on official AWS docs
- Include relevant links and references when available
- Be concise and helpful
- If you can't find information, say so clearly""",
                tools=tools
            )
            
            return agent, len(tools)
    except Exception as e:
        return None, str(e)

# ============================================================================
# PAGE HEADER
# ============================================================================

st.title("📚 AWS Documentation Agent")
st.markdown("Ask questions about AWS services and get answers from official AWS documentation")

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This agent uses the **AWS Documentation MCP Server** to:
    - Search AWS documentation
    - Read documentation pages
    - Get recommendations
    
    Ask any question about AWS services and the agent will search the official documentation.
    """)
    
    st.divider()
    
    st.header("💡 Example Questions")
    st.markdown("""
    - What is Amazon Bedrock?
    - How do I get started with AWS Lambda?
    - What are the pricing models for S3?
    - Explain AWS EC2 instances
    - What is AWS CloudFormation?
    - How does Amazon RDS work?
    """)
    
    st.divider()
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# ============================================================================
# MAIN CONTENT
# ============================================================================

# Initialize agent if not already done
if not st.session_state.agent_ready:
    with st.spinner("Initializing AWS Documentation Agent..."):
        # Check for AWS credentials
        if not os.environ.get("AWS_ACCESS_KEY_ID"):
            st.error("❌ AWS credentials not found!")
            st.warning("""
            **To deploy on Streamlit Cloud:**
            1. Go to your app settings (⋯ menu)
            2. Click "Secrets"
            3. Add these secrets:
            ```
            aws_access_key_id = "your-access-key"
            aws_secret_access_key = "your-secret-key"
            aws_default_region = "us-east-1"
            ```
            
            **To run locally:**
            Set environment variables:
            ```bash
            export AWS_ACCESS_KEY_ID="your-key"
            export AWS_SECRET_ACCESS_KEY="your-secret"
            export AWS_DEFAULT_REGION="us-east-1"
            streamlit run streamlit_aws_docs_agent.py
            ```
            """)
            st.stop()
        
        agent, result = initialize_agent()
        if agent:
            st.session_state.agent = agent
            st.session_state.agent_ready = True
            st.success(f"✅ Agent initialized! Found {result} tools from AWS Documentation MCP Server")
        else:
            st.error(f"❌ Failed to initialize agent: {result}")
            st.info("""
            Make sure:
            1. `uvx` is installed: `brew install uv`
            2. You have internet connection
            3. AWS Documentation MCP Server is available
            4. AWS credentials are properly configured
            """)
            st.stop()

# ============================================================================
# DISPLAY CHAT HISTORY
# ============================================================================

st.markdown("### 💬 Chat with AWS Documentation Agent")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ============================================================================
# CHAT INPUT
# ============================================================================

user_input = st.chat_input("Ask a question about AWS services...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("Searching AWS documentation..."):
            try:
                response = st.session_state.agent(user_input)
                st.markdown(response)
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                response = error_msg
    
    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 0.8rem;'>
    Powered by Strands Agents + AWS Documentation MCP Server | AWS Docs Agent v1.0
    </div>
    """, unsafe_allow_html=True)
