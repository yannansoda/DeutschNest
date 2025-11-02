#!/bin/bash

# 德语学习工具快速启动脚本

echo "🇩🇪 启动 DeutschNest..."

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在，请先运行 ./install.sh"
    exit 1
fi

# 激活虚拟环境
source venv/bin/activate

# 检查依赖是否已安装
if ! python -c "import streamlit" 2>/dev/null; then
    echo "📥 检测到依赖未安装，正在安装..."
    pip install -r requirements.txt
fi

# 检查 spacy 德语模型
if ! python -c "import spacy; spacy.load('de_core_news_sm')" 2>/dev/null; then
    echo "🌐 安装德语 NLP 模型..."
    python -m spacy download de_core_news_sm
fi

# 启动应用
echo "🚀 启动 Streamlit 应用..."
streamlit run app.py

