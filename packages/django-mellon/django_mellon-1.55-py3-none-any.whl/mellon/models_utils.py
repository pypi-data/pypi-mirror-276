# django-mellon - SAML2 authentication for Django
# Copyright (C) 2014-2019 Entr'ouvert
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

from . import models, utils


def get_issuer(entity_id):
    idp = utils.get_idp(entity_id)
    slug = idp.get('SLUG')
    issuer = None
    if slug:
        issuer = models.Issuer.objects.filter(slug=slug).first()
        # migrate issuer entity_id based on the slug
        if issuer and issuer.entity_id != entity_id:
            issuer.entity_id = entity_id
            issuer.save()

    if issuer is None:
        issuer, _ = models.Issuer.objects.get_or_create(entity_id=entity_id)
        # migrate issuer slug based on the entity_id
        if issuer.slug != slug:
            issuer.slug = slug
            issuer.save()
    return issuer
