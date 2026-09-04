import os
from dotenv import load_dotenv

load_dotenv()

# Get environment variables
MONGODB_URI = os.getenv("MONGODB_URI")
USE_MOCK_DB = os.getenv("USE_MOCK_DB", "true").lower() in ("true", "1", "yes")

import json
import asyncio
import copy

# Ensure data directory exists
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

MOCK_DB_FILE = os.path.join(DATA_DIR, 'mock_db.json')
db_lock = asyncio.Lock()

if USE_MOCK_DB:
    # Load from file if exists
    if os.path.exists(MOCK_DB_FILE):
        with open(MOCK_DB_FILE, 'r', encoding='utf-8') as f:
            mock_db = json.load(f)
    else:
        # In-memory mock database initially
        mock_db = {
            "users": {},  # key: enrollment (uppercase), value: user dict
            "subjects": [],
            "quizzes": []
        }

    async def save_mock_db():
        async with db_lock:
            # We use an async lock to ensure safety, even though the file IO is synchronous.
            # In a heavy load scenario, we'd use aiofiles, but this is sufficient for this lock context.
            with open(MOCK_DB_FILE, 'w', encoding='utf-8') as f:
                json.dump(mock_db, f, indent=2, default=str)

    class MockCursor:
        def __init__(self, docs):
            self._docs = docs

        async def to_list(self, length=None):
            return self._docs[:length] if length else self._docs

        def __aiter__(self):
            self._iter = iter(self._docs)
            return self

        async def __anext__(self):
            try:
                return next(self._iter)
            except StopIteration:
                raise StopAsyncIteration

    class MockCollection:
        def __init__(self, collection_name):
            self.collection_name = collection_name
        
        async def find_one(self, query):
            if self.collection_name == "users" and "enrollment" in query:
                user = mock_db["users"].get(query["enrollment"])
                return copy.deepcopy(user) if user else None
            return None
        
        async def insert_one(self, document):
            if self.collection_name == "users":
                enrollment = document["enrollment"]
                if enrollment in mock_db["users"]:
                    from pymongo.errors import DuplicateKeyError
                    raise DuplicateKeyError("Enrollment already exists")
                mock_db["users"][enrollment] = copy.deepcopy(document)
                await save_mock_db()
            return None
        
        async def update_one(self, query, update):
            if self.collection_name == "users" and "enrollment" in query:
                enrollment = query["enrollment"]
                if enrollment in mock_db["users"]:
                    if "$set" in update:
                        mock_db["users"][enrollment].update(copy.deepcopy(update["$set"]))
                        await save_mock_db()
                    return {"modified_count": 1}
            return {"modified_count": 0}

    class GenericMockCollection:
        def __init__(self, collection_name):
            self.collection_name = collection_name
            if collection_name not in mock_db:
                mock_db[collection_name] = []
                # Can't await save_mock_db in sync __init__, but it's safe 
                # since this only happens on startup.
                with open(MOCK_DB_FILE, 'w', encoding='utf-8') as f:
                    json.dump(mock_db, f, indent=2)

        def _matches(self, doc, query):
            if not query:
                return True
            return all(doc.get(k) == v for k, v in query.items())

        def find(self, query=None):
            docs = [copy.deepcopy(d) for d in mock_db[self.collection_name] if self._matches(d, query)]
            return MockCursor(docs)

        async def find_one(self, query=None):
            for d in mock_db[self.collection_name]:
                if self._matches(d, query):
                    return copy.deepcopy(d)
            return None

        async def insert_one(self, document):
            mock_db[self.collection_name].append(copy.deepcopy(document))
            await save_mock_db()
            return None

        async def insert_many(self, documents):
            mock_db[self.collection_name].extend([copy.deepcopy(d) for d in documents])
            await save_mock_db()
            return None

        async def delete_many(self, query=None):
            initial_count = len(mock_db[self.collection_name])
            if not query:
                mock_db[self.collection_name].clear()
                deleted_count = initial_count
            else:
                mock_db[self.collection_name] = [
                    d for d in mock_db[self.collection_name] if not self._matches(d, query)
                ]
                deleted_count = initial_count - len(mock_db[self.collection_name])
            await save_mock_db()
            class DeleteResult:
                def __init__(self, count):
                    self.deleted_count = count
            return DeleteResult(deleted_count)


        async def count_documents(self, query=None):
            return len([d for d in mock_db[self.collection_name] if self._matches(d, query)])

        async def update_one(self, query, update):
            for d in mock_db[self.collection_name]:
                if self._matches(d, query):
                    if "$set" in update:
                        d.update(copy.deepcopy(update["$set"]))
                    await save_mock_db()
                    return {"modified_count": 1}
            return {"modified_count": 0}

    class MockDatabase:
        def __init__(self):
            self.users = MockCollection("users")
            self.subjects = GenericMockCollection("subjects")
            self.quizzes = GenericMockCollection("quizzes")
            self.performance = GenericMockCollection("performance")
            self.admin_credentials = GenericMockCollection("admin_credentials")
            self.resources = GenericMockCollection("resources")
            self.playlists = GenericMockCollection("playlists")

    db = MockDatabase()


    async def init_db():
        # No need for indexes with mock db
        pass
        
    async def upload_file(filename: str, content: bytes, content_type: str = "application/octet-stream"):
        import base64, uuid
        file_id = str(uuid.uuid4())
        if "files" not in mock_db:
            mock_db["files"] = {}
        mock_db["files"][file_id] = {
            "filename": filename,
            "content_type": content_type,
            "content_b64": base64.b64encode(content).decode("utf-8")
        }
        await save_mock_db()
        return file_id

    async def get_file(file_id: str):
        import base64
        file_obj = mock_db.get("files", {}).get(file_id)
        if file_obj:
            return {
                "filename": file_obj.get("filename", "document.pdf"),
                "content_type": file_obj.get("content_type", "application/pdf"),
                "content": base64.b64decode(file_obj.get("content_b64", ""))
            }
        return None

else:
    # Real MongoDB
    from motor.motor_asyncio import AsyncIOMotorClient
    from motor.motor_asyncio import AsyncIOMotorGridFSBucket

    client = AsyncIOMotorClient(MONGODB_URI)
    db = client.edumind
    fs = None

    def get_fs():
        global fs
        if fs is None:
            fs = AsyncIOMotorGridFSBucket(db)
        return fs

    async def init_db():
        get_fs()
        # Create unique index on enrollment
        try:
            await db.users.create_index("enrollment", unique=True)
            await db.admin_credentials.create_index("admin_id", unique=True)
        except Exception:
            pass

    async def upload_file(filename: str, content: bytes, content_type: str = "application/octet-stream"):
        bucket = get_fs()
        file_id = await bucket.upload_from_stream(
            filename,
            content,
            metadata={"contentType": content_type}
        )
        return str(file_id)

    async def get_file(file_id: str):
        from bson import ObjectId
        bucket = get_fs()
        try:
            grid_out = await bucket.open_download_stream(ObjectId(file_id))
            content = await grid_out.read()
            return {
                "filename": grid_out.filename,
                "content_type": grid_out.metadata.get("contentType", "application/octet-stream"),
                "content": content
            }
        except Exception:
            return None

