import requests, random, string, os, unidecode
from faker import Faker

class AnneInfo:
    def __init__(self, country='vn'):
        self.name_list = {
            "vn": ['fname_vn', 'lname_vn'],
            "us": ['fname_us', 'lname_us']
        }
        if country not in self.name_list: raise ValueError(f"Không hỗ trợ quốc gia: {country}\nCác quốc gia được hỗ trợ: vn, us")
        self.country = country
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.faker = Faker()

    def get_name(self):
        if self.country in self.name_list:
            fname_path = os.path.join(self.current_dir, 'data', f'{self.name_list[self.country][0]}.txt')
            lname_path = os.path.join(self.current_dir, 'data', f'{self.name_list[self.country][1]}.txt')
            with open(fname_path, 'r', encoding='utf-8') as f: first_names = f.readlines()
            with open(lname_path, 'r', encoding='utf-8') as l: last_names = l.readlines()
            first_name = random.choice(first_names).strip()
            last_name = random.choice(last_names).strip()
            data = {
                "first_name": first_name,
                "last_name": last_name
            }
            return data
        else:
            raise ValueError(f"Unsupported country: {country}")

    def get_birth(self, day_space=(1, 28), month_space=(1, 12), year_space=(1960, 2004)):
        day = random.randint(day_space[0], day_space[1])
        month = random.randint(month_space[0], month_space[1])
        year = random.randint(year_space[0], year_space[1])
        full = f"{day}/{month}/{year}"
        data = {
            "day": day,
            "month": month,
            "year": year,
            "full": full
        }
        return data

    def get_email(self, first_name=None, last_name=None, username_custom=None, domain=None):
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
            return f"{email}@{domain}"

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
            return f"{email}@{domain}"

    def get_password(self, password_space=(12, 18), password_custom=None):
        min, max = password_space
        if not password_custom:
            all_chars = string.ascii_letters + string.digits
            return ''.join(random.choice(all_chars) for _ in range(random.randint(min, max)))
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
            return psw
        else:
            return "annesayhi"

    def get_ua(self, platform='auto'):
        _platform = ['auto', 'android', 'ios', 'win', 'mac', 'linux']
        if platform not in _platform: raise ValueError(f"Không hỗ trợ platform: {platform}\nPlatforms được hỗ trợ: {_platform}")
        if platform in _platform:
            if platform == 'auto': return self.faker.user_agent()
            uas = os.path.join(self.current_dir, 'data', f'ua_{platform}.txt')
            with open(uas, 'r', encoding='utf-8') as f: user_agents = f.readlines()
            return random.choice(user_agents).strip()

    def get_info(self,
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
                "first": "",
                "last": "",
                "full": ""
            },
            "birth": {
                "day": "",
                "month": "",
                "year": "",
                "full": ""
            },
            "email": "",
            "password": "",
            "user_agent": ""
        }


        name_data = self.get_name()
        birth_data = self.get_birth(day_space, month_space, year_space)

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
        data["email"] = self.get_email(name_data["first_name"], name_data["last_name"], username_custom, domain)

        # Password
        data["password"] = self.get_password(password_space, password_custom)

        # User Agent
        data["user_agent"] = self.get_ua(platform)

        return data













