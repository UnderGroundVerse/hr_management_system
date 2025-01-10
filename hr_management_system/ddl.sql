CREATE TABLE hr_management_system.team (
  id BIGINT NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  description LONGTEXT,
  PRIMARY KEY (id),
  UNIQUE KEY name (name)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE hr_management_system.subteam (
  id BIGINT NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  team_id BIGINT NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY subteam_team_id_name_uniq (team_id, name),
  CONSTRAINT subteam_team_id_fk FOREIGN KEY (team_id) REFERENCES team (id)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


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
  KEY employee_sub_team_id_fk (sub_team_id),
  KEY employee_team_id_fk (team_id),
  CONSTRAINT employee_sub_team_id_fk FOREIGN KEY (sub_team_id) REFERENCES subteam (id),
  CONSTRAINT employee_team_id_fk FOREIGN KEY (team_id) REFERENCES team (id)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



CREATE TABLE hr_management_system.hrrole (
  id BIGINT NOT NULL AUTO_INCREMENT,
  created_at DATETIME(6) NOT NULL,
  updated_at DATETIME(6) NOT NULL,
  member_id BIGINT NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY member_id (member_id),
  CONSTRAINT rrole_member_id_fk FOREIGN KEY (member_id) REFERENCES employee (id)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE hr_management_system.hrrole_teams (
  hrrole_id BIGINT NOT NULL,
  team_id BIGINT NOT NULL,
  PRIMARY KEY (hrrole_id, team_id),
  KEY hrrole_teams_team_id_fk (team_id),
  CONSTRAINT hrrole_teams_hrrole_id_fk FOREIGN KEY (hrrole_id) REFERENCES hrrole (id),
  CONSTRAINT hrrole_teams_team_id_fk FOREIGN KEY (team_id) REFERENCES team (id)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
  KEY meeting_created_by_id_fk (created_by_id),
  CONSTRAINT meeting_created_by_id_fk FOREIGN KEY (created_by_id) REFERENCES employee (id)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE hr_management_system.meetingevaluation (
  id BIGINT NOT NULL AUTO_INCREMENT,
  created_at DATETIME(6) NOT NULL,
  updated_at DATETIME(6) NOT NULL,
  attendance VARCHAR(2) NOT NULL,
  task SMALLINT NOT NULL,
  performance SMALLINT NOT NULL,
  interaction SMALLINT NOT NULL,
  behavior SMALLINT NOT NULL,
  bonus TINYINT(1) NOT NULL,
  total SMALLINT NOT NULL,
  comment VARCHAR(500) NOT NULL,
  created_by_id BIGINT DEFAULT NULL,
  meeting_id BIGINT NOT NULL,
  member_id BIGINT NOT NULL,
  PRIMARY KEY (id),
  KEY meetingevaluation_created_by_id_fk (created_by_id),
  KEY meetingevaluation_meeting_id_fk (meeting_id),
  KEY meetingevaluation_member_id_fk (member_id),
  CONSTRAINT meetingevaluation_created_by_id_fk FOREIGN KEY (created_by_id) REFERENCES employee (id),
  CONSTRAINT meetingevaluation_meeting_id_fk FOREIGN KEY (meeting_id) REFERENCES meeting (id),
  CONSTRAINT meetingevaluation_member_id_fk FOREIGN KEY (member_id) REFERENCES employee (id)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;




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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
