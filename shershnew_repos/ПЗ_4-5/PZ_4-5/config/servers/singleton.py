class SlowQueryMonitor:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._queries = []   # список медленных запросов
        return cls._instance

    def log_query(self, query: str, duration_ms: float, threshold_ms: float = 1000):
        if duration_ms >= threshold_ms:
            self._queries.append({
                "query": query,
                "duration_ms": duration_ms,
            })
            return True
        return False

    def get_queries(self):
        return list(self._queries)

    def clear(self):
        self._queries.clear()