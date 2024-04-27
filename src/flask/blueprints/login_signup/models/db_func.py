# python で mysql を使用するためのモジュール
import mysql.connector as mydb
# ハッシュ化のためのモジュール
import hashlib

# コネクションの作成
conn = mydb.connect(
    host='db',
    port='3306',
    user='username',
    password='password',
    database='app_db'
)

# コネクションが切れた時に再接続してくれるよう設定
conn.ping(reconnect=True)

# DB操作用にカーソルを作成
cur = conn.cursor()

def register(username, password):
    """ 入力されたユーザ名とパスワードを登録するメソッド

        Args:
            username : ユーザの名前
            password : ユーザのパスワード
    """
    print("ユーザを追加")
    # パスワードをハッシュ化し16進数に変更
    hash_hex_pass = hashlib.sha256(password.encode()).hexdigest()
    print(username)
    print(hash_hex_pass)

    # DBにデータを追加
    cur.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{hash_hex_pass}')")
    # DBの変更を確定する
    conn.commit()


def auth(username, password):
    """ 入力されたユーザ名とパスワードがデータベースに格納されているか確認するメソッド

        Args:
            username : ユーザの名前
            password : ユーザのパスワード
        
        Return:
            登録されている場合: True
            other : False
    """

    # データを取得する
    cur.execute('select * from users')
    result = cur.fetchall()

    # パスワードをハッシュ化し16進数に変更
    hash_hex_pass = hashlib.sha256(password.encode()).hexdigest()

    # 同名のユーザ名とパスワードがあるか確認する
    isAuth = False
    for list in result:
        if username == list[1] and hash_hex_pass == list[2]:
            isAuth = True
            break

    return isAuth

def isSameUser(username):
    """ 入力されたユーザ名がすでに存在するか確認するメソッド

        Args:
            username : ユーザの名前
        
        Return:
            すでに登録されている場合: True
            other : False
    """
    # データを取得する
    cur.execute('select * from users')
    result = cur.fetchall()
    # 名前が同じかどうか
    isSame = False

    for list in result:
        # print(list)
        # 同じ名前ならfalseにする
        if list[1] == username:
            print("OK")
            isSame = True
            break

    return isSame