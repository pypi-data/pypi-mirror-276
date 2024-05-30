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


import base64
import hashlib
from unittest import mock
from urllib.parse import parse_qs, urlparse

import lasso
import pytest
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlencode
from httmock import HTTMock
from utils import error_500, html_response
from xml_utils import assert_xml_constraints

pytestmark = pytest.mark.django_db


def test_null_character_on_samlresponse_post(app):
    app.post(reverse('mellon_login'), params={'SAMLResponse': '\x00'}, status=400)


def test_metadata(private_settings, app):
    ns = {
        'sm': 'urn:oasis:names:tc:SAML:2.0:metadata',
        'ds': 'http://www.w3.org/2000/09/xmldsig#',
    }
    private_settings.MELLON_PUBLIC_KEYS = ['xxx', '/yyy']
    private_settings.MELLON_NAME_ID_FORMATS = [lasso.SAML2_NAME_IDENTIFIER_FORMAT_UNSPECIFIED]
    private_settings.MELLON_DEFAULT_ASSERTION_CONSUMER_BINDING = 'artifact'
    private_settings.MELLON_ORGANIZATION = {
        'NAMES': [
            'Foobar',
            {
                'LABEL': 'FoobarEnglish',
                'LANG': 'en',
            },
        ],
        'DISPLAY_NAMES': [
            'Foobar',
            {
                'LABEL': 'FoobarEnglish',
                'LANG': 'en',
            },
        ],
        'URLS': [
            'https://foobar.com/',
            {
                'URL': 'https://foobar.com/en/',
                'LANG': 'en',
            },
        ],
    }
    private_settings.MELLON_CONTACT_PERSONS = [
        {
            'CONTACT_TYPE': 'administrative',
            'COMPANY': 'FooBar',
            'GIVENNAME': 'John',
            'SURNAME': 'Doe',
            'EMAIL_ADDRESSES': [
                'john.doe@foobar.com',
                'john.doe@personal-email.com',
            ],
            'TELEPHONE_NUMBERS': [
                '+abcd',
                '+1234',
            ],
        },
        {
            'CONTACT_TYPE': 'technical',
            'COMPANY': 'FooBar2',
            'GIVENNAME': 'John',
            'SURNAME': 'Doe',
            'EMAIL_ADDRESSES': [
                'john.doe@foobar.com',
                'john.doe@personal-email.com',
            ],
            'TELEPHONE_NUMBERS': [
                '+abcd',
                '+1234',
            ],
        },
    ]

    with mock.patch('mellon.utils.open', mock.mock_open(read_data='BEGIN\nyyy\nEND'), create=True):
        response = app.get('/metadata/')
    assert_xml_constraints(
        response.content,
        (
            '/sm:EntityDescriptor[@entityID="https://testserver/metadata/"]',
            1,
            ('/*', 4),
            (
                '/sm:SPSSODescriptor',
                1,
                ('/*', 7),
                ('/sm:NameIDFormat', 1),
                ('/sm:SingleLogoutService', 2),
                (
                    '/sm:AssertionConsumerService',
                    None,
                    (
                        '[@isDefault="true"]',
                        None,
                        ('[@Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Artifact"]', 1),
                        ('[@Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"]', 0),
                    ),
                    ('[@Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"]', 1),
                ),
                (
                    '/sm:KeyDescriptor/ds:KeyInfo/ds:X509Data',
                    2,
                    ('/ds:X509Certificate', 2),
                    ('/ds:X509Certificate[text()="xxx"]', 1),
                    ('/ds:X509Certificate[text()="yyy"]', 1),
                ),
            ),
            (
                '/sm:Organization',
                1,
                ('/sm:OrganizationName', 2),
                ('/sm:OrganizationName[text()="Foobar"]', 1),
                ('/sm:OrganizationName[text()="FoobarEnglish"]', 1, ('[@xml:lang="en"]', 1)),
                ('/sm:OrganizationDisplayName', 2),
                ('/sm:OrganizationDisplayName[text()="Foobar"]', 1),
                ('/sm:OrganizationDisplayName[text()="FoobarEnglish"]', 1, ('[@xml:lang="en"]', 1)),
                ('/sm:OrganizationURL', 2),
                ('/sm:OrganizationURL[text()="https://foobar.com/"]', 1),
                ('/sm:OrganizationURL[text()="https://foobar.com/en/"]', 1, ('[@xml:lang="en"]', 1)),
            ),
            (
                '/sm:ContactPerson',
                2,
                ('[@contactType="technical"]', 1),
                ('[@contactType="administrative"]', 1),
            ),
        ),
        namespaces=ns,
    )


def test_sp_initiated_login_improperly_configured2(private_settings, app):
    private_settings.MELLON_IDENTITY_PROVIDERS = []
    response = app.get('/login/', status=400)
    assert 'no idp found' in response


def test_sp_initiated_login_discovery_service(private_settings, app):
    private_settings.MELLON_DISCOVERY_SERVICE_URL = 'https://disco'
    response = app.get('/login/')
    assert response.status_code == 302
    params = parse_qs(urlparse(response['Location']).query)
    assert response['Location'].startswith('https://disco?')
    assert params == {
        'return': ['https://testserver/login/?nodisco=1'],
        'entityID': ['https://testserver/metadata/'],
    }


