from abc import ABC, abstractmethod

class InvalidSystemsCountError(ValueError):
    def __init__(self, count):
        self.count = count
        super().__init__(f"Количество затронутых систем должно быть ≥ 1, получено: {count}")


class InvalidHoursError(ValueError):
    def __init__(self, hours):
        self.hours = hours
        super().__init__(f"Часы с момента обнаружения не могут быть отрицательными, получено: {hours}")


class IncidentQueueFullError(Exception):
    def __init__(self, capacity):
        self.capacity = capacity
        super().__init__(f"Очередь переполнена! Максимальная ёмкость: {capacity}")

class SecurityIncident(ABC):

    def __init__(self, incident_id: str, affected_systems: int, hours_since_detected: float):
        self.__incident_id = incident_id
        self.affected_systems = affected_systems
        self.hours_since_detected = hours_since_detected

    @property
    def incident_id(self):
        return self.__incident_id

    @property
    def affected_systems(self):
        return self.__affected_systems

    @affected_systems.setter
    def affected_systems(self, value):
        if value < 1:
            raise InvalidSystemsCountError(value)
        self.__affected_systems = value

    @property
    def hours_since_detected(self):
        return self.__hours_since_detected

    @hours_since_detected.setter
    def hours_since_detected(self, value):
        if value < 0:
            raise InvalidHoursError(value)
        self.__hours_since_detected = value

    @property
    @abstractmethod
    def base_severity(self) -> float:
        ...

    def calculate_weight(self) -> float:
        time_factor = 1 + self.hours_since_detected / 24
        return self.base_severity * self.affected_systems * time_factor

    def get_criticality(self) -> str:
        weight = self.calculate_weight()
        if weight >= 50:
            return "CRITICAL"
        elif weight >= 20:
            return "HIGH"
        elif weight >= 5:
            return "MEDIUM"
        return "LOW"

    def __str__(self):
        return (f"[{self.incident_id}] {self.__class__.__name__}: "
                f"вес={self.calculate_weight():.2f}, "
                f"критичность={self.get_criticality()}")

    def __repr__(self):
        return (f"{self.__class__.__name__}(id={self.incident_id!r}, "
                f"affected_systems={self.affected_systems}, "
                f"hours_since_detected={self.hours_since_detected})")

    def __eq__(self, other):
        if not isinstance(other, SecurityIncident):
            return NotImplemented
        return self.incident_id == other.incident_id

    def __lt__(self, other):
        if not isinstance(other, SecurityIncident):
            return NotImplemented
        return self.calculate_weight() < other.calculate_weight()

    def __add__(self, other):
        if not isinstance(other, SecurityIncident):
            return NotImplemented
        return self.calculate_weight() + other.calculate_weight()

class DDoSAtack(SecurityIncident):
    @property
    def base_severity(self) -> float:
        return 10


class Phishing(SecurityIncident):
    @property
    def base_severity(self) -> float:
        return 3


class DataLeak(SecurityIncident):
    @property
    def base_severity(self) -> float:
        return 8

class IncidentQueue:

    def __init__(self, capacity: int = 100):
        self.__capacity = capacity
        self.__items = []

    def add(self, incident: SecurityIncident):
        if len(self.__items) >= self.__capacity:
            raise IncidentQueueFullError(self.__capacity)
        self.__items.append(incident)

    def __len__(self):
        return len(self.__items)

    def __getitem__(self, index):
        return self.__items[index]

    def __str__(self):
        if not self.__items:
            return "IncidentQueue: пусто"
        lines = [f"IncidentQueue ({len(self)} инцидентов):"]
        for i, inc in enumerate(self.__items, 1):
            lines.append(f"  {i}. {inc}")
        return "\n".join(lines)

    def __repr__(self):
        return f"IncidentQueue(items={len(self)}, capacity={self.__capacity})"

if __name__ == "__main__":
    print("=" * 60)
    print("СОЗДАНИЕ ИНЦИДЕНТОВ")
    print("=" * 60)

    ddos = DDoSAtack("INC-001", affected_systems=3, hours_since_detected=12)
    phish = Phishing("INC-002", affected_systems=1, hours_since_detected=0)
    leak = DataLeak("INC-003", affected_systems=5, hours_since_detected=48)

    print(ddos)
    print(phish)
    print(leak)

    print("\n" + "=" * 60)
    print("МАГИЧЕСКИЕ МЕТОДЫ")
    print("=" * 60)
    print(f"repr(ddos) = {ddos!r}")
    print(f"ddos == DDoSAtack('INC-001', 3, 12): "
          f"{ddos == DDoSAtack('INC-001', 3, 12)}")
    print(f"ddos + leak (общий вес) = {ddos + leak:.2f}")

    print("\n" + "=" * 60)
    print("РАБОТА С КОНТЕЙНЕРОМ")
    print("=" * 60)
    queue = IncidentQueue(capacity=5)
    queue.add(ddos)
    queue.add(phish)
    queue.add(leak)
    print(queue)
    print(f"\nlen(queue) = {len(queue)}")
    print(f"queue[0]   = {queue[0]}")

    print("\n" + "=" * 60)
    print("СОРТИРОВКА ПО ВЕСУ (__lt__)")
    print("=" * 60)
    for inc in sorted(queue):
        print(f"  {inc}")

    print("\n" + "=" * 60)
    print("ПОЛИМОРФНЫЙ ВЫЗОВ calculate_weight()")
    print("=" * 60)
    for inc in queue:
        print(f"  {inc.incident_id}: {inc.calculate_weight():.2f} → {inc.get_criticality()}")

    print("\n" + "=" * 60)
    print("ПЕРЕХВАТ ИСКЛЮЧЕНИЙ")
    print("=" * 60)

    try:
        bad = DDoSAtack("INC-ERR-1", affected_systems=0, hours_since_detected=5)
    except InvalidSystemsCountError as e:
        print(f"[✗] {e}")

    try:
        bad = Phishing("INC-ERR-2", affected_systems=2, hours_since_detected=-3)
    except InvalidHoursError as e:
        print(f"[✗] {e}")

    try:
        full_queue = IncidentQueue(capacity=2)
        full_queue.add(ddos)
        full_queue.add(phish)
        full_queue.add(leak)
    except IncidentQueueFullError as e:
        print(f"[✗] {e}")