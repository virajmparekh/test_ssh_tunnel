from plugins.ssh_postgres_plugin.hooks.astroSSHHook import AstroSSHHook
from airflow.operators import PostgresOperator


class SSHPostgresOperator(PostgresOperator):
    """

    """

    def __init__(
            self, sql,
            postgres_conn_id='postgres_default',
            autocommit=False,
            parameters=None,
            database=None,
            create_tunnel=True,
            * args, **kwargs):
        super(PostgresOperator, self).__init__(*args, **kwargs)
        self.sql = sql
        self.postgres_conn_id = postgres_conn_id
        self.autocommit = autocommit
        self.parameters = parameters
        self.database = database

    def create_tunnel(self):
        print("CREATING TUNNEL")
        if self.create_tunnel is True:
            tunnel = AstroSSHHook(
                ssh_conn_id=self.sftp_conn_id).create_tunnel()
