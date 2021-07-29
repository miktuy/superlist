Provide site's run
=========================
## Necessary packages:
* nginx
* python3.6+
* virtualenv + pip
* git

For Ubuntu:
    ```sudo apt-get install nginx python-venv```

## Configure nginx
* see nginx.template.conf
* replace SITENAME

## Configure systemd
* see gunicorn-systemd.template.service
* replace SITENAME

## Folder structure:
For <username>
/home/<username>
└── sites
 └── SITENAME
 ├── database
 ├── source
 ├── static
 └── venv