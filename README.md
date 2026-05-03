# GitBob Assistant 🤖

AI-powered Git workflow automation using IBM Bob.

---

## 🚀 What is GitBob?

GitBob is a simple CLI tool that helps developers:

- ✨ write commit messages  
- 🌿 create branch names  
- 📝 generate PR descriptions  

👉 So you can focus on coding, not Git overhead.

---

## 🎯 Why use it?

Developers spend **a lot of time on Git tasks**:

- Writing commit messages  
- Creating PR descriptions  
- Naming branches  

GitBob helps you:
- ⚡ Save time (~70%)
- 📏 Stay consistent
- 📚 Keep clean project history  

---

## ⚙️ Features

### 📝 Commit Messages
```bash
git add .
gitbob commit
```

## 🌿 Branch Names

gitbob branch
✔ Suggests good branch names automatically

---

## 🔗 PR Descriptions

gitbob pr
Creates full PR descriptions (summary + changes + testing)

---

## 🛠️ Installation

git clone https://github.com/rafa-legend21/gitbob-assistant.git
cd gitbob-assistant

python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
pip install -e .

---

## 🔑 Setup (Optional)

Set your API key:
$env:IBM_BOB_API_KEY="your_api_key_here"

👉 No API? No problem — use demo mode 👇

---

## 🧪 Demo Mode (Recommended)

gitbob --mock commit
gitbob --mock branch
gitbob --mock pr

✔ Works without API
✔ Perfect for testing & demo

---

## 🧠 Tech Stack

Python
GitPython
Click (CLI)
Rich (terminal UI)

---

## 📊 Impact

⚡ ~70% faster Git workflow
📚 cleaner commit history
🤝 better team collaboration

---

## 🚧 Notes

Requires Git installed
Best used with mock mode for demo
API access depends on IBM setup

---

## 🔮 Future Plans
VS Code extension
GitHub integration
smarter AI suggestions

## 📄 License

MIT License

---

## 🙌 Built for Hackathon

This project shows how AI can simplify developer workflows.
