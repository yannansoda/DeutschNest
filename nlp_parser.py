"""
NLP 解析模块 - 使用 spacy 进行德语文本分析
"""
import spacy
from typing import List, Tuple
import re

class NLPParser:
    def __init__(self):
        try:
            self.nlp = spacy.load("de_core_news_sm")
        except OSError:
            raise Exception("请先安装德语模型: python -m spacy download de_core_news_sm")
    
    def parse_text(self, text: str) -> Tuple[List[str], List[str], List[str]]:
        """
        解析文本，提取词根、词性和标签
        返回: (lemma_list, pos_list, tags)
        """
        doc = self.nlp(text)
        
        lemma_list = [token.lemma_.lower() for token in doc if not token.is_punct and not token.is_space]
        pos_list = [token.pos_ for token in doc if not token.is_punct and not token.is_space]
        
        tags = []
        text_lower = text.lower()
        
        # 检测常见短语和句型
        patterns = {
            "auch wenn + Nebensatz": r"auch\s+wenn",
            "obwohl + Nebensatz": r"obwohl",
            "trotzdem": r"trotzdem",
            "deshalb": r"deshalb",
            "weil + Nebensatz": r"weil\s",
            "damit + Nebensatz": r"damit\s",
            "wenn + Nebensatz": r"^wenn\s",
            "als + Nebensatz": r"^als\s",
            "dass + Nebensatz": r"\sdass\s",
            "um zu + Infinitiv": r"um\s+zu",
            "ohne zu + Infinitiv": r"ohne\s+zu",
            "ohne dass": r"ohne\s+dass",
            "seit/seitdem": r"seit(dem)?\s",
            "bis": r"^bis\s",
            "sodass": r"sodass",
            "während": r"während",
            "anstatt/anstatt dass": r"anstatt\s+(dass\s)?",
        }
        
        for tag, pattern in patterns.items():
            if re.search(pattern, text_lower):
                tags.append(tag)
        
        # 检测其他常见结构
        if len([w for w in text.split()]) == 1:
            tags.append("单词")
        elif "?" in text:
            tags.append("疑问句")
        elif "!" in text:
            tags.append("感叹句")
        
        return lemma_list, pos_list, tags
    
    def extract_main_lemma(self, text: str) -> List[str]:
        """提取主要词根（去重）"""
        lemma_list, _, _ = self.parse_text(text)
        return list(set(lemma_list))

