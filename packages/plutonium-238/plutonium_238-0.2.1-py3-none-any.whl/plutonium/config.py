import os
from uuid import uuid4
import logging
import tempfile
LOGO = r"""
   ,-------------------------------------------------------------------------------.
   |                                                                               |
   |                                                                               |
   |       ____  _       _              _                   ____  _____  ___       |
   |      |  _ \| |_   _| |_ ___  _ __ (_)_   _ _ __ ___   |___ \|___ / ( _ )      |
   |      | |_) | | | | | __/ _ \| '_ \| | | | | '_ ` _ \    __) | |_ \ / _ \      |
   |      |  __/| | |_| | || (_) | | | | | |_| | | | | | |  / __/ ___) | (_) |     |
   |      |_|   |_|\__,_|\__\___/|_| |_|_|\__,_|_| |_| |_| |_____|____/ \___/      |
   |                                                                               |
   |                                                                               |
   |                                                             version 0.2.1     |
   |                                                                               |
   |                 This is a SCA Agent, Copyright@Plutonium Team                 |
   |                                                                               |
   |                                                                               |
   `-------------------------------------------------------------------------------'
"""
# 结果轮询最大时间
RESULT_CHECK_INTERVAL = 1
RESULT_CHECK_TIME_MAX = 1 * 10
# 结果轮询最大次数
RESULT_CHECK_COUNT = 20

# DATA_DIR = os.path.dirname(os.path.abspath(__file__)) +'/data/'
VOYAGER_SERVER = os.getenv('VOYAGER_SERVER') if os.getenv('VOYAGER_SERVER') else 'http://localhost:6600/'
VOYAGER_USERNAME = os.getenv('VOYAGER_USERNAME') if os.getenv('VOYAGER_USERNAME') else 'dev'
VOYAGER_PASSWORD = os.getenv('VOYAGER_PASSWORD') if os.getenv('VOYAGER_PASSWORD') else 'dev'
VOYAGER_TOKEN = os.getenv('VOYAGER_TOKEN') if os.getenv('VOYAGER_TOKEN') else 'x'
AGENT_UUID = uuid4().hex
# 默认忽略的目录
TEMP_DIR = tempfile.gettempdir()
if not TEMP_DIR:
    TEMP_DIR = './tmp/'
    try:
        if not os.path.exists(TEMP_DIR):
            os.makedirs(TEMP_DIR)
    except Exception as e:
        print(e)
DATA_DIR = TEMP_DIR + '/plutonium-{}/'.format(AGENT_UUID)
if not os.path.exists(DATA_DIR):
    try:
        os.makedirs(DATA_DIR)
    except Exception as e:
        DATA_DIR = './tmp'

# 日志配置
if os.getenv("DEBUG"):
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.INFO
LOG_FILENAME = DATA_DIR + 'plutonium_run_{}.log'.format(uuid4().hex)
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s  - %(lineno)d - %(message)s'
SCA_TOOLS = {
    'cdxgen': {
        'description': 'cdxgen tool',
        'default_options':[],
    },
    'jd_sca': {
        'descripion': '',
        'result': ''
    },
    'opensca': {
        'descripion': '',
        'result': ''
    },
}

VOYAGER_GET_TOKEN_API="/sbom/api/base/get-auth-token/"
VOYAGER_CHECK_TOKEN_API="/sbom/api/base/check-token/"
VOYAGER_BASE_API="/sbom/api/sbom/gather/"

# 调用命令超时时间，默认5分钟
CMD_TIME_OUT = 5 * 60