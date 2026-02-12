import subprocess
import re
import os
import shutil
import platform

def strip_ansi(text):
    """Strip ANSI escape codes from text."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def run_command(args):
    """Run npx skills command."""
    # Check if npx is available
    if shutil.which("npx") is None:
        return None, "未找到 npx 命令，请先安装 Node.js。"

    cmd = ["npx", "skills"] + args
    try:
        # Using shell=False is safer, but need to ensure npx is in PATH
        # On Windows, shell=True might be needed for npx
        use_shell = platform.system() == "Windows"
        result = subprocess.run(cmd, capture_output=True, text=True, shell=use_shell)
        return result.stdout, result.stderr
    except Exception as e:
        return None, str(e)

def list_skills(global_scope=True):
    """List installed skills."""
    args = ["list"]
    if global_scope:
        args.append("-g")
    
    stdout, stderr = run_command(args)
    
    # If command fails completely, try to return what we can or empty
    if not stdout:
        return [], stderr

    stdout = strip_ansi(stdout)
    skills = []
    lines = stdout.splitlines()
    
    current_skill = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Skip known header/footer lines
        if "Global Skills" in line or "Project Skills" in line:
            continue
        if line.startswith("Need to install") or line.startswith("Ok to proceed"):
            continue
        if "No global skills found" in line or "No project skills found" in line:
            continue # Don't return early, just skip this line
            
        if line.startswith("Agents:"):
            if current_skill:
                current_skill['agents'] = line.replace("Agents:", "").strip()
        else:
            # Format: skill-name path
            # Try to parse as "name path"
            parts = line.split()
            if len(parts) >= 2:
                # Heuristic: The last part is likely the path
                # But path could have spaces. 
                # Usually name is the first part.
                name = parts[0]
                
                # Verify name is not some random word
                # Skill names are usually lowercase, dashes, maybe dots
                if not re.match(r'^[a-zA-Z0-9_\-\.]+$', name):
                    continue
                    
                path = " ".join(parts[1:]) 
                
                # Heuristic: path usually has / or \ or starts with ~
                # Also check if it looks like a path
                if "/" in path or "\\" in path or path.startswith("~"):
                    # Expand user path if it starts with ~
                    if path.startswith("~"):
                        path = os.path.expanduser(path)
                        
                    current_skill = {
                        "name": name,
                        "path": path,
                        "agents": "None",
                        "scope": "global" if global_scope else "project"
                    }
                    skills.append(current_skill)
    
    return skills, None

def get_repo_skills(repo):
    """List skills in a repository."""
    stdout, stderr = run_command(["add", repo, "--list"])
    if not stdout:
        return [], stderr
        
    stdout = strip_ansi(stdout)
    skills = []
    lines = stdout.splitlines()
    
    # We need to find the section "Available Skills"
    in_skills_section = False
    current_skill_name = None
    
    for line in lines:
        # Don't strip yet, we need indentation
        if "Available Skills" in line:
            in_skills_section = True
            continue
        
        if not in_skills_section:
            continue
            
        clean_line = line.replace("│", "").rstrip()
        if not clean_line.strip():
            continue

        # Determine if it's a name or description based on indent
        # Name usually has less indent than description
        # Let's count leading spaces after removing │
        leading_spaces = len(clean_line) - len(clean_line.lstrip())
        
        content = clean_line.strip()
        
        if "Installation Summary" in line or "Use --skill" in line or "Selected" in line:
            break

        # Heuristic: Name usually has indentation around 4 (after pipe removal)
        # Description has more (6+).
        # Also check if content looks like a skill name (no spaces) for extra safety on name detection
        is_name_format = re.match(r'^[a-zA-Z0-9_\-\.]+$', content)

        if leading_spaces <= 5 and is_name_format: # Relaxed from == 4
            current_skill_name = content
            skills.append({"name": content, "description": "", "repo": repo})
        elif leading_spaces >= 6 and current_skill_name: # Heuristic for description
             skills[-1]["description"] += content + " "
                
    return skills, None

def install_skill(repo, skill_name=None, global_install=True):
    args = ["add", repo]
    if skill_name:
        args.extend(["--skill", skill_name])
    if global_install:
        args.append("-g")
    args.append("-y")
    
    return run_command(args)

def remove_skill(skill_name, global_scope=True):
    args = ["remove", skill_name]
    if global_scope:
        args.append("-g")
    args.append("-y")
    return run_command(args)

def update_skills():
    """Update all skills."""
    return run_command(["update"])

def check_updates():
    """Check for updates."""
    stdout, stderr = run_command(["check"])
    if stdout:
        stdout = strip_ansi(stdout)
        if "All skills are up to date" in stdout:
            return False, "所有 Skills 已是最新"
        else:
            return True, stdout
    return False, stderr

def open_file(path):
    """Open file or directory in default application."""
    try:
        if platform.system() == 'Windows':
            os.startfile(path)
        elif platform.system() == 'Darwin': # macOS
            subprocess.call(('open', path))
        else: # Linux
            subprocess.call(('xdg-open', path))
    except Exception as e:
        return str(e)
    return None

def save_file(path, content):
    """Save content to file."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, None
    except Exception as e:
        return False, str(e)

