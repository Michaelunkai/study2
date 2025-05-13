from howlongtobeatpy import HowLongToBeat
import difflib

def select_best_match(query, results):
    names = [r.game_name for r in results]
    matches = difflib.get_close_matches(query, names, n=3, cutoff=0.4)
    
    if not matches:
        return None

    if len(matches) == 1:
        return next(g for g in results if g.game_name == matches[0])

    print("\nMultiple close matches found:")
    for i, name in enumerate(matches):
        print(f"{i + 1}. {name}")
    
    try:
        choice = int(input("Choose the correct one (1/2/3): ").strip())
        if 1 <= choice <= len(matches):
            return next(g for g in results if g.game_name == matches[choice - 1])
    except:
        pass
    
    return None

def get_game_playtime(game_name):
    print(f"Searching for '{game_name}'...")
    results = HowLongToBeat().search(game_name)

    if not results:
        print("❌ No results found.")
        return

    best_match = select_best_match(game_name, results)

    if best_match:
        print(f"\n🎮 Found: {best_match.game_name}")
        print(f"🕹️  Main Story: {best_match.main_story} hours")
        print(f"📦 Main + Extra: {best_match.main_extra} hours")
        print(f"🏆 Completionist: {best_match.completionist} hours")
    else:
        print("⚠️ Couldn't confidently identify the correct game.")

if __name__ == "__main__":
    try:
        while True:
            game_name = input("\nEnter game name (or 'exit'): ").strip()
            if game_name.lower() in ['exit', 'quit']:
                break
            get_game_playtime(game_name)
    except KeyboardInterrupt:
        print("\nExited.")

