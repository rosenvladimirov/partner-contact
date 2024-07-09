# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import yaml
from enum import Enum, auto, unique
from datetime import datetime as dt

COMPLEMENTARYSERVICEALLOWANCE = [
    ('BANNED', 'The complementary service is not allowed.'),
    ('ALLOWED', 'The complementary service is allowed (but not required).'),
    ('REQUIRED', 'The complementary service is required.'),
    ]

CARGOTYPE = [
    (1, 'CARGO_TYPE_PARCEL'),
    (2, 'CARGO_TYPE_PALLET'),
    ]

PARAMPICKING = '{\
"billOfLading":%s,\
"takingDate":%s,\
"serviceTypeId":%s,\
"officeToBeCalledId":%s,\
"fixedTimeDelivery":%s,\
"deferredDeliveryWorkDays":%s,\
"backDocumentsRequest":%s,\
"backReceiptRequest":%s,\
"willBringToOffice":%s,\
"willBringToOfficeId":%s,\
"amountInsuranceBase":%s,\
"amountCodBase":%s,\
"payCodToThirdParty":%s,\
"retMoneyTransferReqAmount":%s,\
"parcelsCount":%s,\
"weightDeclared":%s,\
"contents":%s,\
"packing":%s,\
"packId":%s,\
"documents":%s,\
"fragile":%s,\
"palletized":%s,\
"sender":%s,\
"receiver":%s,\
"payerType":%s,\
"payerRefId":%s,\
"payerTypeInsurance":%s,\
"payerRefInsuranceId":%s,\
"payerTypePackings":%s,\
"payerRefPackingsId":%s,\
"noteClient":%s,\
"discCalc":%s,\
"retToClientId":%s,\
"retToOfficeId":%s,\
"ref1":%s,\
"ref2":%s,\
"clientSystemId":%s,\
"parcels":%s,\
"pendingParcelsDescription":%s,\
"pendingShipmentDescription":%s,\
"specialDeliveryId":%s,\
"optionsBeforePayment":%s,\
"retServicesRequest":%s,\
"retShipmentRequest":%s,\
"retThirdPartyPayer":%s,\
"packings":%s,\
"returnVoucher":%s,\
"deliveryToFloorNo":%s,\
"includeShippingPriceInCod":%s,\
"halfWorkDayDelivery":%s,\
"automaticConvertionToWin1251":%s,\
}'


PARAMCALCULATION = '{\
"takingDate":%s,\
"autoAdjustTakingDate":%s,\
"serviceTypeId":%s,\
"willBringToOfficeId":%s,\
"broughtToOffice":%s,\
"officeToBeCalledId":%s,\
"toBeCalled":%s,\
"fixedTimeDelivery":%s,\
"deferredDeliveryWorkDays":%s,\
"amountInsuranceBase":%s,\
"amountCodBase":%s,\
"payCodToThirdParty":%s,\
"parcelsCount":%s,\
"weightDeclared":%s,\
"documents":%s,\
"fragile":%s,\
"palletized":%s,\
"senderId":%s,\
"senderCountryId":%s,\
"senderPostCode":%s,\
"senderSiteId":%s,\
"receiverId":%s,\
"receiverCountryId":%s,\
"receiverPostCode":%s,\
"receiverSiteId":%s,\
"payerType":%s,\
"payerRefId":%s,\
"payerTypeInsurance":%s,\
"payerRefInsuranceId":%s,\
"payerTypePackings":%s,\
"payerRefPackingsId":%s,\
"parcels":%s,\
"specialDeliveryId":%s,\
"includeShippingPriceInCod":%s,\
"checkTBCOfficeWorkDay":%s,\
"ignoreAmountInsuranceBaseIfNotApplicable":%s,\
}'

PARAMCLIENTDATA = '{\
"clientId":%s,\
"partnerName":%s,\
"objectName":%s,\
"address":%s,\
"contactName":%s,\
"phones":%s,\
"email":%s,\
"privatePersonType":%s,\
}'

