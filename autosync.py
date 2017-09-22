#!/usr/bin/env python3

import logging
from sys import argv
from time import sleep
from lms import find_server

_LOGGER = logging.getLogger(__name__)


def _autosync(players):
    # mute all synced inactive players to
    # avoid surprises when starting playing again
    for player in players:
        _LOGGER.info('%20s: %s %d%%%s', player.name,
                     player.track_id if player.is_playing else 'idle',
                     player.volume, '(mute)' if player.is_muted else '')

    for player in [p for p in players
                   if p.is_synced
                   and not p.is_playing
                   and not p.is_muted
                   and p.volume != 0]:
        _LOGGER.info('Muting %s', player.name)
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
        level = logging.DEBUG
    elif '-v' in argv:
        level = logging.INFO
    else:
        level = logging.ERROR
    logging.basicConfig(level=level, format='%(asctime)s %(name)s: %(message)s', datefmt='%H:%M:%S')

    server = find_server()
    if not server:
        exit('Server not found')
    while True:
        sleep(1)
        _LOGGER.debug('Checking')
        server.update_players()
        _autosync(server.players)
