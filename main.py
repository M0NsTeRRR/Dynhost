# ----------------------------------------------------------------------------
# Copyright © Ludovic Ortega, 2019
#
# Contributeur(s):
#     * Ortega Ludovic - mastership@hotmail.fr
#
# Ce logiciel, Dynhost, est un programme informatique servant à mettre à jour des entrées DynDns
# chez OVH
#
# Ce logiciel est régi par la licence CeCILL soumise au droit français et
# respectant les principes de diffusion des logiciels libres. Vous pouvez
# utiliser, modifier et/ou redistribuer ce programme sous les conditions
# de la licence CeCILL telle que diffusée par le CEA, le CNRS et l'INRIA
# sur le site "http://www.cecill.info".
#
# En contrepartie de l'accessibilité au code source et des droits de copie,
# de modification et de redistribution accordés par cette licence, il n'est
# offert aux utilisateurs qu'une garantie limitée.  Pour les mêmes raisons,
# seule une responsabilité restreinte pèse sur l'auteur du programme,  le
# titulaire des droits patrimoniaux et les concédants successifs.
#
# A cet égard  l'attention de l'utilisateur est attirée sur les risques
# associés au chargement,  à l'utilisation,  à la modification et/ou au
# développement et à la reproduction du logiciel par l'utilisateur étant
# donné sa spécificité de logiciel libre, qui peut le rendre complexe à
# manipuler et qui le réserve donc à des développeurs et des professionnels
# avertis possédant  des  connaissances  informatiques approfondies.  Les
# utilisateurs sont donc invités à charger  et  tester  l'adéquation  du
# logiciel à leurs besoins dans des conditions permettant d'assurer la
# sécurité de leurs systèmes et ou de leurs données et, plus généralement,
# à l'utiliser et l'exploiter dans les mêmes conditions de sécurité.
#
# Le fait que vous puissiez accéder à cet en-tête signifie que vous avez
# pris connaissance de la licence CeCILL, et que vous en avez accepté les
# termes.
# ----------------------------------------------------------------------------

import logging
from json import load
from sys import exit
from datetime import datetime
from time import sleep
from requests import get

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# endpoint to get this public address IP
urlIP = [
    'https://api.ipify.org',
    'https://ipinfo.io/ip',
    'https://ifconfig.me/'
]

# current IP address
currentIP = ''

IPfound = False

def getIP(url):
    """
    Get public address IP
    """
    r = get(url)
    if r.status_code == 200:
        return r.text.strip()
    else:
        raise Exception('Can\'t get IP from : {url}'.format(url))

def updateDyndns(hostname, ip, username, password):
    """
    Update DynDns entry
    """
    payload = {'system': 'dyndns', 'hostname': hostname, 'myip': ip}
    r = get('https://www.ovh.com/nic/update', params=payload, auth=(username, password))
    if r.status_code == 200:
        logger.info('DynDns with hostname : {hostname} updated with ip : {ip}'.format(hostname=hostname, ip=ip))
    else:
        raise Exception('An error occured when tried to update DynDNS HTTP error : {HTTP_CODE}, HTTP message : {HTTP_MESSAGE}'.format(HTTP_CODE=r.status_code, HTTP_MESSAGE=r.text))

# get DynDns configuration
try:
    with open('config.json') as json_data_file:
        config = load(json_data_file)

    if "delay" not in config or 60 <= config["delay"] >= 3600:
        raise Exception("config.json not filled properly")
    for dyndns in config['dyndns']:
        for parameter in ["hostname", "username", "password"]:
            if parameter not in dyndns or not isinstance(dyndns[parameter], str):
                raise Exception("config.json not filled properly")
except Exception as e:
    logger.error("{error}".format(error=e))
    exit(1)

logger.info('Dynhost started')

while True:
    while not IPfound:
        for url in urlIP:
            try:
                resultIP = getIP(url)
                if currentIP != resultIP:
                    currentIP = resultIP
                    logger.info('New public IP address detected : {ip}'.format(ip=currentIP))
                    for dyndns in config['dyndns']:
                        updateDyndns(dyndns['hostname'], currentIP, dyndns['username'], dyndns['password'])
                IPfound = True
            except Exception as e:
                logger.error("{error}".format(error=e))
        sleep(10)
    IPfound = False
    sleep(config["delay"])