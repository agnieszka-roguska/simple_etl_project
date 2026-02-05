import extract
from collections import Counter


def process_users_data(users_data: list[dict]) -> list[dict[str]]: 
    required_fields = {"id", "firstName", "lastName", "age", "gender", "email"}

    for index, user in enumerate(users_data):
        user_filtered = {k: v for k, v in user.items() if k in required_fields}
        coords = user.get("address", {}).get("coordinates", {})
        lat = coords.get("lat")
        lng = coords.get("lng")
        user_filtered["lat"] = lat
        user_filtered["lng"] = lng
        user_filtered["country"] = extract.get_country(lng, lat)
        users_data[index] = user_filtered

    return users_data


def get_category_from_thumbnail(thumbnail: str) -> str:
    prefix_to_remove = "https://cdn.dummyjson.com/products/images/" 
    if thumbnail.startswith(prefix_to_remove):
        category = thumbnail[len(prefix_to_remove) :].split("/")[0]
        return category
    else:
        raise ValueError("Thumbnail prefix has changed or is invalid.")


"""def find_fav_cart_category_for_users(
    users: list[dict], carts: list[dict]
) -> list[dict]:
    user_map = {user["id"]: user for user in users}
    for cart in carts:
        category_counts = {}
        for product in cart.get("products", []):
            try:
                category = get_category_from_thumbnail(product.get("thumbnail", ""))
            except ValueError as e:
                print(f"ValueError: {e}")
                continue

            quantity = product.get("quantity", 0)
            category_counts[category] = category_counts.get(category, 0) + quantity

        fav_category_str = "Unknown"
        if category_counts:
            max_quantity = max(category_counts.values())
            fav_categories = [
                category
                for category, quantity in category_counts.items()
                if quantity == max_quantity
            ]

            fav_category_str = "; ".join(fav_categories)

        user = user_map.get(cart.get("userId"))
        if user:
            user["fav_category_in_cart"] = fav_category_str

    for user in users:  # ensure all users have the key
        user["fav_category_in_cart"] = user.get("fav_category_in_cart")

    return users"""

def find_fav_cart_category(cart: dict) -> list[dict]:
    counter = Counter()
    products = cart["products"]
    for product in products:
        title = product["title"]
        quantity = product["quantity"]

        if title and quantity > 0:
            counter[title] += quantity
        
        if not counter:
            return None

    return counter.most_common(1)[0][0]

def users_add_fav_cart_category(users : list[dict], carts : list[dict]) -> list[dict]:
    user_map = {user["id"] : user for user in users}
    for user in users:
        user["fav_category_in_cart"] = None

    for cart in carts:
        user = user_map.get(cart.get("userId"))
        if not user:
            continue

        user["fav_category_in_cart"] = find_fav_cart_category(cart = cart)  

    return users