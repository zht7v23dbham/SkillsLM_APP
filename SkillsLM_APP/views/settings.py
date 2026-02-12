
import streamlit as st
import SkillsLM_APP.core.utils as utils

def render_view():
    """Render Settings View."""
    st.title("⚙️ 设置")
    st.markdown("<p class='header-subtitle'>应用偏好设置与更新</p>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
        <div class='skill-card'>
            <h3>软件更新</h3>
            <p>当前版本: <strong>1.0.3</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("检查更新"):
            with st.spinner("Checking..."):
                 has_update, msg = utils.check_updates()
                 if has_update:
                     st.info(msg)
                 else:
                     st.success("已是最新版本")
    
    st.markdown("### 关于")
    st.info("SkillsLM 是基于 skills.sh 构建的开源桌面管理工具。")
    st.caption("Author: da.zuo")
