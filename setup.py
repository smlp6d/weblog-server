from os import mkdir, path


if not path.exists('data'):
    mkdir('data')
if not path.exists('data/config'):
    with open('data/config', 'tw') as f:
        pass


class config:
    @staticmethod
    def get(param, name='', default=None):
        if not name:
            name = param
        with open('data/config', 'r') as f:
            data = []
            for b in f.read().replace('  #', '#').replace(' #', '#').split('\n'):
                if b.replace(' ', '') != '':
                    data.append(b.split('#')[0].split(' - '))

        for i in range(len(data)):
            if data[i][0] == param:
                return data[i][1]
        else:
            if default is None:
                print(name, 'does not configured')
                val = None
                while not val:
                    val = input(f'{name}:_')
            else:
                val = default
            with open('data/config', 'a') as f:
                f.write(f'{param} - {val}\n')
            return val

    @staticmethod
    def get_all():
        with open('data/config', 'r') as f:
            data = {}
            for b in f.read().replace('  #', '#').replace(' #', '#').split('\n'):
                if b.replace(' ', '') != '':
                    data[b.split('#')[0].split(' - ')[0]] = b.split('#')[0].split(' - ')[1]

        return data


sql_uri = config.get('sql', 'sql uri', 'sqlite:///data/weblog.a.dbl')
debug = bool(int(config.get('debug', '', 0)))


port = int(config.get('port', 'app port'))
addr = config.get('addr', '', '')

const_key = bool(int(config.get('const_key', '', 1)))
key_size = int(config.get('key_size', 'key_size', 2**10))
key_file = config.get('key_file', 'key_file', 'data/mp.chain')
package_max_size = int(config.get('package_max_size', '', 1200))

pass_hash = config.get('pass_hash', 'password sha512')

default_limit = int(config.get('default_limit', '', 50))

if __name__ != '__main__':
    print('[ + ] setup')
