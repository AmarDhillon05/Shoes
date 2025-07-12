

This is a website that scrapes the websites of popular sneaker brands for upcoming drops, and uses a model fitted to past resell data to predict what the shoe will resell for after being sold out.

It was made with the intent of finding trends in shoe data and educating beginner resellers to make their first profitable decisions

Model was built with a group of cross-validated sklearn regressors on official StockX data (though I plan to look for/make better sources of data), and hosted on a flask API. Application was made with React.

Future imporvements will include:

  1). Take into account the change in hype of shoe reselling, 
  
  2). Aim to use more powerful models and provide more useful information, and 
  
  3). Be an all-in-one utility or proof of concept in if using models for this task is still relevant
