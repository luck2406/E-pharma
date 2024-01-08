# Pharmacy management system
## Inspiration
Many a times, doctor prescribe such medicines that are not available in pharmacy but have the meds of same compositions, might also be cheeper then the that, this helps both customer and pharmacy owner.
Hence I've come up with an idea, where user can update inventory with some easy entries and make super quick and effectively and also get an get a keen eye about meds flow and revenue generation.

## Tools used
- Backend: Django
- Frontend: HTML5, CSS3, Javascript, Jquery, Bootstrap
- Dinamic Data Fetch: AJAX
- Web Scrapping: Beautiful Soup
- database: SQLite3
- Graphs: Graph jS


## Features
- New Inventory with automatic composition fetch
- Billing with alternative suggestion management
- Bill with dedicated UPI Qr code to pay the bill with Grand total embedded
- Retrival of old bills by bill number
- Admin Dashboard
- Sales Analytics with daily, monthly revenue measures and most demanded medicine with total revenue collected till date
- Admin can view Inventory.
- Can view old inventory
- Option to take database backup for future revert back point
- Pharmacy profile with ability to change and update.

## How to execute
```
git clone 
cd medical
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```