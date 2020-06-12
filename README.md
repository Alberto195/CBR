КАК УСТАНОВИТЬ БАЗУ ДАННЫХ НА ВАШ КОМПЬЮТЕР

1  Откройте MySQL Workbench, если у вас нет данного приложения, скачайте его с сайта https://dev.mysql.com/downloads/workbench/
2  Нажмите на Import Data
3  Нажмите на кнопку рядом с которой текст Import from Dump Profect Folder и укажите в поле для текста путь к папке all_in_one/dread, которое у вас в проекте в папке Data
3.1 Нажмите на Load Folder Contents
3.2 В Deault Target Schema нажмите на "New..." и создайте all_in_one
4  Нажмите на кнопку Start Import
5  Загрузка началась, подождите минут 20-30, в зависимости от "начинки" вашего ПК, может установить быстрее
6  Загрузите нужные библиотеки в IDE pip install -r requirements.txt
6.1 Если не получилось запустить pip install -r requirements.txt, то пропишите отдельно для каждой библиотеки pip install и по порядку из списка
7 Запустите main.py





