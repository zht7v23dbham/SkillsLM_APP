
import streamlit as st
import os
import SkillsLM_APP.core.utils as utils

def render_view():
    """Render Testing Agent Generator View."""
    st.title("🤖 测试智能体生成器")
    st.markdown("<p class='header-subtitle'>一键部署标准化的软件测试智能体 (Test Case Design Agent)</p>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
        <div class='skill-card'>
            <h4>🚀 什么是测试智能体？</h4>
            <p style='color:#c9d1d9; font-size:0.9em; line-height: 1.5;'>
            Skills架构的核心思想是：把专业知识封装成独立的技能模块，每个技能包含特定领域的最佳实践。
            此生成器将为您创建一套完整的测试用例设计智能体，包含以下5个核心技能：
            </p>
            <ul style='color:#8b949e; font-size:0.9em;'>
                <li><strong>requirements-analysis</strong>: 需求分析技能</li>
                <li><strong>test-point-design</strong>: 测试点设计技能</li>
                <li><strong>test-case-writing</strong>: 测试用例编写技能</li>
                <li><strong>test-case-review</strong>: 测试用例评审技能</li>
                <li><strong>test-case-export</strong>: 测试用例导出技能</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns([2, 1])
        with c1:
             st.info("每个技能将包含 `SKILL.md` (AI手册), `tools.py` (工具函数), `prompts.py` (专家提示词)。")
        
        with c2:
             if st.button("🚀 立即部署技能组", use_container_width=True):
                 with st.spinner("正在生成技能文件..."):
                     # Generate to project directory
                     project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                     target_dir = os.path.join(project_root, "generated_skills")
                     
                     count, errors = utils.generate_testing_agent_skills(base_path=target_dir)
                     
                     if errors:
                         for err in errors:
                             st.error(err)
                     else:
                         st.success(f"成功部署 {count} 个测试技能到工程目录！")
                         st.info(f"路径: {target_dir}")
                         st.balloons()
                         # Trigger refresh to show in local skills if logic supports it
                         st.session_state['show_generated_skills'] = True
    
    # Check if generated skills exist, always show if so (or if triggered)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    target_dir = os.path.join(project_root, "generated_skills")
    has_generated_skills = os.path.exists(target_dir) and os.listdir(target_dir)

    if has_generated_skills or st.session_state.get('show_generated_skills'):
        st.divider()
        st.subheader("📂 工程中的生成技能")
        
        if os.path.exists(target_dir):
            skills = []
            for item in os.listdir(target_dir):
                item_path = os.path.join(target_dir, item)
                if os.path.isdir(item_path):
                     skills.append(item)
            
            if skills:
                cols = st.columns(3)
                for i, skill_name in enumerate(skills):
                    with cols[i % 3]:
                        with st.container():
                            st.markdown(f"**{skill_name}**")
                            
                            if st.button("📥 安装到本地", key=f"inst_gen_{skill_name}"):
                                with st.spinner(f"Installing {skill_name}..."):
                                    skill_full_path = os.path.join(target_dir, skill_name)
                                    stdout, stderr = utils.install_skill(skill_full_path)
                                    if stderr and "error" in stderr.lower():
                                        st.error(stderr)
                                    else:
                                        st.success(f"已安装 {skill_name}")
            else:
                st.info("暂无生成的技能")
        else:
            st.info("暂无生成的技能目录")
    
    st.divider()
    st.markdown("### 📚 技能架构预览")
    
    tab_arch, tab_flow = st.tabs(["📂 目录结构", "🔄 工作流程"])
    
    with tab_arch:
        st.code("""
testcase-skills/
├── requirements-analysis/
│   ├── SKILL.md
│   ├── tools.py
│   └── prompts.py
├── test-point-design/
│   ├── SKILL.md
│   ├── tools.py
│   └── prompts.py
├── test-case-writing/ ...
├── test-case-review/ ...
└── test-case-export/ ...
        """, language="bash")
        
    with tab_flow:
        st.markdown("""
        ```mermaid
        graph TD;
            A[需求文档] --> B(requirements-analysis);
            B --> C{test-point-design};
            C --> D(test-case-writing);
            D --> E(test-case-review);
            E -->|修正| D;
            E -->|通过| F(test-case-export);
            F --> G[Excel/XMind];
        ```
        """)
