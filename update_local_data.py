# update_local_data.py
# -*- coding: utf-8 -*-
"""
统一调度脚本：一键更新本地研究热点数据（大脚本）。
"""

import os
import sys
import time
import traceback
import subprocess
from datetime import datetime


# =========================
# 0. 安全打印工具
# =========================
def safe_print(text: str):
    """
    在不同控制台编码下安全打印字符串。
    """
    try:
        print(text, flush=True) # 加上 flush=True 确保日志即时推送到前端
    except UnicodeEncodeError:
        encoding = sys.stdout.encoding or "utf-8"
        safe_text = text.encode(encoding, errors="replace").decode(encoding)
        print(safe_text, flush=True)

# =========================
# 1. 导入全局配置以锚定根目录
# =========================
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = CURRENT_DIR
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from config import BASE_DIR


# =========================
# 2. 工具函数：执行子脚本 (已升级为流式输出 + 强制 UTF-8)
# =========================
def run_step(cmd: list, step_name: str):
    safe_print(f"\n[{datetime.now().strftime('%H:%M:%S')}] === 开始步骤：{step_name} ===")
    start_t = time.time()

    # 【关键修复 1】：强制为子脚本注入 UTF-8 环境，彻底防止子脚本 print Emoji 时崩溃
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    try:
        # 【关键修复 2】：使用 Popen 替代 run，实现子脚本日志的“边运行边输出”
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, # 将错误日志合并到标准输出，防止丢失
            text=True,
            encoding="utf-8",         # 强制按 utf-8 解析管道数据
            errors="replace",
            bufsize=1,                # 行缓冲
            env=env
        )

        # 实时逐行读取子脚本的输出，并通过 safe_print 抛给外层（供 Streamlit UI 捕获）
        for line in process.stdout:
            safe_print(line.rstrip('\n'))

        # 等待子进程完全结束
        process.wait()
        elapsed = time.time() - start_t

        if process.returncode != 0:
            safe_print(f"❌ 步骤失败：{step_name}（耗时 {elapsed:.1f} 秒，返回码 {process.returncode}）")
            raise RuntimeError(f"{step_name} 失败，返回码 {process.returncode}")
        else:
            safe_print(f"✅ 步骤完成：{step_name}（耗时 {elapsed:.1f} 秒）")

    except Exception as e:
        safe_print(f"运行 {step_name} 时异常：{e}")
        traceback.print_exc()
        raise

# =========================
# 3. 总流程入口
# =========================
def run_full_update():
    overall_start = time.time()
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    safe_print(f"{ts} 🚀 开始本地数据全量更新流程...")

    arxiv_path = str(BASE_DIR / "arxiv_crawler.py")
    openalex_path = str(BASE_DIR / "openalex_crawler.py")
    cleaner_path = str(BASE_DIR / "cleaner.py")
    bertopic_path = str(BASE_DIR / "chuli2.py")
    namer_path = str(BASE_DIR / "namer.py")
    reviews_path = str(BASE_DIR / "review5.py")

    for script_path, name in [
        (arxiv_path, "arxiv_crawler.py"),
        (openalex_path, "openalex_crawler.py"),
        (cleaner_path, "cleaner.py"),
        (bertopic_path, "chuli2.py"),
        (namer_path, "namer.py"),
        (reviews_path, "review5.py"),
    ]:
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"找不到脚本 {name}，预期路径为：{script_path}")

    # --- 依次执行各步骤 ---
    run_step([sys.executable, arxiv_path], "arXiv 爬虫")
    run_step([sys.executable, openalex_path], "OpenAlex 爬虫")
    run_step([sys.executable, cleaner_path], "数据清洗")
    run_step([sys.executable, bertopic_path], "BERTopic 主题聚类")
    run_step([sys.executable, namer_path], "LLM 热点中文命名")
    run_step([sys.executable, reviews_path], "LLM 本地热点综述生成")

    overall_elapsed = time.time() - overall_start
    ts_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    safe_print(f"\n🎉 {ts_end} 本地数据更新流程全部完成，总耗时约 {overall_elapsed/60:.1f} 分钟。")

if __name__ == "__main__":
    run_full_update()
