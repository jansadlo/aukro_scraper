# Extract the values of class "buy-price" from the HTML
broad_prices = re.findall(r'class="buy-price">\s*([\d\s]+)\s*Kč\s*<', broad_html)


This code is looking for all the prices on the website. Here is an example piece of HTML that my code works with:
<span _ngcontent-sc399="" class="buyers-count hidden-min-tablet"> 1 přihazuje </span><!----></p><p _ngcontent-sc399="" class="buy-price"> 1 690 Kč <span _ngcontent-sc399="" class="time-to-end hidden-min-tablet"> 2 minuty </span></p>

The code works so far. It extracts all price values from the website as it should (in this case "1 690 Kč"). 
I want to apply some additional conditions, that has to be met, so that the price value could be scraped.

FIRST CONDITION: within 90 characters before the price value, there has to be partial word "přihazuj". 
If the first condition is met, there is a SECOND CONDITION: within 90 characters after the price value, there has to be partial word "min". 
If the second condition is met, there is a THIRD CONDITION: within 100 characters after the price value, there has to be partial word "min" AND the value of the "time-to-end hidden-min-tablet" has to by less than or equal to 20. 