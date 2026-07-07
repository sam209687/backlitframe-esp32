from app.services.product_matcher import ProductMatcher

print("=" * 70)
print("SMART SHOWROOM PRODUCT MATCHER")
print("=" * 70)

while True:

    text = input("\nCustomer : ").strip()

    if text.lower() in ("exit", "quit"):
        break

    result = ProductMatcher.match(text)

    if result:

        print("\nMATCHED")
        print("Product :", result["product"].name)
        print("Effect  :", result["product"].led_effect)
        print("Media   :", result["product"].media_path)
        print("Score   :", result["score"])

    else:

        print("\nNO PRODUCT FOUND")