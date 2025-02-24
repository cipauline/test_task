## Основные файлы проекта

- ``scripts/main.py`` - файл с извлечением данных из API и заливкой их в clickhouse
- ``clickhouse_sql/click.sql`` - файл с созданием базы данных и таблиц (raw_data, people), а также mv
- ``astro_project`` - папка dbt проекта с моделями в models


## Алгоритм действий

1. создаем ``docker-compose.yml`` c clickhouse (указываем :latest чтобы получить последнюю версию) и поднимаем docker
2. подключаемся к контейнеру clickhouse в dbeaver
3. создаем базу данных astro и там создаем таблицу raw_data для сырых данных из json-файла. raw_data на движке ReplacingMergeTree и настраиваем так, чтобы в таблице сохранялась только последняя добавленная запись, чтобы избежать дубликатов данных в таблице при повторных выполнениях запроса
4. далее создаем таблицу people, в которую пойдут данные mv. движок ReplacingMergeTree с order by (craft, name). так, мы избежим дубликатов если в raw_data появятся данные и окажутся точно такими же как и ранее
6. создаем mv, где парсим данные из raw_data с помощью табличных функций clickhouse
7. пишем программу для извлечения данных из api (где обрабатываются ошибки которые могут возникнуть и exponential backoff retry обеспечивается с помощью декоратора), заливки данных в clickhouse
8. запускаем программу. данные и в таблице raw_data, и в таблице people
<img width="722" alt="Снимок экрана 2025-02-24 в 04 44 48" src="https://github.com/user-attachments/assets/cecc5707-3a25-4feb-a57a-ca0ef35b5cdb" />

<img width="446" alt="Снимок экрана 2025-02-24 в 04 45 35" src="https://github.com/user-attachments/assets/d92fb8ea-73ea-47ec-9abe-31a8d945fb44" />

9. создаем dbt проект с помощью ``dbt init astro_project``
10. настраиваем ``profiles.yml``
11. проверяем подключение с помощью ``dbt debug``
12. создаем две модели - people_per_craft (количество людей на каждом косм. аппарате) и people_summary (общее колво людей). настраиваем их как таблицы
13. ``dbt run`` и получаем таблицы в нашей базе данных
<img width="172" alt="Снимок экрана 2025-02-24 в 04 51 38" src="https://github.com/user-attachments/assets/73b3b668-cf6f-43ca-a5b3-7d38fcfa64cc" />

<img width="312" alt="Снимок экрана 2025-02-24 в 04 52 19" src="https://github.com/user-attachments/assets/39be3396-2e1c-4572-8710-14d17f3b7b3d" />
<img width="213" alt="Снимок экрана 2025-02-24 в 04 52 07" src="https://github.com/user-attachments/assets/1971b87d-aee3-439f-9b98-beee48617c98" />
