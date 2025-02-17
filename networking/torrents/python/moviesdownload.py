import subprocess

# List of titles
titles = [
"Nebraska (2013)",
"The Great Beauty (2013)",
"The Past (2013)",
"Godzilla vs. Kong",
"Redline",
"'The Mist (2007) [1080p] [YTS.AG]'",
"'The Negotiator (1998) [BluRay] [1080p] [YTS.LT]'",
"'The One I Love (2014) [1080p]'",
"'The Place Beyond the Pines (2012) [1080p]'",
"'The Raid 2 (2014) 1080p BluRay AV1 Opus MULTi3 [RAV1NE]'",
"'The Remains of the Day (1993) (1080p BluRay x265 HEVC 10bit AAC 5.1 Tigole)'",
"'The Score (2001) [BluRay] [1080p] [YTS.AM]'",
"'The Social Network (2010) [1080]'",
"'The Station Agent (2003) [WEBRip] [1080p] [YTS.LT]'",
"'The Talented Mr. Ripley (1999) + Extras (1080p BluRay x265 HEVC 10bit AAC 5.1 Silence)'",
"'The Uninvited (2009) [1080p]'",
"'The Village (2004) [1080p] [WEBRip] [5.1] [YTS.MX]'",
"'The Virgin Suicides (1999) [BluRay] [1080p] [YTS.AM]'",
"'The.Burial.2023.1080p.WEBRip.1400MB.DD5.1.x264-GalaxyRG[TGx]'",
"'The.Good.Nurse.2022.1080p.NF.WEBRip.1400MB.DD5.1.x264-GalaxyRG[TGx]'",
"'The.Holdovers.2023.1080p.WEBRip.1600MB.DD5.1.x264-GalaxyRG[TGx]'",
"The.Illusionist.2006.1080p.BluRay.x265-RBG.mp4",
"The.Life.of.David.Gale.2003.720p.BluRay.x264-x0r",
"The.Man.Without.a.Past.2002.1080p.BluRay.x265.HEVC.EAC3-SARTRE",
"The.Player.1992.Criterion.1080p.BluRay.x265.HEVC.AAC-SARTRE",
"The.Pledge.2001.1080p.BluRay.x265.HEVC.EAC3-SARTRE",
"The.Water.Diviner.2014.BDRip.1080p.H264.Ita,Eng.mkv",
"The.Zero.Theorem.2013.1080p.BluRay.x265",
"The.Zero.Theorem.2013.1080p.BluRay.x265.mp4",
"'This Is the End (2013) [1080p]'",
"'Three Colors Blue (1993) [BluRay] [1080p] [YTS.AM]'",
"'Three Colors Red (1994) [BluRay] [1080p] [YTS.AM]'",
"'Three Colors White (1994) [BluRay] [1080p] [YTS.AM]'",
"'Timecrimes (2007) [1080p] [BluRay] [5.1] [YTS.MX]'",
"Top.Gun.Maverick.2022.1080p.HDTS.V2.x264-HushRips.mkv",
"'Train To Busan (2016) [1080p] [YTS.AG]'",
"'True Grit (1969) [BluRay] [1080p] [YTS.LT]'",
"'True Romance (1993) [1080p]'",
"'Under the Skin (2013) [1080p]'",
"'Upstream Color (2013) [1080p]'",
"Whats.Eating.Gilbert.Grape.1993.1080p.BluRay.x264.YIFY.mp4",
"'Who Am I (2014) [BluRay] [1080p] [YTS.AM]'",
"'Wild Things 2 (2004) [WEBRip] [1080p] [YTS.AM]'",
"Woman.in.Gold.2015.1080p.BluRay.x265-RBG.mp4",
"'Your.Lucky.Day.2023.1080p.AMZN.WEBRip.1400MB.DD5.1.x264-GalaxyRG[TGx]'",
"'Ichi The Killer (2001) [BluRay] [1080p] [YTS.AM]'",
"'In America (2002) [1080p] [WEBRip] [5.1] [YTS.MX]'",
"In.The.Name.Of.The.Father.1993.1080p.BluRay.x265-RBG.mp4",
"'Infernal Affairs (2002) [1080p] [BluRay] [5.1] [YTS.MX]'",
"'Inside Llewyn Davis (2013) [1080p]'",
"'JFK 1991 Remastered 1080p BluRay HEVC x265 5.1 BONE.mkv'",
"Jackie.Brown.1997.1080p.BluRay.HEVC.EAC3-SARTRE",
"'Jacob'''s Ladder (2019) [WEBRip] [1080p] [YTS.LT]'",
"'Jeepers Creepers (2001) [1080p]'",
"'K-PAX (2001) (1080p D-VHS x265 HEVC 10bit AC3 5.1 Silence)'",
"Killers.Of.The.Flower.Moon.2023.1080p.WEBRip.1600MB.DD5.1.x264-GalaxyRG.mkv",
"'Killers.Of.The.Flower.Moon.2023.1080p.WEBRip.1600MB.DD5.1.x264-GalaxyRG[TGx]'",
"'Legend (2015) [1080p] [YTS.AG]'",
"'Love Actually 2003 Remastered 1080p BluRay HEVC x265 5.1 BONE.mkv'",
"'Me and Earl and the Dying Girl (2015) [1080p]'",
"'Million Dollar Arm (2014) [1080p]'",
"'Misery (1990) [BluRay] [1080p] [YTS.AM]'",
"'Monster'''s Ball (2001) (1080p BluRay x265 HEVC 10bit AAC 5.1 Silence)'",
"Morvern.Callar.2002.1080p.BluRay.x265.HEVC.AAC-SARTRE",
"'Moulin Rouge! (2001) [1080p]'",
"'Night Moves (2013) [1080p]'",
"'Nine.Queens.2000.Dvdrip[Eng.HC.Subs]Avi.Xvid[Toolie]'",
"'No Man'''s Land (2001) [BluRay] [1080p] [YTS.AM]'",
"'O Brother, Where Art Thou (2000) [1080p]'",
"'Oblivion (2013) [1080p]'",
"'Orphan (2009) [1080p]'",
"'Past.Lives.2023.1080p.WEBRip.1400MB.DD5.1.x264-GalaxyRG[TGx]'",
"'Philadelphia.1993.REMASTERED.1080p.BluRay.H264.AAC-LAMA[TGx]'",
"'Predestination (2014) [1080p]'",
"'Primal Fear (1996) [BluRay] [1080p] [YTS.AM]'",
"'Road to Predition (2002) [1080p]'",
"'Rush Hour (1998) (1080p BluRay x265 HEVC 10bit EAC3 5.1 YOGI)'",
"'Rush Hour 2 (2001) [1080p]'",
"RushHour320071080PHevcBluury",
"'SOUTH.PARK.JOINING.THE.PANDERVERSE.2023.1080p.WEB.H264-HUZZAH[TGx]'",
"'Side Effects (2013) [1080p]'",
"'Snatch (2000) [BluRay] [1080p] [YTS.AM]'",
"'Sorry To Bother You (2018) [BluRay] [1080p] [YTS.AM]'",
"'Southpaw (2015) [1080p]'",
"'Stardust (2007) [1080p]'",
"'Stranger Than Fiction (2006) [1080p]'",
"Strawberry.Mansion.2021.HDRip.XviD.AC3-EVO",
"Tenet.2020.1080p.HDRip.x264.AAC2.0-SHITBOX",
"'The Boondock Saints 1999 BluRay 1080p.H264 Ita Eng AC3 5.1 Sub Ita Eng ODS.mkv'",
"'The Butler (2013) [1080p]'",
"'The Commitments (1991) [BluRay] [1080p] [YTS.LT]'",
"'The Dressmaker (2015) (1080p BluRay x265 HEVC 10bit AAC 5.1 Tigole)'",
"'The Drop (2014) [1080p]'",
"'The Impossible 2012 1080p BRRip x264 AC3-JYK'",
"'The Intern (2015) [1080p] [YTS.AG]'",
"'The Judge (2014) [1080p]'",
"'The Last Emperor (1987) [BluRay] [1080p] [YTS.AM]'",
"'The Last King of Scotland (2006) (1080p BluRay x265 HEVC 10bit AAC 5.1 Silence)'",
"'The Limey (1999) [BluRay] [1080p] [YTS.LT]'",
"'The Lost Boys (1987) RM4K (1080p BluRay x265 HEVC 10bit AAC 5.1 Tigole)'",
"'The Lovely Bones (2009) [1080p]'",
"About a Boy",
"The Constant Gardener (2005)",
"Crazy, Stupid, Love.",
"A Quiet Place",
"The Conjuring",
"Platoon 1986",
"127 Hours",
"The Breakfast Club",
"Easy A",
"Speed 1994",
"Sleepy Hollow",
"Constantine 2005",
"Jack Reacher",
"50/50",
"Les Misérables 2012",
"Total Recall 1990",
"From Dusk Till Dawn",
"There's Something About Mary",
"O Brother, Where Art Thou?",
"The Man from U.N.C.L.E.",
"Gattaca",
"Pitch Perfect",
"The Accountant",
"The Fugitive",
"Apollo 13",
"Starship Troopers",
"The Patriot",
"Dredd",
"Stardust",
"Blade",
"The Goonies",
"Sully",
"Jerry Maguire",
"Office Space",
"The Accountant",
"True Lies",
"Vicky Cristina Barcelona",
"Paul 2011",
"Walk the Line",
"The Bucket List",
"The Descendants",
"Valkyrie",
"Philadelphia",
"Southpaw",
"Meet Joe Black",
"Lion 2016",
"Old School 2003",
"Munich",
"Los Idus de Marzo",
"Clerks",
"Hidden Figures",
"Closer 2004",
"Match Point 2005",
"Sleepers 1996",
"Everest 2015",
"Captain Fantastic",
"Bram Stoker's Dracula",
"Revolutionary Road",
"P.S. I Love You",
"Planet Terror",
"A Walk to Remember",
"I, Tonya",
"Finding Neverland",
"War Dogs",
"I Love You, Man",
"Misery",
"The Next Three Days",
"Straight Outta Compton",
"Blue Valentine",
"The Hunt for Red October",
"Darkest Hour",
"Shame 2011",
"Sideways 2004",
"The English Patient",
"Side Effects 2013",
"First Man 2018",
"Grindhouse",
"About a Boy",
"K-PAX",
"Ronin 1998",
"Dangal",
"Wonder 2017",
"Invictus 2009",
"Spy Game 2001",
"True Romance (1993)",
"Begin Again 2013",
"Allied 2016",
"JKF 1991",
"Wall Street 1987",
"The Skin I Live In",
"The House That Jack Built",
"'BlackBerry.2023.1080p.WEBRip.1400MB.DD5.1.x264-GalaxyRG[TGx]'",
"'Jesus.Revolution.2023.1080p.WEBRip.1400MB.DD5.1.x264-GalaxyRG[TGx]'",
"'Nightcrawler (2014) [1080p]'",
"'Saltburn.2023.1080p.AMZN.WEBRip.1600MB.DD5.1.x264-GalaxyRG[TGx]'",
"'Short Cuts (1993) [BluRay] [1080p] [YTS.AM]'",
"'Sleepers 1996 Open Matte 1080p WEB-DL HEVC x265 5.1 BONE.mkv'",
"'Sound.of.Freedom.2023.1080p.WEBRip.1600MB.DD5.1.x264-GalaxyRG[TGx]'",
"'A Most Violent Year (2014) [1080p]'",
"'Durante la tormenta-Mirage (2018).1080p.H264.ITA.SPA.Ac3-5.1.multisub-BaMax71-iDN'",
"'Frost Nixon (2008) (1080p BluRay50 x265 HEVC 10bit AAC 5.1 Silence)'",
"'Goldfinger (1964) [BluRay] [1080p] [YTS.AM]'",
"'Gone Baby Gone (2007) [1080p]'",
"'Hector and the Search for Happiness (2014) [1080p]'",
"Home.2009.1080p.BluRay.x265.HEVC.EAC3-SARTRE",
"May 2002",
"Charlotte's Net",
"The Dying Rooms",
"13th (2016)",
"Jiro Dreams of Sushi",
]

# Iterate over titles and run the command
for title in titles:
    command = ["python", "-m", "1337x", title]
    subprocess.run(command)
