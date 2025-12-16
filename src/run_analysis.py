import csv
import math


#simple function for mean
def mean(values: list[float]) -> float:
    """Compute the arithmetic mean of a list of numeric values."""
    return sum(values) / len(values)


#slightly less simple function to run correlation
def pearson_correlation(x: list[float], y: list[float]) -> float | None:
    """Compute the Pearson correlation coefficient between two numeric lists."""
    x_mean = mean(x)
    y_mean = mean(y)

    numerator: float = 0
    denom_x: float = 0
    denom_y: float = 0

    for i in range(len(x)):
        numerator += (x[i] - x_mean) * (y[i] - y_mean)
        denom_x += (x[i] - x_mean) ** 2
        denom_y += (y[i] - y_mean) ** 2

    denominator: float = math.sqrt(denom_x * denom_y)

    if denominator == 0:
        return None
    else:
        return numerator / denominator


#main funct
def main() -> None:
    """Run descriptive analysis and correlation analysis on indie game data."""
    path = "data/processed/games_clean.csv"

    f = open(path, "r", encoding="utf-8")
    reader = csv.DictReader(f)

    #we only want Indie games
    indie_games: list[dict] = []

    for row in reader:
        genres_text: str = row["genres"]
        genres_list: list[str] = genres_text.split("|")

        is_indie: bool = False
        for g in genres_list:
            if g.strip().lower() == "indie":
                is_indie = True

        if is_indie == True:
            try:
                row["added"] = int(row["added"])
                row["ratings_count"] = int(row["ratings_count"])
                row["rating"] = float(row["rating"])
                indie_games.append(row)
            except:
                pass

    f.close()

    print("Total indie games:", len(indie_games))
    print()

    #descriptive statistics
    added_values: list[int] = [g["added"] for g in indie_games]
    ratings_count_values: list[int] = [g["ratings_count"] for g in indie_games]
    rating_values: list[float] = [g["rating"] for g in indie_games]

    print("Descriptive Statistics (Indie Games)")
    print("Average added:", round(mean(added_values), 2))
    print("Average rating:", round(mean(rating_values), 2))
    print()

    #genre info, looking at frequency and avg
    genre_counts: dict[str, int] = {}
    genre_added_totals: dict[str, int] = {}
    genre_rating_totals: dict[str, float] = {}

    for g in indie_games:
        genres: list[str] = g["genres"].split("|")

        for genre in genres:
            if genre != "":
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
                genre_added_totals[genre] = genre_added_totals.get(genre, 0) + g["added"]
                genre_rating_totals[genre] = genre_rating_totals.get(genre, 0) + g["rating"]

    #genre frequency
    print("Top Genres by Frequency (Indie Games)")
    genre_freq_list: list[tuple[int, str]] = []

    for genre in genre_counts:
        genre_freq_list.append((genre_counts[genre], genre))

    genre_freq_list.sort(reverse=True)

    for item in genre_freq_list[:10]:
        print(item[1], "- count:", item[0])

    print()

    print("Top Genres by Average Added (Indie Games)")
    genre_avg_added: list[tuple[float, str, int]] = []

    for genre in genre_counts:
        avg_added: float = genre_added_totals[genre] / genre_counts[genre]
        genre_avg_added.append((avg_added, genre, genre_counts[genre]))

    genre_avg_added.sort(reverse=True)

    for item in genre_avg_added[:10]:
        print(item[1], "- avg added:", round(item[0], 2), "| count:", item[2])

    print()

    print("Top Genres by Average Rating (Indie Games)")
    genre_avg_rating: list[tuple[float, str, int]] = []

    for genre in genre_counts:
        avg_rating: float = genre_rating_totals[genre] / genre_counts[genre]
        genre_avg_rating.append((avg_rating, genre, genre_counts[genre]))

    genre_avg_rating.sort(reverse=True)

    for item in genre_avg_rating[:10]:
        print(item[1], "- avg rating:", round(item[0], 2), "| count:", item[2])

    print()

    #tag info, looking at frequency and avg
    tag_counts: dict[str, int] = {}
    tag_added_totals: dict[str, int] = {}
    tag_rating_totals: dict[str, float] = {}

    for g in indie_games:
        tags: list[str] = g["tags"].split("|")

        for tag in tags:
            if tag != "":
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
                tag_added_totals[tag] = tag_added_totals.get(tag, 0) + g["added"]
                tag_rating_totals[tag] = tag_rating_totals.get(tag, 0) + g["rating"]

    print("Top Tags by Frequency (Indie Games)")
    tag_freq_list: list[tuple[int, str]] = []

    for tag in tag_counts:
        tag_freq_list.append((tag_counts[tag], tag))

    tag_freq_list.sort(reverse=True)

    for item in tag_freq_list[:15]:
        print(item[1], "- count:", item[0])

    print()

    #bc there are many tags, only include tags that show up at least 10 times
    min_tag_count: int = 10

    print("Top Tags by Average Added")
    tag_avg_added: list[tuple[float, str, int]] = []

    for tag in tag_counts:
        if tag_counts[tag] >= min_tag_count:
            avg_added: float = tag_added_totals[tag] / tag_counts[tag]
            tag_avg_added.append((avg_added, tag, tag_counts[tag]))

    tag_avg_added.sort(reverse=True)

    for item in tag_avg_added[:15]:
        print(item[1], "- avg added:", round(item[0], 2), "| count:", item[2])

    print()

    print("Top Tags by Average Rating")
    tag_avg_rating: list[tuple[float, str, int]] = []

    for tag in tag_counts:
        if tag_counts[tag] >= min_tag_count:
            avg_rating: float = tag_rating_totals[tag] / tag_counts[tag]
            tag_avg_rating.append((avg_rating, tag, tag_counts[tag]))

    tag_avg_rating.sort(reverse=True)

    for item in tag_avg_rating[:15]:
        print(item[1], "- avg rating:", round(item[0], 2), "| count:", item[2])

    print()

    #run the tests
    corr: float | None = pearson_correlation(rating_values, added_values)

    print("Correlation Analysis")
    print("Pearson correlation between ratings_count and added:")

    if corr is None:
        print("Error. Correlation could not be computed.")
    else:
        print(round(corr, 3))


if __name__ == "__main__":
    main()
