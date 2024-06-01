# Face Genius

Демонстрационный проект для распознавания лиц
с помощью библиотеки `face_recognition`.


## Использование

Примеры использования находятся директории `examples`:
- `enroll_faces.py` - для обучения на лицах
- `recognize_faces.py` - для распознавания лиц


## Загрузка проекта на PyPI

Команды для загрузки проекта на PyPI:
```sh
python setup.py sdist bdist_wheel
twine upload dist/*
```


## Установка пакета в дальнейшем

```sh
pip install face_genius
```
