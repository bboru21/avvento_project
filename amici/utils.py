import logging

import pandas

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