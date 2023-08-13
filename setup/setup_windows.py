import logging
import setup_common

errors = 0  # Define the 'errors' variable before using it
log = logging.getLogger('sd')


def install_torch2():
    # setup_common.check_repo_version()
    setup_common.check_python()

    # Upgrade pip if needed
    setup_common.install('--upgrade pip')
    # Install requirements
    setup_common.install_requirements('requirements.txt', check_no_verify_flag=False)


if __name__ == '__main__':
    setup_common.ensure_base_requirements()
    setup_common.setup_logging()
    install_torch2()
