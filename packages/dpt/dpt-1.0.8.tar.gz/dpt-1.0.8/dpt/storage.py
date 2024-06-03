from __future__ import annotations
import json
from pymongo import MongoClient
from pymongo.database import Database as MongoDatabase
from pymongo.collection import Collection
from typing import Any, Optional
import jsonschema
import copy


class ConnectionInfo:
    def __init__(self, connectionString):
        self.connectionString = connectionString
        # if self.connectionString == None:
        #     from .system import system
        #     self.connectionString = system.db_connection_string
        self._instance = None

    def instance(self) -> MongoClient:
        if self._instance == None:
            self._instance = MongoClient(self.connectionString)
        return self._instance


class DatabaseInfo:
    def __init__(
        self,
        name: str = None,
        connection: ConnectionInfo = None,
        instance: MongoDatabase = None,
    ):
        if instance != None:
            self._instance = instance
        else:
            self.name = name
            self.connection = connection
            self._instance = None

    def instance(self) -> MongoDatabase:
        if self._instance == None:
            self._instance = self.connection.instance()[self.name]
        return self._instance


class CollectionInfo:
    def __init__(self, collectionName: str, database: DatabaseInfo):
        self._collection_name = collectionName
        self.name = collectionName
        self.database = database
        self._count = None
        # if self.database == None:
        #     self.database = Database()
        self._instance = None

    def get_count(self):
        if self._count == None:
            self._update_count_from_collection()
        return self._count

    def get_coll_name(self):
        return self.name

    def get_info(self):
        return f"collection '{self.name}'"

    def instance(self) -> Collection:
        if self._instance == None:
            self._instance = self.database.instance()[self.name]
        return self._instance

    def _update_count_from_collection(self):
        self._count = self.instance().count_documents({})

    def _create_lookup_indexes(self, item: list[dict] | dict):
        objects = []
        if isinstance(item, dict):
            objects = [item]
        if isinstance(item, list):
            objects = item
        for obj in objects:
            if isinstance(obj, dict):
                for name in obj:
                    if name == "$lookup":
                        spec = obj["$lookup"]
                        coll_name = spec["from"]
                        if "foreignField" in spec:
                            field = spec["foreignField"]
                            coll = self.instance().database[coll_name]
                            ind_opt = (field, 1)
                            coll.create_index([ind_opt])
                    self._create_lookup_indexes(obj[name])

    def _aggregate(self, pipeline: list[dict[str, Any]], out: CollectionInfo = None):

        if len(pipeline) > 0:
            last_step = pipeline[-1]

            bad_step = None
            if "$out" in last_step:
                bad_step = "$out"
            if "$merge" in last_step:
                bad_step = "$merge"

            if bad_step != None:
                raise Exception(
                    f'{bad_step} stage is not allowed. Please use "out" parameter instead, e. g. aggregate(out=task.temp_coll("my_temp_coll"),pipeline=[...])'
                )

        if out != None:
            self._update_count_from_collection()
            print(f"read {self._count} documents from {self.get_info()}")
            print("")

        prep_pipeline = _prepare_pipeline(pipeline)
        self._create_lookup_indexes(prep_pipeline)
        if out != None:
            prep_pipeline.append({"$out": out._collection_name})
        pipeline_json = json.dumps(prep_pipeline, ensure_ascii=False)
        print("run aggregation:")
        print("")
        print(
            f'db.getCollection("{self.instance().name}").aggregate(\n{pipeline_json}\n)'
        )
        print("")
        if out != None:
            self.instance().aggregate(prep_pipeline)
            out._update_count_from_collection()
            if isinstance(out, DbWriter):
                out.close()
        else:
            return self.instance().aggregate(prep_pipeline)

    def _read_all(self):
        self._count = self.instance().count_documents({})
        print(f"read {self._count} documents from {self.get_info()}")
        return self.instance().find({})

    def _read_one(self):
        return self.instance().find_one({})

    def _clear(self):
        self._count = 0
        self.instance().delete_many({})

    def _write_many(self, documents: list[dict]):
        if len(documents) > 0:
            self.instance().insert_many(documents)
        self._count += len(documents)

    def create_index(
        self,
        keys,
    ) -> str:
        self.instance().create_index(keys=keys)


