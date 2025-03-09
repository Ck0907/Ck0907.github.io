from rapidfuzz import fuzz
import pandas as pd

def load_data(file1, file2):
    df1 = pd.read_csv(file1, encoding="ISO-8859-1")
    df2 = pd.read_csv(file2, encoding="ISO-8859-1")
    return df1, df2

def compare_titles(df1, df2, threshold=85):
    matches = []
    rating_match_count = 0
    year_match_count = 0
    all_matches = pd.DataFrame(columns=["ID", "ltable_ID", "rtable_ID", "ltable_Title", "ltable_ratingIMDB", "rtable_metascore","ltable_MPA_Rating","ltable_IMDB Year"])  # Initialize as DataFrame
    id = 0

    for _, row1 in df1.iterrows():
        best_match = None
        best_score = 0
        best_row = None

        for _, row2 in df2.iterrows():

            row1StringArr = str(row1['title']).split(".")
            if len(row1StringArr) > 2:
                row1StringArr[0] = ""
                row1String = ".".join(row1StringArr[1:])
            else:
                row1String = row1StringArr[1]

            row2StringArr = str(row2['title']).split(".")
            if len(row2StringArr) > 2:
                row2StringArr[0] = ""
                row2String = ".".join(row2StringArr[1:])
            else:
                row2String = row2StringArr[1]

            # Calculate fuzzy score
            score = fuzz.ratio(row1String.strip(), row2String.strip())
            if score > best_score:
                best_score = score
                best_match = row2String.strip()
                best_row = row2
        if best_score>= 100 and best_row is not None:

            rating_match = str(row1['MPA_rating']).strip() == str(best_row['MPA_rating']).strip()


            try:
                year_b = str(best_row['date']).strip().split("/")[-1]
            except IndexError:
                year_b = ""

            year_match = str(row1['date']).strip() == year_b.strip()

            rating_status = "rating_match" if rating_match else "rating_dont_match"
            year_status = "year_match" if year_match else "year_dont_match"

            matches.append((row1String.strip(), best_match, best_score, rating_status, year_status))

            id += 1


            new_row = pd.DataFrame([{
                "ID": id, "ltable_ID": row1['id'], "rtable_ID": best_row['id'], "ltable_Title": row1String.strip(),
                "ltable_ratingIMDB": row1['rating'], "rtable_metascore": best_row['rating'], "ltable_MPA_Rating": row1['MPA_rating'],
                "ltable_IMDB Year": row1['date']
            }])
            all_matches = pd.concat([all_matches, new_row], ignore_index=True)

        elif best_score >= threshold and best_row is not None:

            rating_match = str(row1['MPA_rating']).strip() == str(best_row['MPA_rating']).strip()


            try:
                year_b = str(best_row['date']).strip().split("/")[-1]
            except IndexError:
                year_b = ""

            year_match = str(row1['date']).strip() == year_b.strip()

            rating_status = "rating_match" if rating_match else "rating_dont_match"
            year_status = "year_match" if year_match else "year_dont_match"

            matches.append((row1String.strip(), best_match, best_score, rating_status, year_status))

            id +=1

            print(f"Mismatch Found: '{row1String.strip()}' (Rating: {row1['MPA_rating']}, Year: {row1['date']})")
            print(f"Best Match: '{best_row['title']}' (Rating: {best_row['MPA_rating']}, Year: {best_row['date']})")
            print("-" * 40)

            i = input()
            if i == "y":
                new_row = pd.DataFrame([{
                    "ID": id, "ltable_ID": row1['id'], "rtable_ID": best_row['id'], "ltable_Title": row1String.strip(),
                    "ltable_ratingIMDB": row1['rating'], "rtable_metascore": best_row['rating'], "ltable_MPA_Rating": row1['MPA_rating'],
                    "ltable_IMDB Year": row1['date']
                }])
                all_matches = pd.concat([all_matches, new_row], ignore_index=True)


    return matches, rating_match_count, year_match_count, all_matches

def main():
    file1 = "TableIMDB_A.csv"
    file2 = "TableMeta_B.csv"
    df1, df2 = load_data(file1, file2)

    matches, rating_match_count, year_match_count, all_matches = compare_titles(df1, df2)

    for title1, title2, score, ratingMatch, yearMatch in matches:
        print(f"Match Found: '{title1}' ~ '{title2}' ({ratingMatch}, {yearMatch}) (Score: {score})")

    print(f"\nTotal Matches where rating and year match: {rating_match_count} , {year_match_count}")
    print(f"Total matches: {len(matches)}")


    if not all_matches.empty:
        all_matches.to_csv("matchedTitles_C.csv", index=False)
        print("\nExported matched titles to 'matched_titles.csv'.")

if __name__ == "__main__":
    main()
