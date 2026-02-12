
import streamlit as st
import os
import sys
import SkillsLM_APP.core.utils as utils

def render_view():
    """Render Prompt Generator View."""
    st.title("✨ 智能提示词生成器")
    st.markdown("<p class='header-subtitle'>基于 skill-prompt-generator 的多领域提示词生成系统</p>", unsafe_allow_html=True)

    # Setup path to import generator
    # Assuming standard structure relative to this file:
    # SkillsLM_APP/views/prompts.py -> ../../skill-prompt-generator-main
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir)) # Up 2 levels to root
    generator_path = os.path.join(project_root, "skill-prompt-generator-main")
    
    if generator_path not in sys.path:
        sys.path.insert(0, generator_path)
    
    try:
        from core.cross_domain_generator import CrossDomainGenerator
        
        # Initialize generator (cache it)
        if 'prompt_generator' not in st.session_state:
            with st.spinner("初始化生成器核心..."):
                # Construct paths relative to the generator directory
                db_path = os.path.join(generator_path, "extracted_results", "elements.db")
                yaml_dir = os.path.join(generator_path, "variables")
                st.session_state['prompt_generator'] = CrossDomainGenerator(db_path=db_path, yaml_dir=yaml_dir)
        
        generator = st.session_state['prompt_generator']
        
        with st.container():
            st.markdown("""
            <div class='skill-card'>
                <h4>输入您的需求</h4>
                <p style='color:#8b949e; font-size:0.9em;'>
                支持自然语言输入，自动识别领域：
                <br>• <b>软件工程</b>: "用Python写一个登录API测试脚本", "部署Docker容器"
                <br>• <b>艺术设计</b>: "温馨可爱的儿童海报", "赛博朋克风格的城市"
                <br>• <b>人像摄影</b>: "年轻女性肖像，电影级光影"
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            user_input = st.text_area("描述", height=100, placeholder="例如：编写一个Python脚本测试用户登录接口...")
            
            col_btn, col_type = st.columns([1, 2])
            with col_type:
                gen_type = st.selectbox("强制指定类型 (可选)", ["auto", "software", "design", "portrait", "cross_domain"], index=0)
            
            if col_btn.button("🚀 生成提示词", use_container_width=True):
                if not user_input:
                    st.warning("请输入描述")
                else:
                    with st.spinner("正在分析意图并生成..."):
                        try:
                            result = generator.generate(user_input, generation_type=gen_type)
                            st.session_state['gen_result'] = result
                        except Exception as e:
                            st.error(f"生成失败: {str(e)}")
                            import traceback
                            st.code(traceback.format_exc())

        if 'gen_result' in st.session_state:
            result = st.session_state['gen_result']
            st.divider()
            
            st.subheader("生成结果")
            
            # Metadata
            c1, c2, c3 = st.columns(3)
            with c1:
                st.info(f"**类型**: {result['type']}")
            with c2:
                meta = result.get('metadata', {})
                if result['type'] == 'software':
                    st.success(f"**角色**: {meta.get('role', 'N/A')}")
                elif result['type'] == 'design':
                    st.success(f"**风格**: {meta.get('design_style', 'N/A')}")
                else:
                    st.success(f"**元素数**: {meta.get('element_count', 0)}")
            with c3:
                if result['type'] == 'software':
                    st.warning(f"**任务**: {meta.get('task', 'N/A')}")
                else:
                    st.warning(f"**Domain**: {', '.join(meta.get('domains_used', []))}")

            # Prompt Display
            st.markdown("### 📝 完整提示词")
            st.code(result['prompt'], language="text")
            
            c_copy, c_save = st.columns([1, 1])
            with c_copy:
                if st.button("📋 复制到剪贴板"):
                    st.write("已复制! (模拟)") # Streamlit restriction
            
            with c_save:
                if st.button("💾 保存为工程 Skill"):
                    st.session_state['save_skill_dialog'] = True
            
            if st.session_state.get('save_skill_dialog'):
                with st.form("save_skill_form"):
                    st.write("保存为本地 Skill")
                    new_skill_name = st.text_input("Skill 名称", value="my-generated-skill")
                    new_skill_desc = st.text_input("描述", value=f"Generated from prompt: {result['type']}")
                    
                    if st.form_submit_button("确认保存"):
                        # Use project root from earlier
                        target_dir = os.path.join(project_root, "generated_skills")
                        
                        success, err = utils.create_skill_from_prompt(
                            new_skill_name, 
                            result['prompt'], 
                            new_skill_desc, 
                            target_dir
                        )
                        
                        if success:
                            st.success(f"已保存到 {target_dir}/{new_skill_name}")
                            st.session_state['show_generated_skills'] = True # Enable view in Testing Agent tab (or we should add view here too)
                            st.session_state['save_skill_dialog'] = False
                        else:
                            st.error(f"保存失败: {err}")

    except ImportError as e:
        st.error(f"无法加载生成器模块: {e}")
        st.info(f"搜索路径: {generator_path}")
    except Exception as e:
        st.error(f"初始化错误: {e}")
