# coding: utf-8
from django.http import Http404
from rest_framework import (
    renderers,
    viewsets, status,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from kpi.serializers.v2.service_usage import ServiceUsageSerializer
from kpi.utils.object_permission import get_database_user


class ServiceUsageViewSet(viewsets.ViewSet):
    """
    ## Service Usage Tracker
    <p>Tracks the total usage of different services for each account in the current user's organization</p>
    <p>Tracks the submissions and NLP seconds/characters for the current month/year/all time</p>
    <p>Tracks the current total storage used</p>

    <pre class="prettyprint">
    <b>GET</b> /api/v2/service_usage/?=organization_id={organization_id}
    </pre>

        > **Payload**
    >
    >        {
    >           "organization_id": "orgA34cds8fmske3tf",
    >        }

    where:

    * "organization_id" (optional) is an organization ID string. User must be the organization's owner.
    ** If "organization_id" is set, endpoint will return aggregated usage data for all the organization's users.

    > Example
    >
    >       curl -X GET https://[kpi]/api/v2/service_usage/
    >       {
    >           "total_nlp_asr_seconds_current_month": {integer},
    >           "total_nlp_asr_seconds_current_year": {integer},
    >           "total_nlp_asr_seconds_all_time": {integer},
    >           "total_nlp_mt_characters_current_month": {integer},
    >           "total_nlp_mt_characters_current_year": {integer},
    >           "total_nlp_mt_characters_all_time": {integer},
    >           "total_storage_bytes": {integer},
    >           "total_submission_count_current_month": {integer},
    >           "total_submission_count_current_year": {integer},
    >           "total_submission_count_all_time": {integer},
    >           "current_month_start": {string (date), YYYY-MM-DD format},
    >           "current_year_start": {string (date), YYYY-MM-DD format},
    >       }


    ### CURRENT ENDPOINT
    """
    renderer_classes = (
        renderers.BrowsableAPIRenderer,
        renderers.JSONRenderer,
    )
    pagination_class = None
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
        }

    def list(self, request, *args, **kwargs):
        try:
            serializer = ServiceUsageSerializer(
                get_database_user(request.user),
                context=self.get_serializer_context(),
            )
        except Http404:
            return Response(
                {
                    'message': "Couldn't find organization with specified ID"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(data=serializer.data)
