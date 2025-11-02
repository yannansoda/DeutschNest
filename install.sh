#!/bin/bash

# 德语学习工具安装脚本

echo "🇩🇪 DeutschNest 安装脚本"
echo "========================"

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在，正在创建..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "📦 激活虚拟环境..."
source venv/bin/activate

# 升级 pip
echo "⬆️  升级 pip..."
pip install --upgrade pip

# 安装依赖
echo "📥 安装依赖包..."
pip install -r requirements.txt

# 安装德语 NLP 模型
echo "🌐 安装德语 NLP 模型 (spacy)..."
python -m spacy download de_core_news_sm

echo ""
echo "✅ 安装完成！"
echo ""
echo "🚀 运行应用："
echo "   source venv/bin/activate"
echo "   streamlit run app.py"
echo ""

