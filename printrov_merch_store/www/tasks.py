import frappe
from frappe.integrations.utils import make_get_request, make_post_request
 
BASE_URL = "https://api.printrove.com/"   # trailing slash add here

def sync_products_from_printrove():
    access_token = get_printrove_access_token()

    headers = {"Authorization": f"Bearer {access_token}"}
    products_route = "api/external/products"
    all_products = make_get_request(f"{BASE_URL}{products_route}", headers =headers)
    all_products=all_products["products"]

    for product in all_products:
        doc = frappe.get_doc ({
            "doctype":"Stored Product",
            "name1":product["name"],
            "printrove_id":product["id"],
            "front_mockup":product["mockup"]["front_mockup"],
            "back_mockup":product["mockup"]["back_mockup"]
        }).insert(ignore_permissions=True)


def get_printrove_access_token():
    pprintrove_settings = frappe.get_single("Printrove Settings")

    auth_route = "api/external/token"

    response = make_post_request(
        f"{BASE_URL}{auth_route}", 
        data={
            "email":pprintrove_settings.email, 
            "password":pprintrove_settings.get_password("password"),
            },
        )
    return response['access_token']




# import frappe
# from frappe.integrations.utils import make_get_request, make_post_request

# BASE_URL = "https://api.printrove.com/"  # Trailing slash

# def sync_products_from_printrove():
#     try:
#         # Step 1: Get access token
#         access_token = get_printrove_access_token()
#         headers = {"Authorization": f"Bearer {access_token}"}

#         # Step 2: Fetch all products from Printrove
#         products_route = "api/external/products"
#         all_products_response = make_get_request(f"{BASE_URL}{products_route}", headers=headers)
#         all_products = all_products_response.get("products", [])

#         # Step 3: Iterate through each product and insert it into Frappe
#         for product in all_products:
#             try:
#                 # Ensure the mockup data exists to avoid errors
#                 front_mockup = product.get("mockup", {}).get("front_mockup")
#                 back_mockup = product.get("mockup", {}).get("back_mockup")

#                 doc = frappe.get_doc({
#                     "doctype": "Stored Product",
#                     "name": product["name"],
#                     "printrove_id": product["id"],
#                     "front_mockup": front_mockup,
#                     "back_mockup": back_mockup
#                 })

#                 doc.insert(ignore_permissions=True)
#                 frappe.db.commit()  # Commit after each insert to avoid partial syncs
#                 print(f"Successfully synced product: {product['name']}")

#             except Exception as e:
#                 frappe.log_error(f"Error inserting product {product['name']}: {str(e)}", "Printrove Sync Error")

#     except Exception as e:
#         frappe.log_error(f"Error fetching products from Printrove: {str(e)}", "Printrove Sync Error")

# def get_printrove_access_token():
#     try:
#         printrove_settings = frappe.get_single("Printrove Settings")

#         # Step 1: Make the POST request for an access token
#         auth_route = "api/external/token"
#         response = make_post_request(
#             f"{BASE_URL}{auth_route}",
#             data={
#                 "email": printrove_settings.email,
#                 "password": printrove_settings.get_password("password"),
#             },
#         )
#         return response['access_token']
#     except Exception as e:
#         frappe.log_error(f"Error fetching access token from Printrove: {str(e)}", "Printrove Auth Error")
#         raise

