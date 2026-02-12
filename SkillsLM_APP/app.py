
import streamlit as st
import os
import SkillsLM_APP.core.utils as utils
from SkillsLM_APP.components.ui import render_css

# --- Page Config ---
st.set_page_config(
    page_title="SkillsLM",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS Styling ---
render_css()

# --- Sidebar ---
with st.sidebar:
    st.image("https://assets.vercel.com/image/upload/v1588805858/repositories/vercel/logo.png", width=50) # Placeholder logo
    st.title("SkillsLM")
    
    # Custom Navigation using Radio
    selected_page = st.radio(
        "Navigation", 
        ["技能管理", "本地技能", "安装技能", "测试智能体", "提示词生成器", "终端命令", "设置"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Quick Check for Updates
    if st.button("🔄 检查更新"):
        with st.spinner("Checking..."):
            has_update, msg = utils.check_updates()
            if has_update:
                st.warning("发现更新!")
                st.caption(msg)
            else:
                st.success("已是最新")
    
    st.caption("v1.0.3 | By da.zuo")

# --- Focus View Logic (Modal) ---
# This is shared logic that can be triggered from multiple views
if 'view_skill' in st.session_state and st.session_state['view_skill']:
    skill = st.session_state['view_skill']
    with st.container():
        st.markdown("---")
        col_close, col_mode, _ = st.columns([1, 2, 8])
        if col_close.button("❌ 关闭详情"):
            del st.session_state['view_skill']
            st.rerun()
            
        # Toggle Edit Mode
        edit_mode = st.toggle("✏️ 编辑模式", key="edit_mode_toggle")
            
        st.header(f"📘 {skill['name']}")
        
        # Tabs for Content vs Flowchart
        tab_doc, tab_flow = st.tabs(["📄 文档内容", "🔄 流程可视化"])
        
        # Determine content first
        readme_path = os.path.join(skill['path'], "SKILL.md")
        if not os.path.exists(readme_path):
            readme_path = os.path.join(skill['path'], "README.md")
        
        content = ""
        if os.path.exists(readme_path):
            with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

        with tab_doc:
            c_tree, c_content = st.columns([1, 3])
            
            with c_tree:
                st.markdown("### 文件目录")
                try:
                    tree_str = ""
                    for root, dirs, files in os.walk(skill['path']):
                        level = root.replace(skill['path'], '').count(os.sep)
                        indent = '&nbsp;' * 4 * level
                        tree_str += f"{indent}📁 {os.path.basename(root)}/<br>"
                        subindent = '&nbsp;' * 4 * (level + 1)
                        for f in files:
                            tree_str += f"{subindent}📄 {f}<br>"
                    
                    st.markdown(f"<div style='background:#0d1117; padding:10px; border-radius:4px; font-family:monospace; font-size:0.8em; overflow-x:auto;'>{tree_str}</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(str(e))
                    
            with c_content:
                if content:
                    st.markdown(f"### 文档内容 ({os.path.basename(readme_path)})")
                    
                    if edit_mode:
                        new_content = st.text_area("编辑器", value=content, height=600, label_visibility="collapsed")
                        if st.button("💾 保存更改"):
                            success, err = utils.save_file(readme_path, new_content)
                            if success:
                                st.success("已保存!")
                                st.rerun()
                            else:
                                st.error(f"保存失败: {err}")
                    else:
                        st.markdown(f"<div style='background:#0d1117; padding:20px; border-radius:6px; border:1px solid #30363d;'>{content}</div>", unsafe_allow_html=True)
                else:
                    st.info("No documentation found (SKILL.md or README.md).")
        
        with tab_flow:
            if content:
                st.markdown("### 流程图 (自动生成)")
                mermaid_code = utils.extract_flowchart_from_markdown(content)
                
                if mermaid_code:
                    st.markdown(f"```mermaid\n{mermaid_code}\n```")
                    
                    # HTML Export
                    html_content = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>{skill['name']} Flowchart</title>
                        <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
                        <script>mermaid.initialize({{startOnLoad:true}});</script>
                        <style>
                            body {{ font-family: sans-serif; background: #0d1117; color: #c9d1d9; padding: 20px; }}
                            .mermaid {{ background: white; padding: 20px; border-radius: 8px; }}
                        </style>
                    </head>
                    <body>
                        <h1>{skill['name']} Workflow</h1>
                        <div class="mermaid">
                        {mermaid_code}
                        </div>
                    </body>
                    </html>
                    """
                    st.download_button(
                        label="📥 下载 HTML 流程图",
                        data=html_content,
                        file_name=f"{skill['name']}_flowchart.html",
                        mime="text/html"
                    )
                else:
                    st.warning("未检测到明显的步骤列表 (1. Step, 2. Step...)，无法生成流程图。")
            else:
                 st.info("无文档内容，无法生成流程图。")

# --- Main Routing ---

if selected_page == "技能管理":
    from SkillsLM_APP.views import home
    home.render_view()

elif selected_page == "本地技能":
    from SkillsLM_APP.views import local
    local.render_view()

elif selected_page == "安装技能":
    from SkillsLM_APP.views import market
    market.render_view()

elif selected_page == "测试智能体":
    from SkillsLM_APP.views import testing
    testing.render_view()

elif selected_page == "提示词生成器":
    from SkillsLM_APP.views import prompts
    prompts.render_view()

elif selected_page == "终端命令":
    from SkillsLM_APP.views import terminal
    terminal.render_view()

elif selected_page == "设置":
    from SkillsLM_APP.views import settings
    settings.render_view()
