
# Библиотека, предоставляющая доступ к постгрес бд
import psycopg2

# Создание коннекшона по нужным координатам
con = psycopg2.connect(
  database="d346he5v2rbj5e",
  user="yjsaechrwvutfp",
  password="8887db18cd4323b6dd6ec4abe48d7e1a97ac00e6c37d25b63427fcbdcae10cdf",
  host="ec2-54-75-229-28.eu-west-1.compute.amazonaws.com",
  port="5432"
)

# Создание курсора, он отвечает за исполнение запросов
cursor = con.cursor();

cursor.execute("insert into student values ("
               "1, 'Ha', 'Loh', '09-821', '+13372281488', 'joppa@mail.ru');");

cursor.execute('select * from studentstest');  # Теперь в курсоре находится дата по запросу
records = cursor.fetchall();  # fetchall(); возвращает все полученные строки

# Коммит, чтобы сохранить изменения в базу. Иначе ничего не сохранится, но дату получить можно
con.commit();

print(records);