def extract_flowchart_from_markdown(content):
    """Extract workflow steps from markdown content and generate Mermaid flowchart."""
    # Heuristic: Look for numbered lists or sections that imply steps
    steps = []
    
    # Strategy 1: Look for "Steps" or "Instructions" section
    lines = content.split('\n')
    in_steps = False
    
    for line in lines:
        stripped = line.strip()
        if re.match(r'^#+\s*(Steps|Instructions|How to Use|Usage)', stripped, re.IGNORECASE):
            in_steps = True
            continue
        
        if in_steps:
            if stripped.startswith('#'): # New section
                break
            # Match numbered list: 1. Step description
            match = re.match(r'^\d+\.\s+(.+)', stripped)
            if match:
                steps.append(match.group(1))
            # Match bullet list: - Step description (only if we found no numbered steps yet or mixed)
            elif stripped.startswith('- ') or stripped.startswith('* '):
                 steps.append(stripped[2:])

    if not steps:
        # Fallback: Just try to find any numbered list in the whole doc
        for line in lines:
            match = re.match(r'^\d+\.\s+(.+)', line.strip())
            if match:
                steps.append(match.group(1))
                
    if not steps:
        return None

    # Generate Mermaid syntax
    mermaid = "graph TD;\n"
    for i, step in enumerate(steps):
        # Sanitize step text for mermaid
        safe_step = step.replace('"', "'").replace(';', '').replace('(', '').replace(')', '')[:50]
        if len(step) > 50: safe_step += "..."
        
        node_id = f"step{i}"
        mermaid += f'    {node_id}["{i+1}. {safe_step}"]\n'
        
        if i > 0:
            mermaid += f"    step{i-1} --> {node_id}\n"
            
    return mermaid

def create_skill_from_prompt(name, prompt, description, target_dir):
    """Create a new skill from a generated prompt."""
    try:
        skill_path = os.path.join(target_dir, name)
        os.makedirs(skill_path, exist_ok=True)
        
        # SKILL.md with Frontmatter
        skill_md = f"""---
name: {name}
description: {description}
version: 1.0.0
---

# {name}

## Description
{description}

## Prompt
```text
{prompt}
```

## Usage
Copy the prompt above and use it with your favorite LLM.
"""
        save_file(os.path.join(skill_path, "SKILL.md"), skill_md)
        return True, None
    except Exception as e:
        return False, str(e)

