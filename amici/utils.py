import logging
import pandas
import datetime

from django.conf import settings


logger = logging.getLogger(__name__)


def export_to_xlsx(queryset):

    date = queryset.first().date

    date_str = date.strftime('%m-%d-%Y')
    filename = f'Advent Friends List {date_str}.xlsx'
    full_filepath = f'{settings.OUTPUT_DIR}/{filename}'

    data = []
    for item in queryset.all():
        data.append((
            item.giver.display_fullname,
            item.recipient.display_fullname,
        ))

    df = pandas.DataFrame.from_records(
        data,
        columns=(
            'Giver',
            'Recipient',
        ),
    )

    df.to_excel(
        full_filepath,
        index=False,
        encoding='utf-8',
    )

    logger.info(f'ouput file written to: {full_filepath}')

    return full_filepath


def get_email_context(
    recipient_name,
    sender_name=settings.DEFAULT_FROM_EMAIL_NAME,
    notification=1,
    year=datetime.datetime.now(),
    opt_out_urlname='preview',
):

    if notification == 1:
        content = """
            Advent is just around the corner, and we'll be drawing
            names in just a few days! If you don't wish to
            participate, follow the instructions below.
            Otherwise on November 11th I will email you your
            secret name!
        """
    elif notification == 2:
        content = """
            Just a reminder that we'll be drawing names tomorrow, so
            if you don't want to participate, be sure to follow the
            instructions below.
        """

    context = {
        'recipient_name': recipient_name,
        'content': content,
        'opt_out_url': f'{settings.SITE_URL}amici/opt-out/{opt_out_urlname}/',
        'notification': notification,
        'year': year,
        'sender_name': sender_name,
    }
    return context