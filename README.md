## API для предсказания токсичности постов и наличия в них мата в Telegram

Используемые признаки:
- message: string

Формат ответа:
```
{'toxic': результат проверки на токсичность (допустимые значения: toxic, non_toxic, error), 
 'obscene': результата проверки на мат (допустимые значения: obscene, non_obscene, error)}
 ```
Логи в файле clf_API_logs.log

### Клонируем репозиторий и создаем образ
```
$ git clone https://github.com/zhukovnikolay/media_model.git
$ cd media_model
$ docker build -t media_api .
```

### Запускаем контейнер

```
$ docker run -t -d -p 8000:8000 --name <your_container_name> media_api
```

### Смотрим документацию: http://localhost:8000/docs
