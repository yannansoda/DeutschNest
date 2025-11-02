"""
Embedding 工具模块 - 处理向量生成和相似度查询
"""
import pickle
from typing import List, Dict, Tuple, Optional

# 确保 numpy 可用
try:
    import numpy as np
except ImportError:
    raise ImportError("numpy 未安装，请运行: pip install numpy>=1.21.0")

class EmbeddingManager:
    def __init__(self, model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        """
        初始化 Embedding 管理器
        """
        self.model_name = model_name
        self.model = None
    
    def get_model(self):
        """延迟加载模型（仅在需要时加载）"""
        if self.model is None:
            try:
                # 确保 numpy 在导入 sentence_transformers 之前可用
                import numpy as np
                from sentence_transformers import SentenceTransformer
                # 检查 numpy 是否真的可用
                _ = np.array([1, 2, 3])  # 测试 numpy 是否工作
                self.model = SentenceTransformer(self.model_name)
            except ImportError as e:
                raise ImportError(f"请先安装依赖: {e}")
            except Exception as e:
                raise RuntimeError(f"加载模型失败: {e}")
        return self.model
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        生成文本的 embedding 向量
        """
        # 确保 numpy 可用
        try:
            import numpy as np
        except ImportError:
            raise ImportError("numpy 未安装，请运行: pip install numpy")
        
        # 延迟导入 torch，只在需要时导入
        try:
            import torch
        except ImportError:
            raise ImportError("torch 未安装，请运行: pip install torch")
        
        model = self.get_model()
        # 检查模型是否有 encode 方法
        if not hasattr(model, 'encode'):
            raise AttributeError("模型不支持 encode 方法")
        
        try:
            # 先尝试使用 convert_to_numpy=False，然后手动转换
            # 这样可以避免 numpy 版本兼容性问题
            embedding = model.encode(text, convert_to_numpy=False, show_progress_bar=False)
            
            # 如果是 torch tensor，使用 tolist() 方式转换，避免直接调用 .numpy()
            if isinstance(embedding, torch.Tensor):
                # 使用 tolist() 然后转换为 numpy，这样可以绕过 numpy 版本兼容性问题
                embedding_np = np.array(embedding.detach().cpu().tolist())
            elif isinstance(embedding, np.ndarray):
                embedding_np = embedding
            else:
                # 如果是列表或其他类型，直接转换为 numpy array
                embedding_np = np.array(embedding)
            
            # 确保是 1D 或 2D numpy array
            if len(embedding_np.shape) == 1:
                embedding_np = embedding_np.reshape(1, -1)
            
            return embedding_np.squeeze()  # 如果只有一个样本，去掉 batch 维度
        except RuntimeError as e:
            if "Numpy is not available" in str(e) or "numpy" in str(e).lower():
                # 如果遇到 numpy 不可用错误，尝试使用 tolist() 方式
                try:
                    embedding = model.encode(text, convert_to_tensor=True, show_progress_bar=False)
                    if isinstance(embedding, torch.Tensor):
                        # 使用 tolist() 方式转换，避免 .numpy() 调用
                        embedding_np = np.array(embedding.detach().cpu().tolist())
                        return embedding_np.squeeze()
                    else:
                        embedding_np = np.array(embedding)
                        return embedding_np.squeeze()
                except Exception as e2:
                    raise RuntimeError(f"生成 embedding 时出错（尝试了多种方式）: {e2}")
            raise RuntimeError(f"生成 embedding 时出错: {e}")
        except Exception as e:
            raise RuntimeError(f"生成 embedding 时出错: {e}")
    
    def save_embedding(self, embedding: np.ndarray) -> bytes:
        """
        将 embedding 转换为 BLOB 格式存储
        """
        return pickle.dumps(embedding)
    
    def load_embedding(self, embedding_blob: bytes) -> Optional[np.ndarray]:
        """
        从 BLOB 格式加载 embedding
        """
        if embedding_blob is None:
            return None
        try:
            return pickle.loads(embedding_blob)
        except Exception:
            return None


def get_related_items(current_item: Dict, all_items: List[Dict], 
                     top_k: int = 5, embedding_manager: Optional[EmbeddingManager] = None) -> List[Tuple[Dict, float]]:
    """
    获取相关条目
    
    策略：
    1. 首先通过 tags 字段匹配同一主题的条目
    2. 然后计算语义相似度，找出语义相近的条目
    
    返回: [(item, similarity_score), ...] 按相似度降序排序
    """
    if embedding_manager is None:
        embedding_manager = EmbeddingManager()
    
    # 排除当前条目
    other_items = [item for item in all_items if item['id'] != current_item['id']]
    
    # 如果当前条目没有 embedding，返回空列表
    current_embedding = None
    if current_item.get('embedding'):
        current_embedding = embedding_manager.load_embedding(current_item['embedding'])
    
    if current_embedding is None:
        # 如果当前条目没有 embedding，只按标签匹配
        current_tags = set(current_item.get('tags', []))
        if not current_tags:
            return []
        
        related = []
        for item in other_items:
            item_tags = set(item.get('tags', []))
            if current_tags & item_tags:  # 有交集
                related.append((item, 1.0))  # 标签匹配，相似度设为 1.0
        
        return related[:top_k]
    
    # 1. 按标签筛选同主题条目
    current_tags = set(current_item.get('tags', []))
    if current_tags:
        same_tag_items = [
            item for item in other_items 
            if set(item.get('tags', [])) & current_tags
        ]
    else:
        # 如果没有标签，使用所有条目
        same_tag_items = other_items
    
    if not same_tag_items:
        return []
    
    # 2. 计算语义相似度
    try:
        from sentence_transformers import util
        
        related = []
        for item in same_tag_items:
            item_embedding = None
            if item.get('embedding'):
                item_embedding = embedding_manager.load_embedding(item['embedding'])
            
            if item_embedding is not None:
                # 计算余弦相似度
                score = util.cos_sim(current_embedding, item_embedding).item()
                related.append((item, score))
            else:
                # 如果条目没有 embedding，按标签匹配（相似度设为 0.5）
                if current_tags & set(item.get('tags', [])):
                    related.append((item, 0.5))
        
        # 3. 按相似度排序
        related.sort(key=lambda x: x[1], reverse=True)
        return related[:top_k]
    
    except ImportError:
        # 如果无法导入 util，只返回标签匹配的条目
        return [(item, 1.0) for item in same_tag_items[:top_k]]

