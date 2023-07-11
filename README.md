# InteriorClassifier

Для записи данных использовался плагин [**NVIDIA Deep learning Dataset Synthesizer (NDDS)**](https://github.com/NVIDIA/Dataset_Synthesizer) и бесплатные ассеты из Unreal Engine Marketplace. Итоговый датасет и проект UE4.27 (папка `DatasetGenerator`)  находится на [**Яндекс.Диск**](https://disk.yandex.ru/d/TMaafYNDpiERKw)

*Все скрипты рассчитаны на запуск из корня проекта.*

`dataset_converter.py` используется для первичной конвертации полученного датасета в COCO-формат.

Дообучение модели происходит в файле `src\train.py`, проверка - в файле `src\predict.py`.

Обученная модель не заливается на гит из-за размера, выложена отдельно на [ЯндексДиск](https://disk.yandex.ru/d/kAoF2yFe7D6Xpw)
