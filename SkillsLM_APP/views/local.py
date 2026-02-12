
import streamlit as st
import SkillsLM_APP.core.utils as utils
from SkillsLM_APP.components.ui import render_skill_card

def render_view():
    """Render Local/Project Skills View."""
    col_h1, col_h2 = st.columns([6, 2])
    
    with st.spinner("加载项目级 Skills..."):
        skills, error = utils.list_skills(global_scope=False)
    
    with col_h1:
        st.title("本地技能")
        count = len(skills) if skills else 0
        st.markdown(f"<p class='header-subtitle'>管理当前项目下的 {count} 个技能 (Project Scope)</p>", unsafe_allow_html=True)
            
    with col_h2:
        if st.button("🔄 刷新", use_container_width=True):
            st.rerun()

    search_query = st.text_input("🔍 搜索本地技能...", placeholder="Type to search...", label_visibility="collapsed")
    
    if error:
        st.error(error)
    else:
        if skills and search_query:
            skills = [s for s in skills if search_query.lower() in s['name'].lower()]
        
        if not skills:
            st.info("暂无安装技能")
        else:
            for skill in skills:
                render_skill_card(skill, utils, is_global=False)
