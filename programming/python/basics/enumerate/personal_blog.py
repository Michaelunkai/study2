posts = ['My First Blog Post', 'A Day in the Life', 'Understanding Python']


print("Blog Posts:")
for number, post in enumerate(posts, start=1):
    print(f"{number}. {post}")