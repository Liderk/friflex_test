# friflex_test

### Задание:
Разработать API, позволяющий пользователям получить доступ к материалам (pdf-файлам, текстовым описаниям, ссылки) 
по курсам на которые они записаны. Возможность записи на курс, оценка курса должно быть реализованы. 
Административная часть должна содержать возможности по созданию и редактированию курсов 
(в том числе и список материалов), пользователей. На страницу с материалами пользователь попадает 
только после успешной авторизации.

Python 3.7+
Django 3+
DRF
PgSQL\SQLite

## Для запуска проекта:
- Создать файл `.env` на примере `.env.example.`;
- Из папки с `docker-compose.yaml` выполнить команду - `sudo docker-compose up -d --build`;
- Для создания суперпользователя, выполните в командной строке:
```  
sudo docker exec -it friflex_test_web_1 sh
```
Далее создайте суперпользователя:
``` 
python manage.py createsuperuser
``` 

## Основные Ендпоинты для API:

### Пользователи:
- регистрация нового пользователя:

   POST-запрос на 
`http://127.0.0.1:8080/api/v1/auth/users/`
передав их в полях username и password:
`
{
    'username': 'newuser',
    'password': 'changeme!1'
}`

- Получение токена отправляем запрос с 
`http://127.0.0.1:8080/api/v1/auth/jwt/create/`
передав действующий логин и пароль в полях username и password
- Получение всех материалов по курсу: GET запрос

`http://127.0.0.1:8080/api/v1/courses/materials/<course_id>`

### Подписки:
- `api_v1/courses/subscribe/` [GET] - получить все подписи текущего пользователя

- `api_v1/courses/subscribe/` [POST] - подписаться на курс передав номер курса в теле запроса
        `{id: course_id,}`

- `api_v1/courses/subscribe/` [DELETE] - отписаться от курса

### Оценка курса
- `api_v1/courses/{course_id}/score/` [POST] - создать оценку для курса, передав в теле запроса
    `{score: int(1-10);}`

### Информация по курсу
- `api_v1/courses/` [GET] : возвращает информацию о всех курсах, на которые подписан студент

- `api_v1/courses/{id}/` [GET] : возвращает информацию о курсе по-указанному id,
    если человек подписан на него
