#!/usr/bin/env python3
"""
README.md 转换为 guide.html 的脚本

功能：
- 从 README.md 提取版本号和功能特性
- 更新 guide.html 中的版本号
- 保持 guide.html 的精美样式不变

使用方法：
    python scripts/readme_to_guide.py
    
或指定路径：
    python scripts/readme_to_guide.py --readme README.md --guide website/guide.html
"""

import re
import argparse
from pathlib import Path


def extract_version_from_readme(readme_path: Path) -> str:
    """从 README.md 提取版本号"""
    content = readme_path.read_text(encoding='utf-8')
    
    # 匹配 version badge: https://img.shields.io/badge/version-2.9.1-blue.svg
    match = re.search(r'badge/version-(\d+\.\d+\.\d+)-', content)
    if match:
        return match.group(1)
    
    # 备选：匹配 v2.9.1 格式
    match = re.search(r'v(\d+\.\d+\.\d+)', content)
    if match:
        return match.group(1)
    
    raise ValueError(f"无法从 {readme_path} 提取版本号")


def update_guide_version(guide_path: Path, version: str) -> bool:
    """更新 guide.html 中的版本号"""
    content = guide_path.read_text(encoding='utf-8')
    original = content
    
    # 更新 <span class="version">vX.X.X</span>
    content = re.sub(
        r'(<span class="version">v)\d+\.\d+\.\d+(</span>)',
        rf'\g<1>{version}\2',
        content
    )
    
    if content != original:
        guide_path.write_text(content, encoding='utf-8')
        return True
    return False


def main():
    parser = argparse.ArgumentParser(description='将 README.md 版本号同步到 guide.html')
    parser.add_argument('--readme', default='README.md', help='README.md 路径')
    parser.add_argument('--guide', default='website/guide.html', help='guide.html 路径')
    args = parser.parse_args()
    
    # 确定脚本所在目录（hugescreenshot-releases/scripts/）
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    
    readme_path = repo_root / args.readme
    guide_path = repo_root / args.guide
    
    if not readme_path.exists():
        print(f"❌ 找不到 README: {readme_path}")
        return 1
    
    if not guide_path.exists():
        print(f"❌ 找不到 guide.html: {guide_path}")
        return 1
    
    try:
        version = extract_version_from_readme(readme_path)
        print(f"📖 从 README.md 提取版本号: v{version}")
        
        if update_guide_version(guide_path, version):
            print(f"✅ guide.html 版本号已更新为 v{version}")
        else:
            print(f"ℹ️  guide.html 版本号已是 v{version}，无需更新")
        
        return 0
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return 1


if __name__ == '__main__':
    exit(main())
