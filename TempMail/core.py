import requests
import time
from random import choice
from stem import Signal
from stem.control import Controller
from fake_useragent import UserAgent
from .utils import log_error

class TempMail:
    def __init__(self, domain=None, check_interval=0.5, output_file=None, no_box=False, only_subject=False, only_id=False, no_router=False, agent=None, proxy=None, tor_port=9051, tor_password='obagulhoeouvirplug', custom_headers=None, initial_check_interval=0, log_errors=False, storage_type='file'):
        self.base_url = "https://www.1secmail.com/api/v1/"
        self.email = None
        self.processed_emails = set()
        self.domains = []
        self.domain = domain
        self.check_interval = check_interval
        self.output_file = output_file
        self.no_box = no_box
        self.only_subject = only_subject
        self.only_id = only_id
        self.no_router = no_router
        self.agent = agent
        self.proxy = proxy
        self.tor_port = tor_port
        self.tor_password = tor_password
        self.custom_headers = custom_headers or {}
        self.initial_check_interval = initial_check_interval
        self.log_errors = log_errors
        self.storage_type = storage_type

        self.session = requests.Session()
        if self.proxy:
            self.session.proxies = {
                'http': self.proxy,
                'https': self.proxy
            }
        else:
            self.session.proxies = {
                'http': 'socks5h://localhost:9050',
                'https': 'socks5h://localhost:9050'
            }

        self.user_agent = UserAgent() if not self.agent else None
        self.user_agents = [self.agent or self.user_agent.random for _ in range(10)]

    def _get_random_user_agent(self):
        return choice(self.user_agents)

    def _connect_to_tor(self):
        if not self.no_router:
            try:
                with Controller.from_port(port=self.tor_port) as controller:
                    controller.authenticate(password=self.tor_password)
                    controller.signal(Signal.NEWNYM)
            except Exception as e:
                log_error(f"Erro ao conectar com Tor: {e}", self.log_errors)

    def check_proxy(self):
        try:
            response = requests.get('https://api.ipify.org?format=json', proxies=self.session.proxies)
            response.raise_for_status()
            ip_info = response.json()
            ip = ip_info['ip']

            location_response = requests.get(f'https://ipinfo.io/{ip}/json')
            location_response.raise_for_status()
            location_info = location_response.json()

            print(f"IP da proxy: {ip}")
            print(f"Localização da proxy: {location_info.get('city', 'Desconhecida')}, {location_info.get('region', 'Desconhecida')}, {location_info.get('country', 'Desconhecida')}")
        except requests.RequestException as e:
            log_error(f"Erro ao verificar a proxy: {e}", self.log_errors)

    def get_domains(self):
        try:
            response = self.session.get(f"{self.base_url}?action=getDomainList")
            response.raise_for_status()
            self.domains = response.json()
            if not self.domain:
                print("Domínios disponíveis:")
                for index, domain in enumerate(self.domains, start=1):
                    print(f"{index}. {domain}")
                print(f"{len(self.domains) + 1}. Aleatório")
        except requests.RequestException as e:
            log_error(f"Erro ao obter a lista de domínios: {e}", self.log_errors)

    def generate_email(self, domain=None):
        headers = {
            'User-Agent': self._get_random_user_agent(),
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br'
        }
        headers.update(self.custom_headers)
        try:
            response = self.session.get(f"{self.base_url}?action=genRandomMailbox&count=1", headers=headers)
            response.raise_for_status()
            username = response.json()[0].split('@')[0]
            if domain:
                self.email = f"{username}@{domain}"
            else:
                self.email = f"{username}@{choice(self.domains)}"
            print(f"Email temporário criado: {self.email}")
        except requests.RequestException as e:
            log_error(f"Erro ao gerar email: {e}", self.log_errors)

    def check_inbox(self):
        if not self.email:
            print("Nenhum email criado")
            return

        username, domain = self.email.split("@")
        headers = {
            'User-Agent': self._get_random_user_agent(),
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br'
        }
        headers.update(self.custom_headers)
        try:
            response = self.session.get(f"{self.base_url}?action=getMessages&login={username}&domain={domain}", headers=headers)
            response.raise_for_status()
            emails = response.json()

            if not emails:
                return

            new_emails = [email for email in emails if email['id'] not in self.processed_emails]

            if new_emails:
                for email in new_emails:
                    self.process_email(username, domain, email)
                    self.processed_emails.add(email['id'])
        except requests.RequestException as e:
            log_error(f"Erro ao verificar a caixa de entrada: {e}", self.log_errors)

    def process_email(self, username, domain, email):
        output = []
        if self.only_id:
            output.append(f"ID da Mensagem: {email['id']}")
        elif self.only_subject:
            output.append(f"Assunto: {email['subject']}")
        elif self.no_box:
            output.append(f"De: {email['from']}\nAssunto: {email['subject']}\nID da Mensagem: {email['id']}")
        else:
            output.append(f"De: {email['from']}\nAssunto: {email['subject']}\nID da Mensagem: {email['id']}")
            message = self.get_message(username, domain, email['id'])
            if message:
                output.append(f"Corpo: {message['textBody']}")

        output_text = "\n".join(output) + "\n" + "="*50
        print(output_text)

        if self.storage_type == 'file' and self.output_file:
            with open(self.output_file, 'a') as file:
                file.write(output_text + "\n")
        elif self.storage_type == 'csv' and self.output_file:
            import csv
            with open(self.output_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([email['id'], email['from'], email['subject'], message['textBody'] if message else ''])

    def get_message(self, username, domain, message_id):
        headers = {
            'User-Agent': self._get_random_user_agent(),
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br'
        }
        headers.update(self.custom_headers)
        try:
            response = self.session.get(f"{self.base_url}?action=readMessage&login={username}&domain={domain}&id={message_id}", headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            log_error(f"Erro ao obter mensagem: {e}", self.log_errors)
            return None

    def run(self):
        if self.initial_check_interval > 0:
            print(f"Aguardando {self.initial_check_interval} segundos antes de começar...")
            time.sleep(self.initial_check_interval)
        self._connect_to_tor()
        self.check_proxy()
        self.get_domains()
        domain = self.choose_domain()
        self.generate_email(domain)
        try:
            while True:
                self.check_inbox()
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            print("\nSaindo")
