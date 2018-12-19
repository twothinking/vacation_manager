# Simple Vacation Manager


## Installation and running:
1. sudo docker run --rm -p 4000:80 aeao93/vacation_manager
2. Browser: http://localhost:4000/

## Default Admin login:
  - Username: admin@admin.com
  - Password: admin

## Usage:
  - Admin:
    - Can define allowed vacation days with left-click
    - Can create leave request for himself/herself with right-click
  - Employee:
    - Can create leave request for himself/herself with right-click
  - View:
    - Can view allowed vacation days

![alt text](https://github.com/twothinking/vacation_manager/blob/master/Screenshot%20from%202018-12-19%2016-39-01.jpg)

- When admin creating a new allowed vacation day then the color of selected day will change to blue.
- When employees or admins creating a new vacation requests for himself/herself then the color of selected day will change to yellow.
- Employees or admins can delete the vacation request for himself/herself. The color of selected day will change to blue.
- Admin can accepted the 
