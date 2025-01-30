#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# ------------------------------------------------
# Configuration Variables
# ------------------------------------------------

INPUT_FILE="combined.txt"
CLEANED_CSV="cleaned.csv"
DATABASE="combined.db"
DELIMITER="-"

DEFAULT_PLATFORM="Unknown"
DEFAULT_GENRE="Unknown"
DEFAULT_RELEASE_YEAR=2023

COLUMNS=("title" "critic_score" "platform" "genre" "release_year")

# ------------------------------------------------
# Step 1: Validate Input File
# ------------------------------------------------

if [[ ! -f "$INPUT_FILE" ]]; then
    echo "Error: Input file '$INPUT_FILE' does not exist." >&2
    exit 1
fi

# ------------------------------------------------
# Step 2: Preprocess the Input File
# ------------------------------------------------

echo "Preprocessing '$INPUT_FILE' into '$CLEANED_CSV'..."

rm -f "$CLEANED_CSV"

awk -v FS=" *$DELIMITER *" -v OFS="," \
    -v default_platform="$DEFAULT_PLATFORM" \
    -v default_genre="$DEFAULT_GENRE" \
    -v default_release_year="$DEFAULT_RELEASE_YEAR" \
    '
{
    # Skip empty lines
    if (NF == 0) next;

    # Ensure there are at least two fields (title and critic_score)
    if (NF < 2) next;

    title = $1;
    critic_score = $2;
    platform = (NF >= 3) ? $3 : default_platform;
    genre = (NF >= 4) ? $4 : default_genre;
    release_year = (NF >= 5 && $5 ~ /^[0-9]{4}$/) ? $5 : default_release_year;

    # Trim whitespace
    gsub(/^[ \t]+|[ \t]+$/, "", title);
    gsub(/^[ \t]+|[ \t]+$/, "", critic_score);
    gsub(/^[ \t]+|[ \t]+$/, "", platform);
    gsub(/^[ \t]+|[ \t]+$/, "", genre);

    # Escape double quotes in textual fields
    gsub(/"/, "\"\"", title);
    gsub(/"/, "\"\"", platform);
    gsub(/"/, "\"\"", genre);

    # Validate critic_score
    if (critic_score !~ /^[0-9]+(\.[0-9]+)?$/) {
        critic_score = "NULL";
    }

    # Print as CSV
    printf("\"%s\",%s,\"%s\",\"%s\",%d\n", title, critic_score, platform, genre, release_year);
}' "$INPUT_FILE" > "$CLEANED_CSV"

echo "Preprocessing completed. Cleaned data saved to '$CLEANED_CSV'."

# ------------------------------------------------
# Step 3: Create SQLite Database and Table
# ------------------------------------------------

echo "Creating SQLite database '$DATABASE' and table 'games'..."

rm -f "$DATABASE"

CREATE_TABLE_SQL="
CREATE TABLE games (
    title TEXT NOT NULL,
    critic_score REAL,
    platform TEXT,
    genre TEXT,
    release_year INTEGER
);
"

sqlite3 "$DATABASE" <<SQL
BEGIN TRANSACTION;
$CREATE_TABLE_SQL
COMMIT;
SQL

echo "Database and table created successfully."

# ------------------------------------------------
# Step 4: Import Cleaned Data into SQLite
# ------------------------------------------------

echo "Importing cleaned data into SQLite..."

sqlite3 "$DATABASE" <<SQL
.mode csv
.separator ","
.import $CLEANED_CSV games
SQL

echo "Data imported successfully."

# ------------------------------------------------
# Step 5: Verify Import
# ------------------------------------------------

RECORD_COUNT=$(sqlite3 "$DATABASE" "SELECT COUNT(*) FROM games;")
echo "Total records imported: $RECORD_COUNT"

# ------------------------------------------------
# Step 6: Clean Up
# ------------------------------------------------

rm -f "$CLEANED_CSV"

echo "Cleanup completed."
echo "Import process completed successfully."
