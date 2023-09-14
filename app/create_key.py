import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

# ファイル名を指定
private_key_file_name = "private_key.pem"
public_key_file_name = "public_key.pem"

# RSA鍵の生成
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# 秘密鍵をPEM形式で保存
if not os.path.exists(private_key_file_name):
    with open(private_key_file_name, "wb") as private_key_file:
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        private_key_file.write(private_key_pem)

# 公開鍵をPEM形式で保存
if not os.path.exists(public_key_file_name):
    public_key = private_key.public_key()
    with open(public_key_file_name, "wb") as public_key_file:
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        public_key_file.write(public_key_pem)
