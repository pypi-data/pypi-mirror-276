import subprocess
import logging
import os
import sys
import zipfile
import shutil
import requests
import plutonium.config as config
from uuid import uuid4
logger = logging.getLogger(__name__)
formatter = logging.Formatter(config.LOG_FORMAT)
file_handler = logging.FileHandler(config.LOG_FILENAME)
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(config.LOG_LEVEL)
# 获取路径
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)
# 执行命令
def exec_tool(args, log_file, timeout=config.CMD_TIME_OUT, cwd=None, ):
    result = {
        'status': False,
        'message': '',
        'data': ''
    }
    try:
        logger.debug('Executing "{}"'.format(" ".join(args)))

        if os.environ.get("FETCH_LICENSE"):
            logger.debug(
                "License information would be fetched from the registry. This would take several minutes ..."
            )
        with open(log_file, 'a') as f:
            cp = subprocess.run(
                args,
                stdout=f,
                stderr=subprocess.STDOUT,
                cwd=cwd,
                env=os.environ.copy(),
                check=False,
                shell=False,
                encoding="utf-8",
                timeout=timeout
            )
            logger.debug(cp.stdout)
            result['status'] = True
    except subprocess.TimeoutExpired as timeout_error:
        logger.error(timeout)
        result['message'] = '执行超时-{}'.format(timeout_error)
    except Exception as e:
        logger.exception(e)
        result['message'] = str(e)
        return str(e)
    print(result)
    return result

def zip_folder(file_dir):
    target_file = file_dir+'/../'+file_dir.strip('/').split('/')[-1]+'.zip'
    print(target_file)
    with zipfile.ZipFile(target_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, file_dir))
    

# 通过cdxgen来生成sbom
def sca_by_cdxgen(bom_file, src_dir=".", timeout=config.CMD_TIME_OUT):
    result = {
        'status': False,
        'data': {
            'cmd': '',
            'result_file': bom_file
        },
        'message': '',
    }
    cdxgen_cmd = os.environ.get("CDXGEN_CMD", "cdxgen")
    if not shutil.which(cdxgen_cmd):
        local_bin = resource_path(
            os.path.join(
                "local_bin", "cdxgen.exe" if sys.platform == "win32" else "cdxgen"
            )
        )
        if not os.path.exists(local_bin):
            result['message'] = 'command not found'
            return result
        try:
            cdxgen_cmd = local_bin
            # Set the plugins directory as an environment variable
            os.environ["CDXGEN_PLUGINS_DIR"] = resource_path("local_bin")
        except Exception as e:
            result['message'] = e
            return result
    sca_args = [cdxgen_cmd, "-o", bom_file]
    sca_args.append(src_dir)
    logger.info(sca_args)
    exec_status = exec_tool(sca_args, config.LOG_FILENAME, timeout )
    result['status'] = exec_status['status']
    result['message'] = exec_status['message']
    result['data']['cmd'] = ' '.join(sca_args)
    return result


# 服务端检测
class VoyagerDetect():
    def __init__(self, token=None, url=None, username=None, password=None, api=None):
        self.api_url = url
        self.api_token = token
        self.api_username = username
        self.api_password = password
        self.req = requests.Session()

    # 1.token生成，token有效期较长，失效后再进行重新生成
    def get_new_token(self):
        try:
            self.req.headers = {}
            res = self.req.post(self.api_url + config.VOYAGER_GET_TOKEN_API,
                                data={'username': self.api_username, 'password': self.api_password})
            token = res.json()['token']
            headers = {
                # 注意Token后有空格
                'Authorization': 'Token ' + token
            }
            self.req.headers = headers
            return token
        except Exception as e:
            logger.error(e)
            return None

    def check_token_valid(self):
        headers = {
            # 注意Token后有空格
            'Authorization': 'Token ' + self.api_token
        }
        self.req.headers = headers
        try:
            res = self.req.get(self.api_url + config.VOYAGER_CHECK_TOKEN_API, )
            if res.status_code == 200 and res.json()['success']:
                return True
        except Exception as e:
            logger.error(e)
        return False

    # 登录认证
    def login(self):
        login_status = {
            'status': False,
            'message': '',
            'data': None
        }
        if self.api_token:
            if self.check_token_valid():
                login_status['status'] = True
                return login_status
            else:
                # token失效，使用账号密码登录
                login_status['message'] = 'token失效，使用账号密码登录'

        if self.api_username and self.api_password:
            # 获取认证token
            token = self.get_new_token()
            # logger.info(token)
            if token:
                self.api_token = token
                headers = {
                    # 注意Token后有空格
                    'Authorization': 'Token ' + self.api_token
                }
                self.req.headers = headers
                login_status['status'] = True
            else:
                login_status['message'] = '无法生成访问token，账号密码可能错误'
        else:
            login_status['message'] = '请提供API账号以及密码信息'
        logger.info(login_status['message'])
        return login_status

    # sca分析
    def sca_analysis(self, src_dir=".", tool='cdxgen'):
        if tool == 'cdxgen':
            result_file = config.DATA_DIR+'/{}_{}.json'.format(tool, uuid4().hex)
            return sca_by_cdxgen(result_file, src_dir)

        return None

    # upload
    def upload(self, data, files):
        login_status = self.login()
        if login_status['status']:
            if files:
                response = self.req.post(self.api_url + config.VOYAGER_BASE_API, data=data, files=files)
            else:
                response = self.req.post(self.api_url + config.VOYAGER_BASE_API, data=data,
                                         files=[('files', ('', None,)), ])
            return response.json()
        else:
            return login_status['message']
    # 获取扫描结果或报告
    def get_scan_result(self, task_id):
        login_status = self.login()
        if login_status['status']:
            response = self.req.get(self.api_url + VOYAGER_BASE_API+'?task_id={}'.format(task_id),)
            return response.json()
        else:
            return login_status
    
    # 新版的与服务端交互
    def scan(self, data, files):
        login_status = self.login()
        if login_status['status']:
            if files:
                response = self.req.post(self.api_url + config.VOYAGER_BASE_API, data=data, files=files)
            else:
                response = self.req.post(self.api_url + config.VOYAGER_BASE_API, data=data, files=[('files', ('', None,)), ])
            return response.json()
        else:
            return login_status['message']
    

    