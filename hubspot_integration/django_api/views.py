import json
import urllib.request
import requests
from django.views.decorators.csrf import csrf_exempt
from hubspot.crm.associations import PublicAssociation, BatchInputPublicObjectId
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from hubspot.crm.contacts import SimplePublicObjectInputForCreate, SimplePublicObjectInput, AssociationSpec, \
    SimplePublicObjectId
from .serializers import hubspot_contact_serializer, hubspot_deal_serializer, hubspot_association_serializer
from hubspot import HubSpot
from dotenv import load_dotenv
import os
from hubspot.crm.associations import BatchInputPublicObjectId

load_dotenv()
hubspot_token = os.getenv('TOKEN')

api_client = HubSpot(access_token=hubspot_token)

class CreateContactAPIView(APIView):
    def post(self, request):
        first_name = request.data.get('firstname')
        last_name = request.data.get('lastname')

        contact_properties = {
            "firstname": first_name,
            "lastname": last_name
        }

        try:
            simple_public_object_input_for_create = SimplePublicObjectInputForCreate(
                properties=contact_properties
            )
            api_response = api_client.crm.contacts.basic_api.create(
                simple_public_object_input_for_create=simple_public_object_input_for_create
            )

            response_dict = api_response.to_dict()

            serialized_data = hubspot_contact_serializer(response_dict)

            serialized_dict = json.loads(serialized_data)
            return Response(serialized_dict, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateDealAPIView(APIView):
    def post(self, request):
        # contact_id = request.data.get('contact_id')
        deal_name = request.data.get('deal_name')

        deal_properties = {
            "dealname": deal_name,
        }

        try:

            simple_public_object_input_for_create = SimplePublicObjectInputForCreate(
                properties=deal_properties
            )
            api_response = api_client.crm.deals.basic_api.create(
                simple_public_object_input_for_create=simple_public_object_input_for_create
            )
            response_dict = api_response.to_dict()

            serialized_data = hubspot_deal_serializer(response_dict)

            serialized_dict = json.loads(serialized_data)
            return Response(serialized_dict, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AssociateContactWithDealAPIView(APIView):
    def post(self, request):
        contact_id = request.data.get('contact_id')
        deal_id = request.data.get('deal_id')
        if not contact_id or not deal_id:
            return Response({
                "error": "Both contact_id and deal_id are required"
            }, status=status.HTTP_400_BAD_REQUEST)
        # HubSpot API endpoint
        url = "https://api.hubapi.com/crm/v3/associations/contacts/deals/batch/create"

        # Your HubSpot API key

        # Headers
        headers = {
            "Authorization": f"Bearer {hubspot_token}",
            "Content-Type": "application/json"
        }

        # Request body
        # You might want to get these IDs from the request data
        data = {
            "inputs": [
                {
                    "from": {
                        "id": contact_id
                    },
                    "to": {
                        "id": deal_id
                    },
                    "type": "contact_to_deal"
                }
            ]
        }

        try:
            # Send POST request to HubSpot API
            response = requests.post(url, json=data, headers=headers)

            # Check if the request was successful
            if response.status_code in [200, 201]:
                serialized_response = json.loads(hubspot_association_serializer(response.json()))

                return Response(serialized_response, status=status.HTTP_200_OK)
            else:
                return Response({
                    "error": "HubSpot API request failed",
                    "status_code": response.status_code,
                    "response": response.text
                }, status=status.HTTP_400_BAD_REQUEST)

        except requests.RequestException as e:
            return Response({
                "error": "Request to HubSpot API failed",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RetrieveContactsAndDealsAPIView(APIView):
    def get(self, request):
        try:

            # Fetch all contacts
            all_contacts = []
            after = None
            while True:
                contacts_page = api_client.crm.contacts.basic_api.get_page(
                    after=after,
                    properties=["firstname", "lastname", "email", "phone"]
                )
                all_contacts.extend(contacts_page.results)
                if not contacts_page.paging:
                    break
                after = contacts_page.paging.next.after

            # Fetch associated deals for each contact
            contacts_with_deals = []
            for contact in all_contacts:
                contact_dict = json.loads(hubspot_contact_serializer(contact.to_dict()))

                # Fetch associated deals
                associated_deals = api_client.crm.associations.batch_api.read(
                    from_object_type="contacts",
                    to_object_type="deals",
                    batch_input_public_object_id=BatchInputPublicObjectId(inputs=[SimplePublicObjectId(id=contact.id)])
                )

                # Process associations
                associations = json.loads(hubspot_association_serializer(associated_deals.to_dict()))

                # Fetch full deal details
                contact_dict['deals'] = []
                for association in associations['results']:
                    # if len(association)==0:
                    #     print('empty')
                    #     continue
                    print(association)
                    for single_deal in association['to']:
                        deal_id = single_deal['id']
                        deal = api_client.crm.deals.basic_api.get_by_id(
                            deal_id=deal_id,
                            properties=["dealname", "amount", "closedate", "dealstage"]
                        )
                        contact_dict['deals'].append(json.loads(hubspot_deal_serializer(deal.to_dict())))

                contacts_with_deals.append(contact_dict)

            return Response(contacts_with_deals, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)