PARAMADDRESS = '{\
"siteId":%s,\
"siteName":%s,\
"postCode":%s,\
"streetName":%s,\
"streetType":%s,\
"streetId":%s,\
"quarterName":%s,\
"quarterType":%s,\
"quarterId":%s,\
"streetNo":%s,\
"blockNo":%s,\
"entranceNo":%s,\
"floorNo":%s,\
"apartmentNo":%s,\
"addressNote":%s,\
"commonObjectId":%s,\
"coordX":%s,\
"coordY":%s,\
"serializedAddress":%s,\
"countryId":%s,\
"stateId":%s,\
"frnAddressLine1":%s,\
"frnAddressLine1":%s,\
}'

PARAMPHONENUMBER = '{\
"number":%s,\
"internal":%s,\
}'

SIZE = '{\
"width":%s,\
"height":%s,\
"depth":%s,\
}'

PARAMPARCELINFO = '{\
"seqNo":%s,\
"parcelId":%s,\
"packId":%s,\
"size":%s,\
"weight":%s,\
"foreignParcelNumber":%s,\
"predefinedSize":%s,\
}'

PARAMPDF = '{\
"type":%s,\
"ids":%s,\
"includeAutoPrintJS":%s,\
"printerName":%s,\
"additionalBarcodes":%s,\
"additionalBarcodesFormat":%s,\
"additionalCopyForSender":%s,\
}'

PARAMBARCODEINFO = '{\
"barcodeValue":%s,\
"barcodeLabel":%s,\
}'

PARAMFILTERSITE = '{\
"countryId":%s,\
"postCode":%s,\
"name":%s,\
"type":%s,\
"municipality":%s,\
"region":%s,\
"searchString":%s,\
}'

PARAMSEARCHBYREFNUM = '{\
"referenceNumber":%s,\
"searchInField":%s,\
"dateFrom":%s,\
"dateTo":%s,\
"includeReturnBols":%s,\
}'

PARAMPARCEL = '{\
"billOfLading":%s,\
"parcelId":%s,\
"packId":%s,\
"weight":%s,\
"size":%s,\
"foreignParcelNumber":%s,\
"predefinedSize":%s,\
}'

PARAMORDER = '{\
"billOfLadingsToIncludeType":%s,\
"billOfLadingsList":%s,\
"pickupDate":%s,\
"readinessTime":%s,\
"workingEndTime":%s,\
"contactName":%s,\
"phoneNumber":%s,\
}'

PARAMADDRESSSEARCH ='{\
"siteId":%s,\
"quarterId":%s,\
"streetId":%s,\
"commonObjectId":%s,\
"blockNo":%s,\
"streetNo":%s,\
"entranceNo":%s,\
"returnCityCenterIfNoAddress":%s,\
}'

FIXEDDISCOUNTCARDID = '{\
"agreementId":%s,\
"cardId":%s,\
}'

@unique
class ParamLanguage(Enum):
    BG = auto()
    EN = auto()

PARAMLANGUAGE = ParamLanguage

PARAMCLIENTSEARCH = '{\
"clientId":%s,\
"userDefTag":%s,\
"clientName":%s,\
"objectName":%s,\
"phone":%s,\
"siteId":%s,\
}'

PARAMOPTIONSBEFOREPAYMENT = '{\
"open":%s,\
"test":%s,\
"returnServiceTypeId":%s,\
"returnPayerType":%s,\
}'

PARAMPACKINGS = '{\
"packingId":%s,\
"count":%s,\
}'

PARAMFILTERCOUNTRY = '{\
"countryId":%s,\
"name":%s,\
"isoAlhpa2":%s,\
"isoAlpha3":%s,\
}'

PARAMRETURNSERVICEREQUEST = '{\
"serviceTypeId":%s,\
"parcelsCount":%s,\
}'

PARAMRETURNSHIPMENTREQUEST = '{\
"amountInsuranceBase":%s,\
"fragile":%s,\
"parcelsCount":%s,\
"serviceTypeId":%s,\
}'

PARAMSEARCHSECONDARYPICKINGS = '{\
"billOfLading":%s,\
"secondaryPickingType":%s,\
}'

PARAMRETURNVOUCHER = '{\
"serviceTypeId":%s,\
"payerType":%s,\
}'

