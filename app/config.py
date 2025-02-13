# config.py
import configparser
import os

class Config:
    def __init__(self, config_file: str = None):
        self.config = configparser.ConfigParser()
        config_path = config_file or os.getenv('CONFIG_FILE', './app/config/config.ini')
        self.config.read(config_path)
        
        self.gitea = {
            'access_token': self.config['gitea']['access_token'],
            'base_url': self.config['gitea']['base_url']
        }
        
        self.pingcode = {
            'client_id': self.config['pingcode']['client_id'],
            'client_secret': self.config['pingcode']['client_secret'],
            'base_url': self.config['pingcode']['base_url']
        }
        
        
# 创建一个全局配置实例
config = Config()