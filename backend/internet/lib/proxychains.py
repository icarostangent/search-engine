class ProxyChainsConfigurator:
    def __init__(self, config_file='proxychains.conf'):
        self.config_file = config_file
        self.pause_file = 'paused.conf'
        self.proxies = []
        self.randomize = False
        self.chain_length = 1

    def set_randomize(self, randomzie):
        self.randomize = randomize

    def add_proxy(self, proxy_type, address, port):
        proxy_types = {'S4': 'socks4', 'S5': 'socks5', 'HP': 'http', 'HS': 'https'}
        self.proxies.append((proxy_types[proxy_type], address, port))

    def set_dynamic_chain(self):
        self.chain_type = 'dynamic_chain'

    def set_random_chain(self):
        self.chain_type = 'random_chain'

    def set_strict_chain(self):
        self.chain_type = 'strict_chain'

    def write_config(self):
        with open(self.config_file, 'w') as f:
            f.write(f"{self.chain_type}\n")
            f.write("proxy_dns\n")
            f.write("remote_dns_subnet 224\n")
            f.write("tcp_read_time_out 15000\n")
            f.write("tcp_connect_time_out 8000\n")
            f.write("[ProxyList]\n")
            for proxy in self.proxies:
                f.write(f"{proxy[0]} {proxy[1]} {proxy[2]}\n")

    def clean_config(self):
        if os.path.exists(self.config_file):
            os.remove(self.config_file)

        if os.path.exists(self.pause_file):
            os.remove(self.pause_file)