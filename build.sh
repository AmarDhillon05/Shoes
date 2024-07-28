cat requirements.txt | while read PACKAGE; do pip install "$PACKAGE"; done
python -m scrape_and_process.scrapers
python -m scrape_and_process.price_predict