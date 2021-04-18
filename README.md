[![Codacy Badge](https://api.codacy.com/project/badge/Grade/00b415afa9d64866a9bb0781499257c9)](https://www.codacy.com/app/M0NsTeRRR/Dynhost?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=M0NsTeRRR/Dynhost&amp;utm_campaign=Badge_Grade)

The goal of this project is to update your DynDns entries on OVH. It can updates multiple subdomains.

## Requirements
#### Classic
- Python >= 3.7
- Pip3

#### Docker
- Docker CE

## Install

### Classic
Install the requirements `pip install -r requirements.txt`

Fill config.json with your informations (delay : delay between each check of your public address IP (60 <= delay <= 3600))

Start the script `python main.py`

### Docker
Docker version support only one update of DynDns (start many containers to fix the problem)

Fill environment variables

`docker run -d --restart=always -e "DYNHOST_DELAY=" -e "DYNHOST_HOSTANAME=" -e "DYNHOST_USERNAME=" -e "DYNHOST_PASSWORD=" monsterrr/dynhost:latest`

# Licence

The code is under CeCILL license.

You can find all details here: https://cecill.info/licences/Licence_CeCILL_V2.1-en.html

# Credits

Copyright © Ludovic Ortega, 2019

Contributor(s):

-Ortega Ludovic - ludovic.ortega@adminafk.fr
