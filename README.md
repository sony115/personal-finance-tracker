# Personal finance tracker

Financial tracker is an innovative web application that transforms personal financial management through a sophisticated technology ecosystem. By integrating Flask's backend capabilities, JavaScript's interactive features, HTML's structural design, and SQL's data management prowess, the platform offers users a comprehensive, user-friendly tool for tracking income, categorizing expenses, and visualizing financial trends with precision and clarity.
## Project OverView
The general objective of this project is to develop an advanced web application that will assist users in keeping track of their income and expenses in minute detail.In its core, such an application is intended for providing users with a simple, yet powerful tool for the management of personal finances. This shall be achieved by recording each and every transaction of the user in a structured form, categorizing them systematically, and also visually through information charts. In addition, this application will highlight trends within various periods and allow users to obtain useful information about their spending habits and growth of income over time. 

## Features

- **User Authentication**: Secure registration and login functionality.
- **Transaction Management**: Add, delete, and view expense and income transactions.
- **Data Visualization**: Represent financial data in graphical form, 
   including:1.A pie diagram showing the different types of expenditures. 
             2.A bar diagram showing the comparison between income and expenditure.
-**Filtering and Reporting**: This provides the ability for users to filter transactions by category and generates the csv files.
-**Custom Categories**:: The user can add different customized categories to organize the transactions in a better way.

## Problem Defination 

A large group of people find financial management an uphill task because they lack structured tracking facilities that would enable them to keep a proper record of all their income and expenses. This application addresses that need by availing the   user with an easy and hassle-free way to record, categorize,and monitor every bit of income and expenditure. This way,  users will manage their finances better an prepare well for a  financial future.


## Getting Started
To set up and run this project, follow these steps:
1. Clone this repository to your local machine.
2. Set up a SQL database system, such as MySQL, on your local environment.
3. Create the database tables according to the project requirements.

## Prerequisites
-**pip**
-**PyCharm or Visual Studio Code**
-**Flask**
-**SQL database**
-**Chart.js**



## Project Structure
The project structure is as follows:
- `finanacetracker_db.sql`: SQL script for database setup.
- `signup.html`:User registration page
- `login.html` : User Login Page
- `edit_transaction.html` : user can able to update their transactions
- `transaction.html` :User can able to enter their transactions and download the csv report file
- `stastics.html` : User can get the overview of  total income and expenditure on each category 
- `index.html` : Display the datavisulization graphs 
-`app.py` : It contains main method and sql related quires


## Dependencies
- **Flask**: The core web framework for building the backend of the application.
-**SQL**:To connect and interact with the MySQL database.
- **Chart.js**:  A JavaScript library for creating interactive and visually appealing charts and graphs.
- **Flask-Login** : To manage user sessions and authentication.


## Contributing
We welcome contributions to this project. If you have suggestions or improvements, feel free to submit a pull request. Please follow the project's coding standards and guidelines.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.