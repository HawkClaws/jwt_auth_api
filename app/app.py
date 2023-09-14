from flask import Flask, request, jsonify
import jwt
import os
import datetime
from jwt.exceptions import (
    InvalidTokenError,
    DecodeError,
    ExpiredSignatureError,
    InvalidAudienceError,
    InvalidIssuerError,
    InvalidIssuedAtError,
    ImmatureSignatureError,
    InvalidAlgorithmError
)

app = Flask(__name__)

# 設定のデフォルト値
DEFAULTS = {
    "PRIVATE_KEY_PATH": "private_key.pem",
    "PUBLIC_KEY_PATH": "public_key.pem",
    "EXP_MINUTES": 60,
    "ISSUER": "your_issuer",
    "AUDIENCE": "client-app",
    "ALGORITHM": 'RS256'
}

# 設定の読み込みと設定オブジェクトの作成


def load_config():
    config = {key: os.environ.get(key, value)
              for key, value in DEFAULTS.items()}
    return config


CONFIG = load_config()

# JWTの生成


def generate_jwt(payload):
    try:
        exp_minutes = int(CONFIG["EXP_MINUTES"])
        exp_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=exp_minutes)

        payload.update({
            "exp": exp_time,
            "nbf": datetime.datetime.utcnow(),
            "iss": CONFIG["ISSUER"],
            "aud": [CONFIG["AUDIENCE"]],
            "iat": datetime.datetime.utcnow(),
        })

        with open(CONFIG["PRIVATE_KEY_PATH"], 'rb') as private_key_file:
            private_key = private_key_file.read()

        token = jwt.encode(payload=payload, key=private_key,
                           algorithm=CONFIG["ALGORITHM"])
        return token, None
    except Exception as e:
        return None, str(e)

# JWTの検証
def verify_jwt(token):
    try:
        with open(CONFIG["PUBLIC_KEY_PATH"], 'rb') as public_key_file:
            public_key_data = public_key_file.read()

        decoded_payload = jwt.decode(token, public_key_data, audience=[CONFIG["AUDIENCE"]],
                                     issuer=CONFIG["ISSUER"], algorithms=[CONFIG["ALGORITHM"]])
        return decoded_payload, None
    except (ExpiredSignatureError, DecodeError, InvalidAudienceError, InvalidIssuerError,
            InvalidIssuedAtError, ImmatureSignatureError, InvalidAlgorithmError, InvalidTokenError) as e:
        return None, str(e)
    except Exception as e:
        return None, str(e)

# JWT生成エンドポイント
@app.route('/generate_jwt', methods=['POST'])
def generate_jwt_endpoint():
    try:
        payload = request.get_json()

        # "sub"がpayloadに含まれているか確認
        if 'sub' not in payload:
            return jsonify({"error": "Missing 'sub' in the request body"}), 400

        generated_token, error_message = generate_jwt(payload)
        if generated_token:
            return jsonify({"token": generated_token}), 200
        else:
            return jsonify({"error": "JWT generation error", "error_message": error_message}), 500
    except Exception as e:
        return jsonify({"error": "Internal server error", "error_message": str(e)}), 500


# JWT検証エンドポイント
@app.route('/verify_jwt', methods=['POST'])
def verify_jwt_endpoint():
    data = request.get_json()
    token = data.get('token')

    if not token:
        return jsonify({"error": "Missing token or public_key_path"}), 400

    decoded_payload, error_message = verify_jwt(token)
    if decoded_payload:
        return jsonify(decoded_payload), 200
    else:
        return jsonify({"error": "JWT verification error", "error_message": error_message}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
