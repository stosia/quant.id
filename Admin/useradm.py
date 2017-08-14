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
from __future__ import absolute_import, print_function, division, unicode_literals

import datetime
import random
import re
import string
import sys
import time

from dateutil.relativedelta import relativedelta

import MySQLdb as my


# import threading
__author__ = 'Benny Prijono <benny@stosia.com>'
__copyright__ = "Copyright (C)2017 PT. Stosia Teknologi Investasi"

DBHOST = '\x64\x62\x2e\x71\x75\x61\x6e\x74\x2e\x69\x64'
TRACING_ENABLED = False


##################################################################################
class DbLock:
    def __init__(self, conn):
        # self.mutex = conn.mutex
        pass

    def __enter__(self):
        # self.mutex.acquire()
        return self

    def __exit__(self, typ, value, traceback):
        # self.mutex.release()
        pass


##################################################################################
class DbConnection:
    def __init__(self, user, passwd, db):
        # self.mutex = threading.RLock()
        self.conn_obj = my.connect(host=DBHOST, user=user, passwd=passwd, db=db)
        self.conn_obj.autocommit(True)
        self.inside_transaction = 0
        self.tracing_enabled = TRACING_ENABLED

    def __enter__(self):
        with DbLock(self):
            self.inside_transaction += 1
            return self

    def __exit__(self, typ, value, traceback):
        assert self.inside_transaction > 0
        with DbLock(self):
            self.inside_transaction -= 1
            # Only commit/rollback in the outmost context
            if self.inside_transaction:
                return
            if typ is not None:
                self.rollback()
            else:
                self.commit()

    def _trace_sql(self, status, sql, params, t):
        if self.tracing_enabled:
            sql = re.sub('[ \\t]{2,}', ' ', sql).replace('\n', '')
            sys.stderr.write('%s in %.3fs: sql="%s", params=%s\n' % (status, t, sql, str(params)))

    def commit(self):
        with DbLock(self):
            assert not self.inside_transaction
            self.conn_obj.commit()

    def rollback(self):
        with DbLock(self):
            assert not self.inside_transaction
            self.conn_obj.rollback()

    def close(self):
        with DbLock(self):
            assert not self.inside_transaction
            self.conn_obj.close()

    def _query(self, sql, params):
        cur = self.conn_obj.cursor(my.cursors.DictCursor)
        cur.execute(sql, params)
        return cur

    def query(self, sql, params=()):
        t0 = time.time()
        try:
            cur = self._query(sql, params)
            self._trace_sql('Query success', sql, params, time.time() - t0)
            return cur
        except:
            self._trace_sql('**Query error**', sql, params, time.time() - t0)
            raise

    def query_value(self, sql, field, default=None, params=()):
        cur = self.query(sql, params)
        row = cur.fetchone()
        return row[field] if row else default

    def _exec_sql(self, sql, params):
        cur = self.conn_obj.cursor()
        if not params:
            cur.execute(sql)
        else:
            cur.execute(sql, params)
        return cur

    def exec_sql(self, sql, params=()):
        t0 = time.time()
        try:
            cur = self._exec_sql(sql, params)
            self._trace_sql('Exec success', sql, params, time.time() - t0)
            return cur
        except:
            self._trace_sql('**Exec error**', sql, params, time.time() - t0)
            raise

    def exec_many(self, sql, params):
        t0 = time.time()
        try:
            cur = self.conn_obj.cursor()
            cur.executemany(sql, params)
            self._trace_sql('Exec_many success', sql, params, time.time() - t0)
            return cur
        except:
            self._trace_sql('**Exec_many error**', sql, params, time.time() - t0)
            raise


