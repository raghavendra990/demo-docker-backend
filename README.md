Backend Hosted: Aws Ec2 

URL: 3.6.86.118

Fronend Hosted: Using AWS s3 static hosting

	URL: http://demo-backend-123.s3-website.ap-south-1.amazonaws.com

Python 3.10
Django 4.2.9
MySQL 8
React 18.2
Project Structure:

Backend: 

Backend is built using django rest framework and MySQl as backend. It is hosted on Ec2 container using Gunicorn and Nginx.

It majorly contain two apps details below:
	
userauth: It is used for authentication for the user with apis like Login, Register, Logout. I have used JWT custom authentication, code present at demo-backend/userauth/authentication.py .

For Logout, the frontend application will just delete the jwt token from storage, but there is still a chance that token remains valid and the fraudster can miss use it. That is Why we have created a Table BlackListedToken where we will store the blacklisted tokens and we have created Custom Permission Class IsTokenValid present in authentication.py file in userauth app.

	userItem: it contains all the logic related to Items Add, Edit, remove, Get Items for the User and Summary API.

Frontend: Frontend is built using React, bootstrap and hosted on AWS s3.

Postman collection for the APIs: https://api.postman.com/collections/655988-66fc581b-64e4-4c8e-a2a3-4240702ca1a2?access_key=PMAT-01HNCPCJ5Y84FV86H9NJA8X7RX
