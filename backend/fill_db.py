import json
from app.database import SessionLocal
from app.models import Holiday

holidays_data = [
    {
        "name": "День заповедников и национальных парков",
        "day": 11, "month": 0, "type": "eco", "region": "russia",
        "description": "Праздник, посвященный сохранению уникальных природных территорий России.",
        "events": ["Экскурсии в заповедники", "Экологические лекции"],
        "wikipedia_url": "https://ru.wikipedia.org/wiki/День_заповедников"
    },
    {
        "name": "Всемирный день водных ресурсов",
        "day": 22, "month": 2, "type": "eco", "region": "world",
        "description": "День, напоминающий о важности пресной воды.",
        "events": ["Конференции по очистке воды", "Школьные уроки"],
        "wikipedia_url": "https://ru.wikipedia.org/wiki/Всемирный_день_водных_ресурсов"
    },
    {
        "name": "День Земли",
        "day": 22, "month": 3, "type": "eco", "region": "world",
        "description": "Глобальное событие, направленное на защиту окружающей среды.",
        "events": ["Посадка деревьев", "Уборка мусора"],
        "wikipedia_url": "https://ru.wikipedia.org/wiki/День_Земли"
    },
    {
        "name": "День России",
        "day": 12, "month": 5, "type": "national", "region": "russia",
        "description": "Государственный праздник Российской Федерации.",
        "events": ["Праздничные концерты", "Салюты"],
        "wikipedia_url": "https://ru.wikipedia.org/wiki/День_России"
    },
    {
        "name": "Всемирный день окружающей среды",
        "day": 5, "month": 5, "type": "eco", "region": "world",
        "description": "Главный праздник ООН для привлечения внимания к проблемам окружающей среды.",
        "events": ["Экологические форумы", "Акции по переработке"],
        "wikipedia_url": "https://ru.wikipedia.org/wiki/Всемирный_день_окружающей_среды"
    }
]

db = SessionLocal()

# Очищаем старые данные
db.query(Holiday).delete()

# Добавляем новые
for h in holidays_data:
    holiday = Holiday(
        name=h["name"],
        day=h["day"],
        month=h["month"],
        type=h["type"],
        region=h["region"],
        description=h["description"],
        events=json.dumps(h["events"]),
        wikipedia_url=h["wikipedia_url"]
    )
    db.add(holiday)

db.commit()
db.close()

print(f"✅ Добавлено {len(holidays_data)} праздников!")