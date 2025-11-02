# 🇩🇪 德语学习工具 (DeutschNest)

一个功能完整的德语学习网页工具，基于 Python + Streamlit 构建。

## ✨ 功能特点

### 1️⃣ 内容管理
- **多种内容类型**：支持单词、短语、句子输入
- **批量导入**：支持从文本文件或 CSV 批量导入
- **自动解析**：使用 spaCy 自动提取词根、词性和句型标签

### 2️⃣ 数据库管理
- **SQLite 存储**：轻量级本地数据库
- **完整字段**：id, type, content, translation, lemma, tags, examples, created_at, last_reviewed, review_count
- **增删查改**：完整的 CRUD 操作
- **搜索筛选**：支持关键词、类型、标签多维度筛选

### 3️⃣ 复习模式
- **遮词填空**：随机隐藏关键词，测试记忆
- **反向翻译**：英文 → 德语翻译练习
- **听写模式**：TTS 播放德语内容，用户输入检测
- **随机抽题**：可按标签/句型随机选择复习内容

### 4️⃣ 条目关联功能 ⭐ 新功能
- **标签匹配**：首先通过 tags 字段匹配同一主题的条目
- **语义相似度**：使用 sentence-transformers 生成向量，计算余弦相似度
- **相关条目展示**：在条目详情和复习页面显示 top 5 相关条目
- **相似度排序**：按语义相似度从高到低排序显示

### 5️⃣ AI 辅助（预留接口）
- 自动生成例句
- 自动生成周复习集
- 可接入 OpenAI/Anthropic 等 AI API

### 6️⃣ 导出功能
- 导出为 CSV 格式
- 导出为 Anki 卡组（.apkg）

## 🚀 快速开始

### 1. 创建虚拟环境（已完成）

```bash
python3 -m venv venv
```

### 2. 激活虚拟环境

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 安装德语 NLP 模型

```bash
python -m spacy download de_core_news_sm
```

### 5. 首次运行会自动下载 sentence-transformers 模型

首次运行时，系统会自动下载 `paraphrase-multilingual-MiniLM-L12-v2` 模型用于生成语义向量。

### 6. 运行应用

```bash
streamlit run app.py
```

应用会在浏览器中自动打开，默认地址：`http://localhost:8501`

## 📁 项目结构

```
DeutschNest/
├── app.py              # Streamlit 主应用
├── database.py         # 数据库管理模块
├── nlp_parser.py       # NLP 解析模块
├── embedding_utils.py # Embedding 向量生成和相似度查询
├── utils.py            # 工具函数
├── requirements.txt    # Python 依赖
├── README.md          # 项目说明
├── venv/              # 虚拟环境
└── german_learning.db # SQLite 数据库（自动生成）
```

## 📖 使用说明

### 添加条目

1. 进入「➕ 添加」页面
2. 输入德语内容和英文翻译
3. 选择类型（单词/短语/句子）
4. 点击「保存并解析」- 系统会自动提取词根和标签

### 搜索和管理

1. 进入「🔍 搜索/管理」页面
2. 使用关键词、类型、标签筛选
3. 点击条目可展开详情
4. 支持编辑和删除操作

### 复习练习

1. 进入「📚 复习」页面
2. 选择复习模式（遮词填空/反向翻译/听写）
3. 可选择性筛选标签
4. 点击「随机抽题」开始复习
5. 完成后标记为已复习，系统会记录复习次数

### 查看相关条目

1. 在「🔍 搜索/管理」页面，展开任意条目详情
2. 在「📚 复习」页面，显示答案后
3. 系统会显示最多 5 条相关条目，按相似度排序
4. 相关条目显示内容包括：德语内容、翻译、标签、类型和相似度百分比

### 导出数据

1. 进入「⚙️ 设置/导出」页面
2. 点击「导出 CSV」或「导出 Anki」
3. 下载文件保存

## 🛠️ 技术栈

- **Python 3.8+**
- **Streamlit**: Web 应用框架
- **spaCy**: NLP 文本解析
- **SQLite**: 本地数据库
- **genanki**: Anki 卡组生成
- **pyttsx3**: 文本转语音（TTS）
- **sentence-transformers**: 语义向量生成和相似度计算
- **torch**: PyTorch（sentence-transformers 依赖）

## 📝 注意事项

1. **首次运行**：需要安装德语 NLP 模型 `de_core_news_sm`
2. **TTS 功能**：pyttsx3 在某些系统上可能需要额外配置，如不可用可考虑使用在线 TTS
3. **数据库**：数据存储在本地 SQLite 文件 `german_learning.db`
4. **移动端**：支持在手机浏览器中访问，界面会自动适配

## 🔮 后续计划

- [ ] 接入 AI API 自动生成例句
- [ ] 实现云端同步（Supabase/Firebase）
- [ ] 添加更多复习模式（选择题、匹配题等）
- [ ] 添加学习统计和图表
- [ ] 支持多语言翻译（不只是英文）
- [ ] 实现间隔重复算法（Spaced Repetition）

## 📄 许可证

MIT License

## 👥 贡献

欢迎提交 Issue 和 Pull Request！

