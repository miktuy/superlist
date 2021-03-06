from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run

REPO_URL = "https://github.com/miktuy/superlist.git"


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ("database", "static", "venv", "source"):
        run(f"mkdir -p {site_folder}/{subfolder}")


def _get_latest_source(source_folder):
    if exists(source_folder + "/.git"):
        run(f"cd {source_folder} && git fetch")
    else:
        run(f"git clone {REPO_URL} {source_folder}")
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f"cd {source_folder} && git reset --hard {current_commit}")


def _update_virtualenv(source_folder):
    venv_folder = f"{source_folder}/../venv"
    if not exists(f"{venv_folder}/bin/pip"):
        run(f"python3 -m venv {venv_folder}")
    run(f"{venv_folder}/bin/pip install -r {source_folder}/requirements.txt")


def _update_settings(source_folder, host):
    settings_path = f"{source_folder}/superlist/settings.py"
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path, "ALLOWED_HOSTS =.+$", f'ALLOWED_HOSTS = ["{host.replace("www.", "")}"]')
    sed(settings_path, "../database/db.sqlite3", "../../database/db.sqlite3")
    sed(settings_path, "\.\./static", "../../static")

    secret_key_file = f"{source_folder}/superlist/secret_key.py"
    if not exists(secret_key_file):
        import string
        import random

        chars = string.ascii_lowercase + string.digits + "!@#$%^&*(-_=+)"
        key = "".join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    append(settings_path, "\nfrom .secret_key import SECRET_KEY")


def _update_static_files(source_folder):
    run(
        f"cd {source_folder}"
        f" && ../venv/bin/python manage.py collectstatic --noinput"
    )


def _update_database(source_folder):
    run(
        f"pwd"
        f" echo {source_folder}"
        f" && cd {source_folder}"
        f" && ../venv/bin/python manage.py migrate --noinput"
    )


def deploy():
    site_folder = f"/home/{env.user}/sites/{env.host}"
    source_folder = f"{site_folder}/source"
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
