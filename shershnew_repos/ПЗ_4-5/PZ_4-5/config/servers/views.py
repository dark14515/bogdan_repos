from django.http import HttpResponse
from .singleton import SlowQueryMonitor
from .models import QueryReportFactory


def index(request):
    """Главная страница: демонстрация Singleton и Factory."""
    monitor = SlowQueryMonitor()

    # --- Singleton: добавляем запросы ---
    monitor.log_query("SELECT * FROM orders", 1500)
    monitor.log_query("SELECT * FROM users", 250)
    monitor.log_query("UPDATE products SET price = price * 1.1", 3200)
    monitor.log_query("SELECT * FROM logs", 8000)

    queries = monitor.get_queries()

    # --- Singleton: проверка единственности ---
    monitor2 = SlowQueryMonitor()
    same = (id(monitor) == id(monitor2))

    # --- Factory: создаём три отчёта ---
    try:
        daily   = QueryReportFactory.create("daily",   queries)
        weekly  = QueryReportFactory.create("weekly",  queries)
        monthly = QueryReportFactory.create("monthly", queries)
        reports = [daily.get_info(), weekly.get_info(), monthly.get_info()]
    except ValueError as e:
        return HttpResponse(f"Ошибка: {e}", status=400)

    # --- HTML ---
    html = f"""
    <h1>Мониторинг медленных запросов</h1>

    <h2>Singleton: SlowQueryMonitor</h2>
    <p>Один экземпляр? <b>{same}</b> (id: {id(monitor)} == {id(monitor2)})</p>
    <p>Записано медленных запросов: <b>{len(queries)}</b></p>
    <ul>
        {''.join(f'<li>{q["query"]} — {q["duration_ms"]} мс</li>' for q in queries)}
    </ul>

    <h2>Factory: QueryReportFactory</h2>
    <ul>
        {''.join(f'<li>{r}</li>' for r in reports)}
    </ul>
    """
    return HttpResponse(html)


def error_demo(request):
    """Демонстрация ошибки при неизвестном типе отчёта."""
    try:
        QueryReportFactory.create("yearly", [])
    except ValueError as e:
        return HttpResponse(f"Поймано исключение: {e}", status=400)