from datetime import date
from pathlib import Path
from functions import definition_limit_certificate, renaming_folder, end, get_name_folder
import sys


exe_path = Path(sys.executable)
path_dir = exe_path.parent.parent
# path_dir = Path(r'D:\KVRT\ECP_reserve\Действующие')

root = Path(path_dir).resolve()
with open(path_dir / "control" / "installations.config", 'r') as file:
    content = int(file.read())

printable_records = []
Lmax = counter = 0

for cer_file in root.rglob("*.cer"):

    name = get_name_folder(cer_file)
    validity_period = definition_limit_certificate(cer_file)
    name_folder = f'{name[0].lower()}  [{validity_period.strftime('%d.%m.%Y')}]  {name}'
    day_difference = (validity_period - date.today()).days

    if len(name_folder) > Lmax: Lmax = len(name_folder)

    renaming_folder(name_folder, path_dir, cer_file.parts[4])

    if day_difference <= content:
        printable_records.append(
            {'doctor': name_folder,
             'validity_period': validity_period,
             'day_difference': day_difference,
             })

    counter += 1

printable_records = sorted(printable_records, key=lambda x: x['validity_period'])

if not printable_records:
    print(f'ЭЦП с истекающим сроком менее {content} дней нет нихрена')
else:
    for record in printable_records:
        print(f'{record['doctor'].ljust(Lmax - 15, ' ')} - срок действия сертификата'
              f' {record['validity_period'].strftime('%d.%m.%Y')}\t- осталось {record['day_difference']} дней')

    l1 = len(printable_records)

    print(f'\nНайдено {l1} сертификат{end(l1)} с истекающим сроком действия. Всего на учете {Lmax} сертификат{end(Lmax)}.')
input()
