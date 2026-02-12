
import streamlit as st
import SkillsLM_APP.core.utils as utils

def render_view():
    """Render Market / Install Skills View."""
    st.title("安装技能")
    st.markdown("<p class='header-subtitle'>从技能市场或本地安装</p>", unsafe_allow_html=True)
    
    tab_browse, tab_testing, tab_software, tab_local, tab_git = st.tabs(["🌐 技能市场", "🏆 测试专家", "💻 软件工程", "📂 本地安装", "🔗 Git 安装"])
    
    # Define Recommended Testing Skills
    QA_EXPERT_SKILLS = [
        {"name": "qa-test-planner", "desc": "全能测试专家: 自动生成测试计划、手动用例、回归套件、Figma视觉验证及缺陷报告。"},
        {"name": "jira", "desc": "Jira 深度集成: 使用自然语言创建、查询和更新 Jira 工单，无缝管理缺陷追踪。"},
        {"name": "datadog-cli", "desc": "Datadog 监控诊断: 直接在对话中查询日志和指标，快速定位生产环境问题。"},
        {"name": "dependency-updater", "desc": "依赖智能更新: 自动检测并更新项目依赖，确保测试环境的安全性和稳定性。"},
        {"name": "web-to-markdown", "desc": "文档转 Markdown: 将网页测试文档或需求文档转换为 LLM 易读格式，辅助测试设计。"},
        {"name": "writing-clearly-and-concisely", "desc": "专业文档写作: 辅助编写清晰、简洁的测试报告和缺陷描述，提升沟通效率。"}
    ]

    with tab_testing:
        st.info("以下是为您精选的软件测试领域专家级 Agent Skills，均来自 softaworks/agent-toolkit 仓库。")
        cols = st.columns(2)
        for i, skill in enumerate(QA_EXPERT_SKILLS):
            with cols[i % 2]:
                with st.container():
                    st.markdown(f"""
                    <div class='skill-card'>
                        <div style='display: flex; align-items: flex-start; gap: 12px;'>
                            <div style='background: #1f6feb; padding: 8px; border-radius: 6px;'>
                                <span style='font-size: 1.2em;'>🧪</span>
                            </div>
                            <div>
                                <div style='font-weight: bold; font-size: 1.1em; color: #c9d1d9; margin-bottom: 4px;'>{skill['name']}</div>
                                <div style='font-size: 0.9em; color: #8b949e; line-height: 1.4;'>{skill['desc']}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    c_act1, c_act2 = st.columns([1, 1])
                    with c_act1:
                         if st.button("🔍 去安装", key=f"test_search_{i}", use_container_width=True):
                             st.session_state['market_search_query'] = skill['name']
                             st.session_state['current_market_repo'] = "softaworks/agent-toolkit"
                             if 'market_data' in st.session_state: del st.session_state['market_data']
                             st.rerun()
                    with c_act2:
                         st.button("💡 复制名称", key=f"test_copy_{i}", use_container_width=True, help="复制技能名称以供搜索")

    # Software Engineering Skills
    SOFTWARE_ENG_SKILLS = {
        "Development": [
            {"name": "codex", "desc": "高级代码分析与重构 (GPT-5.2 powered)"},
            {"name": "naming-analyzer", "desc": "智能命名建议: 根据上下文和规范优化变量、函数命名"},
            {"name": "reducing-entropy", "desc": "代码熵减: 最小化代码库体积，移除冗余"},
            {"name": "react-dev", "desc": "React 专家: TypeScript, Hooks 最佳实践"}
        ],
        "Architecture": [
            {"name": "c4-architecture", "desc": "C4 架构图生成: 自动绘制系统上下文、容器、组件图"},
            {"name": "database-schema-designer", "desc": "数据库设计专家: 设计规范化、高性能的 SQL/NoSQL 模式"},
            {"name": "design-system-starter", "desc": "设计系统构建: 生成设计令牌、组件架构和文档"}
        ],
        "DevOps & Git": [
            {"name": "commit-work", "desc": "智能提交: 生成符合 Conventional Commits 规范的清晰提交信息"},
            {"name": "dependency-updater", "desc": "依赖管理: 自动检测更新并修复依赖问题"},
            {"name": "datadog-cli", "desc": "Datadog 集成: 日志查询与监控"}
        ],
        "Documentation": [
            {"name": "crafting-effective-readmes", "desc": "README 专家: 针对不同受众生成高质量项目文档"},
            {"name": "backend-to-frontend-handoff-docs", "desc": "前后端交付文档: 自动生成 API 接口文档供前端使用"},
            {"name": "mermaid-diagrams", "desc": "Mermaid 图表: 生成流程图、序列图、类图等"}
        ]
    }

    with tab_software:
        st.info("集成了软件工程全生命周期的核心 Skills (Dev, Ops, Arch, Docs)。")
        
        for category, skills in SOFTWARE_ENG_SKILLS.items():
            st.markdown(f"#### {category}")
            cols = st.columns(2)
            for i, skill in enumerate(skills):
                with cols[i % 2]:
                    with st.container():
                        st.markdown(f"""
                        <div class='skill-card'>
                            <div style='display: flex; align-items: flex-start; gap: 12px;'>
                                <div style='background: #238636; padding: 8px; border-radius: 6px;'>
                                    <span style='font-size: 1.2em;'>💻</span>
                                </div>
                                <div>
                                    <div style='font-weight: bold; font-size: 1.1em; color: #c9d1d9; margin-bottom: 4px;'>{skill['name']}</div>
                                    <div style='font-size: 0.9em; color: #8b949e; line-height: 1.4;'>{skill['desc']}</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        c_act1, c_act2 = st.columns([1, 1])
                        with c_act1:
                             key_suffix = f"sw_{category}_{i}"
                             if st.button("🔍 去安装", key=f"btn_search_{key_suffix}", use_container_width=True):
                                 st.session_state['market_search_query'] = skill['name']
                                 st.session_state['current_market_repo'] = "softaworks/agent-toolkit"
                                 if 'market_data' in st.session_state: del st.session_state['market_data']
                                 st.rerun()

    with tab_browse:
        # Check if search query was set from Testing tab
        default_search = st.session_state.get('market_search_query', '')
        if default_search:
             del st.session_state['market_search_query']
        
        # Featured Repos
        st.markdown("**推荐仓库**")
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        if col_f1.button("Vercel Labs", use_container_width=True):
            st.session_state['current_market_repo'] = "vercel-labs/agent-skills"
            if 'market_data' in st.session_state: del st.session_state['market_data']
            st.rerun()
            
        if col_f2.button("ComposioHQ", use_container_width=True):
             st.session_state['current_market_repo'] = "ComposioHQ/awesome-claude-skills"
             if 'market_data' in st.session_state: del st.session_state['market_data']
             st.rerun()
             
        if col_f3.button("Anthropic Skills", use_container_width=True, help="Official Anthropic Skills"):
             st.session_state['current_market_repo'] = "anthropics/skills"
             if 'market_data' in st.session_state: del st.session_state['market_data']
             st.rerun()
        
        if col_f4.button("OpenAI Skills", use_container_width=True, help="Official OpenAI Codex Skills"): 
             st.session_state['current_market_repo'] = "openai/skills"
             if 'market_data' in st.session_state: del st.session_state['market_data']
             st.rerun()

        # Row 2
        col_f5, col_f6, _, _ = st.columns(4)
        if col_f5.button("Claude Plugins", use_container_width=True, help="Official Claude Code Plugins"):
             st.session_state['current_market_repo'] = "anthropics/claude-plugins-official"
             if 'market_data' in st.session_state: del st.session_state['market_data']
             st.rerun()

        st.markdown("**更多资源**")
        col_ext1, col_ext2 = st.columns([1, 3])
        with col_ext1:
             st.markdown("""
             <a href="https://skillsmp.com/" target="_blank" style="text-decoration: none;">
                 <div style="background-color: #21262d; border: 1px solid #30363d; border-radius: 6px; padding: 10px; text-align: center; color: #c9d1d9; transition: 0.2s;">
                     🌍 访问 SkillsMP.com
                 </div>
             </a>
             """, unsafe_allow_html=True)
        with col_ext2:
             st.caption("SkillsMP 是一个聚合了成千上万 Agent Skills 的第三方市场。")

        current_repo = st.session_state.get('current_market_repo', 'vercel-labs/agent-skills')
        st.caption(f"当前仓库: `{current_repo}`")

        # Load Market Data
        if 'market_data' not in st.session_state:
            with st.spinner(f"正在从 {current_repo} 加载技能列表..."):
                official_skills, err = utils.get_repo_skills(current_repo)
                if official_skills:
                    st.session_state['market_data'] = official_skills
                else:
                    st.error(f"Failed to load market data: {err}")
                    st.session_state['market_data'] = []

        # Filter
        col_search, col_sort = st.columns([3, 1])
        with col_search:
            market_search = st.text_input("🔍 搜索市场...", value=default_search, label_visibility="collapsed")
        with col_sort:
            st.caption(f"共 {len(st.session_state['market_data'])} 个技能")

        # Display Grid
        market_skills = st.session_state['market_data']
        if market_search:
            market_skills = [s for s in market_skills if market_search.lower() in s['name'].lower() or market_search.lower() in s['description'].lower()]
        
        if not market_skills:
            st.info("No skills found.")
        else:
            cols = st.columns(3)
            for i, skill in enumerate(market_skills):
                with cols[i % 3]:
                    with st.container():
                        st.markdown(f"""
                        <div class='market-card'>
                            <div>
                                <h4>{skill['name']}</h4>
                                <div class='repo-link'>{skill.get('repo', current_repo)}</div>
                                <div style='font-size:0.9em; color:#c9d1d9; line-height:1.4;'>{skill.get('description', '')[:100]}...</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button("📥 安装", key=f"mkt_inst_{i}", use_container_width=True):
                             repo = skill.get('repo', current_repo)
                             with st.spinner(f"Installing {skill['name']}..."):
                                 utils.install_skill(repo, skill['name'])
                                 st.success("Installed!")

    with tab_local:
        st.info("输入本地 Skill 路径进行安装")
        path = st.text_input("本地路径", placeholder="/Users/username/my-skill")
        if st.button("安装本地 Skill"):
            if path:
                with st.spinner("Installing..."):
                    stdout, stderr = utils.install_skill(path)
                    if stderr and "error" in stderr.lower():
                        st.error(stderr)
                    else:
                        st.success("Done")

    with tab_git:
        st.info("输入 GitHub 仓库地址")
        col_repo, col_btn = st.columns([3, 1])
        with col_repo:
            repo = st.text_input("GitHub Repo", placeholder="owner/repo", label_visibility="collapsed")
        with col_btn:
            if st.button("获取列表", use_container_width=True):
                with st.spinner("Fetching..."):
                    skills, err = utils.get_repo_skills(repo)
                    if skills:
                        st.session_state['custom_repo_skills'] = skills
                        st.session_state['custom_repo_name'] = repo
                    else:
                        st.error(err)
        
        if 'custom_repo_skills' in st.session_state:
            st.divider()
            st.subheader(f"📦 {st.session_state['custom_repo_name']}")
            for skill in st.session_state['custom_repo_skills']:
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f"**{skill['name']}**")
                    st.caption(skill['description'])
                with c2:
                    if st.button("安装", key=f"cust_inst_{skill['name']}"):
                         with st.spinner("Installing..."):
                             utils.install_skill(st.session_state['custom_repo_name'], skill['name'])
                             st.success("Installed!")
