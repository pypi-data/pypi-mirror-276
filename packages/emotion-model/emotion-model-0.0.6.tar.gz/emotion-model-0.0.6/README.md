# Emotion model

## Установка библиотеки

Чтобы установить библиотеку, выполните:

```
pip install emotion-model
```

После этого сделайте вызов функции на вашем изображении, чтобы получить предсказание:

```
from emotion_model.predict import make_prediction

result = make_prediction(<Путь к вашему изображению>)

print(result)
```