RESULTLOGIN = '{\
"clientId":%s,\
"sessionId":%s,\
"serverTime":%s,\
}'

RESULTCOURIERSERVICE = '{\
"typeId":%s,\
"name":%s,\
"allowanceFixedTimeDelivery":%s,\
"allowanceCashOnDelivery":%s,\
"allowanceInsurance":%s,\
"allowanceBackDocumentsRequest":%s,\
"allowanceBackReceiptRequest":%s,\
"allowanceToBeCalled":%s,\
"cargoType":%s,\
}'

RESULTCOURIERSERVICE_DEFAULT = (\
-1,\
False,\
'BANNED',\
'BANNED',\
'BANNED',\
'BANNED',\
'BANNED',\
'BANNED',\
1,\
)

RESULTCOURIERSERVICEEXT = '{\
"typeId":%s,\
"name":%s,\
"allowanceFixedTimeDelivery":%s,\
"allowanceCashOnDelivery":%s,\
"allowanceInsurance":%s,\
"allowanceBackDocumentsRequest":%s,\
"allowanceBackReceiptRequest":%s,\
"allowanceToBeCalled":%s,\
"deliveryDeadline":!!timestamp \'%s\',\
"cargoType":%s,\
"allowanceDeliveryToFloor":%s,\
"allowanceOptionsBeforePayment":%s,\
"allowanceReturnVoucher":%s,\
"requireParcelsData":%s,\
}'

RESULTCOURIERSERVICEEXT_DEFAULT = (\
-1,\
False,\
'BANNED',\
'BANNED',\
'BANNED',\
'BANNED',\
'BANNED',\
'BANNED',\
dt.now(),\
1,\
'BANNED',\
'BANNED',\
'BANNED',\
False,\
)

RESULTSITE = '{\
"id":%s,\
"type":%s,\
"name":%s,\
"municipality":%s,\
"region":%s,\
"postCode":%s,\
"addrNomen":%s,\
"countryId":%s,\
"servingOfficeId":%s,\
"coordX":%s,\
"coordY":%s,\
"coordType":%s,\
"servingDays":%s,\
}'

RESULTSITEEX = '{\
"site":%s,\
"exactMatch":%s,\
}'

RESULTCOMMONOBJECT = '{\
"id":%s,\
"type":%s,\
"name":%s,\
"address":%s,\
}'

RESULTSTREET = '{\
"id":%s,\
"type":%s,\
"name":%s,\
"actualName":%s,\
}'

RESULTQUARTER = '{\
"id":%s,\
"type":%s,\
"name":%s,\
"actualName":%s,\
}'

RESULTOFFICEEX = '{\
"id":%s,\
"name":%s,\
"siteId":%s,\
"address":%s,\
"workingTimeFrom":%s,\
"workingTimeTo":%s,\
"workingTimeHalfFrom":%s,\
"workingTimeHalfTo":%s,\
"workingTimeHalfTo":%s,\
"workingTimeDayOffFrom":%s,\
"workingTimeDayOffTo":%s,\
"maxParcelDimensions":%s,\
"maxParcelWeight":%s,\
"workingTimeSchedule":%s,\
"officeType":%s,\
"nearbyOfficeId":%s,\
}'

RESULTBOL = '{\
"generatedParcels":%s,\
"amounts":%s,\
"deadlineDelivery":%s,\
}'

RESULTPARCELINFO = '{\
"seqNo":%s,\
"parcelId":%s,\
}'

RESULTCALCULATION = '{\
"amounts":%s,\
"takingDate":%s,\
"deadlineDelivery":%s,\
"partialDiscount":%s,\
}'

RESULTCALCULATIONMS = '{\
"serviceTypeId":%s,\
"errorDescription":%s,\
"resultInfo":%s,\
}'

