import random
from abc import ABC, abstractmethod


class Routor(ABC):
    @abstractmethod
    def route(self, request):
        pass


class PrimaryReplicaRoutor(Routor):
    def __init__(self):
        self.primary = "default"
        self.replica_1 = "replica_1"
        self.replica_2 = "replica_2"

    def route(self, request):
        if request.method == "GET":
            return random.choice([self.replica_1, self.replica_2])
        return self.primary

    def db_for_read(self, model, **hints):
        return self.route(model)

    def db_for_write(self, model, **hints):
        return self.route(model)

    def allow_relation(self, obj1, obj2, **hints):

        db_set = {self.primary, self.replica_1, self.replica_2}
        if db_set.issuperset({self.route(obj1._state.db), self.route(obj2._state.db)}):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
