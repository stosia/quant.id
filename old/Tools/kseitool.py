#############################################################################
# Quant.id System                                                           #
# Copyright (C)2017 PT. Stosia Teknologi Investasi                          #
#                                                                           #
# This file is licensed under  GNU GPL (General Public License) version 3.  #
#                                                                           #
# File ini dilisensikan kepada Anda, bukan  Anda miliki.  Pemilik file ini  #
# adalah pemegang  hak cipta ("copyright holder") di atas. Gunakanlah file  #
# ini sesuai dengan lisensi yang telah ditetapkan untuk file ini.           #
#                                                                           #
# File ini  berlisensi  GNU GPL (General Public License)  versi 3. Artinya  #
# kalau Anda  memodifikasi file ini, atau membuat karya lain yang berbasis  #
# file ini  ("derivative work"),  maka Anda  wajib  mendistribusikan  kode  #
# modifikasi atau karya tersebut kepada publik. Hal ini untuk menjaga agar  #
# pengetahuan yang ada di sini menjadi lebih berkembang  di masa mendatang  #
# untuk kemajuan kita bersama.                                              #
#                                                                           #
# Silakan memakai kode ini untuk kepentingan apapun termasuk untuk mencari  #
# profit di pasar saham baik secara perorangan atau organisasi, asal tidak  #
# jahat. Sebagai tambahan permintaan, kami menghimbau untuk TIDAK  menjual  #
# kode/file  ini secara  apa adanya  atau dalam bundel  produk yang dijual  #
# secara komersial, karena hal itu tidak etis.                              #
#                                                                           #
# Untuk penjelasan lebih lanjut silakan bertanya kepada kami.  Untuk detil  #
# lisensi GPLv3  silakan lihat file GPLv3-LICENSE.md  yang didistribusikan  #
# bersama file ini.                                                         #
#                                                                           #
# Author: Benny Prijono <benny@stosia.com>                                  #
# Contributors:                                                             #
#  -                                                                        #
#############################################################################
import glob
import sys

import pandas as pd


def print_header():
    sys.stderr.write("%-13s %-20s  Local (B)   Frgn (B)\tLocal%%\t Frgn%%\n" % ("  Date", "Type"))
    sys.stderr.write('-' * 78 + '\n')

def print_info(title, df):
    B = 1000000000.0
    local_cap = df['Local'].sum() / B
    foreign_cap = df['Foreign'].sum() / B
    total = df['Total'].sum() / B
    if abs(local_cap + foreign_cap - total) > total * 0.01:
        print('Warning: differ')
    if total:
        local = local_cap * 100 / total
        foreign = foreign_cap * 100 / total
    else:
        local = foreign = 0
    print("%-13s %-20s %10.0f %10.0f \t%6.1f\t%6.1f" % (df.iloc[0, 0], title[:20], local_cap, foreign_cap, local, foreign))


def process_file(csv):
    df = pd.read_csv(csv, sep='|', engine='python')
    df.loc[ pd.isnull(df['Current Amt']), 'Current Amt'] = df['Num. of Sec'] * df['Closing Price']

    df['Foreign'] = df['Current Amt'] * df['Foreign (%)'] / 100
    df['Local'] = df['Current Amt'] * df['Local (%)'] / 100
    df['Total'] = df['Current Amt'] * df['Total (%)'] / 100

    types = df['Type'].unique()
    for type in types:
        grp = df.loc[ df['Type'] == type ]
        print_info(type, grp)
    print_info('TOTAL', df)


def usage():
    print("""KSEI Tool - (C)2018 PT. Stosia Teknologi Investasi
Parse and display KSEI Master File Efek

Instructions:
 1. Download and unzip master efek files from http://www.ksei.co.id/archive_download/master_securities
 2. Give the filename as the argument:
       python3 kseitool.py StatisEfek20180131.txt
 3. You may give more than one files and/or wildcards to process more than one file:
       python3 kseitool.py 2017/*.txt 2017/*.txt
""")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        usage()
        sys.exit(0)

    files = []
    for arg in sys.argv[1:]:
        files.extend(glob.glob(arg))
    print_header()
    for file in sorted(files):
        process_file(file)
