# -*- coding: utf-8 -*-

"""
The Cherwell translation router is a specialized router that allows common names to be used
for business objects, records, fields, etc in a way that remains performant.

The first time a resource is queried the results are stored in the router allowing repeat
queries within the same session to use cached data for rapid retrieval.
"""
import logging

from cherwellapi.apiclient import CherwellAPIClientError
from cherwellapi.routers import CherwellRouter


class TranslationRouter(CherwellRouter):
    ci_index = None

    """
    Class translating Cherwell objects/ids into friendly names and vice versa
    """

    def __init__(self, url, headers, user, password, client_id, ssl_verify):
        super(TranslationRouter, self).__init__(url, headers, user, password, client_id, ssl_verify)
        self.uuid = None

    def _load_configuration_items(self, botype='All'):
        """
        Internal method to load configuration item business object ids into router
        """

        logging.debug('CI business objects index not loaded, fetching.')

        bus_obj_summary = self._router_request(
            method='GET',
            api_version='api/V1',
            action='getbusinessobjectsummaries/type/{0}'.format(botype)
        )

        self.ci_index = {'cis': {}, 'names': {}, 'display_names': {}}

        for bus_obj in bus_obj_summary:
            if bus_obj['name'] == 'ConfigurationItem':
                for ci in bus_obj['groupSummaries']:
                    self.ci_index['cis'].update({ci['busObId']: {}})
                    self.ci_index['names'].update({ci['name']: ci['busObId']})
                    self.ci_index['display_names'].update({ci['displayName']: ci['busObId']})

    def _load_fields(self, ci=None, ci_id=None):
        """
        Internal method to load field information into router from Cherwell API
        """

        # Check that index has been loaded
        if self.ci_index is None:
            self._load_configuration_items()
        if ci is not None:
            ci_id = self.get_ci_id(ci)
        if ci_id is not None:
            ci_fields = self._router_request(
                method='GET',
                api_version='api/V1',
                action='getbusinessobjectschema/busobid/{0}'.format(ci_id)
            )

            self.ci_index['cis'][ci_id]['fields'] = {'names': {}, 'display_names': {}}

            for field in ci_fields['fieldDefinitions']:
                self.ci_index['cis'][ci_id]['fields']['names'].update(
                    {field['name']: field['fieldId'].rsplit('FI:', 1)[1]})
                self.ci_index['cis'][ci_id]['fields']['display_names'].update(
                    {field['displayName']: field['fieldId'].rsplit('FI:', 1)[1]})

    def get_ci_id(self, ci):
        """
        Returns the business object id of a configuration item.
        Either the Name or Display Name may be used.  Name is searched first by default.

        Arguments:
            ci (str): Name or Display name of the CI

        """
        # Check that index has been loaded
        if self.ci_index is None:
            self._load_configuration_items()

        if ci in self.ci_index['names']:
            return self.ci_index['names'][ci]
        elif ci in self.ci_index['display_names']:
            return self.ci_index['display_names'][ci]
        else:
            raise CherwellAPIClientError('{0} not found in CI business objects'.format(ci))

    def get_field(self, ci=None, ci_id=None, field=None):
        """
        Returns the field id of a field.
        Either the CI name, display name or ID AND the field name or display name must be provided.
        """
        # Check that index has been loaded
        if self.ci_index is None:
            self._load_configuration_items()

        # Check if a CI name or display name was provided
        if ci is not None:
            ci_id = self.get_ci_id(ci)
        # Check that we have the CI ID
        if ci_id is not None:
            if 'fields' not in self.ci_index['cis'][ci_id]:
                self._load_fields(ci_id=ci_id)
            if field in self.ci_index['cis'][ci_id]['fields']['names']:
                return self.ci_index['cis'][ci_id]['fields']['names'][field]
            elif field in self.ci_index['cis'][ci_id]['fields']['display_names']:
                return self.ci_index['cis'][ci_id]['fields']['display_names'][field]
            else:
                raise CherwellAPIClientError('Field {0} not found in CI {1} {2}'.format(field, ci, ci_id))

    def get_fields(self, ci=None, ci_id=None, field_list=None):
        """
        Returns a dictinary of fields and their field IDs.
        Either the CI name, display name or ID AND a list of field names or display names must be provided.
        Dictionary is returned in the format {field (display)name: field ID}
        """
        # Check that index has been loaded
        if self.ci_index is None:
            self._load_configuration_items()

        field_dict = {}

        # Check if a CI name or display name was provided
        if ci is not None:
            field_dict = {}
            for field in field_list:
                field_dict[field] = self.get_field(ci=ci, field=field)
        # Check that we have the CI ID
        elif ci_id is not None:
            for field in field_list:
                field_dict[field] = self.get_field(ci_id=ci_id, field=field)
        else:
            raise CherwellAPIClientError('No ci or ci_id provided for fields search, at least one is required!')

        return field_dict
