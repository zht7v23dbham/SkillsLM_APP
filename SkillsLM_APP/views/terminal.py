
import streamlit as st
import SkillsLM_APP.core.utils as utils
import shlex

def render_view():
    """Render Terminal / CLI View."""
    st.title("🖥️ 终端命令")
    st.markdown("<p class='header-subtitle'>执行 npx skills 原生命令</p>", unsafe_allow_html=True)
    
    # Predefined commands
    st.markdown("### 常用命令")
    col_cmd1, col_cmd2, col_cmd3, col_cmd4 = st.columns(4)
    
    if col_cmd1.button("🩺 Doctor (诊断)", use_container_width=True):
        st.session_state['cli_output'] = utils.run_command(["doctor"])
        
    if col_cmd2.button("❓ Help (帮助)", use_container_width=True):
        st.session_state['cli_output'] = utils.run_command(["--help"])
        
    if col_cmd3.button("🔄 Update (更新)", use_container_width=True):
        st.session_state['cli_output'] = utils.run_command(["update"])
        
    if col_cmd4.button("🔍 Check (检查)", use_container_width=True):
        st.session_state['cli_output'] = utils.run_command(["check"])

    st.divider()

    # Raw Command Input
    st.markdown("### 自定义命令")
    st.info("无需输入 `npx skills`，直接输入子命令和参数。例如: `search query` 或 `list -g`")
    
    with st.form("cli_form"):
        cmd_input = st.text_input("命令", placeholder="e.g. doctor")
        submitted = st.form_submit_button("执行")
        
        if submitted and cmd_input:
            # Parse args roughly
            args = shlex.split(cmd_input)
            with st.spinner(f"Running `npx skills {cmd_input}`..."):
                stdout, stderr = utils.run_command(args)
                st.session_state['cli_output'] = (stdout, stderr)

    # Output Display
    if 'cli_output' in st.session_state:
        stdout, stderr = st.session_state['cli_output']
        
        if stdout:
            st.success("Output:")
            st.code(stdout, language="bash")
        
        if stderr:
            st.error("Error/Log:")
            st.code(stderr, language="bash")
