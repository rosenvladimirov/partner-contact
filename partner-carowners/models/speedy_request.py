# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
import binascii
import io
import PIL.PdfImagePlugin   # activate PDF support in PIL
from PIL import Image
import logging
import os
import re
import urllib.parse

import suds
from suds.client import Client
from suds.plugin import MessagePlugin
from suds.sax.element import Element

from datetime import datetime as dt
from zeep import Client

SUDS_VERSION = suds.__version__

from odoo import _
from .speedy_parcer import SpeedyCustomTypes as parcer

_logger = logging.getLogger(__name__)

class LogPlugin(MessagePlugin):
    def __init__(self, debug_logger):
        self.debug_logger = debug_logger

    def sending(self, context):
        self.debug_logger(context.envelope, 'speedy_request')

    def received(self, context):
        self.debug_logger(context.reply, 'speedy_response')

class SpeedyRequest():
    def __init__(self, debug_logger, username, password, prod_environment):
        self.debug_logger = debug_logger
        # Product and Testing url
        self.endurl = "https://www.speedy.bg/"
        if not prod_environment:
            self.endurl = "https://www.speedy.bg/"
        self.wsdl = '../eps/main01.wsdl'
        self.username = username
        self.password = password
        self.session_id = False

        self.client = Client(urllib.parse.urljoin(self.endurl, self.wsdl))
        return self._check_active_session()

    def get_error_message(self, error_code, description):
        result = {}
        result['error_message'] = SPEEDY_ERROR_MAP.get(error_code)
        if not result['error_message']:
            result['error_message'] = description
        return result

    def _check_active_session(self, refreshsession=True):
        ret = self.client.service.isSessionActive(self.session_id, refreshsession)
        if not ret:
            session = self.client.service.login(self.username, self.password)
            self.client_id = session['clientId']
            self.session_id = session['sessionId']
            self.session_datetime = session['serverTime']
            ret = True
        return ret

    def _listServices(self, service, date=dt.now()):
        ret = False
        if not self._check_active_session(True):
            ret = parcer.ResultCourierService(self.client.service.listServices(self.session_id, date))
            for line in ret:
                res = service.search([('code', '', ret['typeId']), ('last_date', '<=', date)])
                if res:
                    res.write({
                        'name': ret['name'],
                        'last_date': date,
                        'allowanceFixedTimeDelivery': ret['allowanceFixedTimeDelivery'],
                        'allowanceCashOnDelivery': ret['allowanceCashOnDelivery'],
                        'allowanceInsurance': ret['allowanceInsurance'],
                        'allowanceBackDocumentsRequest': ret['allowanceBackDocumentsRequest'],
                        'allowanceBackReceiptRequest': ret['allowanceBackReceiptRequest'],
                        'allowanceToBeCalled': ret['allowanceToBeCalled'],
                        'cargoType': ret['cargoType'],
                        })
                else:
                    res.create({
                        'code': ret['typeId'],
                        'name': ret['name'],
                        'last_date': date,
                        'allowanceFixedTimeDelivery': ret['allowanceFixedTimeDelivery'],
                        'allowanceCashOnDelivery': ret['allowanceCashOnDelivery'],
                        'allowanceInsurance': ret['allowanceInsurance'],
                        'allowanceBackDocumentsRequest': ret['allowanceBackDocumentsRequest'],
                        'allowanceBackReceiptRequest': ret['allowanceBackReceiptRequest'],
                        'allowanceToBeCalled': ret['allowanceToBeCalled'],
                        'cargoType': ret['cargoType'],
                        })
        return ret

    def _getAddressNomenclature(self, model, field, operator="ilike", nomenType=1, country=100):
        res_address = []
        if not self._check_active_session(True):
            dictionary = parcer.getAddressNomenclature(nomenType)
            ret = self.client.service.getAddressNomenclature(self.session_id, nomenType, country)
            res = StringIO(ret)
            address = csv.DictReader(res, delimiter=',')
            for line in address:
                row = dict(line)
                res_address.append(row)
                save = dictionary.get(field, False)
                if save:
                    model.search([(field, operator, row[save[0]])])
                    if model:
                        model.write({field: row[save[0]]})
        return res_address

    def _listServicesForSites(self, sender_site_id, receiver_site_id, sender_country_id, sender_post_code, receiver_country_id, receiver_post_code, sender_id, receiver_id, sender_office_id, receiver_office_id, date=dt.now(), language='BG'):
        ret = False
        if not self._check_active_session(True):
            lang = parder.getParamLanguage(language)
            ret = parcer.listServicesForSites(self.client.service.listServicesForSites(self.session_id, date, sender_site_id, receiver_site_id, sender_country_id, sender_post_code, receiver_country_id, receiver_post_code, lang, sender_id, receiver_id, sender_office_id, receiver_office_id))
        return parcer.ResultCourierServiceExt(ret)

    def _getWeightInterval(self, service_type_id, sender_site_id, sender_country_id, sender_post_code, receiver_country_id, receiver_post_code, sender_id, receiver_id, sender_office_id, receiver_office_id, date=dt.now(), documents=False):
        ret = False
        if not self._check_active_session(True):
            ret = parcer.getWeightInterval(self.client.service.getWeightInterval(self.session_id, service_type_id, sender_site_id, date, documents, sender_country_id, sender_post_code, receiver_country_id, receiver_post_code, sender_id, receiver_id, sender_office_id, receiver_office_id))
        return parcer.ResultMinMaxReal(ret)

    def _listSitesEx(self):
        ret = False
        if not self._check_active_session(True):
            ret = parcer.listSitesEx(self.client.service.listSitesEx(self.session_id,))
        return parcer.ResultSiteEx(ret)
