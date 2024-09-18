#!/bin/bash

# Extract the csv folder from the tarball
echo "Extracting csv folder..."
tar -xzf csv.tar.gz
rm csv.tar.gz # Remove the tarball after extraction

# Extract the original title.ratings.tsv file
echo "Extracting title.ratings.tsv..."
gzip -d title.ratings.tsv.gz
