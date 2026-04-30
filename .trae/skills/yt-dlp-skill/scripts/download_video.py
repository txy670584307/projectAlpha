#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
yt-dlp视频下载工具

该脚本使用yt-dlp库下载视频，支持各种视频网站链接。
"""

import os
import subprocess
import argparse
import tempfile
import shutil

def check_yt_dlp():
    """
    检查yt-dlp是否已安装
    
    Returns:
        bool: True if yt-dlp is installed, False otherwise
    """
    try:
        result = subprocess.run(
            ['yt-dlp', '--version'],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_yt_dlp():
    """
    安装yt-dlp
    """
    print("正在安装yt-dlp...")
    try:
        subprocess.run(
            ['pip', 'install', 'yt-dlp'],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("yt-dlp安装成功！")
        return True
    except Exception as e:
        print(f"安装失败: {str(e)}")
        return False

def download_video(url, output_dir=None, quality='best', verbose=False):
    """
    下载视频
    
    Args:
        url (str): 视频链接
        output_dir (str): 输出目录，默认为当前目录
        quality (str): 视频质量，默认为'best'
        verbose (bool): 是否显示详细信息
        
    Returns:
        str: 下载的文件路径
    """
    # 检查yt-dlp
    if not check_yt_dlp():
        if not install_yt_dlp():
            print("无法安装yt-dlp，请手动安装后重试")
            return None
    
    # 设置输出目录
    if output_dir is None:
        output_dir = os.getcwd()
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 构建命令
    cmd = [
        'yt-dlp',
        '-o', f'{output_dir}/%(title)s.%(ext)s',
        url
    ]
    
    # 添加质量参数
    if quality != 'best':
        cmd.extend(['-f', quality])
    
    if verbose:
        cmd.append('-v')
    
    print(f"开始下载视频: {url}")
    print(f"输出目录: {output_dir}")
    
    try:
        # 执行下载
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            # 提取下载的文件名
            lines = result.stdout.split('\n')
            output_file = None
            
            for line in lines:
                if 'Destination:' in line:
                    output_file = line.split('Destination: ')[1].strip()
                    break
            
            if output_file:
                print(f"\n✅ 下载成功！")
                print(f"文件保存路径: {output_file}")
                return output_file
            else:
                print(f"\n✅ 下载成功，但无法确定文件路径")
                return None
        else:
            print(f"\n❌ 下载失败:")
            print(result.stderr)
            return None
            
    except Exception as e:
        print(f"\n❌ 下载过程中发生错误: {str(e)}")
        return None

def main():
    parser = argparse.ArgumentParser(description='使用yt-dlp下载视频')
    parser.add_argument('url', help='视频链接')
    parser.add_argument('-o', '--output', help='输出目录')
    parser.add_argument('-q', '--quality', default='best', help='视频质量 (默认: best)')
    parser.add_argument('-v', '--verbose', action='store_true', help='显示详细信息')
    
    args = parser.parse_args()
    
    download_video(
        args.url,
        output_dir=args.output,
        quality=args.quality,
        verbose=args.verbose
    )

if __name__ == '__main__':
    main()