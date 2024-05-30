"""Python API for Redback Tech Systems"""
from __future__ import annotations
from aiohttp import ClientResponse, ClientSession
from typing import Any
import asyncio
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
import logging

from .constants import (
    BaseUrl, 
    Endpoint, 
    Header,
    InverterOperationType,
    TIMEOUT,
    AUTH_ERROR_CODES,
    DEVICEINFOREFRESH,
)

from .model import (
    Inverters,
    Batterys,
)
from .exceptions import (
        AuthError, 
        RedbackTechClientError,
)

LOGGER = logging.getLogger(__name__)

class RedbackTechClient:
    """Redback Tech Client"""
    
    def __init__(self, client_id: str, client_secret:str, portal_email: str, portal_password: str, session1: ClientSession | None = None, session2: ClientSession | None = None, timeout: int = TIMEOUT) -> None:
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.portal_email: str = portal_email
        self.portal_password: str = portal_password
        self.timeout: int = timeout
        self.serial_numbers: list[str] | None = None
        self._session1: ClientSession = session1 if session1 else ClientSession()
        self._session2: ClientSession = session2 if session2 else ClientSession()
        self.token: str | None = None
        self.token_type: str | None = None
        self.token_expiration: datetime | None = None
        self._GAFToken: str | None = None
        self._device_info_refresh_time: datetime | None = None
        self._flatInverters = []
        self._flatBatterys = []
        self._redback_devices = []
    
    async def get_redback_data(self):
        """Get Redback Data."""
        #Check if we need to get a new device list
        await self.create_device_info()
        
        inverter_data: dict[str, Inverters] = {}
        battery_data: dict[str, Batterys] = {}
        
        if self._redback_devices is not None:
            for device in self._redback_devices:
                if device['device_type'] == 'inverter':
                    in_instance, in_id = await self._handle_inverter(device)
                    inverter_data[in_id] = in_instance
                    
                if device['device_type'] == 'battery':
                    bat_instance, bat_id = await self._handle_battery(device)
                    battery_data[bat_id] = bat_instance
                    
        
        return
        
    async def api_login(self) -> None:
        """Login to Redback API and obtain token."""
        login_url = f'{BaseUrl.API}{Endpoint.API_AUTH}'

        headers = {
            'Content-Type': Header.CONTENT_TYPE,
        }

        data = b'client_id=' + self.client_id.encode() + b'&client_secret=' + self.client_secret.encode()

        response = await self._api_post(login_url, headers, data)
        self.token = response['token_type'] + ' '+ response['access_token']
        self.token_type = ['token_type']
        self.token_expiration = datetime.now() + timedelta(seconds=response['expires_in'])
        
    async def portal_login(self) -> None:
        """Login to Redback Portal and obtain token."""
        self._session2.cookie_jar.clear()
        login_url = f'{BaseUrl.PORTAL}{Endpoint.PORTAL_LOGIN}'
        response = await self._portal_get(login_url, {}, {})
        await self._get_portal_token(response, 1)
        data={
            "Email": self.portal_email,
            "Password": self.portal_password,
            "__RequestVerificationToken": self._GAFToken
        }
        
        headers = {
            'Referer': Header.REFERER_UI,
        }

        response = await self._portal_post(login_url, headers, data)
        return
    
    async def test_api_connection(self) -> dict[str, Any]:
        """Test API connection."""
        await self._check_token()
        if self.token is not None:
            return True
        return False
    
    async def test_portal_connection(self) -> dict[str, Any]:
        """Test Portal connection."""
        self._GAFToken = None
        await self.portal_login()
        if self._GAFToken is not None:
            return True 
        return False

    async def set_inverter_mode(self, serial_number: str, mode: str, power: int, ross_version: str) -> dict[str, Any]:
        """Set inverter mode."""
        self.serial_number = serial_number
        self.mode = mode
        self.power = power
        self.ross_version = ross_version
        
        await self.portal_login()
        
        full_url = f'{BaseUrl.PORTAL}{Endpoint.PORTAL_CONFIGURE}{self.serial_number}'
        response = await self._portal_get(full_url, {}, {})
        await self._get_portal_token(response, 2)
        headers = {
            'X-Requested-With': Header.X_REQUESTED_WITH,
            'Content-Type': Header.CONTENT_TYPE,
            'Referer': full_url
        }
        data = {
            'SerialNumber':self.serial_number,
            'AppliedTariffId':'',
            'InverterOperation[Type]':InverterOperationType.SET,
            'InverterOperation[Mode]':self.mode,
            'InverterOperation[PowerInWatts]':self.power,
            'InverterOperation[AppliedTarrifId]':'',
            'ProductModelName': '',
            'RossVersion':self.ross_version,
            '__RequestVerificationToken':self._GAFToken     
        }  
        full_url = f'{BaseUrl.PORTAL}{Endpoint.PORTAL_INVERTER_SET}'
        await self._portal_post(full_url, headers, data)
        return
     
    async def get_inverter_list(self) -> dict[str, Any]:
        self.serial_numbers = []
        await self._check_token()
        
        headers = {
            'Authorization': self.token
        }
        full_url = f'{BaseUrl.API}{Endpoint.API_NODES}'
        response = await self._api_get(full_url, headers, {})
        
        for site in response['Data']:
            for node in site['Nodes']:
                if node['Type'] == 'Inverter':
                    self.serial_numbers.append(node['SerialNumber'])
        return self.serial_numbers
    
    async def get_dynamic_by_serial(self, serial_number: str) -> dict[str, Any]:
        """/Api/v2.21/EnergyData/Dynamic/BySerialNumber/{serialNumber}"""
        self.serial_number = serial_number
        await self._check_token()
        
        headers = {
            'Authorization': self.token,
            'Content_type': 'text/json',
            'accept': 'text/plain'
        }
        full_url = f'{BaseUrl.API}{Endpoint.API_ENERGY_DYNAMIC_BY_SERIAL}{self.serial_number}'
        response = await self._api_get(full_url, headers, {})
        return response
    
    async def get_config_by_serial(self, serial_number: str) -> dict[str, Any]:
        """/Api/v2/Configuration/Configuration/BySerialNumber/{serialNumber}"""
        self.serial_number = serial_number
        
        headers = {
            'Authorization': self.token,
            'Content_type': 'text/json',
            'accept': 'text/plain'
        }
        full_url = f'{BaseUrl.API}{Endpoint.API_CONFIG_BY_SERIAL}{self.serial_number}'
        response = await self._api_get(full_url, headers, {})
        return response
    
    async def get_static_by_serial(self, serial_number: str) -> dict[str, Any]:
        """/Api/v2/EnergyData/Static/BySerialNumber/{serialNumber}"""
        self.serial_number = serial_number
        await self._check_token()
        
        headers = {
            'Authorization': self.token,
            'Content_type': 'text/json',
            'accept': 'text/plain'
        }
        full_url = f'{BaseUrl.API}{Endpoint.API_STATIC_BY_SERIAL}{self.serial_number}'
        response = await self._api_get(full_url, headers, {})
        return response
    
    async def get_config_by_multiple_serial(self, serial_numbers: str | None=None) -> dict[str, Any]:
        """"""
        self._serial_numbers: str = serial_numbers if serial_numbers else self.serial_numbers
        
        if self._serial_numbers is None:
            self._serial_numbers = await self.get_inverter_list()
        
        await self._check_token()
        
        headers = {
            'Authorization': self.token,
            'Content_type': 'text/json',
            'accept': 'text/plain'
        }
        
        full_url = f'{BaseUrl.API}{Endpoint.API_STATIC_MULTIPLE_BY_SERIAL}'
        response = await self._api_post_json(full_url, headers, self._serial_numbers)
       
        return response
    

    async def get_site_list(self) -> dict[str, Any]:
        self.site_ids = []
        await self._check_token()
        
        headers = {
            'Authorization': self.token
        }
        full_url = f'{BaseUrl.API}{Endpoint.API_SITES}'
        response = await self._api_get(full_url, headers, {})
        
        for site in response['Data']:
            self.site_ids.append(site)
        return self.site_ids
            
    async def close_sessions(self) -> None:
        """Close sessions."""
        await self._session1.close()
        await self._session2.close()
        return True      

    async def create_device_info(self) -> None:
        device_info = True
        if not await self._check_device_info_refresh():
            #Get the device info if it needs to be refreshed
            self._serial_numbers = await self.get_inverter_list()
            device_info = False
        
        for serial_number in self._serial_numbers:
            response1 = await self.get_static_by_serial(serial_number)
            response2 = await self.get_dynamic_by_serial(serial_number)
            self._flatInverters = await self._convert_static_by_serial_to_inverter_list(response1, response2)
            self._redback_devices.append(self._flatInverters)
            #print(self._flatInverters['serial_number'])
            #response = await self.create_dynamic_info()
            if response1['Data']['Nodes'][0]['StaticData']['BatteryCount'] > 0:
                soc_data = await self.get_config_by_serial(response1['Data']['Nodes'][0]['StaticData']['Id'])
                self._flatBatterys = await self._convert_static_by_serial_to_battery_list(response1, response2, soc_data)
            self._redback_devices.append(self._flatBatterys)
        self._device_info_refresh_time = datetime.now() + timedelta(seconds=DEVICEINFOREFRESH)
        return 
    
    async def create_dynamic_info(self) -> None:

        self._serial_numbers = await self.get_inverter_list()
        self._dynamic_data = []
        for serial_number in self._serial_numbers:
            response = await self.get_dynamic_by_serial(serial_number)
            self._dynamic_data.append(response)
        return
        
    async def _convert_static_by_serial_to_inverter_list(self, data, data2) -> list[str]:
        """Convert static by serial to list."""

        dataDict = {}
        pvId =1
        #static
        dataDict['device_type'] = 'inverter'
        dataDict['model'] = data['Data']['Nodes'][0]['StaticData']['ModelName']
        dataDict['sw_version'] = data['Data']['Nodes'][0]['StaticData']['SoftwareVersion']
        dataDict['hw_version'] = data['Data']['Nodes'][0]['StaticData']['FirmwareVersion']
        dataDict['serial_number'] = data['Data']['Nodes'][0]['StaticData']['Id']
        dataDict['latitude'] = data['Data']['StaticData']['Location']['Latitude']
        dataDict['longitude'] = data['Data']['StaticData']['Location']['Longitude']
        dataDict['network_connection'] = data['Data']['StaticData']['RemoteAccessConnection']['Type']
        dataDict['approved_capacity'] = data['Data']['StaticData']['ApprovedCapacityW']
        dataDict['generation_hard_limit_va'] = data['Data']['StaticData']['SiteDetails']['GenerationHardLimitVA']
        dataDict['generation_soft_limit_va'] = data['Data']['StaticData']['SiteDetails']['GenerationSoftLimitVA']
        dataDict['export_hard_limit_kw'] = data['Data']['StaticData']['SiteDetails']['ExportHardLimitkW']
        dataDict['export_soft_limit_kw'] = data['Data']['StaticData']['SiteDetails']['ExportSoftLimitkW']
        dataDict['site_export_limit_kw'] = data['Data']['StaticData']['SiteDetails']['SiteExportLimitkW']
        dataDict['pv_panel_model'] = data['Data']['StaticData']['SiteDetails']['PanelModel']
        dataDict['pv_panel_size_kw'] = data['Data']['StaticData']['SiteDetails']['PanelSizekW']
        dataDict['system_type'] = data['Data']['StaticData']['SiteDetails']['SystemType']
        dataDict['inverter_max_export_power_kw'] = data['Data']['StaticData']['SiteDetails']['InverterMaxExportPowerkW']
        dataDict['inverter_max_import_power_kw'] = data['Data']['StaticData']['SiteDetails']['InverterMaxImportPowerkW']
        dataDict['commissioning_date'] = data['Data']['StaticData']['CommissioningDate']
        dataDict['model_name'] = data['Data']['Nodes'][0]['StaticData']['ModelName']
        dataDict['nmi'] = data['Data']['StaticData']['NMI']
        dataDict['site_id'] = data['Data']['StaticData']['Id']
        dataDict['inverter_site_type'] = data['Data']['StaticData']['Type']
        dataDict['battery_count'] = data['Data']['Nodes'][0]['StaticData']['BatteryCount']
        dataDict['software_version'] = data['Data']['Nodes'][0]['StaticData']['SoftwareVersion']
        dataDict['firmware_version'] = data['Data']['Nodes'][0]['StaticData']['FirmwareVersion']
        dataDict['inverter_serial_number'] = data['Data']['Nodes'][0]['StaticData']['Id']
        #dynamic
        dataDict['timestamp_utc'] = data2['Data']['TimestampUtc']
        dataDict['frequency_instantaneous'] = data2['Data']['FrequencyInstantaneousHz']
        dataDict['pv_power_instantaneous_kw'] = data2['Data']['PvPowerInstantaneouskW']
        dataDict['inverter_temperature_c'] = data2['Data']['InverterTemperatureC']
        dataDict['pv_all_time_energy_kwh'] = data2['Data']['PvAllTimeEnergykWh']
        dataDict['export_all_time_energy_kwh'] = data2['Data']['ExportAllTimeEnergykWh']
        dataDict['import_all_time_energy_kwh'] = data2['Data']['ImportAllTimeEnergykWh']
        dataDict['load_all_time_energy_kwh'] = data2['Data']['LoadAllTimeEnergykWh']
        dataDict['status'] = data2['Data']['Status']
        dataDict['power_mode_inverter_mode'] = data2['Data']['Inverters'][0]['PowerMode']['InverterMode']
        dataDict['power_mode_power_w'] = data2['Data']['Inverters'][0]['PowerMode']['PowerW']
        for pv in data2['Data']['PVs']:
            dataDict[f'pv_{pvId}_current_a'] = pv['CurrentA']
            dataDict[f'pv_{pvId}_voltage_v'] = pv['VoltageV']
            dataDict[f'pv_{pvId}_power_kw'] = pv['PowerkW']
            pvId += 1
        for phase in data2['Data']['Phases']:  
            phaseAlpha=phase['Id']
            dataDict[f'inverter_phase_{phaseAlpha}_active_exported_power_instantaneous_kw'] = phase['ActiveExportedPowerInstantaneouskW']
            dataDict[f'inverter_phase_{phaseAlpha}_active_imported_power_instantaneous_kw'] = phase['ActiveImportedPowerInstantaneouskW']
            dataDict[f'inverter_phase_{phaseAlpha}_voltage_instantaneous_v'] = phase['VoltageInstantaneousV']
            dataDict[f'inverter_phase_{phaseAlpha}_current_instantaneous_a'] = phase['CurrentInstantaneousA']
            dataDict[f'inverter_phase_{phaseAlpha}_power_factor_instantaneous_minus_1to1'] = phase['PowerFactorInstantaneousMinus1to1']
        return dataDict
    
    async def _convert_static_by_serial_to_battery_list(self, data, data2, soc_data) -> list[str]:
        dataDict = {}
        batteryName = ''
        batteryId = 1
        cabinetId = 1
        dataDict['device_type'] = 'battery'
        dataDict['model'] = data['Data']['Nodes'][0]['StaticData']['ModelName']
        dataDict['sw_version'] = data['Data']['Nodes'][0]['StaticData']['SoftwareVersion']
        dataDict['hw_version'] = data['Data']['Nodes'][0]['StaticData']['FirmwareVersion']
        dataDict['serial_number'] = data['Data']['Nodes'][0]['StaticData']['Id']
        
        dataDict['model'] = data['Data']['Nodes'][0]['StaticData']['ModelName']
        dataDict['sw_version'] = data['Data']['Nodes'][0]['StaticData']['SoftwareVersion']
        dataDict['hw_version'] = data['Data']['Nodes'][0]['StaticData']['FirmwareVersion']
        dataDict['serial_number'] = data['Data']['Nodes'][0]['StaticData']['Id']
        dataDict['min_soc_0_to_1'] = soc_data['Data']['MinSoC0to1']
        dataDict['min_Offgrid_soc_0_to_1'] = soc_data['Data']['MinOffgridSoC0to1']
        dataDict['latitude'] = data['Data']['StaticData']['Location']['Latitude']
        dataDict['longitude'] = data['Data']['StaticData']['Location']['Longitude']
        dataDict['battery_max_charge_power_kw'] = data['Data']['StaticData']['SiteDetails']['BatteryMaxChargePowerkW']
        dataDict['battery_max_discharge_power_kw'] = data['Data']['StaticData']['SiteDetails']['BatteryMaxDischargePowerkW']
        dataDict['battery_capacity_kwh'] = data['Data']['StaticData']['SiteDetails']['BatteryCapacitykWh']
        dataDict['battery_usable_capacity_kwh'] = data['Data']['StaticData']['SiteDetails']['UsableBatteryCapacitykWh']
        dataDict['system_type'] = data['Data']['StaticData']['SiteDetails']['SystemType']
        dataDict['commissioning_date'] = data['Data']['StaticData']['CommissioningDate']
        dataDict['site_id'] = data['Data']['StaticData']['Id']
        dataDict['inverter_site_type'] = data['Data']['StaticData']['Type']
        dataDict['model_name'] = data['Data']['Nodes'][0]['StaticData']['ModelName']
        dataDict['battery_count'] = data['Data']['Nodes'][0]['StaticData']['BatteryCount']
        dataDict['software_version'] = data['Data']['Nodes'][0]['StaticData']['SoftwareVersion']
        dataDict['firmware_version'] = data['Data']['Nodes'][0]['StaticData']['FirmwareVersion']
        for battery in data['Data']['Nodes'][0]['StaticData']['BatteryModels']:
            if battery != 'Unknown':
                batteryName = battery
                dataDict[f'battery_{batteryId}_model'] = batteryName
            else:
                dataDict[f'battery_{batteryId}_model'] = batteryName
            dataDict[f'battery_{batteryId}_current_negative_in_charging_a'] = data2['Data']['Battery']['Modules'][batteryId-1]['CurrentNegativeIsChargingA']
            dataDict[f'battery_{batteryId}_voltage_v'] =  data2['Data']['Battery']['Modules'][batteryId-1]['VoltageV']
            dataDict[f'battery_{batteryId}_power_negative_is_charging_kw'] =  data2['Data']['Battery']['Modules'][batteryId-1]['PowerNegativeIsChargingkW']
            dataDict[f'battery_{batteryId}_soc_0to1'] =  data2['Data']['Battery']['Modules'][batteryId-1]['SoC0To1']
            batteryId += 1
        for cabinet in data2['Data']['Battery']['Cabinets']:
            dataDict[f'battery_cabinet_{cabinetId}_temperature_c'] = cabinet['TemperatureC']
            dataDict[f'battery_cabinet_{cabinetId}_fan_state'] = cabinet['FanState']
            cabinetId += 1
        dataDict['inverter_serial_number'] = data['Data']['Nodes'][0]['StaticData']['Id']
        dataDict['timestamp_utc'] = data2['Data']['TimestampUtc']
        dataDict['battery_soc_instantaneous_0to1'] = data2['Data']['BatterySoCInstantaneous0to1']
        dataDict['battery_power_negative_is_charging_kw'] = data2['Data']['BatteryPowerNegativeIsChargingkW']
        dataDict['battery_charge_all_time_energy_kwh'] = data2['Data']['BatteryChargeAllTimeEnergykWh']
        dataDict['battery_discharge_all_time_energy_kwh'] = data2['Data']['BatteryDischargeAllTimeEnergykWh']
        dataDict['status'] = data2['Data']['Status']
        dataDict['battery_current_negative_in_charging_a'] = data2['Data']['Battery']['CurrentNegativeIsChargingA']
        dataDict['battery_voltage_v'] = data2['Data']['Battery']['VoltageV']
        dataDict['battery_voltage_type'] = data2['Data']['Battery']['VoltageType']
        dataDict['battery_no_of_modules'] = data2['Data']['Battery']['NumberOfModules']
        
        dataDict['battery_currently_stored_kwh'] = (data['Data']['StaticData']['SiteDetails']['BatteryCapacitykWh'] * data2['Data']['BatterySoCInstantaneous0to1'] )
        dataDict['battery_currently_usable_kwh'] = round(data['Data']['StaticData']['SiteDetails']['BatteryCapacitykWh'] * (data2['Data']['BatterySoCInstantaneous0to1']- soc_data['Data']['MinSoC0to1']),2)
        return dataDict
        
    async def _handle_inverter(self, device: dict[str, Any]) -> (Inverters, str):
        """Handle inverter data."""
        
        device_type: str = device['device_type'].lower()

        data = {
            'id': device['serial_number'] + device_type
        }
        
               
        inverter_instance = Inverters(
            id=data['id'],
            device_serial_number=device['serial_number'],
            data=device,
            type=device_type
        )
        return inverter_instance, data['id']

    async def _handle_battery(self, device: dict[str, Any]) -> (Batterys, str):
        """Handle inverter data."""
        
        device_type: str = device['device_type'].lower()
        #inverter_data: dict[str, Any] = {}
        data = {
            'id': device['serial_number'] + device_type
        }
               
        battery_instance = Batterys(
            id=data['id'],
            device_serial_number=device['serial_number'],
            data=device,
            type=device_type
        )
        return battery_instance, data['id']
  
    async def _api_post(self, url: str, headers: dict[str, Any], data ) -> dict[str, Any]:
        """Make POST API call."""

        async with self._session1.post(url, headers=headers, data=data, timeout=self.timeout) as resp:
            return await self._api_response(resp)

    async def _api_post_json(self, url: str, headers: dict[str, Any], data ) -> dict[str, Any]:
        """Make POST API call."""

        async with self._session1.post(url, headers=headers, json=data, timeout=self.timeout) as resp:
            return await self._api_response(resp)
    
        
    async def _api_get(self, url: str, headers: dict[str, Any], data: dict[str, Any]) -> dict[str, Any]:
        """Make GET API call."""

        async with self._session1.get(url, headers=headers, data=data, timeout=self.timeout) as resp:
            return await self._api_response(resp)
 
    @staticmethod
    async def _api_response(resp: ClientResponse): # -> dict[str, Any]:
        """Return response from API call."""

        if resp.status != 200:
            error = await resp.text()
            raise RedbackTechClientError(f'RedbackTech API Error Encountered. Status: {resp.status}; Error: {error}')
        try:
            response: dict[str, Any] = await resp.json()
        except Exception as error:
            raise RedbackTechClientError(f'Could not return json {error}') from error
        if 'error' in response:
            code = response['error'] #['code']
            if code in AUTH_ERROR_CODES:
                raise AuthError(f'Redback API Error: {code}')
