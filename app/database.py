from sshtunnel import SSHTunnelForwarder
import pymysql
import logging
from app.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def insert_masked_text_to_db(insert_tuple_data):
    """
    データベースにマスクされたテキストを挿入する。

    Parameters:
    insert_tuple_data (list of tuples): 挿入するデータのリスト。各タプルは以下の形式である必要があります。
        - id (int): メールのID。
        - masked_text (str): マスクされたテキスト。
        - register_date (str): 登録日（'YYYY-MM-DD'形式）。
        - update_date (str): 更新日（'YYYY-MM-DD'形式）。
        - receive_date (str): 受信日（'YYYY-MM-DD'形式）。
    """
    sshConfig = Config.SSH_CONFIG
    dbConfig = Config.DB_CONFIG
    
    try:
        with SSHTunnelForwarder(
                (sshConfig["host"], sshConfig["port"]),
                ssh_username=sshConfig["ssh_username"],
                ssh_pkey=sshConfig["ssh_pkey"],
                ssh_private_key_password=sshConfig["key_password"],
                allow_agent=sshConfig["allow_agent"],
                remote_bind_address=(dbConfig["host"], dbConfig["port"])
        ) as server:
            with pymysql.connect(
                            host=dbConfig["host"],
                            port=server.local_bind_port,
                            user=dbConfig["user"],
                            password=dbConfig["password"],
                            database=dbConfig["database"],
                            charset=dbConfig["charset"],
                            cursorclass=pymysql.cursors.DictCursor
                        ) as connection:
                with connection.cursor() as cursor:
                    insert_sql = "INSERT INTO inquiry (inq_id,inquiry,register_date,update_date,receive_date) VALUES (%s,%s,%s,%s,%s)"
                    cursor.executemany(insert_sql, insert_tuple_data)
                    connection.commit()  # トランザクションのコミット
                    print(f"データ挿入成功: {cursor.rowcount} 行が追加されました。")
    except pymysql.MySQLError as e:
            print(f"データベース接続失敗: {e}")
