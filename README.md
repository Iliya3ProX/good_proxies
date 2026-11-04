# good_proxies
Public verified MTProto proxies and plugins for Telegram / exteraGram.

## Плагины

### 1. [good_proxy.plugin](good_proxy.plugin) (v2.0.0)
Основной плагин для работы с прокси:
- Автоматический сбор и обновление пула MTProto-прокси из репозиториев GitHub и GitVerse.
- Автоматическое скрытие спонсорских каналов на сетевом уровне (`checkPromoInfo`).
- Нативная фоновая MTProto-проверка и удаление нерабочих/медленных узлов.
- Экспорт рабочего пула в буфер обмена.

### 2. [good_proxy_speed.plugin](good_proxy_speed.plugin) (v1.0.0)
Плагин для измерения скорости:
- Одиночный замер скорости текущего активного прокси через Telegram MTProto API.
- Пакетный замер скорости по списку серверов.
- Технология **TCP Window Warmup**: отбрасывание стартового чанка для раскрытия окна TCP без влияния задержки RTT.
- Автоматическая генерация тестового файла (`speed_test_asset`) нужного размера (2, 5, 10 МБ) в «Избранное».
- Запись замеренной скорости прямо в имя прокси.

## Каталог плагинов exteraGram

Репозиторий подключается как источник плагинов прямо из каталога exteraGram:

1. exteraGram → **Настройки → Plugins → Каталог → Репозитории → Добавить → Git Repository**
2. URL: `https://github.com/Iliya3ProX/good_proxies`
3. Или по ссылке: https://t.me/exteraPluginRepo?git=https%3A%2F%2Fgithub.com%2FIliya3ProX%2Fgood_proxies

Манифест: [extera-plugins.json](extera-plugins.json) (schema 1) — генерируется автоматически
(`tools/build_extera_index.py` + GitHub Actions при каждом обновлении `.plugin`-файлов).
