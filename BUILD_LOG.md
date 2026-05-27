## Task 1— Create Flask Project
- Brief: Make folders and files for the GPA tracking website.
- What Claude proposed: Created this file system: 
├── app/
│   ├── __init__.py        ← app factory + DB init
│   ├── models.py
│   ├── routes/            ← auth, students, grades, main
│   ├── templates/         ← login, dashboard, student pages, grade pages
│   └── static/css/
├── config.py
├── run.py
└── requirements.txt
- What I changed before approving: I approved the file structure including app, templates, static, and routes folders. 
- Verification: I ran python run app.py and it showed me to the login screen, but not the sign-up screen. 
- One thing I learned: I learned the Flask project structure of creating a website that utilizes flask and a database (SQL)

## Task 2 — Connect Database
- Brief: Set up SQL database connection inside the Flask app.
- What Claude proposed: Claude set up a database that tracks login, students, grades, and classes. 
- What I changed before approving: I added tracking semesters. 
- Verification: The program could recognize if a username was already taken, store students, grades, subjects.
- One thing I learned: I learned how models.py stores information from user input into database.

## Task 3 — Create Student Tables
- Brief: Make tables for student names, grades, and GPA information.
- What Claude proposed: Claude created a task bar on the top side of the webpage for users to click on, which showed a table of each category. 
- What I changed before approving:  N/A
- Verification: I check if the webpage displayed grades, names, and GPA info. 
- One thing I learned: I learned how to center words and buttons onto a webpage as well as how to create a table. 

## Task 4 — Build Login Page
- Brief: Create an HTML page for student login access.
- What Claude proposed: Claude built a student login page for username and password.
- What I changed before approving: I created a sign-up along with the login page. 
- Verification: I tried to login using the html page,however it didn't work because it didn't have a sign-up page. Once I implemented the sign-up page I was able to successfully login. 
- One thing I learned: I learned how to create a "create now" button for signing up. 

## Task 5 — Create Grade Form
- Brief: Make a form for entering student grades and subjects.
- What Claude proposed: Claude make a button that allows teachers to add students, grades, and subjects. 
- What I changed before approving: I allowed the program to add semesters in there as well. 
- Verification: I successfully was able to add students, grades, semesters, and classes. 
- One thing I learned: I learned how to create a form group in html and I also learned what a form group is. 

## Task 6 — Calculate GPA
- Brief: Create code that calculates GPA from student grades automatically.
- What Claude proposed: Gave options of A+, A, A-,.. and if teacher clicks a grade it automatically would change GPA.
- What I changed before approving: N/A
- Verification: When I insert grade does it change (lower grade lowers GPA, Higher grade, increases GPA)
- One thing I learned: I learned how to insert options for user to choose from. 

## AI Workflow
I used Claude for most of this project because Claude does a great job at following instructions and creating webpages based on my instructions. For planning, I decided to use ChatGPT to help me understand what tasks I should make and what steps I should take while creating a grading system. For executing the program and idea, I chose Claude because it is able to create lots of code that most of the time works. For reviewing the code, I used Copilot because Copilot is great at looking into snippets of code and finding out the bugs. Copilot is great at making snippets of code, but Claude is better at making big projects like these from scratch. Claude also tests the code for me, while Copilot asks whether or not to keep or undo code. For planning out the project I was about to use Claude, but then I used ChatGPT because I was able to understand the steps that ChatGPT gave me and allowed that to be the outline of my program. 