def test_sp_initiated_login_discovery_service_passive(private_settings, app):
    private_settings.MELLON_DISCOVERY_SERVICE_URL = 'https://disco'
    response = app.get('/login/?passive=1')
    assert response.status_code == 302
    params = parse_qs(urlparse(response['Location']).query)
    assert response['Location'].startswith('https://disco?')
    assert params == {
        'isPassive': ['true'],
        'entityID': ['https://testserver/metadata/'],
        'return': ['https://testserver/login/?passive=1&nodisco=1'],
    }


def test_sp_initiated_login_discovery_service_nodisco(private_settings, app):
    private_settings.MELLON_IDENTITY_PROVIDERS = []
    private_settings.MELLON_DISCOVERY_SERVICE_URL = 'https://disco'
    response = app.get('/login/?nodisco=1', status=400)
    assert 'no idp found' in response


def test_sp_initiated_login(private_settings, app):
    private_settings.MELLON_IDENTITY_PROVIDERS = [
        {
            'METADATA': open('tests/metadata.xml').read(),
        }
    ]
    response = app.get('/login/?next=%2Fwhatever')
    assert response.status_code == 302
    params = parse_qs(urlparse(response['Location']).query)
    assert response['Location'].startswith('https://idp5/singleSignOn?')
    assert set(params.keys()) == {'SAMLRequest', 'RelayState'}
    assert len(params['SAMLRequest']) == 1
    assert base64.b64decode(params['SAMLRequest'][0])
    assert app.session['mellon_next_url_%s' % params['RelayState'][0]] == '/whatever'


def test_sp_initiated_login_chosen(private_settings, app):
    private_settings.MELLON_IDENTITY_PROVIDERS = [
        {
            'METADATA': open('tests/metadata.xml').read(),
        }
    ]
    qs = urlencode(
        {
            'entityID': 'https://idp5/metadata',
            'next': '/whatever',
        }
    )
    response = app.get('/login/?' + qs)
    assert response.status_code == 302
    params = parse_qs(urlparse(response['Location']).query)
    assert response['Location'].startswith('https://idp5/singleSignOn?')
    assert set(params.keys()) == {'SAMLRequest', 'RelayState'}
    assert len(params['SAMLRequest']) == 1
    assert base64.b64decode(params['SAMLRequest'][0])
    assert app.session['mellon_next_url_%s' % params['RelayState'][0]] == '/whatever'


def test_sp_initiated_login_requested_authn_context(private_settings, app):
    private_settings.MELLON_IDENTITY_PROVIDERS = [
        {
            'METADATA': open('tests/metadata.xml').read(),
            'AUTHN_CLASSREF': ['urn:be:fedict:iam:fas:citizen:eid', 'urn:be:fedict:iam:fas:citizen:token'],
        }
    ]
    response = app.get('/login/')
    assert response.status_code == 302
    params = parse_qs(urlparse(response['Location']).query)
    assert response['Location'].startswith('https://idp5/singleSignOn?')
    assert list(params.keys()) == ['SAMLRequest']
    assert len(params['SAMLRequest']) == 1
    assert base64.b64decode(params['SAMLRequest'][0])
    request = lasso.Samlp2AuthnRequest()
    assert request.initFromQuery(urlparse(response['Location']).query)
    assert request.requestedAuthnContext.authnContextClassRef == (
        'urn:be:fedict:iam:fas:citizen:eid',
        'urn:be:fedict:iam:fas:citizen:token',
    )


def test_malfortmed_artifact(private_settings, app, caplog):
    private_settings.MELLON_IDENTITY_PROVIDERS = [
        {
            'METADATA': open('tests/metadata.xml').read(),
        }
    ]
    response = app.get('/login/?SAMLart=xxx', status=400)
    assert response['Content-Type'] == 'text/plain'
    assert response['X-Content-Type-Options'] == 'nosniff'
    assert b'artifact is malformed' in response.content
    assert 'artifact is malformed' in caplog.text


@pytest.fixture
def artifact():
    entity_id = b'https://idp5/metadata'
    token = b'x' * 20
    return force_str(base64.b64encode(b'\x00\x04\x00\x00' + hashlib.sha1(entity_id).digest() + token))


def test_error_500_on_artifact_resolve(private_settings, app, caplog, artifact):
    private_settings.MELLON_IDENTITY_PROVIDERS = [
        {
            'METADATA': open('tests/metadata.xml').read(),
        }
    ]
    with HTTMock(error_500):
        app.get('/login/?SAMLart=%s' % artifact)
    assert 'IdP returned 500' in caplog.text


def test_invalid_msg_on_artifact_resolve(private_settings, app, caplog, artifact):
    private_settings.MELLON_IDENTITY_PROVIDERS = [
        {
            'METADATA': open('tests/metadata.xml').read(),
        }
    ]
    with HTTMock(html_response):
        app.get('/login/?SAMLart=%s' % artifact, status=400)
    assert 'ArtifactResolveResponse is malformed' in caplog.text


def test_private_key_unreadable(private_settings, app, tmpdir):
    private_settings.MELLON_IDENTITY_PROVIDERS = [
        {
            'METADATA': open('tests/metadata.xml').read(),
        }
    ]
    # set an unreadable private key
    private_key = tmpdir / 'private.key'
    with private_key.open(mode='w') as fd:
        fd.write('1')
    private_key.chmod(0o000)
    private_settings.MELLON_PRIVATE_KEY = str(private_key)
    response = app.get('/login/?next=%2Fwhatever')
    assert 'Unable to initialize a SAML server object' in response
