# -*- coding: utf-8 -*-


class CSVLoader(object):
    @classmethod
    def load(cls, filename):
        seperator = None

        with open(filename, 'r') as file_obj:
            first_line = file_obj.readline()

            if first_line.startswith('name'):
                has_header = True
            elif first_line.startswith('\''):
                has_header = True
                file_obj.seek(0)
            else:
                has_header = False
                file_obj.seek(0)

            for line in file_obj:
                line = line.strip()
                if line == '':
                    continue

                if seperator is None:
                    if line.find(';') >= 0:
                        seperator = ';'
                    elif line.find(',') >= 0:
                        seperator = ','
                    else:
                        raise Exception('unknown seperator for {}'.format(filename))

                if has_header:
                    parts = line.split(seperator, 2)
                    line = parts[-1]

                vec = list(map(float, line.split(seperator)))
                yield vec
