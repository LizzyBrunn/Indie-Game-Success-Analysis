import csv
import matplotlib.pyplot as plt


def main() -> None:
    """Create and display visualizations for indie game genre success patterns."""
    path = "data/processed/games_clean.csv"

    f = open(path, "r", encoding="utf-8")
    reader = csv.DictReader(f)

    #we only want Indie games
    indie_games: list[dict] = []

    for row in reader:
        genres_list: list[str] = row["genres"].split("|")

        is_indie: bool = False
        for g in genres_list:
            if g.strip().lower() == "indie":
                is_indie = True

        if is_indie == True:
            try:
                row["added"] = int(row["added"])
                row["rating"] = float(row["rating"])
                indie_games.append(row)
            except:
                pass

    f.close()

    #visualize genre frequency
    genre_counts: dict[str, int] = {}

    for g in indie_games:
        genres: list[str] = g["genres"].split("|")

        for genre in genres:
            if genre != "" and genre.lower() != "indie":
                genre_counts[genre] = genre_counts.get(genre, 0) + 1

    #sort genres by frequency
    genre_freq_list: list[tuple[int, str]] = []

    for genre in genre_counts:
        genre_freq_list.append((genre_counts[genre], genre))

    genre_freq_list.sort(reverse=True)

    top_genre_freq: list[tuple[int, str]] = genre_freq_list[:10]

    freq_values: list[int] = []
    freq_labels: list[str] = []

    for item in top_genre_freq:
        freq_values.append(item[0])
        freq_labels.append(item[1])

    plt.figure()
    plt.bar(freq_labels, freq_values)
    plt.title("Top Genres by Frequency (Indie Games)")
    plt.xlabel("Genre")
    plt.ylabel("Number of Games")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

    #visualize genre popularity, how many added games of certain genre into their library
    genre_added_totals: dict[str, int] = {}
    genre_rating_totals: dict[str, float] = {}

    for g in indie_games:
        genres: list[str] = g["genres"].split("|")

        for genre in genres:
            if genre != "" and genre.lower() != "indie":
                genre_added_totals[genre] = genre_added_totals.get(genre, 0) + g["added"]
                genre_rating_totals[genre] = genre_rating_totals.get(genre, 0) + g["rating"]

    genre_avg_added: list[tuple[float, str]] = []

    for genre in genre_counts:
        avg_added: float = genre_added_totals[genre] / genre_counts[genre]
        genre_avg_added.append((avg_added, genre))

    genre_avg_added.sort(reverse=True)

    top_avg_added: list[tuple[float, str]] = genre_avg_added[:10]

    avg_added_values: list[float] = []
    avg_added_labels: list[str] = []

    for item in top_avg_added:
        avg_added_values.append(item[0])
        avg_added_labels.append(item[1])

    plt.figure()
    plt.bar(avg_added_labels, avg_added_values)
    plt.title("Average Popularity by Genre (Indie Games)")
    plt.xlabel("Genre")
    plt.ylabel("Average Added")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

    #how do different genres compare in terms of popularity vs quality (add count vs rating score)
    genre_avg_rating: list[tuple[float, float, str]] = []

    for genre in genre_counts:
        avg_rating: float = genre_rating_totals[genre] / genre_counts[genre]
        avg_added: float = genre_added_totals[genre] / genre_counts[genre]
        genre_avg_rating.append((avg_rating, avg_added, genre))

    x_vals: list[float] = []
    y_vals: list[float] = []
    labels: list[str] = []

    for item in genre_avg_rating:
        x_vals.append(item[0])
        y_vals.append(item[1])
        labels.append(item[2])

    plt.figure()
    plt.scatter(x_vals, y_vals)
    plt.title("Popularity vs Rating by Genre (Indie Games)")
    plt.xlabel("Average Rating")
    plt.ylabel("Average Added")

    for i in range(len(labels)):
        plt.text(
            x_vals[i] + 0.01,
            y_vals[i] - 40,
            labels[i],
            fontsize=7
        )

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