RESULTAMOUNTS = '{\
"insuranceBase":%s,\
"insurancePremium":%s,\
"net":%s,\
"discountFixed":%s,\
"discountToOffice":%s,\
"discountToBeCalled":%s,\
"discountAdditional":%s,\
"packings":%s,\
"tro":%s,\
"fixedTimeDelivery":%s,\
"fuelSurcharge":%s,\
"islandSurcharge":%s,\
"codBase":%s,\
"codPremium":%s,\
"vat":%s,\
"total":%s,\
"discPcntFixed":%s,\
"discPcntToOffice":%s,\
"discPcntToBeCalled":%s,\
"discPcntAdditional":%s,\
"pcntFuelSurcharge":%s,\
"heavyPackageFee":%s,\
"discPcntRetShipment":%s,\
"discountRetShipment":%s,\
"specialDelivery":%s,\
"addrPickupSurcharge":%s,\
"addrDeliverySurcharge":%s,\
"nonStdDeliveryDateSurcharge":%s,\
}'

RESULTTRACKPICKINGEX = '{\
"barcode":%s,\
"moment":%s,\
"operationCode":%s,\
"operationDescription":%s,\
"operationComment":%s,\
"siteType":%s,\
"siteName":%s,\
"consignee":%s,\
"returnBillOfLading":%s,\
"redirectBillOfLading":%s,\
"signatureImage":%s,\
"foreignParcelNumber":%s,\
"exceptionCodes":%s,\
"foreignParcelNumbersList":%s,\
"infoURL":%s,\
}'

RESULTCLIENTDATA = '{\
"clientId":%s,\
"partnerName":%s,\
"objectName":%s,\
"address":%s,\
"contactName":%s,\
"phones":%s,\
}'

RESULTADDRESS = '{\
"siteId":%s,\
"siteName":%s,\
"siteType":%s,\
"municipalityName":%s,\
"regionName":%s,\
"postCode":%s,\
"streetName":%s,\
"streetType":%s,\
"streetId":%s,\
"quarterName":%s,\
"quarterType":%s,\
"quarterId":%s,\
"streetNo":%s,\
"blockNo":%s,\
"entranceNo":%s,\
"floorNo":%s,\
"apartmentNo":%s,\
"addressNote":%s,\
"commonObjectId":%s,\
"commonObjectName":%s,\
"countryId":%s,\
"frnAddressLine1":%s,\
"frnAddressLine2":%s,\
"stateId":%s,\
}'

RESULTADDRESSEX = '{\
"resultSite":%s,\
"postCode":%s,\
"streetName":%s,\
"streetType":%s,\
"streetId":%s,\
"quarterName":%s,\
"quarterType":%s,\
"quarterId":%s,\
"streetNo":%s,\
"blockNo":%s,\
"entranceNo":%s,\
"floorNo":%s,\
"apartmentNo":%s,\
"addressNote":%s,\
"coordX":%s,\
"coordY":%s,\
"coordTypeId":%s,\
"commonObjectId":%s,\
"commonObjectName":%s,\
"fullAddressString":%s,\
"siteAddressString":%s,\
"localAddressString":%s,\
"countryId":%s,\
"frnAddressLine1":%s,\
"frnAddressLine2":%s,\
"stateId":%s,\
}'

RESULTPHONENUMBER = '{\
"number":%s,\
"internal":%s,\
}'

RESULTMINMAXREAL = '{\
"minValue":%s,\
"maxValue":%s,\
}'

RESULTMINMAXREAL_DEFAULT = (\
0,\
30,\
)

RESULTORDERPICKINGINFO = '{\
"billOfLading":%s,\
"errorDescriptions":%s,\
}'

RESULTADDRESSSEARCH = '{\
"text":%s,\
"coordX":%s,\
"coordY":%s,\
"microregionId":%s,\
"distanceToSiteCenter":%s,\
"actual":%s,\
"coordType":%s,\
"additionalAddressProcessing":%s,\
}'

COMPLEMENTARYSIRVICEALLOWANCE = '{\
"BANNED":%s,\
"ALLOWED":%s,\
"REQIRED":%s,\
}'

ADDRNOMEN = '{\
"NO":%s,\
"FULL":%s,\
"PARTIAL":%s,\
}'

RESULTSPECIALDELIVERYREQUIREMENT = '{\
"specialDeliveryId":%s,\
"specialDeliveryText":%s,\
"specialDeliveryPrice":%s,\
}'

