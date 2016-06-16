from tests import BaseTestCase
from redash.models import Query


class TestApiKeyGetByObject(BaseTestCase):
    def test_returns_none_if_not_exists(self):
        data_source = self.factory.create_data_source(group=self.factory.create_group())
        query = self.factory.create_query(data_source=data_source)
        user = self.factory.create_user()
        org=self.factory.org
        Query.fork(query.id, user, org)