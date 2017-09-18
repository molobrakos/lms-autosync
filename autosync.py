#!/usr/bin/env python3

import logging
from sys import argv
from time import sleep
from lms import find_server

_LOGGER = logging.getLogger(__name__)


def _autosync(players):
    # mute all synced inactive players to
    # avoid surprises when starting playing again
    for player in [p for p in players
                   if p.is_synced and not p.is_playing]:
        player.mute()

    # if some other player is playing same content/stream,
    # then auto sync them
    for player in [p for p in players
                   if p.is_playing and
                   not p.is_synced]:

        for other in [p for p in players
                      if p.is_playing and
                      p != player and
                      p.track_id == player.track_id]:

            _LOGGER.info('Autosyncing %s to %s', player.name, other.name)
            other.sync_to(player)
            return


if __name__ == '__main__':
    if '-vv' in argv:
        logging.basicConfig(level=logging.DEBUG)
    elif '-v' in argv:
        logging.basicConfig(level=logging.INFO)

    server = find_server()
    if not server:
        exit('Server not found')
    while True:
        sleep(1)
        _LOGGER.debug('Checking')
        server.update_players()
        _autosync(server.players)