##################################################################################
class User:
    def __init__(self, dbc, user_id=None, row=None):
        self.dbc = dbc
        self.is_exists = False
        self.user_id = user_id
        self.email = None
        self.full_name = None
        self.reg_date = None
        self.cur_acc = None
        self.cur_acc_expiry = None
        self.renew_cnt = None
        if row:
            self._db_load(row)

    @staticmethod
    def db_lookup_by_user_id(dbc, user_id):
        sql = """SELECT * FROM user WHERE user_id = %s"""
        cur = dbc.query(sql, (user_id,))
        rows = cur.fetchall()
        return User(dbc, row=rows[0]) if rows else None

    @staticmethod
    def db_lookup_by_email(dbc, email):
        sql = """SELECT * FROM user WHERE email = %s"""
        cur = dbc.query(sql, (email,))
        rows = cur.fetchall()
        return User(dbc, row=rows[0]) if rows else None

    @staticmethod
    def db_get_expired_users(dbc, when=None):
        if not when:
            when = datetime.date.today()
        sql = """SELECT * FROM user 
                 WHERE cur_acc_expiry IS NOT NULL 
                   AND cur_acc_expiry < %s
                """
        cur = dbc.query(sql, (when,))
        return [User(dbc, row=row) for row in cur]

    @staticmethod
    def generate_user_id(full_name, length=5):
        full_name = full_name.lower()
        chars = "".join([c for c in full_name if c >= 'a' and c <= 'z'])
        while len(chars) < length:
            chars = chars + chars
        idxs = [0]
        while len(idxs) < length:
            idx = random.randint(1, len(chars) - 1)
            if idx not in idxs:
                idxs.append(idx)
        idxs.sort()
        return "".join([chars[idx] for idx in idxs])

    @staticmethod
    def generate_password():
        unallowed_chars = "O0o1l"
        chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
        for char in unallowed_chars:
            chars = chars.replace(char, '')
        plen = len(chars)
        passwd = [chars[random.randint(0, plen - 1)] for i in range(8)]
        return "".join(passwd)

    def _db_load(self, row):
        self.is_exists = True
        self.user_id = row['user_id']
        self.email = row['email']
        self.full_name = row['full_name']
        self.reg_date = row['reg_date']
        self.cur_acc = row['cur_acc']
        self.cur_acc_expiry = row['cur_acc_expiry']
        self.renew_cnt = row['renew_cnt']

    def has_account(self):
        return self.cur_acc is not None

    def is_expired(self):
        return self.cur_acc_expiry < datetime.date.today()

    def db_create(self):
        sql = """INSERT INTO user(user_id, email, full_name, reg_date, renew_cnt)
                 VALUES(%s, %s, %s, %s, %s)
                 """
        self.dbc.exec_sql(sql, (self.user_id, self.email, self.full_name, self.reg_date, self.renew_cnt))
        # self.dbc.commit()

    def db_add_account(self, months=3):
        assert not self.has_account()

        end_date = datetime.date.today()
        if months > 0:
            end_date = end_date + relativedelta(months=months)
        # Get to the end of the month
        end_date = end_date + relativedelta(day=31)

        acc = self.user_id + ("%02d%02d" % (end_date.year % 100, end_date.month))
        passwd = self.generate_password()

        user_created = False

        try:
            sql = """CREATE USER '%s' IDENTIFIED BY '%s'
                    """ % (acc, passwd)
            self.dbc.exec_sql(sql)
            user_created = True

            sql = """GRANT SELECT, EXECUTE ON quant_id.* TO '%s'
                    WITH    MAX_QUERIES_PER_HOUR 3600
                            MAX_UPDATES_PER_HOUR 1
                            MAX_CONNECTIONS_PER_HOUR 60
                            MAX_USER_CONNECTIONS 4
                """ % (acc,)
            self.dbc.exec_sql(sql)

            sql = """UPDATE user
                    SET cur_acc = %s, cur_acc_expiry = %s, renew_cnt = %s
                    WHERE user_id = %s
                """
            self.renew_cnt += 1
            self.dbc.exec_sql(sql, (acc, end_date, self.renew_cnt, self.user_id))

            # self.dbc.commit()
            self.cur_acc = acc
            self.cur_acc_expiry = end_date

            print("Account created for %s <%s>\nUser ID:  %s\nPassword: %s\nExpired:  %s\n" %
                  (self.full_name, self.email, acc, passwd, str(end_date)))

        except:
            if user_created:
                sys.stderr.write("There is an error. Dropping user %s\n" % (acc,))
                sql = """DROP USER '%s';""" % (acc,)
                self.dbc.exec_sql(sql)

            raise

    def db_del_account(self):
        assert self.has_account()

        print("Dropping %s..\n" % (self.cur_acc,))

        sql = """DROP USER '%s'""" % (self.cur_acc,)
        self.dbc.exec_sql(sql)

        sql = """UPDATE user
                SET cur_acc = NULL, cur_acc_expiry = NULL
                WHERE user_id = %s
            """
        self.dbc.exec_sql(sql, (self.user_id,))
        # self.dbc.commit()

        self.cur_acc = None
        self.cur_acc_expiry = None



def usage():
    print("Usage: ")
    print("        useradm [OPTIONS] CMD [parameters..] ")
    print("")
    print("Commands:")
    print("        add email full name     Add an account for new/existing user")
    print("        drop email/user_id      Drop the account")
    print("        warn [now]              Warn expired accounts next month/now")
    print("        clean                   Clean up expired accounts now")
    print("")
    print("Options:")
    print("        -u username             Admin username")
    print("        -p passwd               Admin password")


def normalize_email(email):
    return email.lower().strip()


def normalize_user_id(user_id):
    return user_id.lower().strip()