RESULTADDRESSSTRING = '{\
"siteAddress":%s,\
"localAddress":%s,\
"fullAddress":%s,\
}'

RESULTCOUNTRY = '{\
"countryId":%s,\
"name":%s,\
"isoAlpha2":%s,\
"isoAlpha3":%s,\
"requirePostCode":%s,\
"postCodeFormat":%s,\
"siteNomen":%s,\
"activeCurrencyCode":%s,\
"addressTypeParams":%s,\
}'

RESULTSTATE = '{\
"stateId":%s,\
"name":%s,\
"stateAlpha":%s,\
"countryId":%s,\
}'

RESULTWORKINGTIME = '{\
"date":%s,\
"workingTimeException":%s,\
"workingTimeFrom":%s,\
"workingTimeTo":%s,\
}'

RESULTPICKINGINFO = '{\
"billOfLading":%s,\
"secondaryPickingType":%s,\
"takingDate":%s,\
"serviceTypeId":%s,\
"hasScans":%s,\
}'

RESULTPICKINGEXTENDEDINFO = '{\
"billOfLanding":%s,\
"takingDate":%s,\
"servicetypeId":%s,\
"officeToBeCalledId":%s,\
"fixcedTimeDelivery":%s,\
"deferredDeliveryWorkDays":%s,\
"backDocumentsRequest":%s,\
"backReceiptREquest":%s,\
"willBringToOfficeId":%s,\
"payCodToThirdParty":%s,\
"retMoneyTransferReqAmount":%s,\
"parcelsCount":%s,\
"weightDeclared":%s,\
"weightMeasured":%s,\
"weightCalcilation":%s,\
"contents":%s,\
"packing":%s,\
"documents":%s,\
"fragile":%s,\
"palletized":%s,\
"sender":%s,\
"receiver":%s,\
"payerType":%s,\
"payerRefId":%s,\
"payerTypeInsurance":%s,\
"payerRefInsuranceID":%s,\
"payerTypePackings":%s,\
"payerRefPackingsId":%s,\
"noteClinet":%s,\
"discCalc":%s,\
"retToClinetId":%s,\
"retToOfficeId":%s,\
"ref1":%s,\
"ref2":%s,\
"parcels":%s,\
"palletsListDeclared":%s,\
"palletsListMeasured":%s,\
"palletsListCalcilation":%s,\
"specialDeliveryId":%s,\
"optionsBeforePayment":%s,\
"retServicesRequest":%s,\
"retShipmentRequest":%s,\
"retThirdPartyPayer":%s,\
"packings":%s,\
"returnVoucher":%s,\
"deliveryToFloorNo":%s,\
"amounts":%s,\
"deadlineDelivery":%s,\
"deliveryInfo":%s,\
"codPayment":%s,\
"redirectBillOfLading":%s,\
"returnBillOfLading":%s,\
"primaryPickingBOL":%s,\
"pickingType":%s,\
"pendingParcelsDescription":%s,\
"pendingShipmentDescription":%s,\
"moneyTransferPayment":%s,\
}'

RESULTCLINETINFO = '{\
"clinetId":%s,\
"partnerName":%s,\
"objectName":%s,\
}'

RESULTADDRESSINFO = '{\
"siteID":%s,\
"siteName""%s,\
"siteType":%s,\
"municipalityName":%s,\
"regionName":%s,\
"postCode":%s,\
"streetName":%s,\
"streetType":%s,\
"streetId":%s,\
"quarterName":%s,\
"quarterType":%s,\
"quarterId":%s,\
"streetNo":%s,\
"blockNo":%s,\
"entranceNo":%s,\
"floorNo":%s,\
"apartmentNo":%s,\
"addressNote":%s,\
"commonObjectId":%s,\
"commonObjectName":%s,\
"countryID":%s,\
"frnAddressLine1":%s,\
"trnAddressLine2":%s,\
"stateId":%s,\
}'

RESULTRETURNSERVICEREQUEST ='{\
"serviceTypeId":%s,\
"parcelsCount":%s,\
}'

RESULTPACKINGS = '{\
"packingId":%s,\
"parcelsCount":%s,\
}'

