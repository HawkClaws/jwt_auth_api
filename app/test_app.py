import unittest
import json
from app import app as flask_app
from app import generate_jwt

class YourFlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        # Flaskアプリケーションのテストクライアントを設定
        self.app = flask_app.test_client()

    def test_generate_jwt_endpoint(self):
        # JWT生成エンドポイントのテスト

        # リクエストのJSONペイロード
        payload = {
            "sub": "test_subject"
            # 他の必要なペイロードデータを追加
        }

        # POSTリクエストをシミュレート
        response = self.app.post('/generate_jwt', json=payload)

        # レスポンスのステータスコードを確認
        self.assertEqual(response.status_code, 200)

        # レスポンスのJSONデータを取得
        data = json.loads(response.data)

        # 生成されたトークンが含まれていることを確認
        self.assertIn("token", data)

    def test_verify_jwt_endpoint(self):
        # JWT検証エンドポイントのテスト

        # 有効なJWTトークンを生成
        valid_payload = {
            "sub": "test_subject"
            # 他の必要なペイロードデータを追加
        }
        valid_token, error_message = generate_jwt(valid_payload)  # トークン生成関数を呼び出す

        # リクエストのJSONペイロード
        request_data = {
            "token": valid_token
        }

        # POSTリクエストをシミュレート
        response = self.app.post('/verify_jwt', json=request_data)

        # レスポンスのステータスコードを確認
        self.assertEqual(response.status_code, 200)

        # レスポンスのJSONデータを取得
        data = json.loads(response.data)

        # デコードされたペイロードが含まれていることを確認
        self.assertIn("sub", data)

if __name__ == '__main__':
    unittest.main()
