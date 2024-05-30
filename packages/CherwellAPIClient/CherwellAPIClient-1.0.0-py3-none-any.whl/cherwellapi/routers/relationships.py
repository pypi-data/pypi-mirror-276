# -*- coding: utf-8 -*-

"""
Cherwell Relationships Router
"""

from cherwellapi.routers import CherwellRouter
from cherwellapi.routers.translation import TranslationRouter
from cherwellapi.apiclient import CherwellAPIClientError


class RelationshipsRouter(CherwellRouter):
    """
    Class for interacting with Cherwell relationship functions
    """

    def __init__(self, url, headers, user, password, client_id, ssl_verify):
        super(RelationshipsRouter, self).__init__(url, headers, user, password, client_id, ssl_verify)

    def get_relationships(self, ci=None, ci_id=None, relationship_name=None):

        relationhsip_dict = {}

        if ci is not None:
            tr = TranslationRouter(
                self.api_url, self.api_headers, self.api_user, self.api_password, self.api_client_id, self.ssl_verify)
            ci_id = tr.get_ci_id(ci)
        if ci_id is not None:
            ci_fields = self._router_request(
                method='GET',
                api_version='api/V1',
                action='getbusinessobjectschema/busobid/{0}?includerelationships=true'.format(ci_id)
            )

            for relationship in ci_fields['relationships']:
                relationhsip_dict.update({relationship['displayName']: relationship})

            if relationship_name is not None:
                return relationhsip_dict[relationship_name]
            else:
                return relationhsip_dict
        else:
            raise CherwellAPIClientError('No ci_id provided or ci {0} not found.'.format(ci_id))

    def get_related_business_objects(self, parent_ci_id, parent_rec_id, relationship_id):
        """
        Get related business objects given a business object, record and relationship
        """

        result = self._router_request(
            method='GET',
            api_version='api/V1',
            action='getrelatedbusinessobject/parentbusobid/{0}/parentbusobrecid/{1}/relationshipid/{2}?allfields=true&usedefaultgrid=false'.format(
                parent_ci_id, parent_rec_id, relationship_id)
        )

        related_objects = {
            'total_rows': result['totalRecords'],
            'returned_rows': len(result['relatedBusinessObjects']),
            'data': result['relatedBusinessObjects']
        }

        return related_objects