RESULTPARCELINFOEX = '{\
"seqNo":%s,\
"parcelId":%s,\
"weightMeasured":%s,\
"weightDeclared":%s,\
"sizeMeasured":%s,\
"sizeDeclared":%s,\
"foreignParcelNumber":%s,\
"packId":%s,\
"ForeignParcelNumberList":%s,\
}'

RESULTOPTIONSBEFOREPAYMENT = '{\
"open":%s,\
"test":%s,\
"returnServiceTypeId":%s,\
"returnPayerType":%s,\
}'

RESULTRETURSHIPMNETREQUEST= '{\
"amountInsuranceBase":%s,\
"fragile":%s,\
"parcelsCount":%s,\
"serviceTypeId":%s,\
}'

RESULTRETURNVOUCHER ='{\
"serviceTypeId":%s,\
"payerType":%s,\
}'

RESULTDELIVERYINFO = '{\
"deliverydate":%s,\
"consignee":%s,\
"deliceryNote":%s,\
}'

CODPAYMENT = '{\
"date":%s,\
"totalPayedOutAmount":%s,\
}'

CREATEPDFEXRESPONSE = '{\
"pdfBytes":%s,\
"hubId":%s,\
"officeId":%s,\
"deadlineDay":%s,\
"deadlineMonth":%s,\
"tourId":%s,\
"fullBarcode":%s,\
}'

MONEYTRANSFERPAYMENT = '{\
"date":%s,\
"totalPayedOutAmount":%s,\
}'

#  id, CountryName, CountryName_EN, CountryIsoAlpha2, CountryIsoAlpha3, RequirePostCode, PostCodeFormat, RequireState, SiteNomen, ActiveCurrencyCode, DefaultOfficeId
# 100,    БЪЛГАРИЯ,       BULGARIA,               BG,              BGR,            true,        ",NNNN",        false,         1,                BGN,
ADDRESS_1 = {
    'speedy_country_id': ['CountryId', 'ISO country id'],
    'none': ['CountryName', 'Country name in Bulgarian'],
    'none': ['CountryName_EN', 'Country name in English'],
    'code': ['CountryIsoAlpha2', 'ISO alpha 2 code'],
    'none': ['CountryIsoAlpha3', 'ISO alpha 3 code'],
    'post_require': ['RequirePostCode', 'Flag whether post code is required for the country'],
    'none': ['PostCodeFormat', 'Post code format'],
    'none': ['RequireState', 'Flag whether country requires state'],
    'speedy_nom': ['SiteNomen', 'Specifies if Speedy have (or have not) site nomenclature (sites) for this country. Values can be:', 
            [('0', 'Speedy has no site nomenclature for this country.'),
             ('1', 'Speedy has full site nomenclature for this country.'),
             ('2', 'Speedy has partial site nomenclature for this country.'),]],
    'none': ['ActiveCurrencyCode', 'Current active currency code'],
    'speedy_office_id': ['DefaultOfficeId', 'Default office id'],
    }

ADDRESS_50 = {
    'speedy_state_id': ['StateId', 'State id'],
    'speedy_country_id': ['StateCountryId', 'State country id'],
    'none': ['StateName', 'State name in Bulgarian'],
    'none': ['StateName_EN', 'State name in English'],
    'none': ['StateAlpha', 'State alpha code'],
    }

