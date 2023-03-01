# subset

Manage and share your text ;)

# Installation

First create config file.

```bash
# create config file
mkdir -p ~/.config/.subset
touch ~/.config/.subset/config
```

Add your configuration as in next example.

```json
{
  "user": "your_user_name",
  "file": "/home/your_user/.config/.subset/storage",
  "default_domain": "clip",
  "domains": [
    [
      "clip",
      10,
      "clip"
    ]
  ]
}
```

First use generate storage.

```bash
python3 subset.py --generate
```

This will create a storage file in the path specified in conf file.

# How to

```bash
➜  python3 subset.py --help
usage: subset.py [-h] [-c CONFIG] [-gen] [-a] [-r] [--reset]
                 [-s] [-l] [-i INDEX] [-d DOMAIN] [-v VALUE]

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        configuration file
  -gen, --generate      generate storage
  -a, --add             add elem
  -r, --remove          remove elem
  --reset               reset all elements
  -s, --select          select elem
  -l, --list            add elem
  -i INDEX, --index INDEX
                        elem index
  -d DOMAIN, --domain DOMAIN
                        elem domain
  -v VALUE, --value VALUE
                        elem value

```