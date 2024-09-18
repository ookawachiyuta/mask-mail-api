import re
import emoji
from datetime import datetime
from typing import List
import spacy

def read_words_from_file(file_path):
    """
    マスクしてほしい単語とマスクして欲しくない単語を取得するためのメソッド

    Parameters:
        file_path (str): 読み込むファイルのパス。

    Returns:
        list: 単語を含むリスト。
    """

    words_list = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # 各行の末尾の改行を削除してリストに追加
                words_list.append(line.strip())
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {file_path}")
    except IOError:
        print(f"ファイルの読み込み中にエラーが発生しました: {file_path}")
    
    return words_list


def split_text(text: str, max_bytes: int = 30000) -> List[str]:
    """テキストを指定されたバイト数以下の部分に分割する"""
    parts = []
    current_part = ""
    for char in text:
        if len((current_part + char).encode('utf-8')) > max_bytes:
            parts.append(current_part)
            current_part = char
        else:
            current_part += char
    if current_part:
        parts.append(current_part)
    return parts


def process_token(token, NotMask: List[str], MustMask: List[str]) -> str:
    if token.text in NotMask:
        return token.text
    elif token.text in MustMask:
        return "**固有名詞**"
    
    if token.tag_ == "名詞-固有名詞-地名-一般":
        return "**土地名**"
    elif token.tag_ == "名詞-固有名詞-人名-一般":
        return "**人物名**"
    elif token.pos_ == "PROPN" and token.tag_ != "空白":
        if token.text in ["令和", "平成", "昭和"]:
            return token.text
        else:
            return "**固有名詞**"
    else:
        return token.text


def apply_regex_masks(text: str) -> str:
    # URL
    text = re.sub("https?://[\w!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+", '**URL**', text)
    # クレジットカード番号
    text = re.sub("(?:\d{4}-?){3}\d{4}", '**クレカ番号**', text)
    # 電話番号
    phone_patterns = [
        r'\d{3}（\d{4}）\d{4}',
        r'\d{3}（\d{3}）\d{4}',
        r'((?:\(\d{2,4}\)|\d{2,4}|\（[０-９]{2,4}\）|[０-９]{2,4})[-\s]?([0-9０-９]{2,4})[-\s]?([0-9０-９]{3,4}))(?!\s*(円|年|日|月|万円|千円|%|万))'
    ]
    for pattern in phone_patterns:
        text = re.sub(pattern, '**電話番号**', text)
    # メールアドレス
    text = re.sub(r'\b([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b', lambda x: re.sub(r'[a-zA-Z0-9]', '*', x.group(0)), text)
    # 郵便番号
    text = re.sub("[0-9]{3}-[0-9]{4}", '**郵便番号**', text)
    # 住所
    text = re.sub("丁目", '**', text)
    text = re.sub("番地", '**', text)
    return text


def get_mask_text(text: str) -> str:
    """
    テキスト内の機密情報をマスクし、絵文字も削除し返す

    Parameters:
        text (str): マスクしたいテキスト
    
    Returns:
        str: マスク処理されたテキスト
    """
    nlp = spacy.load('ja_ginza')
    NotMask = read_words_from_file("~~~/wordsNotMask.txt")
    MustMask = read_words_from_file("~~~/wordsMustMask.txt")

    # テキストを分割
    text_parts = split_text(text)
    
    masked_parts = []
    for part in text_parts:
        # テキストを解析
        doc = nlp(part)
        
        masked_text = ""
        for token in doc:
            masked_text += process_token(token, NotMask, MustMask)
        
        masked_text = apply_regex_masks(masked_text)
        masked_parts.append(masked_text)
    
    # 分割されたテキストを結合
    final_masked_text = ''.join(masked_parts)
    
    return emoji.replace_emoji(final_masked_text.strip())
