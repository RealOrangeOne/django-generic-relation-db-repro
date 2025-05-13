from django.test import TransactionTestCase
from django.test.utils import CaptureQueriesContext
from .models import MainModel, Revision
from django.contrib.contenttypes.models import ContentType
from django.db import connections

class TestTestCase(TransactionTestCase):
    databases = "__all__"

    def setUp(self):
        revision = Revision.objects.create()

        MainModel.objects.create(
            content_type=ContentType.objects.get_for_model(Revision),
            object_id=revision.id
        )
        self.revision = Revision.objects.first()

    def test_setup(self):
        self.assertEqual(self.revision.mains.db, "replica")
        self.assertEqual(self.revision._state.db, "replica")

    def test_update(self):
        with CaptureQueriesContext(connections["replica"]) as replica_queries:
            self.revision.mains.update(text="test")

        # Replica should not be doing write queries
        self.assertEqual(replica_queries.captured_queries, [])
