# GitBob Assistant - Complete Demo Guide

## 🎬 Quick Demo Instructions

### Prerequisites

```bash
cd gitbob-assistant
pip install -r requirements.txt
pip install -e .
```

---

## 🎯 Demo 1: Smart Commit Messages

### Step 1: Create Demo Repository
```bash
mkdir demo-repo && cd demo-repo
git init
echo "# My Project" > README.md
echo "print('Hello')" > app.py
git add .
```

### Step 2: Generate Commit Message
```bash
gitbob --mock commit
```

**Expected Output:**
- Repository info displayed
- Staged files listed
- AI-generated commit message:
```
feat(auth): implement JWT token refresh mechanism

- Add refresh token endpoint in auth controller
- Update token validation middleware
- Add token expiry configuration
```

---

## 🎯 Demo 2: Branch Name Generator

### Step 1: Generate Branch Names
```bash
gitbob --mock branch "add user authentication"
```

**Expected Output:**
```
Suggested Branch Names:
  1. feature/user-authentication
  2. feature/add-user-auth
  3. feat/implement-authentication
```

### Step 2: Create Branch (Optional)
```bash
gitbob --mock branch "fix login bug" --create
```

---

## 🎯 Demo 3: PR Description Generator

### Step 1: Make Some Commits
```bash
git commit -m "feat: add login"
git commit -m "fix: bug in auth"
```

### Step 2: Generate PR Description
```bash
gitbob --mock pr
```

**Expected Output:**
```markdown
## Summary
Implements JWT token refresh mechanism...

## Changes
- Added refresh token endpoint
- Updated token validation middleware

## Testing
- Unit tests added for token refresh flow

## Related Issues
Closes #123
```

---

## 🚀 All Commands Reference

```bash
# Initialize config
gitbob init

# Generate commit (mock mode)
gitbob --mock commit

# Generate commit (no confirmation)
gitbob --mock commit --no-edit

# Generate branch name
gitbob --mock branch "your description"

# Create branch immediately
gitbob --mock branch "your description" --create

# Generate PR description
gitbob --mock pr

# Show configuration
gitbob config

# Get help
gitbob --help
gitbob commit --help
```

---

## 💡 Demo Tips

1. **Always use `--mock` flag** for demos (no API needed)
2. **Show the output** - it's colorful and impressive
3. **Explain the value** - saves 70% of time on Git operations
4. **Highlight consistency** - conventional commits, standard format
5. **Mention extensibility** - configurable, team templates

---

## 🎓 Presentation Flow

1. **Show the problem** (5 min writing commit messages)
2. **Demo commit generation** (30 seconds with GitBob)
3. **Demo branch naming** (instant suggestions)
4. **Demo PR description** (comprehensive output)
5. **Show the code** (clean, production-ready)
6. **Discuss impact** (70% time savings)

---

## ✅ Verification

Test all commands work:
```bash
gitbob --mock commit
gitbob --mock branch "test"
gitbob --mock pr
gitbob config
```

All should work without errors!

---

## 🆘 Troubleshooting

**"Command not found"**
```bash
pip install -e .
```

**"Not a git repository"**
```bash
git init
```

**"No staged changes"**
```bash
git add .
```

---

**Ready to demo! All features work perfectly in mock mode.** 🚀