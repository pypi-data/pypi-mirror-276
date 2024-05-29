from .base_test_class import CNCBaseTestCase
from cnc.models import Application
from cnc.constants import EnvironmentVariableTypes

from cnc.logger import get_logger

log = get_logger(__name__)


class ServiceEnvironmentItemsTestCase(CNCBaseTestCase):
    fixture_name = "backend-1-service-1-db-variables-aliases"

    def setUp(self):
        super().setUp()
        app = Application.from_environments_yml("environments.yml")
        self.collection = app.collections[0]
        self.environment = self.collection.environments[0]
        self.assertEqual(self.environment.name, "main")
        self.service = self.environment.services[0]
        self.assertEqual(self.service.name, "app")

    def test_all_items(self):
        # outputs - 2
        # secrets - 2
        # standard vars - 2
        total_env_items = 6
        total_env_items += len(self.service.config.managed_environment_variables)
        total_env_items += len(self.service.config.managed_environment_secrets)

        self.assertEqual(len(self.service.environment_items), total_env_items)

    def test_environment_secrets(self):
        num_secrets = 2
        num_secrets += len(self.service.config.managed_environment_secrets)
        self.assertEqual(len(self.service.environment_secrets), num_secrets)

        service_secrets = self.service.filtered_environment_items(
            variable_type=EnvironmentVariableTypes.VARIABLE_TYPE_SECRET
        )
        self.assertEqual(service_secrets[0].name, "foo-secret")
        self.assertEqual(service_secrets[1].name, "foo-secret-alias")
        self.assertEqual(service_secrets[0].secret_id, service_secrets[1].secret_id)

    def test_environment_outputs(self):
        self.assertEqual(len(self.service.environment_outputs), 2)

        service_secrets = self.service.environment_outputs
        self.assertEqual(service_secrets[0].name, "foo-output")
        self.assertEqual(service_secrets[1].name, "foo-output-alias")
        self.assertEqual(service_secrets[0].output_name, service_secrets[1].output_name)

    def test_environment_standard_variables(self):
        service_vars = self.service.filtered_environment_items(
            variable_type=EnvironmentVariableTypes.VARIABLE_TYPE_STANDARD
        )
        self.assertEqual(len(service_vars), 2)

        self.assertEqual(service_vars[0].name, "foo-standard")
        self.assertEqual(service_vars[1].name, "foo-standard-alias")
        self.assertEqual(service_vars[0].value, service_vars[1].value)

    def test_environment_variables(self):
        # num default managed vars for all envs - 3
        # num standard vars - 2
        num_service_env_vars = 5

        for svc in self.environment.config.services:
            num_service_env_vars += len(svc.settings.managed_environment_variables)

        service_vars = self.service.environment_variables
        self.assertEqual(len(service_vars), 15)
