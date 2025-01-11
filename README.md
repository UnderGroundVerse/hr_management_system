# HR Management System

## Overview
The **HR Management System** is a comprehensive web-based application developed using the Django framework. It is designed to streamline HR operations, including team and subteam management, employee records, performance evaluations, meeting scheduling, and warnings management. The project uses a database-first approach to maintain a robust and scalable architecture.

## Features
- **Team Management:** Create and manage teams and subteams.
- **Employee Management:** Handle employee details, including contact information, profile pictures, and team assignments.
- **Performance Ratings:** Evaluate employee performance through multiple metrics like tasks, behavior, and interaction.
- **Roles Management:** Assign specific HR roles with control over teams.
- **Meeting Scheduling:** Schedule and evaluate meetings with detailed attendance and performance tracking.
- **Warnings System:** Issue and manage official and unofficial warnings with detailed notes.

## Technologies Used
- **Framework:** Django
- **Database:** MySQL (InnoDB engine with UTF-8MB4 encoding)
- **Languages:** Python, SQL

## Database Schema
The application follows a normalized database schema with the following key tables:

### 1. `team`
Manages team information.
```sql
CREATE TABLE hr_management_system.team (
  id BIGINT NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  description LONGTEXT,
  PRIMARY KEY (id),
  UNIQUE KEY name (name)
);
```

### 2. `subteam`
Handles subteam details linked to teams.
```sql
CREATE TABLE hr_management_system.subteam (
  id BIGINT NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  team_id BIGINT NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY subteam_team_id_name_uniq (team_id, name),
  CONSTRAINT subteam_team_id_fk FOREIGN KEY (team_id) REFERENCES team (id)
);
```

### 3. `employee`
Stores employee records and related data.
```sql
CREATE TABLE hr_management_system.employee (
  id BIGINT NOT NULL AUTO_INCREMENT,
  password VARCHAR(128) NOT NULL,
  last_login DATETIME(6) DEFAULT NULL,
  is_superuser TINYINT(1) NULL,
  is_staff TINYINT(1) NULL,
  is_active TINYINT(1) NULL,
  date_joined DATETIME(6) NULL,
  first_name VARCHAR(25) NULL,
  last_name VARCHAR(25) NULL,
  full_name VARCHAR(50) NULL,
  email VARCHAR(254) NOT NULL,
  profile_picture VARCHAR(100) DEFAULT NULL,
  phone_number VARCHAR(11) NULL,
  sub_team_id BIGINT DEFAULT NULL,
  team_id BIGINT DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY email (email),
  UNIQUE KEY phone_number (phone_number),
  CONSTRAINT employee_sub_team_id_fk FOREIGN KEY (sub_team_id) REFERENCES subteam (id),
  CONSTRAINT employee_team_id_fk FOREIGN KEY (team_id) REFERENCES team (id)
);
```

### 4. `rating`
Tracks employee performance metrics.
```sql
CREATE TABLE hr_management_system.rating (
  id BIGINT NOT NULL AUTO_INCREMENT,
  task SMALLINT NOT NULL,
  performance SMALLINT NOT NULL,
  interaction SMALLINT NOT NULL,
  behavior SMALLINT NOT NULL,
  bonus SMALLINT NOT NULL,
  total SMALLINT NOT NULL,
  attended_meetings SMALLINT NOT NULL,
  unattended_meetings SMALLINT NOT NULL,
  employee_id BIGINT NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY employee_id (employee_id),
  CONSTRAINT rating_employee_id_fk FOREIGN KEY (employee_id) REFERENCES employee (id)
);
```

### 5. `hrrole`
Manages HR roles assigned to employees.
```sql
CREATE TABLE hr_management_system.hrrole (
  id BIGINT NOT NULL AUTO_INCREMENT,
  created_at DATETIME(6) NOT NULL,
  updated_at DATETIME(6) NOT NULL,
  member_id BIGINT NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY member_id (member_id),
  CONSTRAINT rrole_member_id_fk FOREIGN KEY (member_id) REFERENCES employee (id)
);
```

### 6. `meeting`
Handles meeting scheduling and attendance.
```sql
CREATE TABLE hr_management_system.meeting (
  id BIGINT NOT NULL AUTO_INCREMENT,
  created_at DATETIME(6) NOT NULL,
  updated_at DATETIME(6) NOT NULL,
  title VARCHAR(50) DEFAULT NULL,
  location VARCHAR(250) DEFAULT NULL,
  description LONGTEXT,
  scheduled_at DATETIME(6) NOT NULL,
  required_to_attend TINYINT(1) NOT NULL,
  evaluated TINYINT(1) NOT NULL,
  created_by_id BIGINT DEFAULT NULL,
  PRIMARY KEY (id),
  CONSTRAINT meeting_created_by_id_fk FOREIGN KEY (created_by_id) REFERENCES employee (id)
);
```