#            elif code in SERVER_ERROR_CODES:
#                raise ServerError(f'PetKit Error {code}: {SERVER_ERROR_CODES[code]}')
            else:
                raise RedbackTechClientError(f'RedbackTech API Error: {code}')
        return response

    async def _check_device_info_refresh(self) -> None:
        """Check to see if device info is about to expire.
        If there is no device info, a new device info is obtained. In addition,
        if the current device info is about to expire within 30 minutes
        or has already expired, a new device info is obtained.
        """

        current_dt = datetime.now()
        if self._device_info_refresh_time is None:
            True
        elif (self._device_info_refresh_time-current_dt).total_seconds() < 10:
            True
        else:
            return False

    async def _check_token(self) -> None:
        """Check to see if there is a valid token or if token is about to expire.
        If there is no token, a new token is obtained. In addition,
        if the current token is about to expire within 60 minutes
        or has already expired, a new token is obtained.
        """

        current_dt = datetime.now()
        if (self.token or self.token_expiration) is None:
            await self.api_login()
        elif (self.token_expiration-current_dt).total_seconds() < 3600:
            await self.api_login()
        else:
            return None
    
    async def _get_portal_token(self, response, type):
        soup = BeautifulSoup(response , features="html.parser")
        if type == 1: #LOGINURL:
            form = soup.find("form", class_="login-form")
        else:
            form = soup.find('form', id='GlobalAntiForgeryToken')
        hidden_input = form.find("input", type="hidden")
        self._GAFToken = hidden_input.attrs['value']
        return     

    async def _portal_post(self, url: str, headers: dict[str, Any], data ) -> dict[str, Any]:
        """Make POST Portal call."""

        async with self._session2.post(url, headers=headers, data=data, timeout=self.timeout) as resp:
            return await self._portal_response(resp)
        
    async def _portal_get(self, url: str, headers: dict[str, Any], data: dict[str, Any]) -> dict[str, Any]:
        """Make GET Portal call."""

        async with self._session2.get(url, headers=headers, data=data, timeout=self.timeout) as resp:
            return await self._portal_response(resp)
 
    @staticmethod
    async def _portal_response(resp: ClientResponse): # -> dict[str, Any]:
        """Return response from Portal call."""

        if resp.status != 200:
            error = await resp.text()
            raise RedbackTechClientError(f'RedbackTech API Error Encountered. Status: {resp.status}; Error: {error}')
        try:
            response: dict[str, Any] = await resp.text()
        except Exception as error:
            raise RedbackTechClientError(f'Could not return text {error}') from error

        return response
