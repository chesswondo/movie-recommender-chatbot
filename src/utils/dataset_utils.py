import pandas as pd

def filter_dataframe(df, year="-1", genre="-1"):
    # Parse year and genre inputs, handling "-1" as a special case to ignore the filter
    year_filter = set(year.split(", ")) if year != "-1" else None
    genre_filter = set(genre.lower().split(", ")) if genre != "-1" else None

    # Define a function to check if a row matches the genre filter
    def genre_match(row_genre):
        row_genres = set(g.lower() for g in eval(row_genre))  # Convert to lowercase
        return bool(row_genres & genre_filter) if genre_filter else True

    # Apply the year and genre filters
    filtered_df = df[
        ((df['year'].apply(lambda y: str(y) in year_filter)) if year_filter else True) &
        (df['genres'].apply(genre_match))
    ]
    
    return filtered_df