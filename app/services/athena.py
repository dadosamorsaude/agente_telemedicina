from pyathena import connect
from pyathena.cursor import DictCursor
from typing import List, Dict, Any
from app.core.config import settings

class AthenaService:
    def __init__(self):
        self.aws_access_key_id = settings.AWS_ACCESS_KEY_ID
        self.aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
        self.region_name = settings.AWS_REGION
        self.s3_staging_dir = settings.ATHENA_S3_STAGING_DIR
        self.schema_name = settings.ATHENA_DATABASE

    def _get_connection(self):
        return connect(
            aws_access_key_id = self.aws_access_key_id,
            aws_secret_access_key = self.aws_secret_access_key,
            region_name = self.region_name,
            s3_staging_dir = self.s3_staging_dir,
            schema_name = self.schema_name
        )

    def execute_query(self,query:str) ->List[Dict[str,Any]]:
        """Executa uma consulta no Athena e retorna os resultados"""
        connection = self._get_connection()
        try:
            with connection.cursor(DictCursor) as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            connection.close()

athena_service = AthenaService()   