def add(dbc, args):
    """Usage:
    add email full name     Add an account for new/existing user
    """
    email = None
    names = []
    for i, arg in enumerate(args):
        if email is None and '@' in arg:
            email = arg.lower()
        else:
            names.append(arg)

    if not email:
        sys.stderr.write("Error: email is required\n")
        sys.exit(1)

    usr = User.db_lookup_by_email(dbc, email)
    if usr:
        if usr.has_account():
            td_to_expiry = usr.cur_acc_expiry - datetime.date.today()
            if td_to_expiry.days > 15:
                sys.stderr.write("Error: %s has valid account %s for the next %d days\n" %
                                 (email, usr.cur_acc, td_to_expiry.days))
                sys.exit(1)
            print("%s's active account %s will be dropped first" % (email, usr.cur_acc))
            usr.db_del_account()
    else:
        if not names:
            sys.stderr.write("Error: full name is required\n")
            sys.exit(1)
        full_name = " ".join(names)
        if len(full_name) < 5:
            sys.stderr.write("Error: Full name is too short\n")
            sys.exit(1)
        for i in range(10):
            user_id = User.generate_user_id(full_name)
            if not User.db_lookup_by_user_id(dbc, user_id):
                break
            user_id = None

        if not user_id:
            sys.stderr.write("Error: unable to generate user ID for full name '%s'\n" % (full_name))
            sys.exit(1)

        usr = User(dbc)
        usr.user_id = user_id
        usr.email = email
        usr.full_name = full_name
        usr.reg_date = datetime.date.today()
        usr.cur_acc = None
        usr.cur_acc_expiry = None
        usr.renew_cnt = 0

        usr.db_create()

    usr.db_add_account()


def drop(dbc, args):
    """Usage:
    drop email/user_id      Drop the account
    """
    if len(args) < 1:
        sys.stderr.write("Error: need email or user id\n")
        sys.exit(1)

    if '@' in args[0]:
        usr = User.db_lookup_by_email(dbc, normalize_email(args[0]))
    else:
        usr = User.db_lookup_by_user_id(dbc, normalize_user_id(args[0]))

    if not usr:
        sys.stderr.write("Error: lookup not found for email/user_id '%s'\n" % (args[0]))
        sys.exit(1)

    if not usr.has_account():
        print("User '%s' does not have account\n" % (args[0]))
        sys.exit(0)

    usr.db_del_account()


def warn(dbc, args):
    """Usage:
    warn [now]              Warn expired accounts next month/now
    """
    if len(args):
        if args[0] == "now":
            when = datetime.date.today()
        else:
            sys.stderr.write("Error: 'warn' command only takes 'now' as optional argument \n")
            sys.exit(1)
    else:
        when = datetime.date.today() + relativedelta(months=1)
        when = when.replace(day=1)

    expired_users = User.db_get_expired_users(dbc, when)
    if not expired_users:
        print("No expired users")
    else:
        print("%d user(s) will expire on %s" % (len(expired_users), str(when)))
        for u in expired_users:
            print("  %s <%s>" % (u.full_name, u.email))


def clean(dbc, args):
    """Usage:
    clean                   Clean up expired accounts now
    """
    if args:
        sys.stderr.write("Error: 'clean' does not need any arguments\n")
        sys.exit(1)

    when = datetime.date.today()
    expired_users = User.db_get_expired_users(dbc, when)

    if not expired_users:
        print("No expired users")
    else:
        print("Cleaning %d expired user(s)" % (len(expired_users)))
        for u in expired_users:
            print("  %s <%s>" % (u.full_name, u.email))
            u.db_del_account()


if __name__ == "__main__":
    db_user = ""
    db_passwd = ""
    cmd = ""
    cmd_args = []

    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "-u":
            db_user = sys.argv[i + 1]
            i += 1
        elif sys.argv[i] == "-p":
            db_passwd = sys.argv[i + 1]
            i += 1
        elif not cmd:
            cmd = sys.argv[i]
        else:
            cmd_args.append(sys.argv[i].strip())
        i += 1

    if cmd in ["-h", "--help", "/?", "?"]:
        usage()
        sys.exit(0)

    if not cmd:
        print("Error: command is required")
        sys.exit(1)
    elif not db_user:
        print("Error: user is required")
        sys.exit(1)

    dbc = DbConnection(db_user, db_passwd, "quant_id_adm")
    if cmd == "add":
        add(dbc, cmd_args)
    elif cmd == "drop":
        drop(dbc, cmd_args)
    elif cmd == "warn":
        warn(dbc, cmd_args)
    elif cmd == "clean":
        clean(dbc, cmd_args)
    else:
        sys.stderr.write("Error: unknown command '%s'\n" % (cmd,))
        sys.exit(1)

    print("Done.")
