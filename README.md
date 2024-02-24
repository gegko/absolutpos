запуск:

```
git clone https://github.com/gegko/absolutpos.git
cd absolutpos/
mv env .env
```

А ТАКЖЕ

```
docker cp backup.sql absolutpos:.
docker exec absolutpos psql -U absolutpos < backup.sql
```
(чтобы закинуть тестовые данные. P.S. возможно придётся psql'нуть два раза и перекомпоузить)

======================================================

Переключение между режимами админка / анкетка происходит по клику на лого.
