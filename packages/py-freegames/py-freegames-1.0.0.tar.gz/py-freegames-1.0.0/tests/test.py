from freegames import get_all_discounts

def print_discounts():
    discounts = get_all_discounts()
    
    print("Steam Discounts:")
    for game in discounts['steam']:
        print(f"Title: {game['title']}, Discount: {game['discount']}, Original Price: {game['original_price']}, Discounted Price: {game['discounted_price']}")
    
    print("\nEpic Games Discounts:")
    for game in discounts['epic']:
        print(f"Title: {game['title']}, Discount: {game['discount']}, Original Price: {game['original_price']}, Discounted Price: {game['discounted_price']}")
    
    print("\nGOG Discounts:")
    for game in discounts['gog']:
        print(f"Title: {game['title']}, Discount: {game['discount']}, Original Price: {game['original_price']}, Discounted Price: {game['discounted_price']}")

if __name__ == "__main__":
    print_discounts()
