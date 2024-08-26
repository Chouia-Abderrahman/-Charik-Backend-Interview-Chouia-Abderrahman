# Charik Backend Developer Technical Test

## Overview

This repository contains the code for the backend technical test for Charik. It includes a Django REST Framework application that integrates with HubSpot's API to manage contacts and deals. The application is containerized using Docker.

## Prerequisites

- **Python 3.8+**: Make sure Python 3.8 or later is installed on your machine.
- **Docker**: Ensure Docker is installed for containerization.
- **HubSpot API Key**: You need a HubSpot API key to interact with HubSpot's API.

## Setup Instructions

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/Chouia-Abderrahman/Charik-Backend-Interview-Chouia-Abderrahman.git
cd Charik-Backend-Interview-Chouia-Abderrahman
```

### 2. Environment variables:

go to the env file located in
```bash
/hubspot_integration/django_api
```
and replace the token placeholder with your hubspot api key:
```bash
TOKEN=YOUR_TOKEN
```

### 3. Docker setup:

Build and run the Docker container:

```bash
docker build -t charik-backend .
docker run -p 8000:8000 charik-backend
```

This will build the Docker image and run the application, mapping port 8000 from the container to port 8000 on your host.

### 4. API Documentation:
Endpoints

    Create Contact
        URL: /contacts/create/
        Method: POST
        Headers: Content-Type: application/json
        Request Body:

        json

    {
      "lastname": "Chouia",
      "firstname": "Abderrahman"
    }

    Response: 201 Created, with the contact ID in the response.

Create Deal

    URL: /deals/create/
    Method: POST
    Headers: Content-Type: application/json
    Request Body:

    json

    {
      "deal_name": "Deal - Chouia Abderrahman"
    }

    Response: 201 Created, with the deal ID in the response.

Associate Contact with Deal

    URL: /deals/associate/
    Method: POST
    Headers: Content-Type: application/json
    Request Body:

    json

    {
      "contact_id": "32109216466",
      "deal_id": "16473007324"
    }

    Response: 200 OK, with a confirmation message.

Retrieve Contacts and Deals

    URL: /contacts/
    Method: GET
    Response: 200 OK, with a list of contacts and associated deals.

### 5. Example requests:
In the `routes.rest` file in the root directory of the project, you can find example requests that you can immediately run using the VSCode extension REST Client. These examples provide a simple demonstration for each endpoint.

You can view and interact with these requests by opening the `routes.rest` file in Visual Studio Code.

[View `routes.rest`](./routes.rest)
