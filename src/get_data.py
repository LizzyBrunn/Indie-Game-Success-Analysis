import os
import json
import requests


def main() -> None:
    """Collect RAWG game data from the API and save the raw JSON to data/raw/."""
    #key is set on my end for security
    api_key = os.getenv("RAWG_API_KEY")

    if api_key is not None and api_key != "":
        url = "https://api.rawg.io/api/games"

        all_games: list[dict] = []
        page: int = 1
        page_size: int = 40
        #collect games until we get to 750
        while len(all_games) < 750:
            params: dict[str, object] = {
                "key": api_key,
                "page": page,
                "page_size": page_size,
                #sorting by most "added," since the only other realistic option is recent and those dont have much info
                "ordering": "-added"
            }

            headers: dict[str, str] = {
                "User-Agent": "Mozilla/5.0"
            }

            response = requests.get(url, params=params, headers=headers)

            if response.status_code == 200:
                data: dict = response.json()
                results: list[dict] = data["results"]

                for game in results:
                    all_games.append(game)
                    if len(all_games) == 750:
                        break

                print("Collected games so far:", len(all_games))
                page = page + 1

            else:
                print("Request failed:", response.status_code)
                print(response.text)
                break

        output_path: str = "data/raw/rawg_games_raw.json"
        f = open(output_path, "w", encoding="utf-8")
        json.dump(all_games, f, indent=2)
        f.close()

        print("Saved raw data to:", output_path)
    else:
        print("RAWG_API_KEY is not set.")


if __name__ == "__main__":
    main()
