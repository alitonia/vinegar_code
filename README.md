# Vinegar decryption

Solving [Vigenère encryption](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher])

### How to use

* Install `python3`
* Install the following libraries: `re`, `colorama`, `collections`, `functools`
* Run `main.py`

### How it works

1. Suppose length of key is __k__. Calculate [Index-of-coincidence](https://en.wikipedia.org/wiki/Index_of_coincidence) (__IC__) for groups of interval k.

    ---> Key length.

2. With known key length __k__, we find character or group of characters that have the highest occurrence. One of them should be letter __e__.
    
3. From that groups of characters, we construct all possible keys.

4. Then apply some filter methods to get most likely key:

    * Calculate __IC__ in text decrypted by a key.
    * Detect sequence of English words in text decrypted by a key.
    * Vote for which character should be used based on majority vote.
    * Take a random one.

### How to improve

* Improve method to get key length
* Add words to wordlist
* Syntax analysis
* Optimize with less for-loops
* Implement algorithms in a faster language (ex: _Go_, _C_, _Java_)