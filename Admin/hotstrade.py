#############################################################################
# Quant.id System  -  https://quant.id                                      #
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
from __future__ import absolute_import, print_function, division, unicode_literals

import csv
import sys

__author__ = 'Benny Prijono <benny@stosia.com>'
__copyright__ = "Copyright (C)2017 PT. Stosia Teknologi Investasi"

LOT = 100


def show_hots_trade(filename):
    class Trade:
        BUY = 0
        SELL = 1
        def __init__(self, code, op, shares, price):
            self.code = code.replace('"', '')
            self.op = int(op.replace('"', ''))
            self.shares = int(shares.replace(",", "").replace('"', ''))
            self.price = float(price.replace(",", "").replace('"', ''))
            self.value = self.shares * self.price
            if self.op == self.SELL:
                self.shares = 0 - self.shares
                self.value = 0 - self.value

        def merge(self, trade):
            assert self.code == trade.code
            self.shares += trade.shares
            self.value += trade.value
            if self.shares:
                self.price = self.value / self.shares
            else:
                self.price = 0

    trades = {}
    with open(filename) as f:
        reader = csv.reader(f, delimiter=str(','), quotechar=str('"'))
        reader.next()
        for row in reader:
            t = Trade(row[3], row[4], row[6], row[7])
            old_t = trades.get(t.code, None)
            if old_t:
                t.merge(old_t)
            trades[t.code] = t

    print("Code\t    Lot\t  Price\tValue(jt)")
    codes = trades.keys()
    codes.sort()
    for code in codes:
        trade = trades[code]
        print("%s\t%7d\t%7.1f\t%7.1f" % (trade.code, trade.shares / LOT, trade.price, trade.value / 1000000.0))


if __name__ == "__main__":
    show_hots_trade(sys.argv[1])
