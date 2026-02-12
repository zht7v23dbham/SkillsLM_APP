
import streamlit as st
import SkillsLM_APP.core.utils as utils
from SkillsLM_APP.components.ui import render_skill_card

def render_view():
    """Render Global Skills Management View."""
    col_h1, col_h2 = st.columns([6, 2])
    
    with st.spinner("加载全局 Skills..."):
        skills, error = utils.list_skills(global_scope=True)
    
    with col_h1:
        st.title("技能管理")
        count = len(skills) if skills else 0
        st.markdown(f"<p class='header-subtitle'>管理全局已安装的 {count} 个技能 (User Scope)</p>", unsafe_allow_html=True)
            
    with col_h2:
        if st.button("🚀 更新所有", use_container_width=True):
            with st.spinner("Updating..."):
                utils.update_skills()
                st.success("Updated!")

    search_query = st.text_input("🔍 搜索全局技能...", placeholder="Type to search...", label_visibility="collapsed")
    
    if error:
        st.error(error)
    else:
        if skills and search_query:
            skills = [s for s in skills if search_query.lower() in s['name'].lower()]
        
        if not skills:
            st.info("暂无安装技能")
        else:
            for skill in skills:
                render_skill_card(skill, utils, is_global=True)
