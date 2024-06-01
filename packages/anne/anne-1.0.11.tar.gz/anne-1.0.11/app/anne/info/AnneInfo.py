import requests, random, string, os




class AnneInfo:
    def __init__(self):
        self.file_list = ['fname_vn.txt', 'lname_vn.txt']
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

    def get_name_random(self, country='vn'):
        if country == 'vn':
            fname_path = os.path.join(self.current_dir, 'data', 'fname_vn.txt')
            lname_path = os.path.join(self.current_dir, 'data', 'lname_vn.txt')

            with open(fname_path, 'r', encoding='utf-8') as f:
                first_names = f.readlines()

            with open(lname_path, 'r', encoding='utf-8') as l:
                last_names = l.readlines()

            first_name = random.choice(first_names).strip()
            last_name = random.choice(last_names).strip()

            return first_name + ' ' + last_name