import os
import pymysql
from configparser import RawConfigParser
from contextlib import contextmanager, suppress


def read_conf(conf_path=''):
    if not conf_path:
        conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.conf')
    assert os.path.isfile(conf_path), "%s not exists!" % conf_path

    cfg = RawConfigParser()
    cfg.read(conf_path)
    _options = {}
    _dict = {
        'mysql': ['host', 'user', 'passwd', 'port', 'db', 'charset'],
        'udp': ['host', 'port']
    }
    for _k in _dict:
        values = _dict[_k]
        _options[_k] = {}
        for value in values:
            _options[_k].update({value: cfg.get(_k, value).strip()})
    _options['mysql']['port'] = int(_options['mysql']['port'])
    _options['udp']['port'] = int(_options['udp']['port'])
    return _options


@contextmanager
def mysql(options):
    conn = pymysql.connect(**options['mysql'])
    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        conn.commit()
        cursor.close()
        conn.close()


if __name__ == '__main__':
    options = read_conf()
    with mysql(options) as cursor:
        r = cursor.execute("select * from table")
        result = cursor.fetchall()
        print(result)

    # ignore Exception, python3 only
    with suppress(OSError):
        os.remove('1.txt')
