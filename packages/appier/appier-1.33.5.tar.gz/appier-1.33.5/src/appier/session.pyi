class Session: ...
class MockSession(Session): ...
class DataSession(Session): ...
class MemorySession(DataSession): ...
class FileSession(DataSession): ...
class RedisSession(DataSession): ...
class ClientSession(DataSession): ...
