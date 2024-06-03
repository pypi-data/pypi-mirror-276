# price-of-gold-now
This package will get information about price of gold from https://www.livepriceofgold.com/usa-gold-price.html#google_vignette

## How It Works
This package will scrap data from [livepriceofgold](https://www.livepriceofgold.com/usa-gold-price.html) to get information about latest price of gold in USA

This package used BeautifulSoup4 and Requests to generate JSON output that'll be used for web or mobile apps

## How to Run
```
import priceofgold

if __name__ == '__main__':
    print('Aplikasi utama')
    result = priceofgold.data_extract()
    priceofgold.show_data(result)
```

# Author
Muhammad Dwi Reza