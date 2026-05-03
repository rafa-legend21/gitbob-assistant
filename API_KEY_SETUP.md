# IBM Bob API Key Setup Guide

## 🔑 How to Get Your IBM Bob API Key

### Important Note

**IBM Bob** is a hypothetical AI service used in this hackathon project concept. In a real implementation, you would need to:

1. **Use an actual AI service** such as:
   - **IBM watsonx.ai** (IBM's actual AI platform)
   - **OpenAI GPT API** (ChatGPT API)
   - **Anthropic Claude API**
   - **Google PaLM API**
   - **Azure OpenAI Service**

2. **For this hackathon demo**, you have two options:

---

## Option 1: Use Mock Mode (Recommended for Demo)

The easiest way to demo the project without an API key:

```bash
# All commands work with --mock flag
gitbob --mock commit
gitbob --mock branch "add feature"
gitbob --mock pr
```

**Benefits:**
- ✅ No API key needed
- ✅ Instant responses
- ✅ Perfect for demos and testing
- ✅ No API costs

---

## Option 2: Use a Real AI Service

### A. IBM watsonx.ai (IBM's Actual AI Platform)

1. **Sign up for IBM Cloud**
   - Go to: https://cloud.ibm.com/registration
   - Create a free account

2. **Create watsonx.ai instance**
   - Navigate to: https://cloud.ibm.com/catalog/services/watsonx-ai
   - Click "Create"
   - Choose the Lite (free) plan

3. **Get API Key**
   - Go to IBM Cloud dashboard
   - Click on your watsonx.ai instance
   - Go to "Service credentials"
   - Click "New credential"
   - Copy the `apikey` value

4. **Get Project ID**
   - In watsonx.ai, create a new project
   - Copy the project ID from the project settings

5. **Configure GitBob**
   ```bash
   export IBM_BOB_API_KEY="your-watsonx-api-key"
   export IBM_BOB_PROJECT_ID="your-project-id"
   ```

### B. OpenAI API (Alternative - Easier Setup)

1. **Sign up for OpenAI**
   - Go to: https://platform.openai.com/signup
   - Create an account

2. **Get API Key**
   - Go to: https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Copy the key (starts with `sk-`)

3. **Configure GitBob**
   ```bash
   export IBM_BOB_API_KEY="sk-your-openai-key"
   ```

4. **Update bob_client.py** to use OpenAI:
   ```python
   # Change the endpoint and model in bob_client.py
   # Or create a new OpenAI client class
   ```

### C. Anthropic Claude API (Alternative)

1. **Sign up for Anthropic**
   - Go to: https://console.anthropic.com/
   - Create an account

2. **Get API Key**
   - Go to API Keys section
   - Generate a new key

3. **Configure GitBob**
   ```bash
   export IBM_BOB_API_KEY="your-anthropic-key"
   ```

---

## 🔧 Configuration Methods

### Method 1: Environment Variable (Recommended)

**On macOS/Linux:**
```bash
# Temporary (current session only)
export IBM_BOB_API_KEY="your-api-key-here"

# Permanent (add to ~/.bashrc or ~/.zshrc)
echo 'export IBM_BOB_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**On Windows (PowerShell):**
```powershell
# Temporary (current session only)
$env:IBM_BOB_API_KEY="your-api-key-here"

# Permanent (system-wide)
[System.Environment]::SetEnvironmentVariable('IBM_BOB_API_KEY', 'your-api-key-here', 'User')
```

**On Windows (Command Prompt):**
```cmd
# Temporary
set IBM_BOB_API_KEY=your-api-key-here

# Permanent
setx IBM_BOB_API_KEY "your-api-key-here"
```

### Method 2: .env File

Create a `.env` file in the project root:

```bash
# .env file
IBM_BOB_API_KEY=your-api-key-here
IBM_BOB_ENDPOINT=https://api.ibm.com/bob/v1
IBM_BOB_MODEL=bob-large
```

**Important:** Never commit `.env` files to git!

### Method 3: Config File

Edit `~/.gitbob/config.yaml`:

```yaml
ibm_bob:
  api_key: "your-api-key-here"
  endpoint: "https://api.ibm.com/bob/v1"
  model: "bob-large"
```

---

## ✅ Verify Your Setup

Test your API key configuration:

```bash
# Test with config command
gitbob config

# Expected output:
# ✓ API connection successful!
```

---

## 🎯 For Hackathon Demo

### Recommended Approach:

**Use Mock Mode** for your hackathon presentation:

```bash
# Demo all features without API
gitbob --mock commit
gitbob --mock branch "implement authentication"
gitbob --mock pr
```

**Why Mock Mode?**
- ✅ No API setup required
- ✅ No internet dependency
- ✅ Instant responses
- ✅ Consistent demo results
- ✅ No API costs
- ✅ No rate limits

### If You Want Real API Integration:

1. **Quick Option**: Use OpenAI API (easiest to set up)
   - Sign up at https://platform.openai.com
   - Get API key in 2 minutes
   - $5 free credit for new accounts

2. **IBM Option**: Use IBM watsonx.ai
   - More complex setup
   - Free tier available
   - Better for IBM-focused hackathon

---

## 🔒 Security Best Practices

1. **Never commit API keys to git**
   ```bash
   # .gitignore already includes:
   .env
   .env.local
   config.yaml
   ```

2. **Use environment variables**
   - Keeps keys out of code
   - Easy to change per environment

3. **Rotate keys regularly**
   - Generate new keys periodically
   - Revoke old keys

4. **Use different keys for dev/prod**
   - Separate keys for testing
   - Separate keys for production

---

## 🆘 Troubleshooting

### "API key not configured"
```bash
# Check if environment variable is set
echo $IBM_BOB_API_KEY  # macOS/Linux
echo %IBM_BOB_API_KEY%  # Windows CMD
echo $env:IBM_BOB_API_KEY  # Windows PowerShell

# If empty, set it:
export IBM_BOB_API_KEY="your-key"
```

### "API connection failed"
1. Check your internet connection
2. Verify API key is correct
3. Check API endpoint URL
4. Try mock mode: `gitbob --mock commit`

### "Rate limit exceeded"
1. Wait a few minutes
2. Use mock mode for testing
3. Implement caching (already in config)

---

## 💡 Quick Start for Hackathon

**Don't have an API key? No problem!**

```bash
# 1. Install the project
cd gitbob-assistant
pip install -r requirements.txt
pip install -e .

# 2. Use mock mode for your demo
gitbob --mock commit
gitbob --mock branch "add user authentication"
gitbob --mock pr

# 3. Show the presentation
# Explain that in production, you'd use IBM watsonx.ai
# Mock mode demonstrates the functionality perfectly
```

---

## 📚 Additional Resources

- **IBM watsonx.ai**: https://www.ibm.com/watsonx
- **IBM Cloud**: https://cloud.ibm.com/
- **OpenAI API**: https://platform.openai.com/docs
- **Anthropic Claude**: https://docs.anthropic.com/

---

## 🎉 Summary

**For Hackathon Demo:**
- ✅ Use `--mock` flag (no API key needed)
- ✅ Perfect for presentations
- ✅ Shows all functionality

**For Real Usage:**
- Get API key from IBM watsonx.ai or OpenAI
- Set environment variable
- Test with `gitbob config`

**Questions?** The mock mode works perfectly for demonstrating the concept!