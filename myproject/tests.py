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
        self.assertEqual(self.revision._state.db, "replica")

        # This is correct, as Django assumes reads by default
        self.assertEqual(self.revision.mains.db, "replica")

    def test_update(self):
        with CaptureQueriesContext(connections["replica"]) as replica_queries:
            self.revision.mains.update(text="test")

        # Replica should not be doing write queries
        self.assertEqual(replica_queries.captured_queries, [])

    def test_explicit(self):
        revision = Revision.objects.using("default").first()

        self.assertEqual(revision._state.db, "default")

        # This is correct, as Django assumes reads by default
        self.assertEqual(revision.mains.db, "replica")

        with CaptureQueriesContext(connections["replica"]) as replica_queries:
            revision.mains.update(text="test")

        # Replica should not be doing write queries
        self.assertEqual(replica_queries.captured_queries, [])
