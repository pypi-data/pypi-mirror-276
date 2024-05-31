import json
import os
import argparse
from plutonium.utils import logger, VoyagerDetect, zip_folder
from plutonium.config import (
    VOYAGER_SERVER,
    VOYAGER_USERNAME,
    VOYAGER_PASSWORD,
    VOYAGER_TOKEN,
    LOG_FILENAME,
    LOGO,
    DATA_DIR,
    AGENT_UUID
)

def init_parse():
    parser = argparse.ArgumentParser(
        description="SCA Agent based on Cdxgen and internal project Voyager I, for application dependencies and risk discovery。"
    )
    parser.add_argument(
        "-t",
        "--type",
        dest="type",
        required=True,
        help="project_sca/image_sca/package_sca/api/other/project_vul/image_vul",
    )
    parser.add_argument(
        "-trigger-source",
        "--trigger-source",
        dest="trigger_source",
        help="Trigger Source",
    )
    parser.add_argument(
        "-s",
        "--source",
        dest="source",
        required=True,
        help="Source directory or container image or binary file",
    )
    parser.add_argument(
        "--tool",
        dest="tool",
        help="Analysis Tool",
    )
    parser.add_argument(
        "--tool-opitons",
        dest="tool_options",
        help="Analysis Tool options",
    )
    parser.add_argument(
        "--firewall-status",
        dest="firewall_status",
        action="store_true",
        default=False,
        help="是否进行拦截检测",
    )
    parser.add_argument(
        "--is-sync",
        dest="is_sync",
        action="store_true",
        default=False,
        help="是否同步检测",
    )
    # 服务端参数
    parser.add_argument(
        "--voyager-server",
        default=VOYAGER_SERVER,
        dest="voyager_server",
        help="Voyager server url. Eg: https://api.voyager.com",
    )
    parser.add_argument(
        "--voyager-username",
        default=VOYAGER_USERNAME,
        dest="voyager_username",
        help="Voyager username",
    )
    parser.add_argument(
        "--voyager-password",
        default=VOYAGER_PASSWORD,
        dest="voyager_password",
        help="Voyager password",
    )
    parser.add_argument(
        "--voyager-token",
        default=VOYAGER_TOKEN,
        dest="voyager_token",
        help="Voyager token for token based submission",
    )
    parser.add_argument(
        "--voyager-api",
        default="",
        dest="voyager_api",
        help="Voyager api url",
    )
    parser.add_argument(
        "--analyze-uuid",
        dest="analyze_uuid",
        help="分析任务id",
    )
    # 项目参数信息
    parser.add_argument(
        "--project-name",
        dest="project_name",
        help="project name",
    )
    parser.add_argument(
        "--project-url",
        dest="project_url",
        help="project repository url",
    )
    parser.add_argument(
        "--project-user",
        dest="project_user",
        help="project user",
    )
    parser.add_argument(
        "--project-branch",
        dest="project_branch",
        help="project branch",
    )
    parser.add_argument(
        "--project-file",
        dest="project_file",
        help="project file",
    )
    parser.add_argument(
        "--project-commit-id",
        dest="project_commit_id",
        help="project commit id",
    )
    # 镜像参数信息
    parser.add_argument(
        "--image-name",
        dest="image_name",
        help="镜像名称",
    )
    parser.add_argument(
        "--image-file",
        dest="image_file",
        help="镜像文件",
    )
    parser.add_argument(
        "--image-repository-url",
        dest="image_repository_url",
        help="镜像仓库地址",
    )
    parser.add_argument(
        "--extra-data",
        dest="extra_data",
        help="附加参数a=b&c=d",
    )
    parser.print_help()
    return parser.parse_args()


def main():
    print(LOGO)
    args = init_parse()
    data = {
        'type': args.type,
        'agent_uuid': AGENT_UUID,
        'trigger_source': args.trigger_source,
        'tool': args.tool,
        'tool_options': args.tool_options,
        'firewall_status': args.firewall_status,
        'is_sync': args.is_sync,
        'analyze_uuid': args.analyze_uuid if args.analyze_uuid else '',
        # 项目信息
        # 镜像类
        'image_name': args.image_name,
        'image_repository_url': args.image_repository_url,
        # 项目类
        'project_name': args.project_name,
        'project_branch': args.project_branch,
        'project_user': args.project_user,
        'project_commit_id': args.project_commit_id,
        'project_url': args.project_url,
        # 附加参数
        'extra_data': args.extra_data,
    }
    attach_files = [
        # 提交的名称前缀需要与scan_log_detail的type一致
        # 项目文件
        # ('log_file', (SCA, open('./todo.md', 'rb'),)),
        # ('core_files_list', ('pom.xml', open('./todo.md', 'rb'), )),
        # ('core_files_list', ('package.json.lock', open('./todo.md', 'rb'), )),
        # ('sbom_files_list', ('sca_cdxgen.json', open('./voyager.json', 'rb'),)),
        # ('sbom_files_list', ('sca_dependency_tree.txt', open('./todo.md', 'rb'), )),
        # ('vul_files_list', ('vul_veinmind.json', open('./todo.md', 'rb'), )),
    ]
    detector = VoyagerDetect(
        token=args.voyager_token if args.voyager_token else VOYAGER_TOKEN,
        url=args.voyager_server if args.voyager_server else VOYAGER_SERVER,
        username=args.voyager_username if args.voyager_username else VOYAGER_USERNAME,
        password=args.voyager_password if args.voyager_password else VOYAGER_PASSWORD,
        api=args.voyager_api if args.voyager_api else ''
    )
    # 项目安全检测
    if args.type in ['project_sca', 'image_sca']:
        # 逐步进行检测
        for tool in args.tool.split(','):
            detector.sca_analysis(args.source, tool)
        # 打包上传
        zip_folder(DATA_DIR)
        target_file = DATA_DIR.rstrip('/')+'.zip'
        try:
            attach_files.append(
                ('attach_file', (target_file.split('/')[-1], open(target_file, 'rb'),)),
            )
        except Exception as e:
            logger.error(e)
        scan_status = detector.upload(data, attach_files)
        print(scan_status)
    # 镜像安全检测
    elif args.type in ['image_vul',]:
        if args.image_file:
            try:
                attach_files.append(
                    ('attach_file', (args.image_file.split('/')[-1].split('.')[0], open(args.image_file, 'rb'),)),
                )
            except Exception as e:
                logger.error(e)
        scan_status = detector.scan(data, attach_files)
        print(scan_status)
    
    else:
        pass
if __name__ == '__main__':
    main()
