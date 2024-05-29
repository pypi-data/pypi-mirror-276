from abstra_internals.repositories.authn import authn_repository_factory
from abstra_internals.repositories.connectors import connectors_api_http_client_factory
from abstra_internals.repositories.env_vars import env_vars_repository_factory
from abstra_internals.repositories.execution import execution_repository_factory
from abstra_internals.repositories.execution_logs import (
    execution_logs_repository_factory,
)
from abstra_internals.repositories.lock import lock_repository_factory
from abstra_internals.repositories.notifications import notification_repository_factory
from abstra_internals.repositories.requirements import requirements_repository_factory
from abstra_internals.repositories.roles import roles_repository_factory
from abstra_internals.repositories.stage_run import stage_run_repository_factory
from abstra_internals.repositories.tables import tables_api_http_client_factory
from abstra_internals.repositories.users import users_repository_factory

connectors_api_http_client = connectors_api_http_client_factory()
execution_logs_repository = execution_logs_repository_factory()
requirements_repository = requirements_repository_factory()
notification_repository = notification_repository_factory()
tables_api_http_client = tables_api_http_client_factory()
stage_run_repository = stage_run_repository_factory()
execution_repository = execution_repository_factory()
env_vars_repository = env_vars_repository_factory()
authn_repository = authn_repository_factory()
lock_repository = lock_repository_factory()
users_repository = users_repository_factory()
roles_repository = roles_repository_factory()


__all__ = [
    "connectors_api_http_client",
    "execution_logs_repository",
    "notification_repository",
    "tables_api_http_client",
    "stage_run_repository",
    "execution_repository",
    "env_vars_repository",
    "authn_repository",
    "lock_repository",
    "users_repository",
    "roles_repository",
]
