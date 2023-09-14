# JWT_AUTH_API

JWTの生成と検証を行うシンプルなFlask製APIアプリケーションです。  
このアプリケーションはDockerとDocker Composeを使用して簡単にセットアップできます。

## 使い方

### 設定方法

#### JWT生成/検証に使用する公開鍵/秘密鍵について
`docker-compose up`を実行すると、`create_key.py`が実行され、appディレクトリに`private_key.pem`と`public_key.pem`が存在しない場合、自動的に生成されます。

#### JWTペイロードの設定
ISSUER、AUDIENCE、EXP_MINUTESに関しては環境変数で変更可能です。これらの値を変更するには、`docker-compose.yml`の`environment`で定義された値を変更してください。

### 起動方法
アプリケーションを起動するには、`docker-compose up`を実行します。

### エンドポイント

- JWT生成

POST: `http://localhost:5000/generate_jwt`

JWTを生成します。JWTペイロードはJSON形式でbodyに送信し、"sub"の値を必ず指定する必要があります。

例:

```json
{
    "sub": "F151494071C94FF58944DF4F4AC0A7CA",
    "roles": ["guest", "member"]
}
```

- JWT検証

POST: `http://localhost:5000/verify_jwt`

JWTを検証します。検証に失敗した場合はエラーが返され、成功した場合はデコードされたペイロードが返されます。

```json
{
    "token": "JWTトークン"
}
```