ADDRESS_100 = {
    'speedy_site_id': ['SiteID', 'Site ID'],
    'none': ['SiteType', 'Site type in Bulgarian'],
    'none': ['SiteType_EN', 'Site type in English'],
    'none': ['SiteName', 'Site name in English'],
    'none': ['SiteName_EN', 'Site name in English'],
    'none': ['MunicipalityName', 'Municipality name in Bulgarian'],
    'none': ['MunicipalityName_EN', 'Municipality name in English'],
    'none': ['RegionName', 'Region name in Bulgarian'],
    'none': ['RegionName_EN', 'Region name in English'],
    'none': ['CountryId', 'ISO country id'],
    'zip': ['PostCode', 'Post code'],
    'speedy_nom': ['SiteNomen', 'Specifies if Speedy have (or have not) site nomenclature (sites) for this country. Values can be:', 
            [('0', 'Speedy has no site nomenclature for this country.'),
             ('1', 'Speedy has full site nomenclature for this country.'),
             ('2', 'Speedy has partial site nomenclature for this country.')]],
    'speedy_service_office_id': ['ServingOfficeID', "Serving office's ID"],
    'speedy_hub_office_id': ['ServingHubOfficeID', 'The hub office ID to which serving office is connected'],
    'speedy_work_days': ['ServingDays', 'Serving days for this site. Format: 7 serial digits (0 or 1) where each digit corresponds to a day in week (the first digit corresponds to Monday, the second to Tuesday and so on). Value of \'0\' (zero) means that the site is not served by Speedy on this day while \'1\' (one) means that it is served. (Example: the text \"0100100\" means that the site is served on Tuesday and Friday only.)'],
    'none': ['CoordX', 'GPS X coordinate'],
    'none': ['CoordY', 'GPS Y coordinate'],
    'none': ['CoordType', 'GPS coordinates type id'],
    'none': ['MainSiteId', 'Main Site ID'],
    }

ADDRESS_300 = {
    'speedy_street_id': ['StreetID', 'Street ID'],
    'none': ['StreetType', ' Street type in Bulgarian'],
    'none': ['StreetType_EN', 'Street type in English'],
    'none': ['StreetName', 'Street name in Bulgarian'],
    'none': ['StreetName_EN', 'Street name in English'],
    'none': ['ActualID', 'Actual ID used for old street names, refers to the actual street'],
    'speedy_site_id': ['SiteID', 'Site ID'],
    }

ADDRESS_400 = {
    'speedy_quarter_id': ['QuarterID', 'Quarter ID'],
    'none': ['QuarterType', 'Quarter type in Bulgarian'],
    'none': ['QuarterType_EN', 'Quarter type in English'],
    'none': ['QuarterName', 'Quarter name in Bulgarian'],
    'none': ['QuarterName_EN', 'Quarter name in English'],
    'none': ['ActualID', 'Actual ID used for old quarter names, refers to the actual quarter'],
    'speedy_site_id': ['SiteID', 'Site ID'],
    }

ADDRESS_500 = {
    'speedy_common_object_id': ['CommonObjectID', 'Common object ID'],
    'none': ['CommonObjectType', 'Common object type in Bulgarian'],
    'none': ['CommonObjectType_EN', 'Common object type in English'],
    'none': ['CommonObjectName', 'Common object name in Bulgarian'],
    'none': ['CommonObjectName_EN', 'Common object name in English'],
    'speedy_address': ['Address', 'Address text description of the address'],
    'speedy_site_id': ['SiteID', 'Site ID'],
    }

ADDRESS_700 = {
    'none': ['BlockName', 'Block name in Bulgarian'],
    'none': ['BlockName_EN', 'Block name in English'],
    'speedy_site_id': ['SiteID', 'Site ID'],
    }

ADDRESS_800 = {
    'zip': ['PostCode', 'Site PostCode'],
    'speedy_site_id': ['SiteID', 'Site ID'],
    }

