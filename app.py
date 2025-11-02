"""
德语学习工具 - Streamlit 主应用
"""
import streamlit as st
import datetime
from database import Database
from database_supabase import SupabaseDB
from nlp_parser import NLPParser
# from googletrans import Translator
from deep_translator import GoogleTranslator

from utils import cloze_deletion, create_anki_deck, batch_import_from_text
from embedding_utils import EmbeddingManager, get_related_items
from i18n import get_text, TEXTS
# from vocab_sync import download_vocab, load_vocab, save_vocab

# 启动 app 时下载最新 JSON
# download_vocab()
# vocab_list = load_vocab()
# st.session_state.vocab_list = vocab_list  # 可用于后续添加条目或显示


# 页面配置
st.set_page_config(
    page_title="DeutschNest",
    page_icon="🇩🇪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化 session state
if 'db' not in st.session_state:
    # st.session_state.db = Database()
    st.session_state.db = SupabaseDB()
if 'parser' not in st.session_state:
    try:
        st.session_state.parser = NLPParser()
    except Exception as e:
        st.session_state.parser = None
        # 错误信息会在语言选择后显示
        st.session_state._nlp_init_error = e
if 'embedding_manager' not in st.session_state:
    try:
        # 确保 numpy 可用
        import numpy as np
        st.session_state.embedding_manager = EmbeddingManager()
    except ImportError as e:
        st.session_state.embedding_manager = None
        # 错误消息会在语言选择后显示
        st.session_state._embedding_init_error = e
    except Exception as e:
        st.session_state.embedding_manager = None
        st.session_state._embedding_init_warning = e

# 语言选择（在侧边栏顶部）
if 'language' not in st.session_state:
    st.session_state.language = "中文"

language = st.sidebar.selectbox(
    get_text("language_select", st.session_state.language),
    ["中文", "English", "Deutsch"],
    index=["中文", "English", "Deutsch"].index(st.session_state.language)
)
st.session_state.language = language

# 侧边栏导航
st.sidebar.title(get_text("sidebar_title", language))

# 使用内部标识符来追踪当前页面，而不是多语言文本
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"

page_options = [
    get_text("nav_home", language),
    get_text("nav_add", language),
    get_text("nav_search", language),
    get_text("nav_review", language),
    get_text("nav_settings", language)
]

page_mapping = {
    get_text("nav_home", language): "home",
    get_text("nav_add", language): "add",
    get_text("nav_search", language): "search",
    get_text("nav_review", language): "review",
    get_text("nav_settings", language): "settings"
}

# 获取当前页面的索引
current_index = list(page_mapping.values()).index(st.session_state.current_page) if st.session_state.current_page in page_mapping.values() else 0

selected_page_text = st.sidebar.radio(
    get_text("navigation", language),
    page_options,
    index=current_index
)

# 更新当前页面
st.session_state.current_page = page_mapping[selected_page_text]
page = st.session_state.current_page

# 显示初始化错误（如果有）
if hasattr(st.session_state, '_nlp_init_error'):
    st.error(f"{get_text('nlp_init_failed', language)} {st.session_state._nlp_init_error}")
    st.info(get_text("install_german_model", language))
    delattr(st.session_state, '_nlp_init_error')

if hasattr(st.session_state, '_embedding_init_error'):
    st.error(f"{get_text('embedding_init_failed', language)} {st.session_state._embedding_init_error}")
    st.info(get_text("install_numpy", language))
    st.info(get_text("related_items_unavailable", language))
    delattr(st.session_state, '_embedding_init_error')
elif hasattr(st.session_state, '_embedding_init_warning'):
    st.warning(f"{get_text('embedding_init_failed', language)} {st.session_state._embedding_init_warning}")
    st.info(get_text("related_items_unavailable", language))
    delattr(st.session_state, '_embedding_init_warning')

# ==================== 主页 ====================
if page == "home":
    st.title(get_text("title_home", language))
    st.markdown("---")
    
    # 统计信息
    col1, col2, col3, col4 = st.columns(4)
    
    all_items = st.session_state.db.get_all_items()
    
    with col1:
        st.metric(get_text("metric_total", language), len(all_items))
    
    with col2:
        # 数据库中使用中文存储类型
        word_count = len([i for i in all_items if i['type'] == "Word"])
        st.metric(get_text("metric_word", language), word_count)
    
    with col3:
        phrase_count = len([i for i in all_items if i['type'] == "Phrase"])
        st.metric(get_text("metric_phrase", language), phrase_count)
    
    with col4:
        sentence_count = len([i for i in all_items if i['type'] == "Sentence"])
        st.metric(get_text("metric_sentence", language), sentence_count)
    
    st.markdown("---")
    
    # 最近添加
    st.subheader(get_text("recent_added", language))
    if all_items:
        recent_items = all_items[:10]
        for item in recent_items:
            with st.expander(f"{item['type']} | {item['content'][:50]}..."):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**{get_text('label_german', language)}** {item['content']}")
                    if item['tags']:
                        st.write(f"**{get_text('label_tags', language)}** {', '.join(item['tags'])}")
                with col2:
                    st.write(f"**{get_text('label_translation', language)}** {item['translation']}")
                    if item['lemma']:
                        st.write(f"**{get_text('label_lemma', language)}** {', '.join(item['lemma'][:5])}")
    else:
        st.info(get_text("no_items_msg", language))

# ==================== 添加页面 ====================
elif page == "add":
    st.title(get_text("title_add", language))
    st.markdown("---")
    
    # 单条添加
    st.subheader(get_text("subtitle_single_add", language))
    
    col1, col2 = st.columns(2)
    
    with col1:
        content_de = st.text_area(
            get_text("label_german_content", language), 
            height=100, 
            placeholder=get_text("placeholder_german_content", language)
        )
        # 类型选择需要映射到中文（数据库中使用中文存储）
        type_options = {
            get_text("type_word", language): "Word",
            get_text("type_phrase", language): "Phrase",
            get_text("type_sentence", language): "Sentence"
        }
        type_display = st.selectbox(get_text("label_type", language), list(type_options.keys()))
        item_type = type_options[type_display]
    
    with col2:
        translation_en = st.text_area(
            get_text("label_translation_optional", language), 
            height=100, 
            placeholder=get_text("placeholder_translation", language)
        )
    
    if st.button(get_text("button_save", language), type="primary"):
        if content_de.strip():
            # 自动翻译（如果用户没输入）
            if not translation_en.strip():
                # translator = Translator()
                translator = GoogleTranslator(source='de', target='en')
                try:
                    # translation_en = translator.translate(content_de, src='de', dest='en').text
                    translation_en = translator.translate(content_de)
                    st.info(f"{get_text('auto_translated', language)} {translation_en}")
                except Exception as e:
                    st.warning(f"{get_text('auto_translate_failed', language)} {e}")
                    translation_en = ""

            if st.session_state.parser:
                lemma_list, pos_list, tags = st.session_state.parser.parse_text(content_de)
                
                # 生成 embedding
                embedding_blob = None
                if st.session_state.embedding_manager:
                    try:
                        # 确保 numpy 可用
                        import numpy as np
                        embedding = st.session_state.embedding_manager.generate_embedding(content_de.strip())
                        embedding_blob = st.session_state.embedding_manager.save_embedding(embedding)
                    except ImportError as e:
                        st.error(get_text("embedding_failed", language))
                    except Exception as e:
                        st.warning(f"{get_text('embedding_warning', language)} {e}")
                        st.info(get_text("embedding_info", language))
                
                st.session_state.db.add_item(
                    type_=item_type,
                    content=content_de.strip(),
                    translation=translation_en.strip(),
                    lemma=lemma_list,
                    tags=tags,
                    examples=[],
                    embedding=embedding_blob
                )

                # # 同步到 JSON + 云端
                # st.session_state.vocab_list.append({
                #     "type": item_type,
                #     "content": content_de.strip(),
                #     "translation": translation_en.strip(),
                #     "lemma": lemma_list,
                #     "tags": tags,
                #     "examples": []
                # })
                # save_vocab(st.session_state.vocab_list)
                
                if 'vocab_list' not in st.session_state:
                    st.session_state.vocab_list = []
                st.session_state.vocab_list.append({
                    "type": item_type,
                    "content": content_de.strip(),
                    "translation": translation_en.strip(),
                    "lemma": lemma_list,
                    "tags": tags,
                    "examples": []
                    })

                st.success(get_text("success_saved", language))
                
                # 显示解析结果
                with st.expander(get_text("view_parse_result", language)):
                    st.write(f"**{get_text('label_lemma', language)}** {', '.join(lemma_list[:10])}")
                    st.write(f"**{get_text('label_pos', language)}** {', '.join(pos_list[:10])}")
                    st.write(f"**{get_text('label_tags', language)}** {', '.join(tags)}")
                    if embedding_blob:
                        st.write(get_text("embedding_generated", language))
            else:
                st.error(get_text("nlp_not_initialized", language))
        else:
            st.warning(get_text("warning_empty_content", language))
    
    st.markdown("---")
    
    # 批量导入
    st.subheader(get_text("subtitle_batch_import", language))
    
    # 类型映射
    type_options_map = {
        get_text("type_word", language): "Word",
        get_text("type_phrase", language): "Phrase",
        get_text("type_sentence", language): "Sentence"
    }
    import_type_display = st.selectbox(get_text("label_import_type", language), list(type_options_map.keys()), key="import_type")
    import_type = type_options_map[import_type_display]
    
    upload_method_options = [get_text("method_text_input", language), get_text("method_file_upload", language)]
    upload_method = st.radio(get_text("label_import_method", language), upload_method_options)
    
    if upload_method == get_text("method_text_input", language):
        batch_text = st.text_area(
            get_text("label_batch_text", language),
            height=200,
            placeholder="Hallo | Hello\nWie geht es dir? | How are you?"
        )
        
        if st.button(get_text("button_batch_import", language)):
            if batch_text.strip():
                items = batch_import_from_text(batch_text, import_type)
                
                progress_bar = st.progress(0)
                success_count = 0
                
                for idx, item in enumerate(items):
                    if st.session_state.parser:
                        lemma_list, pos_list, tags = st.session_state.parser.parse_text(item['content'])
                    else:
                        lemma_list, pos_list, tags = [], [], []
                    
                    # 生成 embedding
                    embedding_blob = None
                    if st.session_state.embedding_manager:
                        try:
                            # 确保 numpy 可用
                            import numpy as np
                            embedding = st.session_state.embedding_manager.generate_embedding(item['content'].strip())
                            embedding_blob = st.session_state.embedding_manager.save_embedding(embedding)
                        except ImportError:
                            pass  # 批量导入时静默失败（numpy 未安装）
                        except Exception:
                            pass  # 批量导入时静默失败
                    
                    st.session_state.db.add_item(
                        type_=item['type'],
                        content=item['content'].strip(),
                        translation=item['translation'].strip(),
                        lemma=lemma_list,
                        tags=tags,
                        examples=[],
                        embedding=embedding_blob
                    )
                    success_count += 1
                    progress_bar.progress((idx + 1) / len(items))
                
                st.success(get_text("success_batch_import", language).format(count=success_count))
            else:
                st.warning(get_text("warning_empty_text", language))
    
    else:  # 文件上传
        uploaded_file = st.file_uploader(get_text("label_select_file", language), type=['txt', 'csv'])
        
        if uploaded_file:
            content = uploaded_file.read().decode('utf-8')
            st.text_area(get_text("label_file_preview", language), content, height=200)
            
            if st.button(get_text("button_import_file", language)):
                items = batch_import_from_text(content, import_type)
                
                progress_bar = st.progress(0)
                success_count = 0
                
                for idx, item in enumerate(items):
                    if st.session_state.parser:
                        lemma_list, pos_list, tags = st.session_state.parser.parse_text(item['content'])
                    else:
                        lemma_list, pos_list, tags = [], [], []
                    
                    # 生成 embedding
                    embedding_blob = None
                    if st.session_state.embedding_manager:
                        try:
                            # 确保 numpy 可用
                            import numpy as np
                            embedding = st.session_state.embedding_manager.generate_embedding(item['content'].strip())
                            embedding_blob = st.session_state.embedding_manager.save_embedding(embedding)
                        except ImportError:
                            pass  # 批量导入时静默失败（numpy 未安装）
                        except Exception:
                            pass  # 批量导入时静默失败
                    
                    st.session_state.db.add_item(
                        type_=item['type'],
                        content=item['content'].strip(),
                        translation=item['translation'].strip(),
                        lemma=lemma_list,
                        tags=tags,
                        examples=[],
                        embedding=embedding_blob
                    )
                    success_count += 1
                    progress_bar.progress((idx + 1) / len(items))
                
                st.success(get_text("success_batch_import", language).format(count=success_count))

# ==================== 搜索/管理页面 ====================
elif page == "search":
    st.title(get_text("title_search", language))
    st.markdown("---")
    
    # 搜索栏
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_keyword = st.text_input(get_text("label_search_keyword", language), placeholder=get_text("placeholder_search", language))
    
    with col2:
        # 类型筛选需要映射回中文（数据库使用中文存储）
        type_options_map = {
            get_text("filter_all", language): None,
            get_text("type_word", language): "Word",
            get_text("type_phrase", language): "Phrase",
            get_text("type_sentence", language): "Sentence"
        }
        type_options_display = [get_text("filter_all", language)] + [get_text("type_word", language), get_text("type_phrase", language), get_text("type_sentence", language)]
        type_filter_display = st.selectbox(get_text("label_type_filter", language), type_options_display)
        type_filter_val = type_options_map[type_filter_display]
    
    with col3:
        all_items = st.session_state.db.get_all_items()
        all_tags = set()
        for item in all_items:
            all_tags.update(item.get('tags', []))
        tag_filter = st.selectbox(get_text("label_tag_filter", language), [get_text("filter_all", language)] + sorted(list(all_tags)))
    
    # 执行搜索（type_filter_val 已在上面设置）
    tag_filter_val = None if tag_filter == get_text("filter_all", language) else tag_filter
    
    results = st.session_state.db.search_items(
        keyword=search_keyword,
        type_filter=type_filter_val,
        tag_filter=tag_filter_val
    )
    
    st.write(get_text("results_found", language).format(count=len(results)))
    st.markdown("---")
    
    # 显示结果
    for item in results:
        with st.expander(f"ID: {item['id']} | {item['type']} | {item['content'][:60]}..."):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**{get_text('label_german', language)}** {item['content']}")
                st.write(f"**{get_text('label_translation', language)}** {item['translation']}")
                if item['lemma']:
                    st.write(f"**{get_text('label_lemma', language)}** {', '.join(item['lemma'][:10])}")
                if item['tags']:
                    st.write(f"**{get_text('label_tags', language)}** {', '.join(item['tags'])}")
                st.write(f"**{get_text('label_created_at', language)}** {item['created_at']}")
                st.write(f"**{get_text('label_review_count', language)}** {item['review_count']}")
                if item['last_reviewed']:
                    st.write(f"**{get_text('label_last_reviewed', language)}** {item['last_reviewed']}")
            
            with col2:
                if st.button(get_text("button_delete", language), key=f"delete_{item['id']}"):
                    st.session_state.db.delete_item(item['id'])
                    st.rerun()
                
                if st.button(get_text("button_edit", language), key=f"edit_{item['id']}"):
                    st.session_state[f"editing_{item['id']}"] = True
                
                if st.session_state.get(f"editing_{item['id']}", False):
                    new_content = st.text_input(get_text("label_new_content", language), value=item['content'], key=f"content_{item['id']}")
                    new_translation = st.text_input(get_text("label_new_translation", language), value=item['translation'], key=f"trans_{item['id']}")
                    
                    if st.button(get_text("button_save_edit", language), key=f"save_{item['id']}"):
                        st.session_state.db.update_item(
                            item['id'],
                            content=new_content,
                            translation=new_translation
                        )
                        st.session_state[f"editing_{item['id']}"] = False
                        st.rerun()
            
            # 显示相关条目
            st.markdown("---")
            st.subheader(get_text("related_items", language))
            if st.session_state.embedding_manager:
                try:
                    all_items = st.session_state.db.get_all_items()
                    related_items = get_related_items(
                        item, 
                        all_items, 
                        top_k=5,
                        embedding_manager=st.session_state.embedding_manager
                    )
                    
                    if related_items:
                        for related_item, similarity in related_items:
                            similarity_pct = f"{similarity * 100:.1f}%"
                            with st.expander(f"🔗 {related_item['content'][:50]}... ({get_text('similarity', language)} {similarity_pct})"):
                                st.write(f"**{get_text('label_german', language)}** {related_item['content']}")
                                st.write(f"**{get_text('label_translation', language)}** {related_item['translation']}")
                                if related_item['tags']:
                                    st.write(f"**{get_text('label_tags', language)}** {', '.join(related_item['tags'])}")
                                st.write(f"**{get_text('label_type', language)}** {related_item['type']}")
                    else:
                        st.info(get_text("no_related_items", language))
                except Exception as e:
                    st.warning(f"{get_text('get_related_failed', language)} {e}")
            else:
                st.info(get_text("embedding_not_initialized", language))

# ==================== 复习页面 ====================
elif page == "review":
    st.title(get_text("title_review", language))
    st.markdown("---")
    
    # 复习设置
    col1, col2 = st.columns(2)
    
    with col1:
        review_mode_options = [get_text("mode_cloze", language), get_text("mode_reverse", language), get_text("mode_dictation", language)]
        review_mode_display = st.radio(
            get_text("label_review_mode", language),
            review_mode_options,
            horizontal=True
        )
        # 映射到内部标识符
        review_mode_map = {
            get_text("mode_cloze", language): "cloze",
            get_text("mode_reverse", language): "reverse",
            get_text("mode_dictation", language): "dictation"
        }
        review_mode = review_mode_map[review_mode_display]
    
    with col2:
        all_items = st.session_state.db.get_all_items()
        all_tags = set()
        for item in all_items:
            all_tags.update(item.get('tags', []))
        review_tag = st.selectbox(get_text("label_tag_filter_optional", language), [get_text("filter_all", language)] + sorted(list(all_tags)))
    
    st.markdown("---")
    
    # 开始复习
    if 'current_review_item' not in st.session_state or st.button(get_text("button_random", language)):
        tag_filter = None if review_tag == get_text("filter_all", language) else review_tag
        items = st.session_state.db.get_random_items(limit=1, tag_filter=tag_filter)
        
        if items:
            st.session_state.current_review_item = items[0]
            st.session_state.review_mode = review_mode
            st.session_state.show_answer = False
        else:
            st.warning(get_text("no_items_found", language))
            st.session_state.current_review_item = None
    
    if 'current_review_item' in st.session_state and st.session_state.current_review_item:
        item = st.session_state.current_review_item
        
        st.subheader(f"📝 {item['type']} 复习")
        
        if review_mode == "cloze":
            if st.session_state.parser:
                cloze_sentence = cloze_deletion(item['content'], item['lemma'])
            else:
                # 简单版本：随机遮住一个词
                words = item['content'].split()
                if words:
                    import random
                    idx = random.randint(0, len(words) - 1)
                    words[idx] = "___"
                    cloze_sentence = ' '.join(words)
                else:
                    cloze_sentence = item['content']
            
            st.write(f"**{get_text('review_cloze', language)}** {cloze_sentence}")
            user_answer = st.text_input(get_text("label_your_answer", language))
            
            if st.button(get_text("button_show_answer", language)):
                st.session_state.show_answer = True
            
            if st.session_state.show_answer:
                st.success(f"**{get_text('correct_answer', language)}** {item['content']}")
                st.info(f"**{get_text('label_translation', language)}** {item['translation']}")
                
                if user_answer.strip():
                    # 简单检查（可以改进）
                    if user_answer.lower().strip() in item['content'].lower():
                        st.balloons()
                
                if st.button(get_text("button_mark_reviewed", language)):
                    st.session_state.db.update_review(item['id'])
                    st.success(get_text("review_recorded", language))
                    del st.session_state.current_review_item
                
                # 显示相关条目
                st.markdown("---")
                st.subheader(get_text("related_items", language))
                if st.session_state.embedding_manager:
                    try:
                        all_items = st.session_state.db.get_all_items()
                        related_items = get_related_items(
                            item, 
                            all_items, 
                            top_k=5,
                            embedding_manager=st.session_state.embedding_manager
                        )
                        
                        if related_items:
                            for related_item, similarity in related_items:
                                similarity_pct = f"{similarity * 100:.1f}%"
                                with st.expander(f"🔗 {related_item['content'][:50]}... ({get_text('similarity', language)} {similarity_pct})"):
                                    st.write(f"**{get_text('label_german', language)}** {related_item['content']}")
                                    st.write(f"**{get_text('label_translation', language)}** {related_item['translation']}")
                                    if related_item['tags']:
                                        st.write(f"**{get_text('label_tags', language)}** {', '.join(related_item['tags'])}")
                                    st.write(f"**{get_text('label_type', language)}** {related_item['type']}")
                        else:
                            st.info(get_text("no_related_items", language))
                    except Exception as e:
                        st.warning(f"{get_text('get_related_failed', language)} {e}")
        
        elif review_mode == "reverse":
            st.write(f"**{get_text('review_reverse_label', language)}** {item['translation']}")
            user_answer = st.text_input(get_text("review_reverse_input", language))
            
            if st.button(get_text("button_show_answer", language)):
                st.session_state.show_answer = True
            
            if st.session_state.show_answer:
                st.success(f"**{get_text('correct_answer', language)}** {item['content']}")
                
                if user_answer.strip():
                    # 简单检查
                    similarity = len(set(user_answer.lower().split()) & set(item['content'].lower().split()))
                    total_words = len(item['content'].split())
                    if total_words > 0:
                        score = similarity / total_words
                        st.write(f"**{get_text('match_score', language)}** {score:.1%}")
                
                if st.button(get_text("button_mark_reviewed", language)):
                    st.session_state.db.update_review(item['id'])
                    st.success(get_text("review_recorded", language))
                    del st.session_state.current_review_item
                
                # 显示相关条目
                st.markdown("---")
                st.subheader(get_text("related_items", language))
                if st.session_state.embedding_manager:
                    try:
                        all_items = st.session_state.db.get_all_items()
                        related_items = get_related_items(
                            item, 
                            all_items, 
                            top_k=5,
                            embedding_manager=st.session_state.embedding_manager
                        )
                        
                        if related_items:
                            for related_item, similarity in related_items:
                                similarity_pct = f"{similarity * 100:.1f}%"
                                with st.expander(f"🔗 {related_item['content'][:50]}... ({get_text('similarity', language)} {similarity_pct})"):
                                    st.write(f"**{get_text('label_german', language)}** {related_item['content']}")
                                    st.write(f"**{get_text('label_translation', language)}** {related_item['translation']}")
                                    if related_item['tags']:
                                        st.write(f"**{get_text('label_tags', language)}** {', '.join(related_item['tags'])}")
                                    st.write(f"**{get_text('label_type', language)}** {related_item['type']}")
                        else:
                            st.info(get_text("no_related_items", language))
                    except Exception as e:
                        st.warning(f"{get_text('get_related_failed', language)} {e}")
        
        elif review_mode == "dictation":
            st.write(f"**{get_text('review_dictation_label', language)}**")
            
            if st.button(get_text("button_play_audio", language)):
                try:
                    import pyttsx3
                    engine = pyttsx3.init()
                    engine.setProperty('rate', 150)
                    engine.setProperty('voice', 'german')
                    engine.say(item['content'])
                    engine.runAndWait()
                    st.success(get_text("playback_complete", language))
                except Exception as e:
                    st.warning(f"{get_text('tts_unavailable', language)} {e}")
                    st.info(get_text("tts_online_info", language))
            
            user_answer = st.text_input(get_text("review_dictation_input", language))
            
            if st.button(get_text("button_show_answer", language)):
                st.session_state.show_answer = True
            
            if st.session_state.show_answer:
                st.success(f"**{get_text('correct_answer', language)}** {item['content']}")
                st.info(f"**{get_text('label_translation', language)}** {item['translation']}")
                
                if user_answer.strip():
                    if user_answer.strip().lower() == item['content'].lower():
                        st.balloons()
                        st.success(get_text("perfect_correct", language))
                
                if st.button(get_text("button_mark_reviewed", language)):
                    st.session_state.db.update_review(item['id'])
                    st.success(get_text("review_recorded", language))
                    del st.session_state.current_review_item
                
                # 显示相关条目
                st.markdown("---")
                st.subheader(get_text("related_items", language))
                if st.session_state.embedding_manager:
                    try:
                        all_items = st.session_state.db.get_all_items()
                        related_items = get_related_items(
                            item, 
                            all_items, 
                            top_k=5,
                            embedding_manager=st.session_state.embedding_manager
                        )
                        
                        if related_items:
                            for related_item, similarity in related_items:
                                similarity_pct = f"{similarity * 100:.1f}%"
                                with st.expander(f"🔗 {related_item['content'][:50]}... ({get_text('similarity', language)} {similarity_pct})"):
                                    st.write(f"**{get_text('label_german', language)}** {related_item['content']}")
                                    st.write(f"**{get_text('label_translation', language)}** {related_item['translation']}")
                                    if related_item['tags']:
                                        st.write(f"**{get_text('label_tags', language)}** {', '.join(related_item['tags'])}")
                                    st.write(f"**{get_text('label_type', language)}** {related_item['type']}")
                        else:
                            st.info(get_text("no_related_items", language))
                    except Exception as e:
                        st.warning(f"{get_text('get_related_failed', language)} {e}")

# ==================== 设置/导出页面 ====================
elif page == "settings":
    st.title(get_text("title_settings", language))
    st.markdown("---")
    
    st.subheader(get_text("subtitle_export", language))
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(get_text("button_export_csv", language), type="primary"):
            csv_data = st.session_state.db.export_to_csv()
            st.download_button(
                label=get_text("button_download_csv", language),
                data=csv_data,
                file_name=f"german_learning_{datetime.datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button(get_text("button_export_anki", language), type="primary"):
            all_items = st.session_state.db.get_all_items()
            if all_items:
                try:
                    anki_data = create_anki_deck(all_items, "German Learning")
                    st.download_button(
                        label=get_text("button_download_anki", language),
                        data=anki_data,
                        file_name=f"german_learning_{datetime.datetime.now().strftime('%Y%m%d')}.apkg",
                        mime="application/apkg"
                    )
                    st.success(get_text("anki_success", language))
                except Exception as e:
                    st.error(f"{get_text('anki_error', language)} {e}")
            else:
                st.warning(get_text("no_data_export", language))
    
    st.markdown("---")
    
    st.subheader(get_text("subtitle_ai", language))
    
    st.info(get_text("ai_info", language))
    
    with st.expander(get_text("expand_generate_example", language)):
        word_input = st.text_input(get_text("label_input_word", language), placeholder=get_text("placeholder_example_word", language))
        if st.button(get_text("button_generate_example", language)):
            st.info(get_text("ai_api_required", language))
    
    with st.expander(get_text("expand_weekly_review", language)):
        if st.button(get_text("button_generate_weekly", language)):
            st.info(get_text("ai_api_required", language))
    
    st.markdown("---")
    
    st.subheader(get_text("subtitle_system_info", language))
    st.write(f"{get_text('label_db_count', language)} {len(st.session_state.db.get_all_items())}")
    nlp_status = get_text("status_initialized", language) if st.session_state.parser else get_text("status_not_initialized", language)
    st.write(f"{get_text('label_nlp_status', language)} {nlp_status}")

