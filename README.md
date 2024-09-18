# メールテキストマスクApi

## 概要

このAPIにJSON形式でメールのテキストを渡すと、テキスト内にある機密情報を隠しデータベースに登録してくれるApiです。

## このAPIへのリクエスト方法
【Base Url】<br>
https://あなたのドメイン/domask<br>
【Header】<br>
Content-Type: application/json<br>
x-access-token: 生成した秘密トークン<br>
【Body】<br>
{<br>
　"id":メールのユニークID -> str、int、null可能,<br>
　"text": 相談内容 -> strのみ,<br>
　"date" 受信日 -> 形式はYYYY-MM-DD HH:MM:SSでstrのみ<br>
}<br>
【リクエスト例】<br>
curl -X POST https://あなたのドメイン/domask \
-H "Content-Type: application/json" \
-H "x-access-token: 生成した秘密トークン" \
-d '{"id":123,"text":"こんにちは。メールテキストです。","date":"2030-06-06 12:00:00"}'

## 使用技術
- データベース:mysql
- 言語:Python、Flask

## インストール
- Python -m venv 任意の名前で仮想環境を構築
- venvをactivateし、pipを用いてrequirements.txt内のライブラリインストール
- congfig内にシークレットトークンと、データベースの情報を記入
- Flaskサーバーを起動

