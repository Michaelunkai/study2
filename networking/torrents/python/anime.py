import subprocess

# List of titles
titles = [
"Kôkaku Kidôtai",
"Saiki Kusuo no Psi Nan",
"March Comes In like a Lion",
"Beck: Mongolian Chop Squad",
"Shôwa Genroku Rakugo Shinjû",
"Golden Boy",
"Bakuman",
"monster",
"Rurouni Kenshin",
"Mushi-Shi",
"Yu Yu Hakusho: Ghost Files",
"Baccano!",
" Serial Experiments Lain ",
" Wolf's Rain",
" KILL la KILL",
" Darker Than Black",
"Frieren: Beyond Journey's End",
"Haikyu!!",
"Mob Psycho 100",
"Run with the Wind",
"Neon Genesis Evangelion",
"Violet Evergarden",
"My Hero Academia",
"Gintama",
"Monster Rancher",
"The Melancholy of Harumi Suzumiya",
"Yuri!!! On Ice",
"Kakegurui",
"Slam Dunk",
"Detective Conan",
" 91 Days",
" Basilisk: The Kouga Ninja Scrolls ",
" Beck: Mongolian Chop Squad",
" 5 Centimeters per Second",
" City Hunter ",
" The Disastrous Life of Saiki K.",
" Showa Genroku Rakugo Shinju"
" Kids on the Slope",
"usagi drop",
"Wolf Children",
"Planetes",
" Gungrave ",



]

# Iterate over titles and run the command
for title in titles:
    command = ["python", "-m", "1337x", title + " dual audio"]
    subprocess.run(command)

