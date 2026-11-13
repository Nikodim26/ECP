import os
from datetime import date
from pathlib import Path

from OpenSSL import crypto


def definition_limit_certificate(certificate) -> date:
    """Определяет срок действия сертификата"""

    certificate = str(certificate)
    with open(certificate, 'rb') as file: cert_data = file.read()

    not_after_str = crypto.load_certificate(crypto.FILETYPE_ASN1, cert_data).get_notAfter().decode('utf-8')
    expiry_date = crypto.datetime.datetime.strptime(not_after_str, '%Y%m%d%H%M%SZ')

    return expiry_date.date()


def renaming_folder(name, path_dir, name_folder):
    entries = os.listdir(path_dir)

    for entry in entries:
        if name_folder == entry:
            path = Path(path_dir/entry)
            path.rename(path.with_name(name))


def end(number):
    if 10 <= number % 100 <= 14:
        return 'ов'
    else:
        last_digit = number % 10
        if last_digit == 1:
            return ''
        elif last_digit in (2, 3, 4):
            return 'a'
        else:
            return 'ов'


def get_name_folder(certificate):
    with open(certificate, 'rb') as file:
        cert_data = file.read()
    try:
        cert_subject = crypto.load_certificate(crypto.FILETYPE_ASN1, cert_data).get_subject()
        subject_dict = {k.decode('utf-8'): v.decode('utf-8') for k, v in cert_subject.get_components()}
        last_name = subject_dict.get('SN')

        if last_name:
            io = subject_dict.get('GN').split(' ')
            title = subject_dict.get('title')

            io_print = ''
            for i in io:
                io_print = io_print + i[0] + '.'
            if len(subject_dict.get('CN').split(' '))<=3:
                return f'{last_name} {io_print}    ({title})'
            else:
                return 'обезличенная'
        else:
            return 'обезличенная вааще'


    except Exception:
        return False




