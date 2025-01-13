cat dependencies.txt | while read PACKAGE; do pip install "$PACKAGE"; done
pip install gunicorn
python -m scrape_and_process.scrapers
python -m scrape_and_process.price_predict