class SpeedyCustomTypes():

    def ParamPicking(params):
        res = yaml.load(PARAMPICKING % params)
        return dict((k,v) for k,v in res.items() if v)

    def ParamCalculation(params):
        res = yaml.load(PARAMCALCULATION % params)
        return dict((k,v) for k,v in res.items() if v)

    def ParamClientData(params):
        res = yaml.load(PARAMCLIENTDATA % params)
        return dict((k,v) for k,v in res.items() if v)

    def ParamAddress(params):
        res = yaml.load(PARAMADDRESS % params)
        return dict((k,v) for k,v in res.items() if v)

    def ParamPhoneNumber(params):
        res = yaml.load(PARAMPHONENUMBER % params)
        return dict((k,v) for k,v in res.items() if v)

    def Size(params):
        res = yaml.load(PARAMPHONENUMBER % params)
        return dict((k,v) for k,v in res.items() if v)

    def ParamParcelInfo(params):
        res = yaml.load(PARAMPARCELINFO % params)
        return dict((k,v) for k,v in res.items() if v)

    def ParamPDF(params):
        res = yaml.load(PARAMPDF % params)
        return dict((k,v) for k,v in res.items() if v)

    def ParamBarcodeInfo(params):
        res = yaml.load(PARAMBARCODEINFO % params)
        return dict((k,v) for k,v in res.items() if v)

    def ParamFilterSite(params):
        res = yaml.load(PARAMFILTERSITE % params)
        return dict((k,v) for k,v in res.items() if v)

    def ParamSearchByRefNum(params):
        res = yaml.load(PARAMSEARCHBYREFNUM % params)
        return dict((k,v) for k,v in res.items() if v)

    def ParamParcel(params):
        res = yaml.load(PARAMPARCEL % params)
        return dict((k,v) for k,v in res.items() if v)

    def ParamOrder(params):
        res = yaml.load(PARAMORDER % params)
        return dict((k,v) for k,v in res.items() if v)

    def ParamAddressSearch(params):
        res = yaml.load(PARAMADDRESSSEARCH % params)
        return dict((k,v) for k,v in res.items() if v)

    def FixedDiscountCardId(params):
        res = yaml.load(FIXEDDISCOUNTCARDID % params)
        return dict((k,v) for k,v in res.items() if v)

    def ParamClientSearch(params):
        res = yaml.load(PARAMCLIENTSEARCH % params)
        return dict((k,v) for k,v in res.items() if v)

    def ParamOptionsBeforePayment(params):
        res = yaml.load(PARAMOPTIONSBEFOREPAYMENT % params)
        return dict((k,v) for k,v in res.items() if v)

    def ParamPackings(params):
        res = yaml.load(PARAMPACKINGS % params)
        return dict((k,v) for k,v in res.items() if v)

    def ParamFilterCountry(params):
        res = yaml.load(PARAMFILTERCOUNTRY % params)
        return dict((k,v) for k,v in res.items() if v)

    def ParamReturnServiceRequest(params):
        res = yaml.load(PARAMRETURNSERVICEREQUEST % params)
        return dict((k,v) for k,v in res.items() if v)

    def ParamReturnShipmentRequest(params):
        res = yaml.load(PARAMRETURNSHIPMENTREQUEST % params)
        return dict((k,v) for k,v in res.items() if v)

    def ParamSearchSecondaryPickings(params):
        res = yaml.load(PARAMSEARCHSECONDARYPICKINGS % params)
        return dict((k,v) for k,v in res.items() if v)

    def ParamReturnVoucher(params):
        res = yaml.load(PARAMSEARCHSECONDARYPICKINGS % params)
        return dict((k,v) for k,v in res.items() if v)

    def getAddressNomenclature(nomenType):
        dictionary = ADDRESS_1
        if nomenType == 50:
            dictionary = ADDRESS_50
        elif nomenType == 100:
            dictionary = ADDRESS_100
        elif nomenType == 300:
            dictionary = ADDRESS_300
        elif nomenType == 400:
            dictionary = ADDRESS_400
        elif nomenType == 500:
            dictionary = ADDRESS_500
        elif nomenType == 700:
            dictionary = ADDRESS_700
        elif nomenType == 800:
            dictionary = ADDRESS_800
        return dictionary

    def getParamLanguage(language='BG'):
        return RESULTCOURIERSERVICE[language].value

    def ResultCourierService(params):
        default = RESULTCOURIERSERVICE_DEFAULT
        res = yaml.load(RESULTCOURIERSERVICE % RESULTCOURIERSERVICE_DEFAULT)
        res.update(params)
        return res

    def ResultCourierServiceExt(params):
        default = RESULTCOURIERSERVICEEXT_DEFAULT
        res = yaml.load(RESULTCOURIERSERVICEEXT % RESULTCOURIERSERVICEEXT_DEFAULT)
        res.update(params)
        return res

    def ResultMinMaxReal(params):
        default = RESULTMINMAXREAL
        res = yaml.load(RESULTMINMAXREAL % RESULTMINMAXREAL_DEFAULT)
        res.update(params)
        return res

    def ResultSiteEx(params):
        return res
