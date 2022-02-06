# Benchmark of the different languages over time
The benchmark is ran against 3 languages: english, french and spanish  
We run the algorithm on every word in the dictionary and report the average, median and max number of guesses.  
The minimum number of guesses is always 1, since the first guess is always the same.

# Dictionaries
The dictionaries were taken from the source code of popular wordle sites  
- English: https://www.powerlanguage.co.uk/wordle/  
- French: https://wordle.louan.me/  
- Spanish: https://wordle.danielfrg.com/  

# English (12972 words)
| Commit | Success rate | Average | Median | Max | First guess |
|--------|--------------|---------|--------|-----|-------------|
|[8487a94](https://github.com/Guillaume-Docquier/wordle-solver/commit/8487a94849ceee206ca339ea8f86aababde572b6)|87.30%|4.84|4|16|aeros|

# French (6025 words)
| Commit | Success rate | Average | Median | Max | First guess |
|--------|--------------|---------|--------|-----|-------------|
|[8487a94](https://github.com/Guillaume-Docquier/wordle-solver/commit/8487a94849ceee206ca339ea8f86aababde572b6)|93.68%|4.28|4|13|raies|

# Spanish (11094 words)
| Commit | Success rate | Average | Median | Max | First guess |
|--------|--------------|---------|--------|-----|-------------|
|[8487a94](https://github.com/Guillaume-Docquier/wordle-solver/commit/8487a94849ceee206ca339ea8f86aababde572b6)|85.12%|4.88|5|14|orase|