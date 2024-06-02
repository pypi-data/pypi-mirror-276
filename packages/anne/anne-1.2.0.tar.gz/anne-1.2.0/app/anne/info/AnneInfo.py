import requests, random, string, os, unidecode
from faker import Faker

class AnneInfo:
    def __init__(self, country='vn', debug=False):
        self.name_list = {
            "vn": ['fname_vn', 'lname_vn'],
            "us": ['fname_us', 'lname_us']
        }
        if country not in self.name_list: raise ValueError(f"Không hỗ trợ quốc gia: {country}")
        self.country = country
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.faker = Faker()
        self.debug = debug

    def getName(self):
        data = {"first_name": None, "last_name": None}
        try:
            if self.country in self.name_list:
                fname_path = os.path.join(self.current_dir, 'data', f'{self.name_list[self.country][0]}.txt')
                lname_path = os.path.join(self.current_dir, 'data', f'{self.name_list[self.country][1]}.txt')
                with open(fname_path, 'r', encoding='utf-8') as f: first_names = f.readlines()
                with open(lname_path, 'r', encoding='utf-8') as l: last_names = l.readlines()
                first_name = random.choice(first_names).strip()
                last_name = random.choice(last_names).strip()
                data["first_name"] = first_name
                data["last_name"] = last_name
                return data
            else: print(f"Không hỗ trợ quốc gia: {self.country}")
        except Exception as e:
            if self.debug: print(f'Lỗi [getName]: {e}')
            return data

    def getBirth(self, day_space=(1, 28), month_space=(1, 12), year_space=(1960, 2004)):
        try:
            data = {"day": None, "month": None, "year": None, "full": None}
            day = random.randint(day_space[0], day_space[1])
            month = random.randint(month_space[0], month_space[1])
            year = random.randint(year_space[0], year_space[1])
            data["day"] = day
            data["month"] = month
            data["year"] = year
            data["full"] = f"{day}/{month}/{year}"
            return data
        except Exception as e:
            if self.debug: print(f'Lỗi [getBirth]: {e}')
            return data

    def getEmail(self, first_name=None, last_name=None, username_custom=None, domain=None):
        data = {"email": None}
        try:
            if not first_name and not last_name: first_name, last_name = self.get_name()
            if not domain: domain = random.choice(['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com'])

            first_name = unidecode.unidecode(first_name).replace(" ", "").lower()
            last_name = unidecode.unidecode(last_name).replace(" ", "").lower()
            fname, lname = first_name, last_name

            if not username_custom:
                random_string = random.choice(string.ascii_lowercase) + ''.join(random.choices(string.ascii_lowercase + string.digits + '_', k=random.randint(5, 11)))
                if random.choice([True, False]): fname, lname = last_name, first_name
                position = random.choice(['before', 'middle', 'after'])
                if position == 'before':  email = f"{random_string}{fname}{lname}"
                elif position == 'middle': email = f"{fname}{random_string}{lname}"
                elif position == 'after': email = f"{fname}{lname}{random_string}"
                data["email"] = f"{email}@{domain}"
                return data

            elif username_custom:
                parts = username_custom.split('*')
                email = ''
                for part in parts:
                    if part == '':
                        num_random_chars = 1
                        random_string = random.choice(string.ascii_lowercase) + ''.join(
                        random.choices(string.ascii_lowercase + string.digits + '_', k=num_random_chars - 1))
                        email += random_string
                    else:
                        email += part
                data["email"] = f"{email}@{domain}"
                return data
        except Exception as e:
            if self.debug: print(f'Lỗi [getEmail]: {e}')
            return data

    def getPassword(self, password_space=(12, 18), password_custom=None):
        data = {"password": None}
        min, max = password_space

        try:
            if not password_custom:
                all_chars = string.ascii_letters + string.digits
                psw = ''.join(random.choice(all_chars) for _ in range(random.randint(min, max)))
                data["password"] = psw
                return data

            elif password_custom:
                psw = ''
                parts = password_custom.split('*')
                for part in parts:
                    if part == '':
                        num_random_chars = 1
                        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=num_random_chars))
                        psw += random_string
                    else:
                        psw += part
                data["password"] = psw
                return data
            else:
                data["password"] = 'Anne'
        except Exception as e:
            if self.debug: print(f'Lỗi [getPassword]: {e}')
            return data

    def getUserAgent(self, platform='auto'):
        _platform = ['auto', 'android', 'ios', 'win', 'mac', 'linux']
        if platform not in _platform: raise ValueError(f"Không hỗ trợ platform: {platform}")
        data = {"user_agent": None}
        try:
            if platform in _platform:
                if platform == 'auto': return self.faker.user_agent()
                uas = os.path.join(self.current_dir, 'data', f'ua_{platform}.txt')
                with open(uas, 'r', encoding='utf-8') as f: user_agents = f.readlines()
                ua = random.choice(user_agents).strip()
                data["user_agent"] = ua
                return data
        except Exception as e:
            if self.debug: print(f'Lỗi [getUserAgent]: {e}')
            return data

    def getInfo(self,
                day_space=(1, 28),
                month_space=(1, 12),
                year_space=(1960, 2004),
                username_custom=None,
                password_custom=None,
                password_space=(12, 18),
                domain=None,
                platform='auto'
                ):

        data = {
            "name": {
                "first": None,
                "last": None,
                "full": None
            },
            "birth": {
                "day": None,
                "month": None,
                "year": None,
                "full": None
            },
            "email": None,
            "password": None,
            "user_agent": None
        }

        try:
            name_data = self.getName()
            birth_data = self.getBirth(day_space, month_space, year_space)

            # Name
            data["name"]["first"] = name_data["first_name"]
            data["name"]["last"] = name_data["last_name"]

            if self.country == 'vn': data["name"]["full"] = f"{name_data['last_name']} {name_data['first_name']}"
            elif self.country == 'us': data["name"]["full"] = f"{name_data['first_name']} {name_data['last_name']}"

            # Birth
            data["birth"]["day"] = birth_data["day"]
            data["birth"]["month"] = birth_data["month"]
            data["birth"]["year"] = birth_data["year"]
            data["birth"]["full"] = birth_data["full"]

            # Email
            data["email"] = self.getEmail(name_data["first_name"], name_data["last_name"], username_custom, domain)

            # Password
            data["password"] = self.getPassword(password_space, password_custom)

            # User Agent
            data["user_agent"] = self.getUserAgent(platform)

            return data

        except Exception as e:
            if self.debug: print(f'Lỗi [getInfo]: {e}')
            return data









