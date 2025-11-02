"""
Supabase version of the DB manager
"""
import os
import json
import datetime
from typing import List, Dict, Optional
from supabase import create_client, Client
from dotenv import load_dotenv
import base64
from typing import List, Union, Optional

load_dotenv()


class SupabaseDB:
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        assert url and key, "⚠️ Missing SUPABASE_URL or SUPABASE_KEY in .env"

        self.supabase: Client = create_client(url, key)
        self.table_name = "entries"

    # ----------------------
    # helper method
    # ----------------------
    def _normalize_row(self, row: Dict) -> Dict:
        """Convert row to same format as SQLite version"""
        return {
            'id': row.get('id'),
            'type': row.get('type'),
            'content': row.get('content'),
            'translation': row.get('translation'),
            'lemma': row.get('lemma') or [],
            'tags': row.get('tags') or [],
            'examples': row.get('examples') or [],
            'created_at': row.get('created_at'),
            'last_reviewed': row.get('last_reviewed'),
            'review_count': row.get('review_count', 0),
            'embedding': row.get('embedding'),
        }

    # ----------------------
    # CRUD
    # ----------------------
    def add_item(
        self,
        type_: str,
        content: str,
        translation: str,
        lemma: List[str],
        tags: List[str],
        examples: Optional[List[str]] = None,
        embedding: Optional[Union[bytes, str]] = None,
    ) -> int:
        """
        在 Supabase 表中插入一条记录，自动处理 JSON 序列化问题。
        """
        if examples is None:
            examples = []

        # 处理 embedding
        if embedding is not None:
            if isinstance(embedding, bytes):
                embedding_str = base64.b64encode(embedding).decode('utf-8')
            elif isinstance(embedding, str):
                embedding_str = base64.b64encode(embedding.encode('utf-8')).decode('utf-8')
            else:
                raise TypeError(f"Unsupported type for embedding: {type(embedding)}")
        else:
            embedding_str = None

        # 构建数据字典
        data = {
            "type": type_,
            "content": content,
            "translation": translation,
            "lemma": lemma or [],
            "tags": tags or [],
            "examples": examples or [],
            "created_at": datetime.datetime.now().isoformat(),
            "last_reviewed": None,
            "review_count": 0,
            "embedding": embedding_str,
        }

        # 插入到 Supabase
        result = (
            self.supabase.table(self.table_name)
            .insert(data)
            .execute()
        )

        return result.data[0]["id"]

    def get_item(self, item_id: int) -> Optional[Dict]:
        result = (
            self.supabase.table(self.table_name)
            .select("*")
            .eq("id", item_id)
            .execute()
        )
        if not result.data:
            return None

        return self._normalize_row(result.data[0])

    def delete_item(self, item_id: int):
        self.supabase.table(self.table_name).delete().eq("id", item_id).execute()

    def update_item(self, item_id: int, **kwargs):
        allowed = ['type', 'content', 'translation', 'lemma', 'tags', 'examples', 'embedding']
        update_data = {k: v for k, v in kwargs.items() if k in allowed}
        if not update_data:
            return
        self.supabase.table(self.table_name).update(update_data).eq("id", item_id).execute()

    # ----------------------
    # Review tracking
    # ----------------------
    def update_review(self, item_id: int):
        self.supabase.table(self.table_name).update({
            "last_reviewed": datetime.datetime.now().isoformat(),
            "review_count": "review_count + 1"
        }).eq("id", item_id).execute()

    # ----------------------
    # Query
    # ----------------------
    def search_items(self, keyword: str = "", type_filter: str = None, tag_filter: str = None) -> List[Dict]:
        q = self.supabase.table(self.table_name).select("*")

        if keyword:
            q = q.ilike("content", f"%{keyword}%")
            # translation search also?
            # Could do OR query later if needed

        if type_filter:
            q = q.eq("type", type_filter)

        if tag_filter:
            q = q.contains("tags", [tag_filter])

        result = q.order("created_at", desc=True).execute()

        return [self._normalize_row(row) for row in result.data]

    def get_random_items(self, limit: int = 1, tag_filter: str = None) -> List[Dict]:
        q = self.supabase.table(self.table_name).select("*").limit(limit)

        if tag_filter:
            q = q.contains("tags", [tag_filter])

        # Supabase doesn't have true RANDOM() client-side, we rely on server sorting
        result = q.order("id", desc=False).execute()

        return [self._normalize_row(row) for row in result.data]

    def get_all_items(self) -> List[Dict]:
        result = (
            self.supabase.table(self.table_name)
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )

        return [self._normalize_row(row) for row in result.data]

    # ----------------------
    # CSV Export (optional)
    # ----------------------
    def export_to_csv(self) -> str:
        raise NotImplementedError("Export not supported for cloud DB")

    def close(self):
        pass  # Nothing required for Supabase