def generate_testing_agent_skills(base_path=None):
    """Generate the 5 Software Testing Expert skills."""
    if base_path is None:
        base_path = os.path.expanduser("~/.agents/skills")
    
    # Ensure directory exists
    try:
        os.makedirs(base_path, exist_ok=True)
    except Exception as e:
        return 0, [f"Failed to create directory {base_path}: {str(e)}"]

    skills = [
        {
            "name": "requirements-analysis",
            "desc": "需求分析技能：从URL或文本中提取关键测试点，识别功能模块、业务规则、数据流转。",
            "tools": """
def analyze_requirements_from_input(url_or_text: str):
    \"\"\"
    从URL或文本中获取需求文档
    
    支持：
    - 语雀文档URL (模拟)
    - Markdown格式文本
    - 纯文本
    \"\"\"
    # 模拟获取内容
    content = url_or_text
    if url_or_text.startswith('http'):
        content = f"Fetched content from {url_or_text}"
    
    return {
        "content": content,
        "source_type": "url" if url_or_text.startswith('http') else "text"
    }
""",
            "prompts": """
REQUIREMENTS_ANALYSIS_PROMPT = \"\"\"
你是一位资深需求分析师。
你的任务是阅读需求文档，识别核心功能、业务规则和潜在风险。
输出格式应包含：
1. 功能模块列表
2. 业务规则（输入、输出、约束）
3. 数据流转图描述 (Mermaid格式)
\"\"\"
"""
        },
        {
            "name": "test-point-design",
            "desc": "测试点设计技能：从需求文档中提取关键测试点，覆盖正常、边界、异常场景。",
            "tools": """
def generate_test_points(requirements_text: str):
    \"\"\"
    基于需求文本生成结构化测试点
    \"\"\"
    # 实际逻辑由LLM处理，这里仅提供占位符
    return "Ready to generate test points based on requirements."
""",
            "prompts": """
TEST_POINT_DESIGN_EXPERT_PROMPT = \"\"\"
你是一位资深测试工程师，擅长从需求中提取测试点。

测试点设计原则：
1. 功能覆盖：每个功能点都要有对应测试点
2. 场景分类：正常场景、边界场景、异常场景
3. 数据覆盖：有效数据、无效数据、边界数据
4. 交互覆盖：UI交互、接口调用、数据库操作

测试点格式：
- 功能模块
  - 正常场景
    - [测试点] 描述
  - 边界场景
    - [测试点] 描述
  - 异常场景
    - [测试点] 描述
\"\"\"
"""
        },
        {
            "name": "test-case-writing",
            "desc": "测试用例编写技能：基于测试点编写详细的测试步骤和预期结果。",
            "tools": """
def format_test_case(case_id, title, steps, expected):
    \"\"\"
    格式化测试用例
    \"\"\"
    return {
        "id": case_id,
        "title": title,
        "steps": steps,
        "expected": expected
    }
""",
            "prompts": """
TEST_CASE_WRITING_PROMPT = \"\"\"
你是一位细致的测试用例编写专家。
请将测试点转化为可执行的测试用例。
每个用例必须包含：
- 用例ID
- 标题
- 前置条件
- 测试步骤（分步描述）
- 预期结果（对应每一步）
- 优先级 (P0-P3)
\"\"\"
"""
        },
        {
            "name": "test-case-review",
            "desc": "测试用例评审技能：检查用例覆盖率、完整性和规范性。",
            "tools": """
def review_checklist(cases):
    \"\"\"
    自动检查用例完整性
    \"\"\"
    issues = []
    if not cases:
        issues.append("无测试用例")
    return issues
""",
            "prompts": """
TEST_CASE_REVIEW_PROMPT = \"\"\"
你是一位严格的测试经理。请评审提交的测试用例。
检查点：
1. 是否覆盖了所有需求点？
2. 步骤是否清晰无歧义？
3. 预期结果是否可验证？
4. 是否遗漏了明显的异常场景？

请输出评审报告和改进建议。
\"\"\"
"""
        },
        {
            "name": "test-case-export",
            "desc": "测试用例导出技能：生成 Excel 和 XMind 格式文件。",
            "tools": """
def export_to_excel(cases_json, filename="test_cases.xlsx"):
    \"\"\"
    模拟导出到 Excel
    \"\"\"
    return f"Exported {len(cases_json)} cases to {filename}"

def export_to_xmind(cases_json, filename="test_cases.xmind"):
    \"\"\"
    模拟导出到 XMind
    \"\"\"
    return f"Exported {len(cases_json)} cases to {filename}"
""",
            "prompts": """
TEST_CASE_EXPORT_PROMPT = \"\"\"
你负责将测试用例转换为标准交付格式。
请确保导出的数据结构符合 Excel 模板或 XMind 脑图结构。
\"\"\"
"""
        }
    ]
    
    created_count = 0
    errors = []
    
    for skill in skills:
        skill_path = os.path.join(base_path, skill['name'])
        try:
            os.makedirs(skill_path, exist_ok=True)
            
            # SKILL.md
            skill_md = f"""# {skill['name']}

## Description
{skill['desc']}

## Capabilities
- 自动化处理测试流程中的特定环节
- 与其他测试技能协同工作

## Usage
此技能是 "测试用例设计智能体" 的一部分。
通常配合 requirements-analysis, test-point-design, test-case-writing, test-case-review, test-case-export 组合使用。

## Components
- `tools.py`: 核心工具函数
- `prompts.py`: 专家提示词
"""
            save_file(os.path.join(skill_path, "SKILL.md"), skill_md)
            
            # tools.py
            save_file(os.path.join(skill_path, "tools.py"), skill['tools'])
            
            # prompts.py
            save_file(os.path.join(skill_path, "prompts.py"), skill['prompts'])
            
            created_count += 1
            
        except Exception as e:
            errors.append(f"Failed to create {skill['name']}: {str(e)}")
            
    return created_count, errors

