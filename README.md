# Amici dell'Avvento

An app for generating an Advent Frield (Secret Santa) list and sending e-mail notifications.

Run Command: `python avvento/manage.py send_advent_notification --notification 1 --settings=avvento.settings.production`
Run Command: `python avvento/manage.py send_advent_notification --notification 2 --settings=avvento.settings.production`
Run Command: `python avvento/manage.py generate_advent_friends_list --settings=avvento.settings.production --send_email`

## Testing
If you wish to test the script without database writes or e-mail, run:

`python avvento/manage.py generate_advent_friends_list --settings=avvento.settings.production --test`


Setup task to send reminders on November 8th, November 10th and finally run the process on November 11, the Feast of St. Martin of Tours.