# TurboWarpScratch-with-MediaPipe

Проєкт для інтеграції розпізнавання пози людини (MediaPipe Pose) зі середовищем **TurboWarp / Scratch** через WebSocket.

Python-сервер отримує відеопотік з вебкамери, визначає 33 опорні точки скелета за допомогою MediaPipe та транслює їхні координати у форматі JSON в режимі реального часу до проєкту Scratch/TurboWarp.

## Структура проєкту

- `webserver.py` — WebSocket-сервер (`ws://localhost:8765`), що передає координати точок тіла в TurboWarp.
- `skeleton.py` — автономний скрипт для локального тестування захоплення камери та візуалізації скелета у вікні OpenCV.
- `TurboWarpApplications/MediaPipe.sb3` — готовий проєкт для Scratch / TurboWarp.
- `requirements.txt` — перелік необхідних Python-бібліотек.

## Встановлення

1. (Рекомендовано) Створіть та активуйте віртуальне середовище Python:
   ```bash
   python -m venv venv
   # Для Windows:
   venv\Scripts\activate
   # Для Linux / macOS:
   source venv/bin/activate
   ```
2. Встановіть необхідні залежності:
   ```bash
   pip install -r requirements.txt
   ```

## Запуск та використання (Usage)

1. **Локальне тестування камери та розпізнавання:**
   ```bash
   python skeleton.py
   ```
   *(Для виходу з вікна перегляду натисніть клавішу `q`)*

2. **Запуск WebSocket-сервера:**
   ```bash
   python webserver.py
   ```
   Сервер запуститься за адресою `ws://localhost:8765`.

3. **Запуск TurboWarp:**
   - Відкрийте [TurboWarp](https://turbowarp.org/) (або десктопний застосунок).
   - Завантажте проєкт `TurboWarpApplications/MediaPipe.sb3`.
   - Запустіть проєкт для отримання координат та взаємодії зі спрайтами.

