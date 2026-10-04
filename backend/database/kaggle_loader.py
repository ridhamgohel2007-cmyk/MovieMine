"""
MovieMine Kaggle Dataset Processor & Realistic Data Generator
Academic Topic: KDD Pipeline - Data Extraction & Synthesis from The Movies Dataset / MovieLens

Citations:
1. The Movies Dataset (Kaggle): https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset
2. MovieLens Small Latest Dataset: https://www.kaggle.com/datasets/shubhammehta21/movie-lens-small-latest-dataset
"""

import os
import random
import datetime
import pandas as pd
from pathlib import Path

# Popular real-world movies curated from Kaggle / TMDB / MovieLens with real poster images
CURATED_MOVIES = [
    # Sci-Fi / Action
    ("Inception", 2010, 148, "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.", "English", 8.8, ["Action", "Sci-Fi", "Adventure"], "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg"),
    ("Interstellar", 2014, 169, "When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team of researchers, to find a new planet for humans.", "English", 8.7, ["Adventure", "Drama", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg"),
    ("The Matrix", 1999, 136, "When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth--the life he knows is the elaborate deception of an evil cyber-intelligence.", "English", 8.7, ["Action", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg"),
    ("The Dark Knight", 2008, 152, "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.", "English", 9.0, ["Action", "Crime", "Drama"], "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg"),
    ("The Dark Knight Rises", 2012, 164, "Eight years after the Joker's reign of chaos, Batman is forced to resurface to protect Gotham City from the brutal guerrilla terrorist Bane.", "English", 8.4, ["Action", "Thriller"], "https://image.tmdb.org/t/p/w500/hr0L2aueqlP2BYUblTTjmtn0hw4.jpg"),
    ("Batman Begins", 2005, 140, "After training with his mentor, Batman begins his fight to free crime-ridden Gotham City from corruption.", "English", 8.2, ["Action", "Crime", "Drama"], "https://image.tmdb.org/t/p/w500/1P3GslsqN0jT5bVzG717hL1A5gS.jpg"),
    ("Avengers: Endgame", 2019, 181, "After the devastating events of Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more to reverse Thanos' actions.", "English", 8.4, ["Action", "Adventure", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg"),
    ("Avengers: Infinity War", 2018, 149, "The Avengers and their allies must be willing to sacrifice all in an attempt to defeat the powerful Thanos before his blitz of devastation puts an end to the universe.", "English", 8.4, ["Action", "Adventure", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/7WsyChQLEftFiDOVTGkv3hFpyyt.jpg"),
    ("The Avengers", 2012, 143, "Earth's mightiest heroes must come together and learn to fight as a team if they are going to stop the mischievous Loki and his alien army from enslaving humanity.", "English", 8.0, ["Action", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/RYMX2wcKCBAr24UyPD7xwmjaTn.jpg"),
    ("Iron Man", 2008, 126, "After being held captive in an Afghan cave, billionaire engineer Tony Stark creates a unique weaponized suit of armor to fight evil.", "English", 7.9, ["Action", "Adventure", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/78lPtwv72eTNqFW9COBYI0dWDJa.jpg"),
    ("Iron Man 3", 2013, 130, "When Tony Stark's world is torn apart by a formidable terrorist called the Mandarin, he starts an odyssey of rebuilding and retribution.", "English", 7.1, ["Action", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/qhPtAc1TKbMPqNvcdXSOn9Bn7hZ.jpg"),
    ("Captain America: Civil War", 2016, 147, "Political involvement in the Avengers' affairs causes a rift between Captain America and Iron Man.", "English", 7.8, ["Action", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/rAGiXaUfPzY7CnjyNKsqvdM99No.jpg"),
    ("Spider-Man: No Way Home", 2021, 148, "With Spider-Man's identity now revealed, Peter asks Doctor Strange for help. When a spell goes wrong, dangerous foes from other worlds appear.", "English", 8.2, ["Action", "Adventure", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg"),
    ("Spider-Man: Into the Spider-Verse", 2018, 117, "Teen Miles Morales becomes the new Spider-Man and joins other Spider-Heroes from parallel dimensions to stop a threat to all reality.", "English", 8.4, ["Animation", "Action", "Adventure"], "https://image.tmdb.org/t/p/w500/iiZZdoQBEYBv6id8su7ImL0oCbD.jpg"),
    ("Avatar", 2009, 162, "A paraplegic Marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.", "English", 7.9, ["Action", "Adventure", "Fantasy", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/kyeqWdyUXW608qlYkRqosgbbJyK.jpg"),
    ("Avatar: The Way of Water", 2022, 192, "Jake Sully lives with his newfound family formed on the extrasolar moon Pandora. Once a familiar threat returns to finish what was previously started, Jake must work with Neytiri.", "English", 7.6, ["Action", "Adventure", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"),
    ("The Martian", 2015, 144, "An astronaut becomes stranded on Mars after his team assume him dead, and must rely on his ingenuity to find a way to signal to Earth that he is alive.", "English", 8.0, ["Adventure", "Drama", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/5BHuvQ6p9kL09NM279hDYW8572P.jpg"),
    ("Gravity", 2013, 91, "Two astronauts work together to survive after an accident leaves them stranded in space.", "English", 7.7, ["Drama", "Sci-Fi", "Thriller"], "https://image.tmdb.org/t/p/w500/2LNSZf96B2yqJqM3aFhXqM1p1zF.jpg"),
    ("Arrival", 2016, 116, "A linguist works with the military to communicate with alien lifeforms after twelve mysterious spacecraft appear around the world.", "English", 7.9, ["Drama", "Mystery", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/x2FJsf1ElAgr63Y3PNPtJrcmpoe.jpg"),
    ("Blade Runner 2049", 2017, 164, "Young Blade Runner K's discovery of a long-buried secret leads him to track down former Blade Runner Rick Deckard, who's been missing for thirty years.", "English", 8.0, ["Action", "Drama", "Mystery", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/gajva2L0rPYkEWjzgFlBXCAVBE5.jpg"),
    ("Jurassic Park", 1993, 127, "A pragmatic paleontologist touring an almost complete theme park on an island in Central America is tasked with protecting a couple of kids after a power failure causes the cloned dinosaurs to run loose.", "English", 8.2, ["Action", "Adventure", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/oU7Oq2kFAAlGqbU4VoAE36g4hoI.jpg"),
    ("Jurassic World", 2015, 124, "A new theme park, built on the original site of Jurassic Park, creates a genetically modified hybrid dinosaur, the Indominus Rex, which escapes containment and goes on a killing spree.", "English", 6.9, ["Action", "Adventure", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/A0LZH8JlsQj6c8mox7f7eKqB22w.jpg"),
    ("Dune", 2021, 155, "A noble family becomes embroiled in a war for control over the galaxy's most valuable asset while its heir becomes troubled by visions of a dark future.", "English", 8.0, ["Action", "Adventure", "Drama", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/d5NXSklXo0qyIYkgV94XAgMIckC.jpg"),
    ("Dune: Part Two", 2024, 166, "Paul Atreides unites with Chani and the Fremen while seeking revenge against the conspirators who destroyed his family.", "English", 8.6, ["Action", "Adventure", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/1pdfLvkbY9ohJlCjQH2CZjjYVvJ.jpg"),
    ("Terminator 2: Judgment Day", 1991, 137, "A cyborg, identical to the one who failed to kill Sarah Connor, must now protect her ten-year-old son John from an even more advanced and powerful cyborg.", "English", 8.6, ["Action", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/5M0j0B18abtBI5P2nnQiY06I9zg.jpg"),
    ("Mad Max: Fury Road", 2015, 120, "In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler in search for her homeland with the aid of a group of female prisoners and a drifter named Max.", "English", 8.1, ["Action", "Adventure", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/hA2ple9q4qnwxp3hKVNhroipsir.jpg"),

    # Drama & Classics
    ("The Shawshank Redemption", 1994, 142, "Over the course of several years, two convicts form a friendship, seeking consolation and, eventually, redemption through basic compassion.", "English", 9.3, ["Drama"], "https://image.tmdb.org/t/p/w500/9cqNxx0GxF0bflZmeSMuL5tnGzr.jpg"),
    ("The Godfather", 1972, 175, "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.", "English", 9.2, ["Crime", "Drama"], "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg"),
    ("The Godfather Part II", 1974, 202, "The early life and career of Vito Corleone in 1920s New York City is portrayed, while his son, Michael, expands and tightens his grip on the family crime syndicate.", "English", 9.0, ["Crime", "Drama"], "https://image.tmdb.org/t/p/w500/hek3koDUyMrk7uOBzWq39f60u9v.jpg"),
    ("Forrest Gump", 1994, 142, "The history of the United States from the 1950s to the '70s unfolds from the perspective of an Alabama man with an IQ of 75, who yearns to be reunited with his childhood sweetheart.", "English", 8.8, ["Drama", "Romance"], "https://image.tmdb.org/t/p/w500/arw2tPUoHG9ipiyvBPdfKiOXY9n.jpg"),
    ("Titanic", 1997, 194, "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.", "English", 7.9, ["Drama", "Romance"], "https://image.tmdb.org/t/p/w500/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg"),
    ("Gladiator", 2000, 155, "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.", "English", 8.5, ["Action", "Adventure", "Drama"], "https://image.tmdb.org/t/p/w500/ty8TGRuvJLPUmAR1H1nRIsgwvim.jpg"),
    ("Schindler's List", 1993, 195, "In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazis.", "English", 9.0, ["Biography", "Drama", "History"], "https://image.tmdb.org/t/p/w500/sF1U4EUQS8YHUYjNl3pMGNIQyr0.jpg"),
    ("Pulp Fiction", 1994, 154, "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.", "English", 8.9, ["Crime", "Drama"], "https://image.tmdb.org/t/p/w500/vQWk5YBFWF4bZaofAbv0tShwBvQ.jpg"),
    ("Fight Club", 1999, 139, "An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into much more.", "English", 8.8, ["Drama"], "https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg"),
    ("Goodfellas", 1990, 145, "The story of Henry Hill and his life in the mafia, covering his relationship with his wife Karen and his mob partners Jimmy Conway and Tommy DeVito.", "English", 8.7, ["Biography", "Crime", "Drama"], "https://image.tmdb.org/t/p/w500/aKuFiU82s5ISJpGZp7YkIr3kCUd.jpg"),
    ("The Prestige", 2006, 130, "After a tragic accident, two stage magicians in 1890s London engage in a battle to create the ultimate illusion while sacrificing everything they have to outwit each other.", "English", 8.5, ["Drama", "Mystery", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/tRNlZbgNCNOpLpbPEz5L8G8A0JN.jpg"),
    ("Whiplash", 2014, 106, "A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are mentored by an instructor who will stop at nothing to realize a student's potential.", "English", 8.5, ["Drama", "Music"], "https://image.tmdb.org/t/p/w500/7fn624j5lj3xTme2SgiLCeuedmO.jpg"),
    ("The Social Network", 2010, 120, "As Harvard student Mark Zuckerberg creates the social networking site that would become known as Facebook, he is sued by the twins who claimed he stole their idea.", "English", 7.8, ["Biography", "Drama"], "https://image.tmdb.org/t/p/w500/n0ybibhJtQ5icDqTpTcvRnv0YvB.jpg"),
    ("Oppenheimer", 2023, 180, "The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb.", "English", 8.9, ["Biography", "Drama", "History"], "https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg"),

    # Animation & Family
    ("Toy Story", 1995, 81, "A cowboy doll is profoundly threatened and jealous when a new spaceman action figure supplants him as top toy in a boy's bedroom.", "English", 8.3, ["Animation", "Adventure", "Comedy"], "https://image.tmdb.org/t/p/w500/uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg"),
    ("Toy Story 3", 2010, 103, "The toys are mistakenly delivered to a day-care center instead of the attic right before Andy leaves for college, and it's up to Woody to convince the other toys that they weren't abandoned.", "English", 8.3, ["Animation", "Adventure", "Comedy"], "https://image.tmdb.org/t/p/w500/AbbXspwhIR19YsjeTvrmFiBAFbZ.jpg"),
    ("Finding Nemo", 2003, 100, "After his son is captured in the Great Barrier Reef and taken to Sydney, a timid clownfish sets out on a journey to bring him home.", "English", 8.2, ["Animation", "Adventure", "Comedy"], "https://image.tmdb.org/t/p/w500/eHuGQ10FUzK1mdOY692F5qGVEZe.jpg"),
    ("The Lion King", 1994, 88, "Lion prince Simba and his father are targeted by his bitter uncle, who wants to ascend the throne himself.", "English", 8.5, ["Animation", "Adventure", "Drama"], "https://image.tmdb.org/t/p/w500/sKCr78MXSLixwmZ8DyJLrpMsd15.jpg"),
    ("Up", 2009, 96, "78-year-old Carl Fredricksen travels to Paradise Falls in his house equipped with balloons, inadvertently taking a young stowaway.", "English", 8.3, ["Animation", "Adventure", "Comedy"], "https://image.tmdb.org/t/p/w500/vpbaStTMt8qqGBE2580rBgHNQMe.jpg"),
    ("WALL-E", 2008, 98, "In the distant future, a small waste-collecting robot inadvertently embarks on a space journey that will ultimately decide the fate of mankind.", "English", 8.4, ["Animation", "Adventure", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/hbhFnRzzg6ZDmm8YAmxBnQpQIPh.jpg"),
    ("Spirited Away", 2001, 125, "During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches and spirits, and where humans are changed into beasts.", "Japanese", 8.6, ["Animation", "Adventure", "Family", "Fantasy"], "https://image.tmdb.org/t/p/w500/39wmItIWsg5sZMyRUHLkWBcuVCM.jpg"),
    ("Coco", 2017, 105, "Aspiring musician Miguel, confronted with his family's ancestral ban on music, enters the Land of the Dead to find his great-great-grandfather, a legendary singer.", "English", 8.4, ["Animation", "Adventure", "Family"], "https://image.tmdb.org/t/p/w500/gGEsBPAijhVUFoiNpgZXqRVWJt2.jpg"),
    ("Inside Out", 2015, 95, "After young Riley is uprooted from her Midwest life and moved to San Francisco, her emotions - Joy, Fear, Anger, Disgust and Sadness - conflict on how best to navigate a new city.", "English", 8.1, ["Animation", "Adventure", "Comedy"], "https://image.tmdb.org/t/p/w500/2H1TmgdfNbfKlUkjlOXMNSlB1Cr.jpg"),
    ("Shrek", 2001, 90, "A mean lord exiles fairytale creatures to the swamp of a grumpy ogre, who must go on a quest and rescue a princess for the lord in order to get his land back.", "English", 7.9, ["Animation", "Adventure", "Comedy"], "https://image.tmdb.org/t/p/w500/iB64vpL3dIObOtMZgX3RqWCPCPo.jpg"),

    # Comedy & Romance
    ("The Grand Budapest Hotel", 2014, 99, "A writer encounters the owner of an aging high-class hotel, who tells him of his early years serving as a lobby boy in the hotel's glorious years under an exceptional concierge.", "English", 8.1, ["Adventure", "Comedy", "Crime"], "https://image.tmdb.org/t/p/w500/eWdyYQreja6JGCzqHWX9NZkt5BW.jpg"),
    ("Superbad", 2007, 113, "Two co-dependent high school seniors are forced to deal with separation anxiety after their plan to stage a booze-soaked party goes awry.", "English", 7.6, ["Comedy"], "https://image.tmdb.org/t/p/w500/ek8e8txUyUwd2BNqj6lFEerJqEB.jpg"),
    ("The Hangover", 2009, 100, "Three buddies wake up from a bachelor party in Las Vegas, with no memory of the previous night and the bachelor missing. They make their way around the city in order to find their friend.", "English", 7.7, ["Comedy"], "https://image.tmdb.org/t/p/w500/uluhlXubGu1VxU63X9VgMeQvXxx.jpg"),
    ("La La Land", 2016, 128, "While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their aspirations for the future.", "English", 8.0, ["Comedy", "Drama", "Music", "Romance"], "https://image.tmdb.org/t/p/w500/uDO8zWDhfWwoFdKS4fzkVJb0Rf0.jpg"),
    ("Crazy Rich Asians", 2018, 120, "This contemporary romantic comedy, based on a global bestseller, follows native New Yorker Rachel Chu to Singapore to meet her boyfriend's family.", "English", 6.9, ["Comedy", "Romance"], "https://image.tmdb.org/t/p/w500/gnTqi6b7puv6Ww232eA1vWqQv4t.jpg"),
    ("Groundhog Day", 1993, 101, "A narcissistic TV weatherman, along with his attractive producer and cynical cameraman, is sent to report on Groundhog Day in the small town of Punxsutawney, where he finds himself repeating the same day over and over.", "English", 8.0, ["Comedy", "Fantasy", "Romance"], "https://image.tmdb.org/t/p/w500/7u37H8dsxOhnhn2AqU99w30u7y5.jpg"),
    ("Knives Out", 2019, 130, "A detective investigates the death of a patriarch of an eccentric, combative family.", "English", 7.9, ["Comedy", "Crime", "Drama", "Mystery"], "https://image.tmdb.org/t/p/w500/pThyQovXQrw2m0s9x82twj48Jq4.jpg"),
    ("The Wolf of Wall Street", 2013, 180, "Based on the true story of Jordan Belfort, from his rise to a wealthy stock-broker living the high life to his fall involving crime, corruption and the federal government.", "English", 8.2, ["Biography", "Comedy", "Crime"], "https://image.tmdb.org/t/p/w500/34m2tygAYBGqA9MXKhRDtzYd4MR.jpg"),

    # Horror & Thriller
    ("The Shining", 1980, 146, "A family heads to an isolated hotel for the winter where a sinister presence influences the father into violence, while his psychic son sees horrific forebodings from both past and future.", "English", 8.4, ["Drama", "Horror"], "https://image.tmdb.org/t/p/w500/b33nnKl12nLoTQiq5tQYh5cO4b.jpg"),
    ("Psycho", 1960, 109, "A Phoenix secretary embezzles $40,000 from her employer's client, goes on the run and checks into a remote motel run by a young man under the domination of his mother.", "English", 8.5, ["Horror", "Mystery", "Thriller"], "https://image.tmdb.org/t/p/w500/yz45KMrciuC5kQ12cbgwL3LuYt4.jpg"),
    ("Get Out", 2017, 104, "A young African-American visits his white girlfriend's parents for the weekend, where his simmering uneasiness about their reception of him eventually reaches a boiling point.", "English", 7.8, ["Horror", "Mystery", "Thriller"], "https://image.tmdb.org/t/p/w500/tFXcEccSQMf3lfhfXKSU9iRBpa3.jpg"),
    ("A Quiet Place", 2018, 90, "In a post-apocalyptic world, a family is forced to live in silence while hiding from monsters with ultra-sensitive hearing.", "English", 7.5, ["Drama", "Horror", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/nAU74GmpUk7t5iklEp3bufwDq4n.jpg"),
    ("Se7en", 1995, 127, "Two detectives, a rookie and a veteran, hunt a serial killer who uses the seven deadly sins as his motives.", "English", 8.6, ["Crime", "Drama", "Mystery", "Thriller"], "https://image.tmdb.org/t/p/w500/6yoghtyTpznpBik8EngEmJskVUO.jpg"),
    ("The Silence of the Lambs", 1991, 118, "A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer.", "English", 8.6, ["Crime", "Drama", "Thriller"], "https://image.tmdb.org/t/p/w500/uS9m8OBk1A8eM9I042bx8XXpqAq.jpg"),
    ("Parasite", 2019, 132, "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.", "Korean", 8.5, ["Drama", "Thriller"], "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg"),
    ("Shutter Island", 2010, 138, "In 1954, a U.S. Marshal investigates the disappearance of a murderer who escaped from a hospital for the criminally insane.", "English", 8.2, ["Mystery", "Thriller"], "https://image.tmdb.org/t/p/w500/kve20wgB2Zq4gGhNo226IRZeBTx.jpg"),

    # Fantasy & Adventure
    ("The Lord of the Rings: The Fellowship of the Ring", 2001, 178, "A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.", "English", 8.9, ["Action", "Adventure", "Drama", "Fantasy"], "https://image.tmdb.org/t/p/w500/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg"),
    ("The Lord of the Rings: The Two Towers", 2002, 179, "While Frodo and Sam edge closer to Mordor with the help of the shifty Gollum, the divided fellowship makes a stand against Sauron's new ally, Saruman.", "English", 8.8, ["Action", "Adventure", "Drama", "Fantasy"], "https://image.tmdb.org/t/p/w500/5VTN0pR8gcqV3EPUHHfMGnJYN9L.jpg"),
    ("The Lord of the Rings: The Return of the King", 2003, 201, "Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring.", "English", 9.0, ["Action", "Adventure", "Drama", "Fantasy"], "https://image.tmdb.org/t/p/w500/rCzpDGLbOoPwLjy3OAm5NUPOTrC.jpg"),
    ("Harry Potter and the Sorcerer's Stone", 2001, 152, "An orphaned boy enrolls in a school of wizardry, where he learns the truth about himself, his family and the terrible evil that haunts the magical world.", "English", 7.6, ["Adventure", "Family", "Fantasy"], "https://image.tmdb.org/t/p/w500/wuMc08IPKEatv9rnMNXvIDxqP4W.jpg"),
    ("Harry Potter and the Prisoner of Azkaban", 2004, 142, "Harry Potter, Ron and Hermione return to Hogwarts School of Witchcraft and Wizardry for their third year of study, where they delve into the mystery surrounding an escaped prisoner.", "English", 7.9, ["Adventure", "Family", "Fantasy"], "https://image.tmdb.org/t/p/w500/aWxHgpL2718E1TcxC9wT23Y2eD1.jpg"),
    ("Pirates of the Caribbean: The Curse of the Black Pearl", 2003, 143, "Blacksmith Will Turner teams up with eccentric pirate \"Captain\" Jack Sparrow to save his love, the governor's daughter, from Jack's former pirate allies.", "English", 8.1, ["Action", "Adventure", "Fantasy"], "https://image.tmdb.org/t/p/w500/z8onk7LV9MPk6zpmCe5V740vdLI.jpg")
]

# Expand list systematically to 220+ realistic movies by pairing classic templates with subgenres
ADDITIONAL_TEMPLATES = [
    ("Alien", 1979, 117, "The crew of a commercial spacecraft encounters a deadly lifeform after investigating an unknown transmission.", "English", 8.5, ["Horror", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/vfrQk5IPloGg1v9Rzmu2u02iRmS.jpg"),
    ("Aliens", 1986, 137, "Decades after surviving the Nostromo incident, Ellen Ripley is sent back to the planetoid LV-426 with a unit of Colonial Marines.", "English", 8.4, ["Action", "Adventure", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/b1bdEb6Y4oXbN136709qF4eXU5L.jpg"),
    ("Inglourious Basterds", 2009, 153, "In Nazi-occupied France during World War II, a plan to assassinate Nazi leaders by a group of Jewish U.S. soldiers coincides with a theatre owner's vengeful plans.", "English", 8.4, ["Adventure", "Drama", "War"], "https://image.tmdb.org/t/p/w500/7sfbEnaARXDD5P0ms7ms1QW2vP0.jpg"),
    ("Django Unchained", 2012, 165, "With the help of a German bounty-hunter, a freed slave sets out to rescue his wife from a brutal Mississippi plantation owner.", "English", 8.5, ["Drama", "Western"], "https://image.tmdb.org/t/p/w500/7oWY8vdWW7thTzWh3OKYRkWUlD5.jpg"),
    ("The Departed", 2006, 151, "An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang in South Boston.", "English", 8.5, ["Crime", "Drama", "Thriller"], "https://image.tmdb.org/t/p/w500/nT97ifvt2J1yMQmeq20Qblg61T.jpg"),
    ("Memento", 2000, 113, "A man with short-term memory loss attempts to track down his wife's murderer.", "English", 8.4, ["Mystery", "Thriller"], "https://image.tmdb.org/t/p/w500/yuNs09hvpHVU1cBTCA99x5w2Qyn.jpg"),
    ("Back to the Future", 1985, 116, "Marty McFly, a 17-year-old high school student, is accidentally sent thirty years into the past in a time-traveling DeLorean.", "English", 8.5, ["Adventure", "Comedy", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/7lyBcpYB0Qt8gYvXYaEZUNNsSOr.jpg"),
    ("The Truman Show", 1998, 103, "An insurance salesman discovers his whole life is actually a reality TV show.", "English", 8.2, ["Comedy", "Drama"], "https://image.tmdb.org/t/p/w500/vuza0WqY239gB21GwIo4vH5EBRo.jpg"),
    ("Eternal Sunshine of the Spotless Mind", 2004, 108, "When their relationship turns sour, a couple undergoes a medical procedure to have each other erased from their memories.", "English", 8.3, ["Drama", "Romance", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/5MwkWH9tYHv3mV9OdYTMR5q9IzL.jpg"),
    ("Gladiator II", 2024, 148, "Years after witnessing the death of Maximus at the hands of his uncle, Lucius must enter the Colosseum.", "English", 7.4, ["Action", "Adventure", "Drama"], "https://image.tmdb.org/t/p/w500/2cxhvwyEwRlysAmRH4iodkvo0z5.jpg"),
    ("Joker", 2019, 122, "During the 1980s, a failed stand-up comedian is driven insane and turns to a life of crime and chaos in Gotham City.", "English", 8.4, ["Crime", "Drama", "Thriller"], "https://image.tmdb.org/t/p/w500/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg"),
    ("No Country for Old Men", 2007, 122, "Violence and mayhem ensue after a hunter stumbles upon a drug deal gone wrong and more than two million dollars in cash.", "English", 8.2, ["Crime", "Drama", "Thriller"], "https://image.tmdb.org/t/p/w500/bj1v6YKF8MH1fP1jD3vE3C9c7vY.jpg"),
    ("There Will Be Blood", 2007, 158, "A story of family, religion, hatred, oil and madness, focusing on a turn-of-the-century prospector in the early days of the business.", "English", 8.2, ["Drama"], "https://image.tmdb.org/t/p/w500/fa0RDkAlCec0STnT78RiNyqhvdg.jpg"),
    ("1917", 2019, 119, "April 6th, 1917. As an infantry battalion assembles to wage war deep in enemy territory, two soldiers are assigned to race against time.", "English", 8.2, ["Action", "Drama", "War"], "https://image.tmdb.org/t/p/w500/iZf0KyrE25z1sage4SYFLCCrMi9.jpg"),
    ("Hacksaw Ridge", 2016, 139, "World War II American Army Medic Desmond T. Doss, who served during the Battle of Okinawa, refuses to bear arms.", "English", 8.1, ["Biography", "Drama", "History"], "https://image.tmdb.org/t/p/w500/jhWv186F00j19nNfl8q1eD5Pq2s.jpg"),
    ("Black Panther", 2018, 134, "T'Challa, heir to the hidden kingdom of Wakanda, must step forward to lead his people into a new future and must confront a challenger.", "English", 7.3, ["Action", "Adventure", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/uxzzxijgPIY7slzFvMotPv8vlum.jpg"),
    ("Doctor Strange", 2016, 115, "While on a journey of physical and spiritual healing, a brilliant neurosurgeon is drawn into the world of the mystic arts.", "English", 7.5, ["Action", "Adventure", "Fantasy"], "https://image.tmdb.org/t/p/w500/xf8PbyQcR5ucsqxuzA5qLwXi4v.jpg"),
    ("Guardians of the Galaxy", 2014, 121, "A group of intergalactic criminals must pull together to stop a fanatical warrior with plans to purge the universe.", "English", 8.0, ["Action", "Adventure", "Comedy"], "https://image.tmdb.org/t/p/w500/r2J02Z2OpNTctetGCGi57q9qJ3w.jpg"),
    ("Thor: Ragnarok", 2017, 130, "Imprisoned on the planet Sakaar, Thor must race against time to return to Asgard and stop Ragnarök.", "English", 7.9, ["Action", "Adventure", "Comedy"], "https://image.tmdb.org/t/p/w500/rzRwTcFvttcN1ZpX2xv4jvoY0KH.jpg"),
    ("Deadpool", 2016, 108, "A wisecracking mercenary gets experimented on and becomes immortal but ugly, and sets out to track down the man who ruined his looks.", "English", 8.0, ["Action", "Comedy"], "https://image.tmdb.org/t/p/w500/fSRb7vyIP8rQpL0I47P3q1u34xL.jpg"),
    ("Logan", 2017, 137, "In a future where mutants are nearly extinct, an elderly and weary Logan leads a quiet life until a mutant child arrives pursued by dark forces.", "English", 8.1, ["Action", "Drama", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/fnbjcRDYn6YviCcePDnGdyAkYsB.jpg"),
    ("Everything Everywhere All at Once", 2022, 139, "A middle-aged Chinese immigrant is swept up into an insane adventure in which she alone can save existence by exploring other universes.", "English", 7.8, ["Action", "Adventure", "Comedy", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/w3LxiVYPqrlexPbtBmhw8um9i0i.jpg"),
    ("Top Gun: Maverick", 2022, 130, "After thirty years, Maverick is still pushing the envelope as a top naval aviator, but must confront ghosts of his past.", "English", 8.2, ["Action", "Drama"], "https://image.tmdb.org/t/p/w500/62HCnUTziyWcpDaBO2i1DX17ljH.jpg"),
    ("Spider-Man 2", 2004, 127, "Peter Parker is beset with troubles in his failing personal life as he battles a brilliant scientist named Doctor Otto Octavius.", "English", 7.4, ["Action", "Sci-Fi"], "https://image.tmdb.org/t/p/w500/olxpyq94zk2HQnTe5c9AzV29hdL.jpg"),
    ("Casino Royale", 2006, 144, "After earning 00 status, secret agent James Bond embarks on his first mission to prevent a private banker from winning a high-stakes poker game.", "English", 8.0, ["Action", "Adventure", "Thriller"], "https://image.tmdb.org/t/p/w500/zlPuvt61m3J4sJ0bX3vM047jBsm.jpg"),
    ("Skyfall", 2012, 143, "James Bond's loyalty to M is tested when her past comes back to haunt her. When MI6 comes under attack, 007 must track down and destroy the threat.", "English", 7.8, ["Action", "Adventure", "Thriller"], "https://image.tmdb.org/t/p/w500/izr0b9Vw2k7K5A4yB1H6n362N.jpg")
]

FIRST_NAMES = [
    "Aarav", "Aditi", "Alexander", "Amara", "Arjun", "Chloe", "Daniel", "Diya",
    "Elena", "Ethan", "Fatima", "Gabriel", "Grace", "Hannah", "Ishaan", "Jack",
    "Jessica", "Kavya", "Leo", "Lucas", "Maya", "Meera", "Noah", "Olivia",
    "Priya", "Rahul", "Rohan", "Samantha", "Sophia", "Tara", "Vikram", "Zoe"
]

LAST_NAMES = [
    "Patel", "Shah", "Sharma", "Gohel", "Smith", "Johnson", "Williams", "Brown",
    "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez",
    "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson"
]

def generate_full_dataset(target_dir: Path):
    """
    Generates synthetic but statistically realistic Kaggle-aligned CSVs:
    1. movies.csv (220+ records)
    2. users.csv (120 records)
    3. ratings.csv (1800+ records with latent cluster taste distribution)
    4. watch_history.csv (700+ records)
    """
    random.seed(42)
    target_dir.mkdir(parents=True, exist_ok=True)

    # 1. Generate Movies
    movies_data = []
    all_raw_movies = CURATED_MOVIES + ADDITIONAL_TEMPLATES

    # Extend dataset to 220+ movies by synthesizing realistic titles in franchise / cinematic universes
    franchise_suffixes = ["Chapter 2", "Origins", "Legacy", "Resurrection", "Retribution", "Final Battle", "Reckoning"]
    genres_pool = ["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery", "Romance", "Sci-Fi", "Thriller", "War"]

    movie_id_counter = 1
    for title, yr, dur, desc, lang, imdb, g_list, poster in all_raw_movies:
        movies_data.append({
            "movie_id": movie_id_counter,
            "title": title,
            "release_year": yr,
            "duration": dur,
            "description": desc,
            "language": lang,
            "imdb_rating": imdb,
            "genres": "|".join(g_list),
            "poster_url": poster
        })
        movie_id_counter += 1

    # Add realistic variations until reaching 220 movies
    base_titles = [m[0] for m in all_raw_movies]
    for i in range(len(movies_data), 225):
        base_movie = all_raw_movies[i % len(all_raw_movies)]
        suffix = franchise_suffixes[i % len(franchise_suffixes)]
        new_title = f"{base_movie[0]}: {suffix}"
        new_year = min(2025, base_movie[1] + (i % 8) + 1)
        new_rating = round(max(5.5, min(9.1, base_movie[5] + random.uniform(-0.8, 0.4))), 1)
        movies_data.append({
            "movie_id": movie_id_counter,
            "title": new_title,
            "release_year": new_year,
            "duration": base_movie[2] + random.randint(-15, 20),
            "description": f"The continuing saga of {base_movie[0]}. " + base_movie[3][:120] + "...",
            "language": base_movie[4],
            "imdb_rating": new_rating,
            "genres": "|".join(base_movie[6]),
            "poster_url": base_movie[7]
        })
        movie_id_counter += 1

    df_movies = pd.DataFrame(movies_data)
    df_movies.to_csv(target_dir / "movies.csv", index=False)

    # 2. Generate 120 Users with latent personas (for natural K-Means clustering and Apriori rules)
    # Personas:
    # 0: Action & Sci-Fi lover
    # 1: Drama & Romance lover
    # 2: Animation & Comedy fan
    # 3: Thriller & Crime devotee
    users_data = []
    user_personas = {}

    for u_id in range(1, 121):
        f_name = random.choice(FIRST_NAMES)
        l_name = random.choice(LAST_NAMES)
        name = f"{f_name} {l_name}"
        email = f"{f_name.lower()}.{l_name.lower()}{u_id}@moviemine.edu"
        age = random.randint(18, 55)
        gender = random.choice(["Male", "Female", "Non-Binary"])
        
        persona = (u_id - 1) % 4
        user_personas[u_id] = persona

        created_days_ago = random.randint(10, 360)
        created_at = datetime.datetime.utcnow() - datetime.timedelta(days=created_days_ago)

        users_data.append({
            "user_id": u_id,
            "name": name,
            "email": email,
            "age": age,
            "gender": gender,
            "created_at": created_at.strftime("%Y-%m-%d %H:%M:%S")
        })

    df_users = pd.DataFrame(users_data)
    df_users.to_csv(target_dir / "users.csv", index=False)

    # 3. Generate Realistic Ratings & Watch History adhering to personas
    ratings_data = []
    watch_data = []
    history_id = 1
    rating_id = 1

    # Map movies by genre affinities
    persona_fav_genres = {
        0: ["Action", "Sci-Fi", "Adventure"],
        1: ["Drama", "Romance", "Biography"],
        2: ["Animation", "Comedy", "Family"],
        3: ["Crime", "Thriller", "Mystery", "Horror"]
    }

    for u_id in range(1, 121):
        persona = user_personas[u_id]
        fav_genres = persona_fav_genres[persona]

        # Each user rates 14 to 28 movies
        num_ratings = random.randint(14, 28)

        # 70% of ratings in favorite genres, 30% random
        fav_movie_pool = [
            m["movie_id"] for m in movies_data
            if any(g in m["genres"].split("|") for g in fav_genres)
        ]
        other_movie_pool = [
            m["movie_id"] for m in movies_data
            if m["movie_id"] not in fav_movie_pool
        ]

        fav_picks = random.sample(fav_movie_pool, min(len(fav_movie_pool), int(num_ratings * 0.75)))
        other_picks = random.sample(other_movie_pool, min(len(other_movie_pool), num_ratings - len(fav_picks)))
        chosen_movies = fav_picks + other_picks
        random.shuffle(chosen_movies)

        for m_id in chosen_movies:
            is_fav = m_id in fav_movie_pool
            if is_fav:
                # Highly positive rating for favorite genres (3.5 to 5.0)
                r_val = random.choice([3.5, 4.0, 4.5, 5.0, 5.0])
            else:
                # Moderate to mixed rating for other genres (1.5 to 3.5)
                r_val = random.choice([1.5, 2.0, 2.5, 3.0, 3.5])

            rating_date = datetime.datetime.utcnow() - datetime.timedelta(days=random.randint(1, 180))
            ratings_data.append({
                "rating_id": rating_id,
                "user_id": u_id,
                "movie_id": m_id,
                "rating": r_val,
                "rating_date": rating_date.strftime("%Y-%m-%d %H:%M:%S")
            })
            rating_id += 1

            # 70% of rated movies also appear in watch history
            if random.random() < 0.70:
                watch_data.append({
                    "history_id": history_id,
                    "user_id": u_id,
                    "movie_id": m_id,
                    "watched_at": rating_date.strftime("%Y-%m-%d %H:%M:%S")
                })
                history_id += 1

    df_ratings = pd.DataFrame(ratings_data)
    df_ratings.to_csv(target_dir / "ratings.csv", index=False)

    df_watch = pd.DataFrame(watch_data)
    df_watch.to_csv(target_dir / "watch_history.csv", index=False)

    return df_movies, df_users, df_ratings, df_watch
