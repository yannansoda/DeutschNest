"""
多语言文本字典
支持语言：中文、English、Deutsch
"""
TEXTS = {
    # 侧边栏
    "sidebar_title": {
        "中文": "🇩🇪 DeutschNest",
        "English": "🇩🇪 DeutschNest",
        "Deutsch": "🇩🇪 DeutschNest"
    },
    "navigation": {
        "中文": "导航",
        "English": "Navigation",
        "Deutsch": "Navigation"
    },
    "nav_home": {
        "中文": "🏠 主页",
        "English": "🏠 Home",
        "Deutsch": "🏠 Startseite"
    },
    "nav_add": {
        "中文": "➕ 添加",
        "English": "➕ Add",
        "Deutsch": "➕ Hinzufügen"
    },
    "nav_search": {
        "中文": "🔍 搜索/管理",
        "English": "🔍 Search/Manage",
        "Deutsch": "🔍 Suchen/Verwalten"
    },
    "nav_review": {
        "中文": "📚 复习",
        "English": "📚 Review",
        "Deutsch": "📚 Wiederholen"
    },
    "nav_settings": {
        "中文": "⚙️ 设置/导出",
        "English": "⚙️ Settings/Export",
        "Deutsch": "⚙️ Einstellungen/Exportieren"
    },
    "language_select": {
        "中文": "选择语言 / Select Language / Sprache wählen",
        "English": "选择语言 / Select Language / Sprache wählen",
        "Deutsch": "选择语言 / Select Language / Sprache wählen"
    },
    
    # 主页
    "title_home": {
        "中文": "🇩🇪 德语学习工具",
        "English": "🇩🇪 German Learning Tool",
        "Deutsch": "🇩🇪 Deutsch Lernwerkzeug"
    },
    "metric_total": {
        "中文": "总条目",
        "English": "Total Items",
        "Deutsch": "Gesamt Einträge"
    },
    "metric_word": {
        "中文": "单词",
        "English": "Words",
        "Deutsch": "Wörter"
    },
    "metric_phrase": {
        "中文": "短语",
        "English": "Phrases",
        "Deutsch": "Phrasen"
    },
    "metric_sentence": {
        "中文": "句子",
        "English": "Sentences",
        "Deutsch": "Sätze"
    },
    "recent_added": {
        "中文": "📝 最近添加",
        "English": "📝 Recently Added",
        "Deutsch": "📝 Kürzlich hinzugefügt"
    },
    "label_german": {
        "中文": "德语:",
        "English": "German:",
        "Deutsch": "Deutsch:"
    },
    "label_translation": {
        "中文": "翻译:",
        "English": "Translation:",
        "Deutsch": "Übersetzung:"
    },
    "label_tags": {
        "中文": "标签:",
        "English": "Tags:",
        "Deutsch": "Tags:"
    },
    "label_lemma": {
        "中文": "词根:",
        "English": "Lemma:",
        "Deutsch": "Lemma:"
    },
    "no_items_msg": {
        "中文": "还没有条目，去「添加」页面开始学习吧！",
        "English": "No items yet. Go to the \"Add\" page to start learning!",
        "Deutsch": "Noch keine Einträge. Gehen Sie zur Seite \"Hinzufügen\", um zu beginnen!"
    },
    
    # 添加页面
    "title_add": {
        "中文": "➕ 添加新条目",
        "English": "➕ Add New Item",
        "Deutsch": "➕ Neuen Eintrag hinzufügen"
    },
    "subtitle_single_add": {
        "中文": "📝 单条添加",
        "English": "📝 Single Item Add",
        "Deutsch": "📝 Einzelner Eintrag"
    },
    "label_german_content": {
        "中文": "德语内容",
        "English": "German Content",
        "Deutsch": "Deutscher Inhalt"
    },
    "placeholder_german_content": {
        "中文": "输入德语单词、短语或句子",
        "English": "Enter German word, phrase or sentence",
        "Deutsch": "Deutsches Wort, Phrase oder Satz eingeben"
    },
    "label_type": {
        "中文": "类型",
        "English": "Type",
        "Deutsch": "Typ"
    },
    "type_word": {
        "中文": "单词",
        "English": "Word",
        "Deutsch": "Wort"
    },
    "type_phrase": {
        "中文": "短语",
        "English": "Phrase",
        "Deutsch": "Phrase"
    },
    "type_sentence": {
        "中文": "句子",
        "English": "Sentence",
        "Deutsch": "Satz"
    },
    "label_translation_optional": {
        "中文": "英文翻译（可选）",
        "English": "English Translation (Optional)",
        "Deutsch": "Englische Übersetzung (Optional)"
    },
    "placeholder_translation": {
        "中文": "输入对应的英文翻译",
        "English": "Enter corresponding English translation",
        "Deutsch": "Entsprechende englische Übersetzung eingeben"
    },
    "button_save": {
        "中文": "💾 保存并解析",
        "English": "💾 Save & Parse",
        "Deutsch": "💾 Speichern & Analysieren"
    },
    "auto_translated": {
        "中文": "🔄 已自动翻译:",
        "English": "🔄 Auto-translated:",
        "Deutsch": "🔄 Automatisch übersetzt:"
    },
    "auto_translate_failed": {
        "中文": "自动翻译失败:",
        "English": "Auto-translation failed:",
        "Deutsch": "Automatische Übersetzung fehlgeschlagen:"
    },
    "embedding_failed": {
        "中文": "生成 embedding 失败: numpy 未安装。请运行: pip install numpy>=1.21.0",
        "English": "Failed to generate embedding: numpy not installed. Please run: pip install numpy>=1.21.0",
        "Deutsch": "Embedding-Generierung fehlgeschlagen: numpy nicht installiert. Bitte ausführen: pip install numpy>=1.21.0"
    },
    "embedding_warning": {
        "中文": "生成 embedding 失败:",
        "English": "Failed to generate embedding:",
        "Deutsch": "Embedding-Generierung fehlgeschlagen:"
    },
    "embedding_info": {
        "中文": "条目已保存，但未生成 embedding。您可以稍后在设置中重新生成。",
        "English": "Item saved, but embedding was not generated. You can regenerate it later in settings.",
        "Deutsch": "Eintrag gespeichert, aber Embedding wurde nicht generiert. Sie können es später in den Einstellungen neu generieren."
    },
    "success_saved": {
        "中文": "✅ 已保存！",
        "English": "✅ Saved!",
        "Deutsch": "✅ Gespeichert!"
    },
    "view_parse_result": {
        "中文": "查看解析结果",
        "English": "View Parse Results",
        "Deutsch": "Analyseergebnisse anzeigen"
    },
    "label_pos": {
        "中文": "词性:",
        "English": "POS:",
        "Deutsch": "Wortart:"
    },
    "embedding_generated": {
        "中文": "✅ **Embedding 已生成**",
        "English": "✅ **Embedding Generated**",
        "Deutsch": "✅ **Embedding generiert**"
    },
    "nlp_not_initialized": {
        "中文": "NLP 解析器未初始化，请先安装德语模型",
        "English": "NLP parser not initialized, please install German model first",
        "Deutsch": "NLP-Parser nicht initialisiert, bitte installieren Sie zuerst das deutsche Modell"
    },
    "warning_empty_content": {
        "中文": "请输入德语内容",
        "English": "Please enter German content",
        "Deutsch": "Bitte geben Sie deutschen Inhalt ein"
    },
    "subtitle_batch_import": {
        "中文": "📦 批量导入",
        "English": "📦 Batch Import",
        "Deutsch": "📦 Batch-Import"
    },
    "label_import_type": {
        "中文": "导入类型",
        "English": "Import Type",
        "Deutsch": "Importtyp"
    },
    "label_import_method": {
        "中文": "导入方式",
        "English": "Import Method",
        "Deutsch": "Importmethode"
    },
    "method_text_input": {
        "中文": "文本输入",
        "English": "Text Input",
        "Deutsch": "Texteingabe"
    },
    "method_file_upload": {
        "中文": "文件上传",
        "English": "File Upload",
        "Deutsch": "Datei-Upload"
    },
    "label_batch_text": {
        "中文": "批量文本（每行一个条目，格式：德语内容 | 英文翻译）",
        "English": "Batch Text (one item per line, format: German | English)",
        "Deutsch": "Batch-Text (ein Eintrag pro Zeile, Format: Deutsch | Englisch)"
    },
    "button_batch_import": {
        "中文": "📥 批量导入",
        "English": "📥 Batch Import",
        "Deutsch": "📥 Batch-Import"
    },
    "success_batch_import": {
        "中文": "✅ 成功导入 {count} 条记录！",
        "English": "✅ Successfully imported {count} records!",
        "Deutsch": "✅ {count} Datensätze erfolgreich importiert!"
    },
    "warning_empty_text": {
        "中文": "请输入文本内容",
        "English": "Please enter text content",
        "Deutsch": "Bitte geben Sie Textinhalt ein"
    },
    "label_select_file": {
        "中文": "选择文件",
        "English": "Select File",
        "Deutsch": "Datei auswählen"
    },
    "label_file_preview": {
        "中文": "文件内容预览",
        "English": "File Content Preview",
        "Deutsch": "Dateivorschau"
    },
    "button_import_file": {
        "中文": "📥 导入文件",
        "English": "📥 Import File",
        "Deutsch": "📥 Datei importieren"
    },
    
    # 搜索/管理页面
    "title_search": {
        "中文": "🔍 搜索与管理",
        "English": "🔍 Search & Manage",
        "Deutsch": "🔍 Suchen & Verwalten"
    },
    "label_search_keyword": {
        "中文": "🔍 搜索关键词",
        "English": "🔍 Search Keyword",
        "Deutsch": "🔍 Suchbegriff"
    },
    "placeholder_search": {
        "中文": "输入关键词或短语",
        "English": "Enter keyword or phrase",
        "Deutsch": "Suchbegriff oder Phrase eingeben"
    },
    "label_type_filter": {
        "中文": "类型筛选",
        "English": "Type Filter",
        "Deutsch": "Typfilter"
    },
    "label_tag_filter": {
        "中文": "标签筛选",
        "English": "Tag Filter",
        "Deutsch": "Tag-Filter"
    },
    "filter_all": {
        "中文": "全部",
        "English": "All",
        "Deutsch": "Alle"
    },
    "results_found": {
        "中文": "找到 {count} 条结果",
        "English": "Found {count} results",
        "Deutsch": "{count} Ergebnisse gefunden"
    },
    "label_created_at": {
        "中文": "创建时间:",
        "English": "Created At:",
        "Deutsch": "Erstellt am:"
    },
    "label_review_count": {
        "中文": "复习次数:",
        "English": "Review Count:",
        "Deutsch": "Wiederholungsanzahl:"
    },
    "label_last_reviewed": {
        "中文": "最后复习:",
        "English": "Last Reviewed:",
        "Deutsch": "Zuletzt wiederholt:"
    },
    "button_delete": {
        "中文": "🗑️ 删除",
        "English": "🗑️ Delete",
        "Deutsch": "🗑️ Löschen"
    },
    "button_edit": {
        "中文": "✏️ 编辑",
        "English": "✏️ Edit",
        "Deutsch": "✏️ Bearbeiten"
    },
    "label_new_content": {
        "中文": "新德语内容",
        "English": "New German Content",
        "Deutsch": "Neuer deutscher Inhalt"
    },
    "label_new_translation": {
        "中文": "新翻译",
        "English": "New Translation",
        "Deutsch": "Neue Übersetzung"
    },
    "button_save_edit": {
        "中文": "💾 保存修改",
        "English": "💾 Save Changes",
        "Deutsch": "💾 Änderungen speichern"
    },
    "related_items": {
        "中文": "📌 相关条目",
        "English": "📌 Related Items",
        "Deutsch": "📌 Verwandte Einträge"
    },
    "similarity": {
        "中文": "相似度:",
        "English": "Similarity:",
        "Deutsch": "Ähnlichkeit:"
    },
    "no_related_items": {
        "中文": "暂无相关条目",
        "English": "No related items",
        "Deutsch": "Keine verwandten Einträge"
    },
    "get_related_failed": {
        "中文": "获取相关条目失败:",
        "English": "Failed to get related items:",
        "Deutsch": "Fehler beim Abrufen verwandter Einträge:"
    },
    "embedding_not_initialized": {
        "中文": "Embedding 管理器未初始化，无法显示相关条目",
        "English": "Embedding manager not initialized, cannot display related items",
        "Deutsch": "Embedding-Manager nicht initialisiert, verwandte Einträge können nicht angezeigt werden"
    },
    
    # 复习页面
    "title_review": {
        "中文": "📚 复习模式",
        "English": "📚 Review Mode",
        "Deutsch": "📚 Wiederholungsmodus"
    },
    "label_review_mode": {
        "中文": "复习模式",
        "English": "Review Mode",
        "Deutsch": "Wiederholungsmodus"
    },
    "mode_cloze": {
        "中文": "遮词填空",
        "English": "Cloze Deletion",
        "Deutsch": "Lückentext"
    },
    "mode_reverse": {
        "中文": "反向翻译",
        "English": "Reverse Translation",
        "Deutsch": "Rückübersetzung"
    },
    "mode_dictation": {
        "中文": "听写",
        "English": "Dictation",
        "Deutsch": "Diktat"
    },
    "label_tag_filter_optional": {
        "中文": "标签筛选（可选）",
        "English": "Tag Filter (Optional)",
        "Deutsch": "Tag-Filter (Optional)"
    },
    "button_random": {
        "中文": "🎲 随机抽题",
        "English": "🎲 Random Question",
        "Deutsch": "🎲 Zufällige Frage"
    },
    "no_items_found": {
        "中文": "没有找到符合条件的条目",
        "English": "No items found matching criteria",
        "Deutsch": "Keine Einträge gefunden, die den Kriterien entsprechen"
    },
    "review_cloze": {
        "中文": "填空:",
        "English": "Fill in:",
        "Deutsch": "Ausfüllen:"
    },
    "label_your_answer": {
        "中文": "你的答案:",
        "English": "Your Answer:",
        "Deutsch": "Ihre Antwort:"
    },
    "button_show_answer": {
        "中文": "✅ 显示答案",
        "English": "✅ Show Answer",
        "Deutsch": "✅ Antwort anzeigen"
    },
    "correct_answer": {
        "中文": "正确答案:",
        "English": "Correct Answer:",
        "Deutsch": "Richtige Antwort:"
    },
    "button_mark_reviewed": {
        "中文": "📊 标记为已复习",
        "English": "📊 Mark as Reviewed",
        "Deutsch": "📊 Als wiederholt markieren"
    },
    "review_recorded": {
        "中文": "已记录复习",
        "English": "Review recorded",
        "Deutsch": "Wiederholung aufgezeichnet"
    },
    "review_reverse_label": {
        "中文": "英文翻译:",
        "English": "English Translation:",
        "Deutsch": "Englische Übersetzung:"
    },
    "review_reverse_input": {
        "中文": "请用德语回答:",
        "English": "Please answer in German:",
        "Deutsch": "Bitte auf Deutsch antworten:"
    },
    "match_score": {
        "中文": "匹配度:",
        "English": "Match Score:",
        "Deutsch": "Übereinstimmung:"
    },
    "review_dictation_label": {
        "中文": "播放德语内容，请听写:",
        "English": "Play German content, please dictate:",
        "Deutsch": "Deutschen Inhalt abspielen, bitte diktieren:"
    },
    "button_play_audio": {
        "中文": "🔊 播放音频",
        "English": "🔊 Play Audio",
        "Deutsch": "🔊 Audio abspielen"
    },
    "playback_complete": {
        "中文": "播放完成",
        "English": "Playback complete",
        "Deutsch": "Wiedergabe abgeschlossen"
    },
    "tts_unavailable": {
        "中文": "TTS 功能不可用:",
        "English": "TTS feature unavailable:",
        "Deutsch": "TTS-Funktion nicht verfügbar:"
    },
    "tts_online_info": {
        "中文": "你可以在浏览器中使用在线 TTS 工具",
        "English": "You can use online TTS tools in your browser",
        "Deutsch": "Sie können Online-TTS-Tools in Ihrem Browser verwenden"
    },
    "review_dictation_input": {
        "中文": "请听写:",
        "English": "Please dictate:",
        "Deutsch": "Bitte diktieren:"
    },
    "perfect_correct": {
        "中文": "🎉 完全正确！",
        "English": "🎉 Perfect!",
        "Deutsch": "🎉 Perfekt!"
    },
    
    # 设置/导出页面
    "title_settings": {
        "中文": "⚙️ 设置与导出",
        "English": "⚙️ Settings & Export",
        "Deutsch": "⚙️ Einstellungen & Export"
    },
    "subtitle_export": {
        "中文": "📊 数据导出",
        "English": "📊 Data Export",
        "Deutsch": "📊 Datenexport"
    },
    "button_export_csv": {
        "中文": "📥 导出 CSV",
        "English": "📥 Export CSV",
        "Deutsch": "📥 CSV exportieren"
    },
    "button_download_csv": {
        "中文": "⬇️ 下载 CSV 文件",
        "English": "⬇️ Download CSV File",
        "Deutsch": "⬇️ CSV-Datei herunterladen"
    },
    "button_export_anki": {
        "中文": "📥 导出 Anki",
        "English": "📥 Export Anki",
        "Deutsch": "📥 Anki exportieren"
    },
    "button_download_anki": {
        "中文": "⬇️ 下载 Anki 卡组",
        "English": "⬇️ Download Anki Deck",
        "Deutsch": "⬇️ Anki-Deck herunterladen"
    },
    "anki_success": {
        "中文": "Anki 卡组生成成功！",
        "English": "Anki deck generated successfully!",
        "Deutsch": "Anki-Deck erfolgreich generiert!"
    },
    "anki_error": {
        "中文": "生成 Anki 卡组时出错:",
        "English": "Error generating Anki deck:",
        "Deutsch": "Fehler beim Generieren des Anki-Decks:"
    },
    "no_data_export": {
        "中文": "没有数据可导出",
        "English": "No data to export",
        "Deutsch": "Keine Daten zum Exportieren"
    },
    "subtitle_ai": {
        "中文": "🤖 AI 辅助功能",
        "English": "🤖 AI Assistant Features",
        "Deutsch": "🤖 KI-Assistenten-Funktionen"
    },
    "ai_info": {
        "中文": "以下功能需要 AI API，可在后续版本中集成",
        "English": "The following features require AI API and can be integrated in future versions",
        "Deutsch": "Die folgenden Funktionen erfordern eine KI-API und können in zukünftigen Versionen integriert werden"
    },
    "expand_generate_example": {
        "中文": "自动生成例句",
        "English": "Auto Generate Examples",
        "Deutsch": "Beispiele automatisch generieren"
    },
    "label_input_word": {
        "中文": "输入单词",
        "English": "Enter Word",
        "Deutsch": "Wort eingeben"
    },
    "placeholder_example_word": {
        "中文": "例如: lernen",
        "English": "e.g.: lernen",
        "Deutsch": "z.B.: lernen"
    },
    "button_generate_example": {
        "中文": "生成例句",
        "English": "Generate Examples",
        "Deutsch": "Beispiele generieren"
    },
    "ai_api_required": {
        "中文": "此功能需要接入 AI API（如 OpenAI, Anthropic 等）",
        "English": "This feature requires AI API (e.g., OpenAI, Anthropic)",
        "Deutsch": "Diese Funktion erfordert eine KI-API (z.B. OpenAI, Anthropic)"
    },
    "expand_weekly_review": {
        "中文": "生成周复习集",
        "English": "Generate Weekly Review Set",
        "Deutsch": "Wöchentliches Wiederholungsset generieren"
    },
    "button_generate_weekly": {
        "中文": "生成本周复习集",
        "English": "Generate Weekly Review Set",
        "Deutsch": "Wöchentliches Wiederholungsset generieren"
    },
    "subtitle_system_info": {
        "中文": "ℹ️ 系统信息",
        "English": "ℹ️ System Information",
        "Deutsch": "ℹ️ Systeminformationen"
    },
    "label_db_count": {
        "中文": "数据库条目数:",
        "English": "Database Items Count:",
        "Deutsch": "Anzahl der Datenbankeinträge:"
    },
    "label_nlp_status": {
        "中文": "NLP 解析器状态:",
        "English": "NLP Parser Status:",
        "Deutsch": "NLP-Parser-Status:"
    },
    "status_initialized": {
        "中文": "已初始化",
        "English": "Initialized",
        "Deutsch": "Initialisiert"
    },
    "status_not_initialized": {
        "中文": "未初始化",
        "English": "Not Initialized",
        "Deutsch": "Nicht initialisiert"
    },
    
    # 错误和信息消息
    "nlp_init_failed": {
        "中文": "NLP 解析器初始化失败:",
        "English": "NLP parser initialization failed:",
        "Deutsch": "NLP-Parser-Initialisierung fehlgeschlagen:"
    },
    "install_german_model": {
        "中文": "请先安装德语模型: python -m spacy download de_core_news_sm",
        "English": "Please install German model first: python -m spacy download de_core_news_sm",
        "Deutsch": "Bitte installieren Sie zuerst das deutsche Modell: python -m spacy download de_core_news_sm"
    },
    "embedding_init_failed": {
        "中文": "Embedding 管理器初始化失败:",
        "English": "Embedding manager initialization failed:",
        "Deutsch": "Embedding-Manager-Initialisierung fehlgeschlagen:"
    },
    "install_numpy": {
        "中文": "💡 请运行以下命令安装依赖: `pip install numpy>=1.21.0`",
        "English": "💡 Please run the following command to install dependencies: `pip install numpy>=1.21.0`",
        "Deutsch": "💡 Bitte führen Sie folgenden Befehl aus, um Abhängigkeiten zu installieren: `pip install numpy>=1.21.0`"
    },
    "related_items_unavailable": {
        "中文": "相关条目功能可能不可用",
        "English": "Related items feature may be unavailable",
        "Deutsch": "Verwandte Einträge-Funktion möglicherweise nicht verfügbar"
    }
}

def get_text(key: str, language: str) -> str:
    """
    获取多语言文本
    
    Args:
        key: 文本键
        language: 语言（中文/English/Deutsch）
    
    Returns:
        对应的文本，如果不存在则返回 key
    """
    if key in TEXTS and language in TEXTS[key]:
        return TEXTS[key][language]
    # 如果找不到，返回中文作为默认值
    if key in TEXTS and "中文" in TEXTS[key]:
        return TEXTS[key]["中文"]
    return key

