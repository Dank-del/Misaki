# Copyright (C) 2018 - 2020 MrYacha. All rights reserved. Source code available under the AGPL.
# Copyright (C) 2019 Aiogram
#
# This file is part of MisakiBot.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pymongo import DeleteOne

from misaki.services.mongo import mongodb
from misaki.utils.logger import log

log.info('Misaki Database v6')
log.info("Feds: fix str user_id and fix duplications")
log.info('Starting updating all feds...')

queue = []

all_bans = mongodb.fed_bans.find({'user_id': {'$type': 'string'}})
all_bans_count = all_bans.count()
changed_feds = 0

for counter, ban in enumerate(all_bans):
    changed_feds += 1
    queue.append(DeleteOne({'_id': ban['_id']}))

mongodb.fed_bans.bulk_write(queue)

log.info('Update done!')
log.info('Modified feds - ' + str(changed_feds))