def _prepare_pipeline(pipeline: list[dict]) -> list[dict]:
    orig_pipeline = pipeline
    new_pipeline: list[dict] = []
    for step in orig_pipeline:
        new_pipeline.append(step.copy())

    def bad_ref_text(step, coll_ref):
        return f'Incorrect collection reference `{coll_ref}`. Use reader object to reference collection, e. g. "from": task.get_named_reader("coll_to_join"). Incorrect step: \n {step}'

    def first_of(d) -> tuple[str, dict]:
        for key, value in d.items():
            return key, value

    for step in new_pipeline:
        step_name, step = first_of(step)
        if step_name in ["$lookup", "$graphLookup", "$unionWith"]:
            coll_ref = step.get("from") or step.get("coll")
            if isinstance(coll_ref, CollectionInfo):
                step["from"] = coll_ref._collection_name
            else:
                raise Exception(bad_ref_text(step, coll_ref))
        if step_name in ["$lookup"]:
            nested_pipeline = step.get("pipeline")
            if nested_pipeline != None:
                step["pipeline"] = _prepare_pipeline(nested_pipeline)
    return new_pipeline


class DbReader(CollectionInfo):
    def __init__(self, collectionName: str, database: DatabaseInfo = None):
        super().__init__(collectionName, database)

    def read_all(self):
        return self._read_all()

    def read_one(self):
        return self._read_one()

    def aggregate(
        self, pipeline: list[dict[str, Any]], out: DbWriter | TempCollection = None
    ):
        return self._aggregate(pipeline, out)


class DbWriter(CollectionInfo):
    def __init__(self, collectionName: str, database: DatabaseInfo = None):
        super().__init__(collectionName, database)
        self._closed = True

    def clear(self):
        self._clear()

    def write_many(self, documents: list[dict]):
        self._write_many(documents)
        self._closed = False

    def close(self):
        self._closed = True
        print(f"loaded {self._count} documents into {self.get_info()}")

    def is_closed(self):
        return self._closed


class TempCollection(CollectionInfo):
    def __init__(self, collectionName: str, database: DatabaseInfo = None):
        super().__init__(collectionName, database)

    def clear(self):
        self._clear()

    def write_many(self, documents: list[dict]):
        self._write_many(documents)

    def read_all(self):
        return self._read_all()

    def read_one(self):
        return self._read_one()

    def aggregate(
        self, pipeline: list[dict[str, Any]], out: DbWriter | TempCollection = None
    ):
        return self._aggregate(pipeline, out)


class MemoryReader:
    def __init__(self, data: list[dict[str, Any]], schema: dict):
        self._data = data
        self.schema = schema

    def _validate(self):
        if self.schema == None:
            return
        for item in self._data:
            jsonschema.validate(instance=item, schema=self.schema)

    def get_count(self):
        return len(self._data)

    def get_coll_name(self):
        return None

    def get_info(self):
        return f"list[]"

    def read_all(self):
        self._validate()
        print(f"read {len(self._data)} documents from {self.get_info()}")
        return self._data

    def read_one(self) -> Any | None:
        self._validate()
        if len(self._data) == 0:
            return None
        return self._data[0]


class MemoryWriter:
    def __init__(self, data: list[dict[str, Any]]):
        self._data = data
        self._count = 0
        self._closed = True

    def get_info(self):
        return f"list[]"

    def clear(self):
        self._data.clear()

    def write_many(self, documents: list[dict]):
        self._data.extend(documents)
        self._count += len(documents)
        self._closed = False

    def close(self):
        print(f"loaded {self._count} documents into {self.get_info()}")
        self._closed = True

    def is_closed(self):
        return self._closed
