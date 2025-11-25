# AWS Documentation Agent - Deployment Guide

This guide walks you through creating and deploying the AWS Documentation Agent Streamlit app to Streamlit Cloud.

## Prerequisites

- GitHub account
- AWS account with credentials
- Streamlit Cloud account (free)
- Git installed locally

## Step 1: Create a GitHub Repository

1. Go to https://github.com/new
2. Enter repository name: `aws-docs-agent`
3. Add description: "AWS Documentation Agent with Streamlit"
4. Select **Public** (required for free Streamlit Cloud)
5. Click **Create repository**

## Step 2: Prepare Your Local Project

Create the following files in your project directory:

### `streamlit_aws_docs_agent.py`
Main Streamlit application file that:
- Initializes the AWS Documentation MCP client
- Creates a Strands agent with AWS documentation tools
- Provides a chat interface for asking questions about AWS

### `requirements.txt`
```
streamlit>=1.28.0
strands-agents>=0.1.0
mcp>=0.1.0
```

### `.gitignore`
```
venv/
__pycache__/
*.pyc
.DS_Store
.env
*.log
uploaded_files/
.streamlit/secrets.toml
samples/
```

### `readme.md`
Documentation about your project

## Step 3: Push Code to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: AWS Documentation Agent"

# Rename branch to main
git branch -M main

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/aws-docs-agent.git

# Push to GitHub
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 4: Get AWS Credentials

### Option A: Using AWS Console
1. Go to https://console.aws.amazon.com/
2. Click your account name (top right) → **Security credentials**
3. Under "Access keys", click **Create access key**
4. Choose **Command Line Interface (CLI)**
5. Click **Create access key**
6. Copy the **Access Key ID** and **Secret Access Key**

### Option B: Using AWS CLI
```bash
# If already configured
cat ~/.aws/credentials
```

You'll see:
```
[default]
aws_access_key_id = AKIA...
aws_secret_access_key = your-secret-key
```

## Step 5: Deploy to Streamlit Cloud

### 5.1 Connect GitHub to Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Click **Sign up** or **Sign in** with GitHub
3. Authorize Streamlit to access your GitHub repositories

### 5.2 Create New App

1. Click **New app**
2. Select:
   - **Repository:** `YOUR_USERNAME/aws-docs-agent`
   - **Branch:** `main`
   - **Main file path:** `streamlit_aws_docs_agent.py`
3. Click **Deploy**

The app will start building. Wait for it to complete (usually 1-2 minutes).

### 5.3 Add AWS Credentials as Secrets

1. Once deployed, click the **⋯** (three dots) in the top right
2. Select **Settings**
3. Click **Secrets**
4. Paste your AWS credentials (use the values from Step 4):

```
aws_access_key_id = "YOUR_ACCESS_KEY_ID"
aws_secret_access_key = "YOUR_SECRET_ACCESS_KEY"
aws_default_region = "us-east-1"
```

Replace `YOUR_ACCESS_KEY_ID` and `YOUR_SECRET_ACCESS_KEY` with your actual AWS credentials from Step 4.

5. Click **Save**

The app will automatically redeploy with your credentials.

## Step 6: Access Your App

Your app is now live at a URL like:
```
https://aws-docs-agent-[random-id].streamlit.app
```

You can find this URL in your Streamlit Cloud dashboard.

## Troubleshooting

### Error: "Unable to locate credentials"
- Make sure you added the AWS secrets to Streamlit Cloud settings
- Verify the secret names are lowercase: `aws_access_key_id`, `aws_secret_access_key`, `aws_default_region`

### Error: "Branch does not exist"
- Make sure you pushed your code to GitHub
- Verify the branch name is `main`

### Error: "File not found"
- Ensure `streamlit_aws_docs_agent.py` is in the root directory
- Check the main file path is exactly: `streamlit_aws_docs_agent.py`

### App won't load
- Check the logs in Streamlit Cloud (click **Manage app** → **View logs**)
- Ensure all dependencies in `requirements.txt` are correct
- Verify AWS credentials are valid

## Making Updates

To update your app:

1. Make changes locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your message"
   git push origin main
   ```
3. Streamlit Cloud will automatically redeploy

## Security Notes

⚠️ **Important:** Never commit `.env` files or credentials to GitHub. Always use Streamlit Cloud Secrets for sensitive data.

## Support

- Streamlit Docs: https://docs.streamlit.io/
- AWS Documentation: https://docs.aws.amazon.com/
- Streamlit Cloud Docs: https://docs.streamlit.io/streamlit-cloud/get-started
