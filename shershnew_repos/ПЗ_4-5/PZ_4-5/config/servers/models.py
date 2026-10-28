from abc import ABC, abstractmethod


class QueryReport(ABC):
    """Базовый класс отчёта о медленных запросах."""

    def __init__(self, queries: list):
        self.queries = queries

    @abstractmethod
    def get_info(self) -> str:
        ...


class DailyReport(QueryReport):
    def get_info(self) -> str:
        total = sum(q["duration_ms"] for q in self.queries)
        return (f"[DAILY] Запросов: {len(self.queries)}, "
                f"суммарно {total:.0f} мс")


class WeeklyReport(QueryReport):
    def get_info(self) -> str:
        total = sum(q["duration_ms"] for q in self.queries)
        avg = total / len(self.queries) if self.queries else 0
        return (f"[WEEKLY] Запросов: {len(self.queries)}, "
                f"среднее {avg:.0f} мс")


class MonthlyReport(QueryReport):
    def get_info(self) -> str:
        total = sum(q["duration_ms"] for q in self.queries)
        slowest = max((q["duration_ms"] for q in self.queries), default=0)
        return (f"[MONTHLY] Запросов: {len(self.queries)}, "
                f"суммарно {total:.0f} мс, самый медленный {slowest:.0f} мс")


class QueryReportFactory:
    """Factory: создаёт отчёт нужного типа."""

    _registry = {
        "daily": DailyReport,
        "weekly": WeeklyReport,
        "monthly": MonthlyReport,
    }

    @classmethod
    def create(cls, report_type: str, queries: list) -> QueryReport:
        key = report_type.lower()
        if key not in cls._registry:
            raise ValueError(f"Неизвестный тип отчёта: {report_type}")
        return cls._registry[key](queries)