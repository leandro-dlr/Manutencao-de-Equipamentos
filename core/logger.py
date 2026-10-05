import logging
import os
from core.config import config

caminho_log = config['logging']['arquivo']
os.makedirs(os.path.dirname(caminho_log), exist_ok=True)

logging.basicConfig(
    filename=caminho_log, 
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
logger = logging.getLogger(__name__)