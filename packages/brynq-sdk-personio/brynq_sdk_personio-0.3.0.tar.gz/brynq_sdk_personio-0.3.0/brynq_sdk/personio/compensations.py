import requests
import pandas as pd
import json

class Compensations:

    def __init__(self, headers, base_url):
        self.headers = headers
        self.base_url = base_url

    def list_compensation_types(self, limit=100):
        """
        Returns a list of Compensation Types for an authorized company. The types include one-time and recurring Compensation Types. Bonuses should use recurring or one time types.
        """
        url = f'{self.base_url}compensations/types?limit={limit}'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        df = pd.DataFrame(response.json()['_data'])
        return df

    def list_compensations(self, limit=100, start_date=None, end_date=None, person_id=None, entity_id=None):
        """
        Returns a list of payroll compensations of people for an authorized company. Compensations listed include base salary (excluding proration), hourly, one time compensation, recurring compensation, and bonuses.
        :param limit: The maximum number of compensations to fetch. Default is 100.
        :param start_date: A start date from which compensations are run. The duration (end_date - start_date) must be equal to or smaller than a month. The format is ISO-8601.
                            Default is the first day of the current month in case end_date is not provided, or the first day of the month of the provided end_date.
        :param end_date: An end date to which compensations are run. The duration (end_date - start_date) must be equal or smaller than a month.
                            Format is ISO-8601. Default is the last day of the current month in case start_date is not provided, or the last day of the month of the provided start_date.
        :param person_id: Filter results matching one or more provided person ids that belong to the company. Divide by comma: 1,2,3
        :param entity_id: Filter results matching one or more provided legal entity ids that belong to the company.. Divide by comma: 1,2,3
        """
        base_url = f'{self.base_url}compensations'
        payload = {
            'limit': limit
        }
        if start_date:
            payload['start_date'] = start_date
        if end_date:
            payload['end_date'] = end_date
        if person_id:
            payload['person_id'] = person_id
        if entity_id:
            payload['entity_id'] = entity_id
        df = pd.DataFrame()
        url = base_url
        while True:
            response = requests.get(url, headers=self.headers, data=json.dumps(payload))
            response.raise_for_status()
            df_temp = pd.json_normalize(response.json()['_data'])
            df = pd.concat([df, df_temp])
            cursor = response.json().get('_meta', {}).get('links', {}).get('next', {}).get('href')
            if cursor:
                url = cursor
            else:
                break

        df.columns = df.columns.str.replace('.', '_')
        return df