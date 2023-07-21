import os,sys
import json
import re
import jieba
from urllib.parse import unquote
os.chdir(sys.path[0])

def process_text(text):
    # 排除非中文元素
    text = re.sub(r'[^\u4e00-\u9fff]+', '', text)  
    # 使用结巴分词对文本进行分词
    words = jieba.cut(text)
    # 去除停用词和单个字的词项
    words = [word for word in words if len(word) > 1]
    return words

def build_inverted_index(documents):
    inverted_index = {}
    for doc_id, doc in documents.items():
        words = process_text(doc)
        # 记录每个词项的文档频率（df）和在该文档中的词频（tf）
        word_frequency = {}
        for word in words:
            word_frequency.setdefault(word, 0)
            word_frequency[word] += 1
        for word, freq in word_frequency.items():
            inverted_index.setdefault(word, {'df': 0, 'tf': 0, 'docs': {}})
            inverted_index[word]['df'] += 1
            inverted_index[word]['tf'] += freq
            inverted_index[word]['docs'][doc_id] = freq
    return inverted_index

# 读取文档数据
document_dir = 'web_doc'
documents = {}
idurl = {}
for filename in os.listdir(document_dir):
    url = filename.split('_')
    dosid = url.pop(0)
    url = unquote(os.path.splitext('_'.join(url))[0].replace('_', '/'))
    idurl[dosid] = url
    with open(os.path.join(document_dir, filename), 'r', encoding='utf-8') as f:
        document = f.read()
        documents[dosid] = document

# 构建倒排索引
inverted_index = build_inverted_index(documents)
inverted_index = dict(sorted(inverted_index.items(), key=lambda x: (x[1]['df'], sorted(x[1]['docs'].items(), key=lambda y: int(y[0])))))
with open('index_table.json','w',encoding='utf-8') as f:
    json.dump(inverted_index, f, ensure_ascii=False, indent=4)
with open('id_url.json','w',encoding='utf-8') as f:
    json.dump(idurl, f, ensure_ascii=False, indent=4)