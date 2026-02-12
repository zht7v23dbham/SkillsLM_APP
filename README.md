# SkillsLM 

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Agent Skills](https://img.shields.io/badge/Agent_Skills-Skills.sh-blueviolet?style=for-the-badge)](https://skills.sh)

> **The Ultimate Desktop Manager for AI Agent Skills**  
> Manage, discover, generate, and install skills for your AI agents (Claude, Trae, Cursor, etc.) with a beautiful graphical interface.

---

## 🚀 Introduction

**SkillsLM** is a powerful desktop application built with Streamlit that serves as a comprehensive management center for **Agent Skills**. It bridges the gap between raw skill repositories and your local AI development environment.

With SkillsLM, you can:
*   **Visualize & Manage**: See all your installed skills (Global & Project-scope) in one place.
*   **One-Click Install**: Browse curated marketplaces (OpenAI, Anthropic, Community) and install skills instantly.
*   **Generate Capabilities**: Create custom "Expert Agent" skills using our built-in Prompt Generator.
*   **Deploy Testing Agents**: Instantly generate a full suite of QA/Testing skills for your software projects.

## ✨ Key Features

### 📦 Skill Management
*   **Dual Scope View**: Distinct views for **Global** (User-level) and **Local** (Project-level) skills.
*   **Visual Cards**: Rich UI showing skill descriptions, paths, and sync status.
*   **CRUD Operations**: Open skill directories, view documentation, or delete skills with a single click.

### 🌐 Integrated Marketplace
Access the world's best agent skills directly from the app:
*   **Official OpenAI Skills**: `openai/skills`
*   **Anthropic Claude Skills**: `anthropics/skills` & `claude-plugins-official`
*   **Community Toolkits**: `softaworks/agent-toolkit`, `vercel-labs/agent-skills`
*   **Git Integration**: Install from *any* public GitHub repository.

### 🧠 Intelligent Generators
*   **Prompt Generator**: A cross-domain prompt engine that turns natural language into structured, expert-level prompts (Software, Design, etc.).
*   **Testing Agent Suite**: One-click generation of a 5-skill QA team (Requirements, Test Points, Case Writing, Review, Export).
*   **Save as Skill**: Directly save generated prompts as new local skills.

### 🛠️ Developer Tools
*   **Terminal Interface**: Built-in GUI for `npx skills` commands (Doctor, Update, Check).
*   **Flowchart Visualization**: Automatically generates Mermaid flowcharts from skill documentation (`SKILL.md`).
*   **Editor**: In-app markdown editor for tweaking skill instructions.

## 🏗️ Architecture

SkillsLM follows a clean **MVC (Model-View-Controller)** architecture for maintainability and scalability:

```text
SkillsLM_APP/
├── app.py               # Main Entry Point (Controller)
├── core/                # Core Logic & Utilities
│   └── utils.py         # File I/O, Command Execution, Parsers
├── components/          # Reusable UI Components
│   └── ui.py            # CSS, Cards, Badges
└── views/               # Page Views
    ├── home.py          # Global Skills Manager
    ├── local.py         # Local Project Skills
    ├── market.py        # Skill Marketplace
    ├── testing.py       # Testing Agent Generator
    ├── prompts.py       # Prompt Generator
    ├── terminal.py      # CLI Wrapper
    └── settings.py      # App Settings
```

## 💻 Installation & Usage

### Prerequisites
*   Python 3.8+
*   Node.js & npm (for `npx skills`)

### Setup
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-repo/skills-lm.git
    cd skills-lm
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r SkillsLM_APP/requirements.txt
    ```

3.  **Run the Application**:
    ```bash
    # Ensure project root is in PYTHONPATH
    export PYTHONPATH=$PYTHONPATH:$(pwd)
    streamlit run SkillsLM_APP/app.py
    ```

## 🤝 Contributing

We welcome contributions! Please follow these steps:
1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/amazing-feature`).
3.  Commit your changes.
4.  Push to the branch.
5.  Open a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**da.zuo**  
*Building better tools for the AI Agent era.*

---
*Built with ❤️ using [Streamlit](https://streamlit.io) and [skills.sh](https://skills.sh)*
