# Old Money
## Project 0 - Da Art of Storytellin'
### Courtesy of Rubin Peci, Qian Zhou, and Maggie Zhao

# Necessary Python modules
 - sqlite3
 - flask
 - wheel
 - [passlib](https://passlib.readthedocs.io/en/stable/)
    
    The `passlib` library executes a hashing algorithm which allows us to store passwords with better safety.
    
 - [time](https://docs.python.org/3.7/library/time.html), [datetime](https://docs.python.org/3.7/library/datetime.html)
   
   The `time` and `datetime` modules provides various methods for the execution and manipulation of information related to time and date. 
   
   We use these modules to generate the Timestamp of user edits to a story.
   

### How to install aforementioned modules
Run the following command
<br>`pip install <submodule name>`

### How to run our site
1. Clone the repo 
<br>`git clone https://github.com/LargeLlama/old-money/tree/master`

2. Navigate to the folder it cloned it under (default will be old-money)
<br>`cd old-money` 

3. Run the app with flask
<br> `flask run` 

4. Go to the following URL on your favorite web browser
<br> localhost:5000/

5. Bask in our amazing work!
