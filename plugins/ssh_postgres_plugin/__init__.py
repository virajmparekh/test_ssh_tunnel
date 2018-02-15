from airflow.plugins_manager import AirflowPlugin
from plugins.ssh_postgres_plugin.operators.ssh_postgres_operator import SSHPostgresOperator
from plugins.ssh_postgres_plugin.hooks.astroSSHHook import AstroSSHHook


class SSHPostgresOperator(AirflowPlugin):
    name = "SSHPostgresOperator"
    operators = [SSHPostgresOperator]
    hooks = [AstroSSHHook]
    executors = []
    macros = []
    admin_views = []
    flask_blueprints = []
    menu_links = []
