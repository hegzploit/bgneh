# B-Gneh
A python script that finds the cheapest electronic component by searching in all the popular stores.

## Supported Stores
- [Future Electronics](https://store.fut-electronics.com/)
- [El-Gammal Electronics](http://elgammalelectronics.com/)
- [RAM Electronics](https://ram-e-shop.com/)
- [Free Electronics](https://free-electronic.com/)
Note: This is still a work in progress, my api wrappers are very basic and still need more polishing.

## TODO:
- [ ] Support all the popular stores in bab-el-louq
    - [x] Future
    - [x] El-Gammal
        - [x] Parse: Item, Price and Link
    - [x] RAM
    - [x] Free
    - [ ] El-Nekhely

        this will be a pain to scrape since the website uses ancient tech. and also a csrf token is present, will work on it later when I have more time on my hands.
- [ ] Concurrency
- [ ] Export Results
- [ ] Web-Interface (might never happen tbh)
