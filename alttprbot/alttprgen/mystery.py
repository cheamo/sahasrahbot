import os
import random

import aiofiles
import pyz3r
import yaml

from alttprbot.util.alttpr_discord import alttpr
from alttprbot.util.http import request_generic


class WeightsetNotFoundException(Exception):
    pass


async def generate_random_game(weightset='weighted', tournament=True,
                               spoilers="off", custom_weightset_url=None):
    basename = os.path.basename(f'{weightset}.yaml')

    if not weightset == 'custom':
        try:
            async with aiofiles.open(os.path.join("weights", basename)) as f:
                weights = yaml.load(await f.read(), Loader=yaml.FullLoader)
        except FileNotFoundError:
            raise WeightsetNotFoundException(
                (f'Could not find weightset {weightset}. '
                 f'See a list of available weights at <https://l.synack.live/weights>'))
    elif weightset == 'custom' and custom_weightset_url:
        weights = await request_generic(custom_weightset_url, method='get', returntype='yaml')

    settings = pyz3r.mystery.generate_random_settings(
        weights=weights, spoilers=spoilers, tournament=tournament)

    seed = await alttpr(settings=settings)
    return seed


def get_random_option(optset):
    return random.choices(population=list(optset.keys()), weights=list(optset.values()))[0]
