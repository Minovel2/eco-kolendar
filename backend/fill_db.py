import json
from app.database import SessionLocal
from app.models import Holiday

holidays_data = [
  {
    "name": "Всемирный день водно-болотных угодий",
    "day": 2, "month": 1, "type": "eco", "region": "world",
    "description": "Отмечается с 1997 года. Подписание Рамсарской конвенции о водно-болотных угодьях.",
    "events": ["Очистка берегов", "Учет водоплавающих птиц", "Эко-лекции"],
    "wikipedia_url": "https://ru.wikipedia.org/wiki/Всемирный_день_водно-болотных_угодий"
  },
  {
    "name": "Всемирный день дикой природы",
    "day": 3, "month": 2, "type": "eco", "region": "world",
    "description": "Установлен ООН в 2013 году для повышения осведомленности о дикой фауне и флоре.",
    "events": ["Фотовыставки", "Конференции", "Акции в зоопарках"],
    "wikipedia_url": "https://ru.wikipedia.org/wiki/Всемирный_день_дикой_природы"
  },
  {
    "name": "Международный день лесов",
    "day": 21, "month": 2, "type": "eco", "region": "world",
    "description": "Учрежден ООН для привлечения внимания к важности лесов.",
    "events": ["Посадка деревьев", "Эко-уроки", "Сбор макулатуры"],
    "wikipedia_url": "https://ru.wikipedia.org/wiki/Международный_день_лесов"
  },
  {
    "name": "Всемирный день водных ресурсов",
    "day": 22, "month": 2, "type": "eco", "region": "world",
    "description": "Установлен ООН в 1993 году. Посвящен важности пресной воды.",
    "events": ["Очистка водоемов", "Конференции", "Эко-акции"],
    "wikipedia_url": "https://ru.wikipedia.org/wiki/Всемирный_день_водных_ресурсов"
  },
  {
    "name": "Час Земли",
    "day": 28, "month": 2, "type": "eco", "region": "world",
    "description": "Ежегодная акция WWF. Люди выключают свет на 1 час.",
    "events": ["Отключение света", "Свечные вечера", "Эко-флешмобы"],
    "wikipedia_url": "https://ru.wikipedia.org/wiki/Час_Земли"
  },
  {
    "name": "Международный день птиц",
    "day": 1, "month": 3, "type": "eco", "region": "world",
    "description": "Отмечается с 1906 года. Приурочен к возвращению перелетных птиц.",
    "events": ["Развешивание скворечников", "Наблюдение за птицами"],
    "wikipedia_url": "https://ru.wikipedia.org/wiki/Международный_день_птиц"
  },
  {
    "name": "День экологических знаний",
    "day": 15, "month": 3, "type": "eco", "region": "russia",
    "description": "Отмечается в России с 1996 года. Просвещение в области экологии.",
    "events": ["Эко-уроки", "Конференции", "Выставки"],
    "wikipedia_url": ""
  },
  {
    "name": "День Земли",
    "day": 22, "month": 3, "type": "eco", "region": "world",
    "description": "Крупнейшая экологическая акция в мире. Проводится с 1970 года.",
    "events": ["Посадка деревьев", "Уборка мусора", "Эко-марши"],
    "wikipedia_url": "https://ru.wikipedia.org/wiki/День_Земли"
  },
  {
    "name": "День заповедников и национальных парков России",
    "day": 11, "month": 0, "type": "eco", "region": "russia",
    "description": "В этот день в 1917 году создан первый Баргузинский заповедник.",
    "events": ["Экскурсии", "Лекции", "Фотовыставки"],
    "wikipedia_url": "https://ru.wikipedia.org/wiki/День_заповедников_и_национальных_парков"
  },
  {
    "name": "Всемирный день окружающей среды",
    "day": 5, "month": 5, "type": "eco", "region": "world",
    "description": "Главный праздник ООН по экологии. Отмечается с 1973 года.",
    "events": ["Эко-форумы", "Выставки", "Акции по переработке"],
    "wikipedia_url": "https://ru.wikipedia.org/wiki/Всемирный_день_окружающей_среды"
  },
  {
    "name": "Всемирный день океанов",
    "day": 8, "month": 5, "type": "eco", "region": "world",
    "description": "Установлен ООН. Привлекает внимание к проблемам загрязнения океанов.",
    "events": ["Очистка пляжей", "Конференции", "Показы фильмов"],
    "wikipedia_url": "https://ru.wikipedia.org/wiki/Всемирный_день_океанов"
  },
  {
    "name": "День эколога в России",
    "day": 5, "month": 5, "type": "eco", "region": "russia",
    "description": "Профессиональный праздник экологов РФ. Отмечается с 2007 года.",
    "events": ["Награждения", "Конференции", "Эко-акции"],
    "wikipedia_url": "https://ru.wikipedia.org/wiki/День_эколога"
  },
  {
    "name": "Всемирный день борьбы с опустыниванием",
    "day": 17, "month": 5, "type": "eco", "region": "world",
    "description": "Установлен ООН в 1994 году. Борьба с деградацией земель.",
    "events": ["Лекции", "Посадка растений", "Семинары"],
    "wikipedia_url": "https://ru.wikipedia.org/wiki/Всемирный_день_борьбы_с_опустыниванием_и_засухой"
  },
  {
    "name": "Международный день Матери-Земли",
    "day": 22, "month": 3, "type": "eco", "region": "world",
    "description": "Принят ООН в 2009 году. Гармония с природой и планетой.",
    "events": ["Фестиваль", "Эко-ярмарка", "Просмотр фильмов"],
    "wikipedia_url": ""
  },
  {
    "name": "День без автомобиля",
    "day": 22, "month": 8, "type": "eco", "region": "world",
    "description": "Международная акция отказа от автомобилей на один день.",
    "events": ["Вело-парады", "Бесплатный транспорт", "Эко-квесты"],
    "wikipedia_url": "https://ru.wikipedia.org/wiki/Всемирный_день_без_автомобиля"
  },
  {
    "name": "День Волги",
    "day": 20, "month": 4, "type": "eco", "region": "russia",
    "description": "Праздник великой русской реки. Очистка берегов и просвещение.",
    "events": ["Уборка берегов", "Концерты", "Речные регаты"],
    "wikipedia_url": "https://ru.wikipedia.org/wiki/День_Волги"
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