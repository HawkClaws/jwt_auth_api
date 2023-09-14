# ベースイメージを指定
FROM python:3.8-slim

# ワークディレクトリを設定
WORKDIR /app

COPY ./app /app/

# 依存パッケージのインストール
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# アプリケーションコードのコピー
COPY . .

# ポートの公開
EXPOSE 5000

# アプリケーションの実行(Dockerfile単体の場合使用)
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
