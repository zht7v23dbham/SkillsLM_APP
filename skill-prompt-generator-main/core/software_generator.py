
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
软件工程生成器 - 基于YAML模板生成测试/开发/部署提示词
"""

import os
import yaml
from typing import Dict, List, Optional

class SoftwareGenerator:
    """软件工程提示词生成器"""

    def __init__(self, yaml_dir: str = "variables"):
        self.yaml_path = os.path.join(yaml_dir, "software.yaml")
        self.data = self._load_yaml()

    def _load_yaml(self) -> Dict:
        """加载YAML配置"""
        if not os.path.exists(self.yaml_path):
            print(f"Warning: {self.yaml_path} not found.")
            return {}
        
        with open(self.yaml_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def generate(self, intent: Dict) -> Dict:
        """
        生成软件工程提示词
        
        Args:
            intent: 解析后的用户意图
            
        Returns:
            生成结果字典
        """
        # 1. 确定角色 (Role)
        role_key = self._determine_role(intent)
        role_data = self.data.get('roles', {}).get(role_key, {})
        role_desc = role_data.get('description', "You are a software engineering expert.")

        # 2. 确定任务 (Task)
        task_type = intent.get('software_task', 'code_generation')
        task_template = self.data.get('tasks', {}).get(task_type, {}).get('template', "")

        # 3. 填充变量
        language = intent.get('language', 'Python') # Default to Python
        framework = intent.get('framework', 'standard library')
        
        # 如果用户没指定framework，尝试自动推荐
        if framework == 'standard library':
            framework = self._recommend_framework(language, task_type)

        # 填充模板
        # 简单的字符串替换，实际应用可能需要更复杂的模板引擎
        task_desc = task_template.replace("{language}", language)
        task_desc = task_desc.replace("{framework}", framework)
        task_desc = task_desc.replace("{tool}", intent.get('tool', 'tool'))
        
        # 处理动态内容
        raw_input = intent.get('raw_input', '')
        if "{feature}" in task_desc:
            # 尝试从raw_input提取feature描述，或者直接使用raw_input
            task_desc = task_desc.replace("{feature}", f"'{raw_input}'")
        if "{target}" in task_desc:
            task_desc = task_desc.replace("{target}", "the specified target")
        if "{stages}" in task_desc:
             task_desc = task_desc.replace("{stages}", "build, test, deploy")
        if "{load}" in task_desc:
            task_desc = task_desc.replace("{load}", "1000")
        if "{type}" in task_desc:
             task_desc = task_desc.replace("{type}", "script")


        # 4. 组合最终Prompt
        prompt = f"{role_desc}\n\nTask:\n{task_desc}\n\nInput Context:\n{raw_input}\n\nConstraints:\n- Ensure code quality and best practices.\n- Include comments and documentation."

        return {
            'prompt': prompt,
            'type': 'software',
            'metadata': {
                'role': role_key,
                'task': task_type,
                'language': language,
                'framework': framework
            }
        }

    def _determine_role(self, intent: Dict) -> str:
        """根据意图确定角色"""
        raw_input = intent.get('raw_input', '').lower()
        software_task = intent.get('software_task', '')

        # 优先匹配task对应的角色
        if 'test' in software_task:
            return 'qa_engineer'
        if 'deploy' in software_task or 'pipeline' in software_task or 'docker' in software_task:
            return 'devops_engineer'
        if 'architecture' in software_task or 'design' in software_task or 'schema' in software_task:
            return 'system_architect'
        if 'security' in software_task or 'audit' in software_task:
            return 'security_engineer'
        if 'readme' in software_task or 'doc' in software_task:
            return 'tech_writer'
            
        if 'ui' in raw_input or 'frontend' in raw_input or 'css' in raw_input:
            return 'frontend_dev'
        
        # 默认后端
        return 'backend_dev'

    def _recommend_framework(self, language: str, task_type: str) -> str:
        """根据语言和任务推荐框架"""
        lang_key = language.lower()
        lang_config = self.data.get('languages', {}).get(lang_key)
        
        if not lang_config:
            return "standard library"

        frameworks = lang_config.get('frameworks', {})
        
        if 'test' in task_type:
            return frameworks.get('testing', ['standard library'])[0]
        if 'performance' in task_type:
            return frameworks.get('performance', ['standard library'])[0]
        
        # Default web/general
        return frameworks.get('web', ['standard library'])[0]

