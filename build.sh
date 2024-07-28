FOR /F %k in (requirements.txt) DO ( if NOT # == %k ( pip install %k ) )
python -m scrape_and_process.scrapers
python -m scrape_and_process.price_predict