# Amici dell'Avvento

An app for generating an Advent Frield (Secret Santa) list and sending e-mail notifications.

Run Command Example: 
```
    python avvento/manage.py send_advent_notification --notification 1 --settings=avvento.settings.production
```

Run Command Example: 
```
    python avvento/manage.py send_advent_notification --notification 2 --settings=avvento.settings.production
```

Run Command Example: 
```
    python avvento/manage.py generate_advent_friends_list --settings=avvento.settings.production
```
Note: This script will throw an `InvalidFriendListException` exception if an invalid list is generated, upon which it will begin to retry up to three times.
To adjust this behavior, update the `MAX_GENERATE_LIST_RETRIES` setting.

Run Command Examples:
```
    python avvento/manage.py send_advent_friends_email --settings=avvento.settings.production --cap 40 --test
    python avvento/manage.py send_advent_friends_email --settings=avvento.settings.production --cap 40
```

## Testing
If you wish to test the script without database writes or e-mail, run:

```
    python avvento/manage.py generate_advent_friends_list --settings=avvento.settings.production --test
    python avvento/manage.py send_advent_friends_email --settings=avvento.settings.production --test
```

Setup task to send reminders on November 8th, November 10th and finally run the process on November 11, the Feast of St. Martin of Tours.