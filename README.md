# subset

Development tool to help you to focus on important stuff and share it between your devices or dev team.

# What is subset?

subset is a CLI development tool, it is designed to automatize and simplify a lot of different use cases.

The main idea is to keep small buffers of elements that you are currently using on your daily development with the possibility to share those buffers with your team or your different machines.

# Example Use Cases

- Clipboard management.
- Goto directory.
- Branch selection.
- Docker environment selection.
- History management.
- Code macros management.

# Installation

Easiest way to install it is to clone repo on your `.config` directory and make it your configuration and storage folder.

```bash
# create .config directoy just in case is not already there
mkdir -p ~/.config/ && cd ~/.config/

# clone subset there.
git clone git@github.com:dcoello-dev/subset.git

# create config file.
touch subset/config
```

Add your configuration as in next example. If you want more info about how to create your own configuration check [configuration section](./docs/configuration.md).

```json
{
  "user": "your_subset_user",
  "storage": {
    "type": "local_file",
    "file": "/home/home_user/.config/subset/storage"
  },
  "default_domain": "clip",
  "proxy": {
    "type": "mqtt_retain",
    "host": "address_of_your_mqtt_broker",
    "port": 1883,
    "subscribe": "subset/#"
  },
  "domains": {
    "clip": {
      "shared": true,
      "buffer_size": 10,
      "default_source": "xclip",
      "default_sink": "clip"
    },
    "git": {
      "shared": true,
      "buffer_size": 5,
      "default_source": "git_dir",
      "default_sink": "goto_checkout"
    }
  }
}
```

First time generate storage.

```bash
# This will create a storage file in the path specified in conf file.
python3 subset.py --generate
```

And you are ready to go!.

# How to

subset is a CLI tool, it is designed to be integrated with your enviroment preferably through macros.

I am currently using it with [ble.sh](https://github.com/akinomyoga/ble.sh) and [i3](https://i3wm.org/) (you can see adapter examples on `adapters` folder), but I am sure it can be integrated in any other environment (zsh, gnome, windows...).

If you want to check CLI arguments just `--help`:

```bash
$ ~/.config/subset (main)
➜  python3 subset.py -h
usage: subset.py [-h] [-c CONFIG] [-gen] [-a] [-r] [--reset] [-s]
                 [-l] [-i INDEX] [-d DOMAIN] [-u USER] [-v VALUE]

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        configuration file
  -gen, --generate      generate storage
  -a, --add             add elem to domain
  -r, --remove          remove elem from domain
  --reset               reset all elements
  -s, --select          select elem from domain
  -l, --list            list domain elementas
  -i INDEX, --index INDEX
                        elem index
  -d DOMAIN, --domain DOMAIN
                        domain, by default it is taken from
                        configuration file
  -u USER, --user USER  user
  -v VALUE, --value VALUE
                        override value of source action
```

# Your own Use Cases

subset is designed to be extremly easy to extend, if you are interested in change or add something I recomend you to check [design](./docs/design.md) docs.

All contribution are wellcome!!.