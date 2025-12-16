import json
import csv


def main() -> None:
    """Clean RAWG game data and save selected fields to a CSV file."""
    input_path = "data/raw/rawg_games_raw.json"
    output_path = "data/processed/games_clean.csv"

    #load the raw data
    f = open(input_path, "r", encoding="utf-8")
    games: list[dict] = json.load(f)
    f.close()

    #open for writing
    out = open(output_path, "w", newline="", encoding="utf-8")
    writer = csv.writer(out)

    #headers for reevant columns
    writer.writerow([
        "title",
        "release_date",
        "rating",
        "ratings_count",
        "added",
        "genres",
        "tags",
        "developers"
    ])

    #get only the categories needed for this project
    for game in games:
        title: str | None = game.get("name")
        release_date: str | None = game.get("released")
        rating: float | None = game.get("rating")
        ratings_count: int | None = game.get("ratings_count")
        added: int | None = game.get("added")

        #genre
        genre_list: list[str] = []
        if game.get("genres") is not None:
            for g in game["genres"]:
                genre_list.append(g.get("name"))
        genres: str = "|".join(genre_list)

        #tags
        tag_list: list[str] = []
        if game.get("tags") is not None:
            for t in game["tags"]:
                tag_list.append(t.get("name"))
        tags: str = "|".join(tag_list)

        #devs
        dev_list: list[str] = []
        if game.get("developers") is not None:
            for d in game["developers"]:
                dev_list.append(d.get("name"))
        developers: str = "|".join(dev_list)

        writer.writerow([
            title,
            release_date,
            rating,
            ratings_count,
            added,
            genres,
            tags,
            developers
        ])

    out.close()
    print("Clean data saved to:", output_path)


if __name__ == "__main__":
    main()
