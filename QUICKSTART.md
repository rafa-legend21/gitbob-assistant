# GitBob Assistant - Quick Start Guide

Get up and running with GitBob Assistant in 5 minutes!

## 🚀 Installation (2 minutes)

```bash
# 1. Clone and navigate
git clone https://github.com/rafa-legend21/gitbob-assistant.git
cd gitbob-assistant

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install
pip install -e .
```

## 🔑 Setup API Key (1 minute)

```bash
# Option 1: Environment variable (recommended)
export IBM_BOB_API_KEY="your-api-key-here"

# Option 2: Config file
gitbob init
# Then edit ~/.gitbob/config.yaml and add your API key
```

## ✅ Test Installation (30 seconds)

```bash
# Test with mock mode (no API calls)
gitbob --mock commit --help

# Test API connection
gitbob config
```

## 🎯 First Use (1.5 minutes)

### Generate Your First Commit Message

```bash
# 1. Make some changes to a file
echo "# Test" > test.txt

# 2. Stage the changes
git add test.txt

# 3. Generate commit message
gitbob commit

# That's it! GitBob will:
# - Analyze your changes
# - Generate a commit message
# - Ask for confirmation
# - Create the commit
```

### Try Branch Name Generation

```bash
# Generate branch name suggestions
gitbob branch "add user authentication feature"

# Select a suggestion and create the branch
```

### Create a PR Description

```bash
# After making several commits on a feature branch
gitbob pr

# Copy the generated description to your PR
```

## 🎓 Common Commands

```bash
# Commit with generated message
gitbob commit

# Commit without confirmation
gitbob commit --no-edit

# Commit and push
gitbob commit --push

# Generate branch name
gitbob branch "your description"

# Create branch immediately
gitbob branch "your description" --create

# Generate PR description
gitbob pr

# PR with specific base branch
gitbob pr --base develop

# Copy PR description to clipboard
gitbob pr --copy
```

## 🧪 Testing Without API

Use `--mock` flag to test without making API calls:

```bash
gitbob --mock commit
gitbob --mock branch "test feature"
gitbob --mock pr
```

## 🆘 Troubleshooting

### "Not a git repository"
Make sure you're inside a git repository:
```bash
git init  # If starting a new repo
```

### "No staged changes found"
Stage your changes first:
```bash
git add .
```

### "API key not configured"
Set your API key:
```bash
export IBM_BOB_API_KEY="your-key"
```

### Import errors
Make sure you're in the virtual environment:
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Customize your [configuration](config.example.yaml)
- Check out [example workflows](#example-workflows)
- Join our community discussions

## 💡 Example Workflows

### Daily Development

```bash
# Start new feature
gitbob branch "implement dark mode"

# Make changes...
# ... edit files ...

# Commit with AI message
git add .
gitbob commit

# More changes...
# ... edit more files ...

# Another commit
git add .
gitbob commit

# Create PR
gitbob pr --copy
# Paste into GitHub
```

### Bug Fix

```bash
# Create bug fix branch
gitbob branch "fix login timeout issue" --create

# Fix the bug
# ... edit files ...

# Commit
git add .
gitbob commit

# Push and create PR
git push origin HEAD
gitbob pr --copy
```

### Code Review Prep

```bash
# Review your changes
git diff --cached

# Generate commit message
gitbob commit

# Review the message
# Edit if needed
# Commit is created automatically
```

## 🎉 You're Ready!

You now know enough to be productive with GitBob Assistant. Happy coding!

For more advanced features and customization, check out the [full documentation](README.md).

---

**Need help?** Open an issue on GitHub or join our discussions!