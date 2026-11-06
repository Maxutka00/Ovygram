# Сборка Ovygram для Windows x64

Этот документ описывает подготовку будущей сборки. Новая версия SDK 2 пока
не скомпилирована и не проверена в готовом клиенте.

## Инструменты и зависимости

Точные инструменты upstream перечислены в [building-win.md](building-win.md).
Используются Visual Studio 2026, MSVC 14.44 и Windows SDK 10.0.26100.0.
Все подмодули берутся по закреплённым Git-коммитам. Перед подготовкой
зависимостей требуется рекурсивная инициализация подмодулей.

Структура рабочей папки:

```text
D:\TBuild\
    tdesktop\         исходники Ovygram
    ThirdParty\       инструменты upstream
    win64\Libraries\ зависимости Windows x64
    plugin-python\    отдельный комплект CPython и pybind11
    python-downloads\ скачанные архивы Python
```

В терминале с окружением MSVC x64 подготовь зависимости через оригинальный
`Telegram\build\prepare\win.bat`. Для согласованной конфигурации Release
и компактных кэшей используй этапы `tools/ovygram/baseline.py`, которые
задействованы в workflow. Одного готового Ovygram.exe для пересборки недостаточно.

## Встроенный Python

Из `D:\TBuild\tdesktop` подготовь комплект:

```powershell
python tools/ovygram/python_bundle.py --root D:/TBuild/plugin-python --downloads D:/TBuild/python-downloads --sdk Telegram/PluginSDK
```

Скрипт проверяет SHA-256 архивов CPython 3.13.16 и pybind11 3.0.2.
Самостоятельно установленный Python используется как инструмент подготовки;
пользователям portable-клиента он не требуется.

## Конфигурация и компиляция

Из корня исходников, после подготовки совместимых Release-зависимостей:

```powershell
python Telegram/configure.py -G "Ninja Multi-Config" -D CMAKE_CONFIGURATION_TYPES=Release -D OVYGRAM_PYTHON_ROOT=D:/TBuild/plugin-python -D DESKTOP_APP_DISABLE_AUTOUPDATE=ON -D DESKTOP_APP_DISABLE_CRASH_REPORTS=ON -D TDESKTOP_API_ID=YOUR_API_ID -D TDESKTOP_API_HASH=YOUR_API_HASH
cmake --build out --config Release --target Telegram --parallel 2
```

`Telegram` остаётся техническим именем CMake-цели upstream. Результат для
Windows — `out/Release/Ovygram.exe` и соседний каталог `python`.
Число параллельных задач выбирай по доступной памяти. Это пример команды,
а не свидетельство успешной сборки.

Для тестовой сборки workflow использует `TDESKTOP_API_TEST=ON`; такие
credentials не предназначены для публичного выпуска собственного приложения.
Не добавляй реальные ключи или каталоги профиля в Git и публичные отчёты.

## GitHub Actions

Файл `.github/workflows/ovygram-windows.yml` запускается только вручную.
Режимы: `inspect`, `plugin-smoke`, `build` и `plugins`. Перед запуском нужно
проверить бесплатные ресурсы, разрешить Actions в настройках репозитория и
подтвердить `free_allowance_verified`. Одна попытка ограничена 345 минутами
скриптов и 360 минутами job — максимальной длительностью job на стандартном
GitHub-hosted runner. Оставшиеся 15 минут нужны для остановки процессов,
отчёта и загрузки артефактов. Платные runners не настроены; увеличение времени
попытки не увеличивает бесплатные квоты аккаунта.

Для режима `plugins` оставляй `require_dependency_cache=true`: при отсутствии
совместимого Release-кэша workflow остановится до подготовки соответствующей
группы зависимостей. Debug-кэш не заменяет готовые Release-зависимости.
Подготовка всех зависимостей с нуля и компиляция клиента могут вместе превысить
345 минут, даже если компилятор не сообщает ошибок.

Если попытка дошла до компиляции клиента и остановилась с
`Build time allowance exhausted`, проверь успешное сохранение кэшей `foundation`,
`qt` и `extras`. Затем запусти новый `plugins` на той же ветке с
`require_dependency_cache=true` и подтверждённым `free_allowance_verified`.
Кэши отдельной ветки недоступны другой рабочей ветке; используй ветку, на которой
они сохранены. Клиент компилируется заново, его объектные файлы не кэшируются.

Отключать `require_dependency_cache` следует только для отдельной попытки
подготовки отсутствующих кэшей после проверки бесплатных ресурсов. Лимит времени
при этом сохраняется; такая попытка может успеть сохранить зависимости, но не
собрать клиент. При смене toolchain или рецептов старые кэши могут не подойти.

Режим `plugins` собирает Ovygram, а `build` — неизменённую закреплённую основу
Telegram. Имена будущих пакетов: `ovygram-7.3.5-win64-release.zip` и
`upstream-baseline-7.3.5-win64-debug.zip` соответственно. Реального нового
ZIP сейчас нет; история прежних личных сборок в этот репозиторий не переносится.
