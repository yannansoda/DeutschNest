"""
工具函数
"""
import random
from typing import List, Dict
import json
import genanki

def cloze_deletion(sentence: str, lemma_list: List[str]) -> str:
    """创建遮词填空"""
    if not lemma_list:
        return sentence
    
    # 选择要遮住的词（优先选择较长的词）
    words = sentence.split()
    if not words:
        return sentence
    
    # 尝试找到 lemma 对应的词
    candidate_words = []
    for word in words:
        word_clean = word.strip('.,!?;:()[]{}"\'')
        if word_clean.lower() in [lemma.lower() for lemma in lemma_list]:
            candidate_words.append((word, len(word_clean)))
    
    if candidate_words:
        # 选择最长的词
        word_to_replace = max(candidate_words, key=lambda x: x[1])[0]
    else:
        # 如果没有匹配，随机选择一个较长的词
        word_to_replace = max(words, key=lambda x: len(x.strip('.,!?;:()[]{}"\'')))
    
    return sentence.replace(word_to_replace, "___", 1)

def create_anki_deck(db_items: List[Dict], deck_name: str = "German Learning") -> bytes:
    """创建 Anki 卡组"""
    my_deck = genanki.Deck(
        random.randrange(1 << 30, 1 << 31),
        deck_name
    )
    
    # 定义模型
    my_model = genanki.Model(
        random.randrange(1 << 30, 1 << 31),
        'German Learning Model',
        fields=[
            {'name': 'German'},
            {'name': 'Translation'},
            {'name': 'Type'},
            {'name': 'Tags'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{German}}<br><small>{{Type}}</small>',
                'afmt': '{{FrontSide}}<hr id="answer">{{Translation}}<br><small>{{Tags}}</small>',
            },
        ],
    )
    
    for item in db_items:
        tags_str = ', '.join(item.get('tags', []))
        note = genanki.Note(
            model=my_model,
            fields=[
                item.get('content', ''),
                item.get('translation', ''),
                item.get('type', ''),
                tags_str
            ]
        )
        my_deck.add_note(note)
    
    # 生成 .apkg 文件的字节数据
    package = genanki.Package(my_deck)
    # 注意：genanki 的 Package.write_to_file 只能写入文件，我们需要使用临时文件
    import tempfile
    import os
    with tempfile.NamedTemporaryFile(delete=False, suffix='.apkg') as tmp:
        package.write_to_file(tmp.name)
        with open(tmp.name, 'rb') as f:
            data = f.read()
        os.unlink(tmp.name)
        return data

def batch_import_from_text(text: str, type_filter: str = "单词") -> List[Dict]:
    """从文本批量导入（每行一个条目）"""
    lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
    items = []
    for line in lines:
        # 简单格式：德语文本 | 英文翻译
        if '|' in line:
            parts = line.split('|')
            if len(parts) >= 2:
                items.append({
                    'content': parts[0].strip(),
                    'translation': parts[1].strip(),
                    'type': type_filter
                })
            else:
                items.append({
                    'content': line,
                    'translation': '',
                    'type': type_filter
                })
        else:
            items.append({
                'content': line,
                'translation': '',
                'type': type_filter
            })
    return items

