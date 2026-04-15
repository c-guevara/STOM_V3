
import sqlite3
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional


class DatabaseManager:
    def __init__(self):
        DB_PATH = Path(__file__).parent.parent.parent / "_database"
        self.tradelist_db = f"{DB_PATH}/tradelist.db"
        self._enable_wal_mode()

    def _enable_wal_mode(self):
        """WAL 모드 활성화로 동시 읽기/쓰기 가능"""
        try:
            conn = sqlite3.connect(self.tradelist_db)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            conn.execute("PRAGMA busy_timeout=5000")  # 5초 타임아웃
            conn.close()
        except Exception as e:
            print(f"WAL 모드 설정 오류: {e}")

    def _get_connection(self):
        """연결 생성 with WAL 최적화"""
        conn = sqlite3.connect(self.tradelist_db, check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA busy_timeout=5000")
        return conn

    def get_jangolist(self, market: str = "stock") -> List[Dict[str, Any]]:
        conn = self._get_connection()
        table_name = f"{market}_jangolist"
        try:
            df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
            return df.to_dict('records')
        except Exception as e:
            print(f"Position list query error: {e}")
            return []
        finally:
            conn.close()

    def get_chegeollist(self, market: str = "stock", limit: int = 20) -> List[Dict[str, Any]]:
        conn = self._get_connection()
        table_name = f"{market}_chegeollist"
        try:
            # 컬럼명에 백틱 사용하여 특수문자/한글 처리
            query = f'SELECT * FROM "{table_name}" ORDER BY "체결시간" DESC LIMIT ?'
            df = pd.read_sql(query, conn, params=(limit,))
            return df.to_dict('records')
        except Exception as e:
            print(f"Execution list query error: {e}")
            return []
        finally:
            conn.close()

    def get_tradelist(self, market: str = "stock", limit: int = 50) -> List[Dict[str, Any]]:
        conn = self._get_connection()
        table_name = f"{market}_tradelist"
        try:
            # 컬럼명에 백틱 사용하여 특수문자/한글 처리
            query = f'SELECT * FROM "{table_name}" ORDER BY "체결시간" DESC LIMIT ?'
            df = pd.read_sql(query, conn, params=(limit,))
            return df.to_dict('records')
        except Exception as e:
            print(f"Trade list query error: {e}")
            return []
        finally:
            conn.close()

    def get_totaltradelist(self, market: str = "stock") -> Optional[Dict[str, Any]]:
        conn = self._get_connection()
        table_name = f"{market}_totaltradelist"
        try:
            df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
            if len(df) > 0:
                return df.to_dict('records')[0]
            return None
        except Exception as e:
            print(f"Total trade summary query error: {e}")
            return None
        finally:
            conn.close()
