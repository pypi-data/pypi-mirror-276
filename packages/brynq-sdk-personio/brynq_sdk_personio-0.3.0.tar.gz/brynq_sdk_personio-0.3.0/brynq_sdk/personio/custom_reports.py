import requests
import pandas as pd
import json


class CustomReports:

    def __init__(self, headers, base_url):
        self.headers = headers
        self.base_url = base_url

    def _flatten_items(self, items):
        flattened_data = []
        for item in items:
            employee_id = item['employee_id']
            historical_attributes = item['historical_attributes']
            record = {'employee_id': employee_id}

            for attr in historical_attributes:
                attribute_id = attr['attribute_id']
                value = attr.get('value', None)
                amount = attr.get('amount', None)
                effective_date = attr['effective_date']

                if value is not None:
                    record[attribute_id] = value
                    record[f'{attribute_id}_effective_date'] = effective_date
                if amount is not None:
                    record[attribute_id] = amount
                    record[f'{attribute_id}_effective_date'] = effective_date

            flattened_data.append(record)
        return flattened_data

    def list_custom_reports(self, report_ids=None, status=None):
        """
        This endpoint provides you with metadata about existing custom reports in your Personio account, such as report name, report type, report date / timeframe.
        :param report_ids: A list of report ID's to filter the results. Divide by comma: 1,2,3
        :param status: The status of the report to filter the results. Possible values are: up_to_date
        """
        url = f'{self.base_url}company/custom-reports/reports?'
        payload = {}
        if report_ids:
            payload['report_ids'] = report_ids
        if status:
            possible_statusses = ['up_to_date']
            if status not in possible_statusses:
                raise ValueError(f'status must be one of: \"{possible_statusses}\"')
            payload['status'] = status
        response = requests.get(url, headers=self.headers, data=json.dumps(payload))
        response.raise_for_status()
        df = pd.json_normalize(response.json()['data'][0]['attributes'])
        return df

    def get_custom_report(self, report_id, limit=100, page=1, locale=None):
        """
        This endpoint provides you with the data of an existing Custom Report.
        :param report_id: The ID of the report to fetch the data.
        :param limit: Pagination parameter to limit the number of employees returned per page. Default is 100.
        :param page: Pagination parameter to identify the page to return. Default = 1.
        :param locale: locale used to translate localized fields.
        """
        url = f'{self.base_url}company/custom-reports/reports/{report_id}'
        payload = {
            'limit': limit,
            'page': 1
        }
        if locale:
            payload['locale'] = locale

        flattened_data = []
        while True:
            response = requests.get(url, headers=self.headers, data=json.dumps(payload))
            response.raise_for_status()
            # Get the columns, but only once in the first iteration
            items = response.json()['data'][0]['attributes']['items']
            flattened_data += self._flatten_items(items)
            # initiate the paging system
            total_pages = response.json()['metadata']['total_pages']
            if page >= total_pages:
                break
            page += 1
            payload['page'] = page

        df = pd.DataFrame(flattened_data)
        return df

    def list_custom_report_columns(self, report_id=None, columns=None, locale=None):
        """
        This endpoint provides human-readable labels for report table columns. It is particularly important if you get a report with custom attributes or absence data to match the column IDs to the translation.
        :param report_id: The ID of the report to filter the result of the columns. If no ID is passed, all columns for the company are returned.
        :param columns: The columns to filter the results. Divide by comma: 1,2,3
        :param locale: locale used to translate localized fields.
        """
        base_url = f'{self.base_url}company/custom-reports/columns'
        payload = {}
        if report_id:
            payload['report_id'] = report_id
        if columns:
            payload['columns'] = columns
        if locale:
            payload['locale'] = locale
        response = requests.get(base_url, headers=self.headers, data=json.dumps(payload))
        response.raise_for_status()
        df = pd.json_normalize(response.json()['data'])
        return df