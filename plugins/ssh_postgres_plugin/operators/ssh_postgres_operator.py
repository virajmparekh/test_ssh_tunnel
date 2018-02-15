from plugins.ssh_postgres_plugin.hooks.astroSSHHook import AstroSSHHook
from airflow.operators import PostgresOperator
from airflow.hooks import PostgresHook
import logging


class SSHPostgresOperator(PostgresOperator):
    """

    """

    def __init__(
            self, sql,
            postgres_conn_id='postgres_default',
            ssh_conn_id='ssh_default',
            autocommit=False,
            parameters=None,
            database=None,
            create_tunnel=True,
            * args, **kwargs):
        super(PostgresOperator, self).__init__(*args, **kwargs)
        self.sql = sql
        self.ssh_conn_id = ssh_conn_id
        self.postgres_conn_id = postgres_conn_id
        self.autocommit = autocommit
        self.parameters = parameters
        self.database = database
        self.create_tunnel = create_tunnel

    def execute(self, context):
        logging.info('Executing: ' + str(self.sql))
        if self.create_tunnel is True:
            self.create_ssh_tunnel()

        self.hook = PostgresHook(postgres_conn_id=self.postgres_conn_id,
                                 schema=self.database)
        self.hook.run(self.sql, self.autocommit, parameters=self.parameters)

    def create_ssh_tunnel(self):
        print("CREATING TUNNEL")
        if self.create_tunnel is True:
            tunnel = AstroSSHHook(ssh_conn_id=self.ssh_conn_id).create_tunnel()
