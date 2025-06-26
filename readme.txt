To run the api:
1. Install necessary library using cmd: pip install -r requirements2.txt

2. Once the dependencies get installed successfully :

python app.py : the api will run on local port by default and will give the url for localhost.

3. Use the url to test on Postman or other api testing platform


NOTE: The image data should be in base 64 from the requested end.
NOTE: The requirements2 file contains requirements more than the required dependencies because i've freeze the requirements from my environment that
ensures smooth run of projects related to image recognition.

-> To test, the payload should be in the format as:

Input: 

{
  "name": "PM",
  "gender": "Male",
  "age": 75,
  "image": "/9j/4AAQSkZJRgABAQEASABIAAD/2wCEAAYEBQYFBAYGBQYHBwYIChAKCgkJChQOD...(Here Give the base 64 encoding)"
}


Output:

1. If the image passed person data is new : New entry get stored in Entry Table of DB.
2. If the image passed person data is matched with the existing : Duplicate entry log get stored in log table of DB.



4. I've shared the following files:
1. Api code 
 - app.py
- db_config.py
2. DB dump file
3. Image on which i've tested and which the data get saved in the DB
4. Screenshot of the postman testing.


