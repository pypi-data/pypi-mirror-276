import requests
import os
from .exceptions import (
    SalableSDKError, AuthenticationError, ProductError, PlanError, LicenseError, PaymentLinkError
)

class SalableClient:
    def __init__(self, base_url=None, api_key=None):
        # Initialize the SalableClient with optional base_url and api_key.
        # If not provided, defaults to the production API URL and retrieves the API key from the environment variables.
        self.base_url = base_url if base_url else 'https://api.salable.app'
        self.api_key = api_key if api_key else os.environ["SALABLE_API_KEY"]
        self.headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json',
            'version': 'v1'
        }

    def _handle_response(self, response):
        # Handle the HTTP response from the API.
        # Raises an error if the response status is not OK (2xx).
        if not response.ok:
            raise SalableSDKError(f'Error: {response.status_code} - {response.text}')
        return response.json()

    # Product methods
    def get_products(self):
        # Retrieve a list of products.
        url = f'{self.base_url}/products'
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    def get_product_by_uuid(self, product_uuid, expand=None):
        # Retrieve a specific product by its UUID.
        # Optionally expand related resources.
        url = f'{self.base_url}/products/{product_uuid}'
        params = {}
        if expand:
            params['expand'] = expand
        response = requests.get(url, headers=self.headers, params=params)
        return self._handle_response(response)

    def get_product_plans(self, product_uuid, **kwargs):
        # Retrieve plans associated with a specific product.
        url = f'{self.base_url}/products/{product_uuid}/plans'
        response = requests.get(url, headers=self.headers, params=kwargs)
        return self._handle_response(response)

    def get_product_pricing_table(self, product_uuid, **kwargs):
        # Retrieve the pricing table for a specific product.
        url = f'{self.base_url}/products/{product_uuid}/pricingtable'
        response = requests.get(url, headers=self.headers, params=kwargs)
        return self._handle_response(response)

    def get_product_features(self, product_uuid):
        # Retrieve features of a specific product.
        url = f'{self.base_url}/products/{product_uuid}/features'
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    def get_product_currencies(self, product_uuid):
        # Retrieve supported currencies for a specific product.
        url = f'{self.base_url}/products/{product_uuid}/currencies'
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    def get_product_capabilities(self, product_uuid):
        # Retrieve capabilities of a specific product.
        url = f'{self.base_url}/products/{product_uuid}/capabilities'
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    # Plan methods (additional placeholder methods for plan-related operations can be added here)

    # License methods
    def create_license(self, plan_uuid, member, grantee_id):
        # Create a new license for a specific plan.
        url = f'{self.base_url}/licenses'
        payload = {
            'planUuid': plan_uuid,
            'member': member,
            'granteeId': grantee_id
        }
        response = requests.post(url, headers=self.headers, json=payload)
        return self._handle_response(response)

    def get_licenses(self, status=None):
        # Retrieve a list of licenses, optionally filtered by status.
        url = f'{self.base_url}/licenses'
        if status:
            url += f'?status={status}'
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    def get_license(self, license_uuid):
        # Retrieve a specific license by its UUID.
        url = f'{self.base_url}/licenses/{license_uuid}'
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    def create_many_licenses(self, licenses):
        # Create multiple licenses in a single request.
        url = f'{self.base_url}/licenses/create-many'
        response = requests.post(url, headers=self.headers, json=licenses)
        return self._handle_response(response)

    def get_license_count(self, product_uuid):
        # Retrieve the count of licenses for a specific product.
        url = f'{self.base_url}/licenses/{product_uuid}/count'
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    def get_license_by_purchaser(self, product_uuid, purchaser):
        # Retrieve licenses by purchaser for a specific product.
        url = f'{self.base_url}/licenses/{product_uuid}/purchaser'
        params = {'purchaser': purchaser}
        response = requests.get(url, headers=self.headers, params=params)
        return self._handle_response(response)

    def check_license(self, license_uuid):
        # Check the validity of a specific license.
        url = f'{self.base_url}/licenses/{license_uuid}/check'
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    def update_license(self, license_uuid, data):
        # Update a specific license.
        url = f'{self.base_url}/licenses/{license_uuid}'
        response = requests.put(url, headers=self.headers, json=data)
        return self._handle_response(response)

    def delete_license(self, license_uuid):
        # Delete a specific license.
        url = f'{self.base_url}/licenses/{license_uuid}'
        response = requests.delete(url, headers=self.headers)
        if response.status_code != 204:
            raise LicenseError(f'Error deleting license: {response.text}')
        return None

    # Subscription methods (additional placeholder methods for subscription-related operations can be added here)

    # Payment Link methods
    def generate_payment_link(self, plan_id, purchaser, grantee, success_url, cancel_url):
        # Generate a payment link for a specific plan and user.
        url = f'{self.base_url}/plans/{plan_id}/checkoutlink?member={purchaser}&granteeId={grantee}&successUrl={success_url}&cancelUrl={cancel_url}'
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    # RBAC methods (Roles and Users)
    def get_roles(self):
        # Retrieve a list of roles.
        url = f'{self.base_url}/roles'
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    def get_role_by_uuid(self, role_uuid):
        # Retrieve a specific role by its UUID.
        url = f'{self.base_url}/roles/{role_uuid}'
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    def create_role(self, name, description, permissions):
        # Create a new role.
        url = f'{self.base_url}/roles'
        payload = {
            'name': name,
            'description': description,
            'permissions': permissions
        }
        response = requests.post(url, headers=self.headers, json=payload)
        return self._handle_response(response)

    def update_role(self, role_uuid, data):
        # Update a specific role.
        url = f'{self.base_url}/roles/{role_uuid}'
        response = requests.put(url, headers=self.headers, json=data)
        return self._handle_response(response)

    def delete_role(self, role_uuid):
        # Delete a specific role.
        url = f'{self.base_url}/roles/{role_uuid}'
        response = requests.delete(url, headers=self.headers)
        if response.status_code != 204:
            raise SalableSDKError(f'Error deleting role: {response.text}')
        return None

    def get_users(self):
        # Retrieve a list of users.
        url = f'{self.base_url}/users'
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    def get_user_by_id(self, user_id):
        # Retrieve a specific user by their ID.
        url = f'{self.base_url}/users/{user_id}'
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    def create_user(self, user_id, name, role, permissions):
        # Create a new user.
        url = f'{self.base_url}/users'
        payload = {
            'id': user_id,
            'name': name,
            'role': role,
            'permissions': permissions
        }
        response = requests.post(url, headers=self.headers, json=payload)
        return self._handle_response(response)

    def update_user(self, user_id, data):
        # Update a specific user.
        url = f'{self.base_url}/users/{user_id}'
        response = requests.put(url, headers=self.headers, json=data)
        return self._handle_response(response)

    def delete_user(self, user_id):
        # Delete a specific user.
        url = f'{self.base_url}/users/{user_id}'
        response = requests.delete(url, headers=self.headers)
        if response.status_code != 204:
            raise SalableSDKError(f'Error deleting user: {response.text}')
        return None

    # Event methods (additional placeholder methods for event-related operations can be added here)

    # Utility methods (additional placeholder methods for utility operations can be added here)