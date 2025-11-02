"""
数据库管理模块
"""
import sqlite3
import json
import datetime
from typing import List, Dict, Optional, Tuple

class Database:
    def __init__(self, db_path: str = "german_learning.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.c = self.conn.cursor()
        self.init_db()
    
    def init_db(self):
        """初始化数据库表"""
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,
                content TEXT,
                translation TEXT,
                lemma TEXT,
                tags TEXT,
                examples TEXT,
                created_at TEXT,
                last_reviewed TEXT,
                review_count INTEGER DEFAULT 0
            )
        """)
        self.conn.commit()
        
        # 检查并添加 embedding 字段（向后兼容）
        try:
            self.c.execute("ALTER TABLE items ADD COLUMN embedding BLOB")
            self.conn.commit()
        except sqlite3.OperationalError:
            # 字段已存在，忽略错误
            pass
    
    def add_item(self, type_: str, content: str, translation: str, 
                 lemma: List[str], tags: List[str], examples: List[str] = None,
                 embedding: bytes = None):
        """添加新条目"""
        if examples is None:
            examples = []
        
        self.c.execute("""
            INSERT INTO items (type, content, translation, lemma, tags, examples, 
                             created_at, last_reviewed, review_count, embedding)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            type_,
            content,
            translation,
            json.dumps(lemma),
            json.dumps(tags),
            json.dumps(examples),
            datetime.datetime.now().isoformat(),
            None,
            0,
            embedding
        ))
        self.conn.commit()
        return self.c.lastrowid
    
    def get_item(self, item_id: int) -> Optional[Dict]:
        """获取单个条目"""
        self.c.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        row = self.c.fetchone()
        if not row:
            return None
        
        # 处理可能不存在的 embedding 字段（向后兼容）
        embedding = row[10] if len(row) > 10 else None
        
        return {
            'id': row[0],
            'type': row[1],
            'content': row[2],
            'translation': row[3],
            'lemma': json.loads(row[4]) if row[4] else [],
            'tags': json.loads(row[5]) if row[5] else [],
            'examples': json.loads(row[6]) if row[6] else [],
            'created_at': row[7],
            'last_reviewed': row[8],
            'review_count': row[9],
            'embedding': embedding
        }
    
    def search_items(self, keyword: str = "", type_filter: str = None, 
                    tag_filter: str = None) -> List[Dict]:
        """搜索条目"""
        query = "SELECT * FROM items WHERE 1=1"
        params = []
        
        if keyword:
            query += " AND (content LIKE ? OR translation LIKE ?)"
            params.extend([f'%{keyword}%', f'%{keyword}%'])
        
        if type_filter:
            query += " AND type = ?"
            params.append(type_filter)
        
        if tag_filter:
            query += " AND tags LIKE ?"
            params.append(f'%{tag_filter}%')
        
        query += " ORDER BY created_at DESC"
        
        self.c.execute(query, params)
        rows = self.c.fetchall()
        
        result = []
        for row in rows:
            # 处理可能不存在的 embedding 字段（向后兼容）
            embedding = row[10] if len(row) > 10 else None
            result.append({
                'id': row[0],
                'type': row[1],
                'content': row[2],
                'translation': row[3],
                'lemma': json.loads(row[4]) if row[4] else [],
                'tags': json.loads(row[5]) if row[5] else [],
                'examples': json.loads(row[6]) if row[6] else [],
                'created_at': row[7],
                'last_reviewed': row[8],
                'review_count': row[9],
                'embedding': embedding
            })
        return result
    
    def update_item(self, item_id: int, **kwargs):
        """更新条目"""
        allowed_fields = ['type', 'content', 'translation', 'lemma', 'tags', 'examples', 'embedding']
        updates = []
        values = []
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                if field in ['lemma', 'tags', 'examples']:
                    value = json.dumps(value) if value else json.dumps([])
                updates.append(f"{field} = ?")
                values.append(value)
        
        if not updates:
            return
        
        values.append(item_id)
        query = f"UPDATE items SET {', '.join(updates)} WHERE id = ?"
        self.c.execute(query, values)
        self.conn.commit()
    
    def delete_item(self, item_id: int):
        """删除条目"""
        self.c.execute("DELETE FROM items WHERE id = ?", (item_id,))
        self.conn.commit()
    
    def update_review(self, item_id: int):
        """更新复习记录"""
        self.c.execute("""
            UPDATE items 
            SET last_reviewed = ?, review_count = review_count + 1 
            WHERE id = ?
        """, (datetime.datetime.now().isoformat(), item_id))
        self.conn.commit()
    
    def get_random_items(self, limit: int = 1, tag_filter: str = None) -> List[Dict]:
        """随机获取条目用于复习"""
        if tag_filter:
            query = "SELECT * FROM items WHERE tags LIKE ? ORDER BY RANDOM() LIMIT ?"
            self.c.execute(query, (f'%{tag_filter}%', limit))
        else:
            query = "SELECT * FROM items ORDER BY RANDOM() LIMIT ?"
            self.c.execute(query, (limit,))
        
        rows = self.c.fetchall()
        result = []
        for row in rows:
            # 处理可能不存在的 embedding 字段（向后兼容）
            embedding = row[10] if len(row) > 10 else None
            result.append({
                'id': row[0],
                'type': row[1],
                'content': row[2],
                'translation': row[3],
                'lemma': json.loads(row[4]) if row[4] else [],
                'tags': json.loads(row[5]) if row[5] else [],
                'examples': json.loads(row[6]) if row[6] else [],
                'created_at': row[7],
                'last_reviewed': row[8],
                'review_count': row[9],
                'embedding': embedding
            })
        return result
    
    def get_all_items(self) -> List[Dict]:
        """获取所有条目"""
        self.c.execute("SELECT * FROM items ORDER BY created_at DESC")
        rows = self.c.fetchall()
        
        result = []
        for row in rows:
            # 处理可能不存在的 embedding 字段（向后兼容）
            embedding = row[10] if len(row) > 10 else None
            result.append({
                'id': row[0],
                'type': row[1],
                'content': row[2],
                'translation': row[3],
                'lemma': json.loads(row[4]) if row[4] else [],
                'tags': json.loads(row[5]) if row[5] else [],
                'examples': json.loads(row[6]) if row[6] else [],
                'created_at': row[7],
                'last_reviewed': row[8],
                'review_count': row[9],
                'embedding': embedding
            })
        return result
    
    def export_to_csv(self) -> str:
        """导出为 CSV 格式"""
        import pandas as pd
        items = self.get_all_items()
        df = pd.DataFrame(items)
        return df.to_csv(index=False)
    
    def close(self):
        """关闭数据库连接"""
        self.conn.close()

