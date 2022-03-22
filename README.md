# My best 2 guess Wordle openers  

Find the best 2 opening guesses for Wordle using a few simple rules.


## Data preparation  

I'll be using the `Webster's Unabridged English Dictionary` as my source of five letter English words, helpfully curated [here](https://github.com/adambom/dictionary). These will be my `challenge words.`


### Packages  

Use the `environment.yml` file to create a fresh workspace for this project. 


## Rules  

- select words with the most common starting letters
- words should have no repeat letters
- create `guess words list` where all the low frequncy anagrams are removed
- sort and keep the top 100 words from the `guess words list` (we can resonably recall a few dozen 5 letter words)
- create a list of guess word pairs where each letter is represented `only once` across the words, these are our `guess pairs`  


## Score challenge word against guess word based on position  

scoring:  

- 0 if letter from guess word in challenge word but in wrong position
- 1 if letter from guess word in challenge word and in correct position
- -1 if letter from guess word not in challenge word
