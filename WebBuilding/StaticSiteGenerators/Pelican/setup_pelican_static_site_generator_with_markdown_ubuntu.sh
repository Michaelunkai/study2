#!/bin/ 

# Step 1: Install Python and Pip
sudo apt install -y python3 python3-pip

# Step 2: Install Pelican and Markdown
pip3 install pelican markdown

# Step 3: Create Project Directory and Initialize Pelican
mkdir my_blog
cd my_blog
pelican-quickstart <<EOF
my_blog
n
http://example.com
n
en
UTC
n
y
EOF

# Step 4: Create Content Directory and Add a Sample Post
mkdir content
echo -e "Title: My First Post\nDate: 2024-08-29\nCategory: Blog\nTags: example, pelican\nSlug: my-first-post\nAuthor: Micha\nSummary: This is a summary of my first post.\n\nThis is the content of my first blog post." > content/my_first_post.md

# Step 5: Generate the Static Site
pelican content

# Step 6: Preview the Site
pelican --listen
