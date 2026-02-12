
import streamlit as st
import datetime

def render_css():
    """Render global CSS styles."""
    st.markdown("""
<style>
    /* Dark Theme Background */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #010409;
        border-right: 1px solid #30363d;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #c9d1d9;
    }
    .header-subtitle {
        color: #8b949e;
        font-size: 0.9em;
        margin-bottom: 20px;
    }

    /* Input Fields */
    .stTextInput input {
        background-color: #0d1117;
        color: #c9d1d9;
        border: 1px solid #30363d;
    }
    .stTextInput input:focus {
        border-color: #58a6ff;
        box-shadow: none;
    }
    
    /* Custom Card Styling */
    .skill-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 16px;
        margin-bottom: 12px;
        transition: border-color 0.2s;
    }
    .skill-card:hover {
        border-color: #2ea043;
    }
    
    /* Badges */
    .badge-success {
        background-color: #2ea043;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8em;
        font-weight: bold;
    }
    .badge-info {
        background-color: #1f6feb;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8em;
        font-weight: bold;
    }
    
    .tool-badge {
        display: inline-flex;
        align-items: center;
        background-color: #21262d;
        border: 1px solid #30363d;
        border-radius: 4px;
        padding: 4px 8px;
        margin-right: 8px;
        margin-bottom: 8px;
        color: #c9d1d9;
        font-size: 0.85em;
    }
    .tool-badge.active {
        border-color: #2ea043;
        background-color: #0d1117;
    }
    .tool-badge .status {
        margin-left: 6px;
        background-color: #2ea043;
        color: white;
        padding: 1px 6px;
        border-radius: 4px;
        font-size: 0.7em;
    }

    /* Buttons */
    .stButton button {
        background-color: #21262d;
        color: #c9d1d9;
        border: 1px solid #30363d;
        border-radius: 6px;
        transition: 0.2s;
    }
    .stButton button:hover {
        background-color: #30363d;
        border-color: #8b949e;
        color: white;
    }
    
    /* Market Grid */
    .market-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 16px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin-bottom: 16px;
    }
    .market-card h4 {
        margin-top: 0;
        color: #c9d1d9;
        font-size: 1.1em;
    }
    .repo-link {
        font-size: 0.8em;
        color: #8b949e;
        margin-bottom: 8px;
        font-family: monospace;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        color: #8b949e;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: transparent;
        color: #c9d1d9;
        border-bottom: 2px solid #2ea043;
    }
    
    /* Chips for Featured Repos */
    .chip-container {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-bottom: 16px;
    }
    .chip {
        background-color: #21262d;
        border: 1px solid #30363d;
        border-radius: 16px;
        padding: 4px 12px;
        font-size: 0.85em;
        color: #c9d1d9;
        cursor: pointer;
        transition: 0.2s;
    }
    .chip:hover {
        border-color: #8b949e;
        background-color: #30363d;
    }
</style>
""", unsafe_allow_html=True)

def parse_agents(agents_str):
    """Parse agents string into a list of tools."""
    if not agents_str or agents_str == "None":
        return []
    return [a.strip() for a in agents_str.split(",")]

def render_skill_card(skill, utils_module, is_global=True):
    """Render a single skill card with details."""
    
    # Card Container
    with st.container():
        st.markdown(f"""
        <div class='skill-card'>
            <div style='display: flex; align-items: center; justify-content: space-between;'>
                <div style='display: flex; align-items: center; gap: 16px;'>
                    <div style='background: #21262d; padding: 10px; border-radius: 8px; border: 1px solid #30363d;'>
                        <span style='font-size: 1.5em;'>📦</span>
                    </div>
                    <div>
                        <div style='font-weight: bold; font-size: 1.1em; color: #c9d1d9; margin-bottom: 4px;'>{skill['name']}</div>
                        <div style='font-size: 0.8em; color: #8b949e; font-family: monospace;'>{skill['path']}</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Actions & Details
        with st.expander("查看详情 & 操作", expanded=False):
            col_act1, col_act2, col_act3, col_act4 = st.columns([1, 1, 1, 3])
            with col_act1:
                 if st.button("📄 文档", key=f"doc_{skill['name']}_{is_global}"):
                     st.session_state['view_skill'] = skill
                     st.rerun()
            with col_act2:
                 if st.button("📂 目录", key=f"open_{skill['name']}_{is_global}"):
                     utils_module.open_file(skill['path'])
            with col_act3:
                 if st.button("🗑️ 删除", key=f"del_{skill['name']}_{is_global}"):
                     if st.session_state.get(f"confirm_del_{skill['name']}"):
                         utils_module.remove_skill(skill['name'], global_scope=is_global)
                         st.rerun()
                     else:
                         st.session_state[f"confirm_del_{skill['name']}"] = True
                         st.warning("点击确认")
            
            st.divider()
            
            # Info Grid
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**基本信息**")
                scope_badge = "<span class='badge-info'>Global</span>" if is_global else "<span class='badge-info'>Project</span>"
                st.markdown(f"Scope: {scope_badge}", unsafe_allow_html=True)
                st.caption(f"创建时间: {datetime.datetime.now().strftime('%Y/%m/%d')}") # Placeholder
            with c2:
                st.markdown("**状态**")
                st.markdown("<span class='badge-success'>Active</span>", unsafe_allow_html=True)
            
            # Sync Tools
            st.markdown("**同步到工具**")
            agents = parse_agents(skill.get('agents', ''))
            
            supported_agents = ["Cursor", "Claude Code", "Cline", "Trae", "OpenCode"]
            
            cols = st.columns(len(supported_agents))
            for i, agent in enumerate(supported_agents):
                is_active = any(a.lower() in agent.lower() for a in agents)
                status_html = "<span class='status'>同步</span>" if is_active else ""
                active_class = "active" if is_active else ""
                with cols[i]:
                    st.markdown(f"""
                    <div class='tool-badge {active_class}'>
                        {agent} {status_html}
                    </div>
                    """, unsafe_allow_html=True)
