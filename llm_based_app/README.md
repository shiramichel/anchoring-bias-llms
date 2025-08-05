# LLM Application Setup Guide

This guide explains how to set up and use the LLM-based application that consists of `llm_based_app.py` and its dependencies.

## Architecture Overview

The application follows a modular structure:

- **`llm_based_app.py`** - Main application file
- **`connect2llm.py`** - Connection module for LLM API integration
- **`.env`** - Environment configuration file containing API credentials and model settings

## Prerequisites

Before running the application, you'll need:

1. Python environment with required dependencies
2. OpenRouter account and API key
3. Minimum $10 credit loaded in your OpenRouter account

## Setup Instructions

### Step 1: Create OpenRouter Account

1. Visit [OpenRouter.ai](https://openrouter.ai/)
2. Create a new account
3. Load your account with a minimum of **$10** credit
4. Navigate to the API section and generate an API key

### Step 2: Check Model Costs

Before selecting a model, review the pricing information:

- Visit the [OpenRouter Models Table](https://openrouter.ai/models?fmt=table)
- Compare different models based on:
  - Cost per token (input/output)
  - Model capabilities
  - Context window size
  - Performance metrics

Choose a model that fits your budget and use case requirements.

### Step 3: Configure Environment Variables

Create a `.env` file in your project root directory with the following structure:

```env
# OpenRouter API Configuration
API_KEY=your_openrouter_api_key_here
MODEL_CHOICE=your_selected_model_name
```

**Important Notes:**
- Replace `your_openrouter_api_key_here` with your actual API key from OpenRouter
- Replace `your_selected_model_name` with your chosen model from the OpenRouter models table
- Keep your `.env` file secure and never commit it to version control
- Add `.env` to your `.gitignore` file

### Step 4: Install Dependencies

Make sure you have the required Python packages installed:

```bash
pip install python-dotenv requests openai
# Add other dependencies as needed
```

## File Structure

Your project should look like this:

```
llm_based_app/
├── llm_based_app.py      # Main application
├── connect2llm.py        # LLM connection module
├── .env                  # Environment variables (not in git)
├── .gitignore           # Include .env here
└── requirements.txt     # Python dependencies
```

## Usage

### Running the Application

```bash
streamlit run llm_based_app.py
```

### How It Works

1. **`llm_based_app.py`** imports the connection module from `connect2llm.py`
2. **`connect2llm.py`** reads configuration from the `.env` file:
   - `OPENROUTER_API_KEY` - Your OpenRouter API key
   - `MODEL_NAME` - The selected LLM model
3. The application establishes a connection to the chosen model via OpenRouter's API
4. Your application logic processes requests through the configured LLM
