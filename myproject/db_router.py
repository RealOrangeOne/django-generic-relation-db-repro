class DBRouter:
    def db_for_read(self, model, **hints):
        return "replica"

    def db_for_write(self, model, **hints):
        return "default"

    def allow_migrate(self, db, app_label, **hints):
        # This method doesn't affect the bug, but a good idea anyway
        return db != "replica"

    def allow_relation(self, obj1, obj2, **hints):
        return True