### 7. `warnings`
Manages warnings issued to employees.
```sql
CREATE TABLE hr_management_system.warnings (
  id BIGINT NOT NULL AUTO_INCREMENT,
  created_at DATETIME(6) NOT NULL,
  updated_at DATETIME(6) NOT NULL,
  is_official BOOLEAN NOT NULL,
  warning_type VARCHAR(20) NOT NULL,
  notes TEXT,
  employee_id BIGINT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (employee_id) REFERENCES employee (id)
);
```


## Query Examples
Here are some SQL query examples used in the HR Management System:

### Query 1: Retrieve Upcoming Meetings for Teams
```sql
SELECT *
FROM meeting hm
INNER JOIN meeting_teams hmt ON hm.id = hmt.meeting_id
WHERE hm.evaluated = FALSE
  AND hmt.team_id IN (
      SELECT et.id
      FROM team et
      INNER JOIN hrrole_teams hrt ON et.id = hrt.team_id
  )
ORDER BY hm.created_at DESC, hm.updated_at DESC
LIMIT 3;
```

### Query 2: Retrieve All Meetings for Specific Teams
```sql
SELECT *
FROM meeting hm
INNER JOIN meeting_teams hmt ON hm.id = hmt.meeting_id
WHERE hmt.team_id IN (
    SELECT et.id
    FROM team et
    INNER JOIN hrrole_teams hrt ON et.id = hrt.team_id
)
ORDER BY hm.created_at DESC, hm.updated_at DESC
LIMIT 3;
```

### Query 3: Retrieve Meeting Evaluations for a Specific Member
```sql
SELECT *
FROM meetingevaluation 
WHERE (meetingevaluation.meeting_id IN (5) AND meetingevaluation.member_id = {member.id});
```


## Normalization Done in the Project
Normalization is applied to reduce data redundancy and improve database design. Here's an example of normalizing the `employee` table:

### Unnormalized Table
| ID  | Name       | Email             | Phone Number | Team Name  | Subteam Name |
|-----|------------|-------------------|--------------|------------|--------------|
| 1   | John Smith | john@example.com  | 1234567890   | HR         | Recruitment  |
| 2   | Jane Doe   | jane@example.com  | 9876543210   | IT         | Development  |

### First Normal Form (1NF)
Separate repeating groups into distinct rows:

| ID  | Name       | Email             | Phone Number | Team ID | Subteam ID |
|-----|------------|-------------------|--------------|---------|------------|
| 1   | John Smith | john@example.com  | 1234567890   | 1       | 1          |
| 2   | Jane Doe   | jane@example.com  | 9876543210   | 2       | 2          |

### Second Normal Form (2NF)
Eliminate partial dependencies by splitting data into related tables:

**Employee Table:**
| ID  | Name       | Email             | Phone Number |
|-----|------------|-------------------|--------------|
| 1   | John Smith | john@example.com  | 1234567890   |
| 2   | Jane Doe   | jane@example.com  | 9876543210   |

**Team Table:**
| ID  | Team Name  |
|-----|------------|
| 1   | HR         |
| 2   | IT         |

**Subteam Table:**
| ID  | Subteam Name | Team ID |
|-----|--------------|---------|
| 1   | Recruitment  | 1       |
| 2   | Development  | 2       |

### Third Normal Form (3NF)
Remove transitive dependencies:

**Team Table (Updated):**
| ID  | Team Name  |
|-----|------------|
| 1   | HR         |
| 2   | IT         |

**Subteam Table (Updated):**
| ID  | Subteam Name | Team ID |
|-----|--------------|---------|
| 1   | Recruitment  | 1       |
| 2   | Development  | 2       |


## ERD Diagram
For a visual representation of the database schema, refer to the ERD diagram:
![ERD Diagram](/images/erd.png)

## Relational Mapping Diagram
![Relational Mapping Diagram](/images/rmd.png)

## MySql Auto Generated Diagram
![MySql Auto Generated Diagram](/images/msql.png)

## Contributors
- **Mario Morcos Wassily**
- **Mohamed Mahmoud Hesham Selim**


## License
This project is licensed under the MIT License.
