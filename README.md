# Amici dell'Avvento

An app for generating an Advent Frield (Secret Santa) list and sending e-mail notifications.

Create App: `python manage.py startapp amici_dell_avvento`
Make Migrations: `python manage.py makemigrations amici_dell_avvento`
SQL Migrate: `python manage.py sqlmigrate amici_dell_avvento 0001`

Run Command: `python manage.py send_advent_notification 1 --settings=website.config.local`
Run Command: `python manage.py send_advent_notification 2 --settings=website.config.local`
Run Command: `python manage.py generate_advent_friends_list --settings=website.config.local`

Setup task to send reminders on November 8th, November 10th and finally run the process on November 11, the Feast of St. Martin of Tours.