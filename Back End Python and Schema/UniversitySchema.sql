# Dept Table -- Departments Table: Stores information about academic departments.
CREATE TABLE Departments (
	dept_code VARCHAR(2) PRIMARY KEY, -- Unique code for each department (e.g., 'CS', 'EE').
    dept_name VARCHAR(100) -- Full name of the department (e.g., 'Computer Science').
);


# Degrees Table -- Degrees Table: Stores details of academic degrees offered by departments.
CREATE TABLE Degrees (
    degree_id INT AUTO_INCREMENT PRIMARY KEY, -- Unique ID for each degree.
    level VARCHAR(50), -- Level of the degree (e.g., 'BS', 'MS').
    degree_name VARCHAR(100), -- Name of the degree (e.g., 'Computer Science').
    dept_code VARCHAR(2), -- Department offering the degree (foreign key).
    FOREIGN KEY (dept_code) REFERENCES Departments(dept_code),
    UNIQUE(degree_name, level) -- Ensures unique combinations of degree name and level.
);


# Courses Table -- Courses Table: Stores information about courses offered by departments.
CREATE TABLE Courses (
    course_id VARCHAR(8) PRIMARY KEY, -- Unique identifier for the course (e.g., 'CS1010'). 
    course_name VARCHAR(100) NOT NULL, -- Full name of the course.
    core_class BOOLEAN, -- Indicates if the course is a core class.
    CHECK (course_id REGEXP '^[A-Z]{2,4}[0-9]{4}$'), -- Ensures course ID follows this specific format.
    dept_code VARCHAR(2), -- Department offering the course (foreign key).
    FOREIGN KEY (dept_code) REFERENCES Departments(dept_code)
);

# Goals Table -- Goals Table: Stores information about learning or program goals.
CREATE TABLE Goals (
    goal_code VARCHAR(4) PRIMARY KEY, -- Unique code for each goal (e.g., 'G001').
    goal_desc VARCHAR(255) -- Description of the goal.
); 

#Goal_Courses -- Goal_Courses Table: Maps courses to specific goals they address.
CREATE TABLE Goal_Courses (
	goal_code VARCHAR(4), -- Goal being addressed (foreign key).
    course_id VARCHAR(8), -- Course addressing the goal (foreign key).
    FOREIGN KEY (course_id) REFERENCES Courses(course_id),
    FOREIGN KEY (goal_code) REFERENCES Goals(goal_code),
    PRIMARY KEY (goal_code, course_id) -- Ensures unique course-goal relationships.
);


# Degree_Goals Relationship -- Degree_Goals Table: Maps goals to degrees, representing program-level objectives.
CREATE TABLE Degree_Goals (
    degree_id INT, -- Degree associated with the goal (foreign key).
    goal_code VARCHAR(4), -- Goal being addressed (foreign key).
    FOREIGN KEY (degree_id) REFERENCES Degrees(degree_id),
    FOREIGN KEY (goal_code) REFERENCES Goals(goal_code),
    PRIMARY KEY (degree_id, goal_code), -- Ensures unique degree-goal relationships.
    CONSTRAINT unique_goal_per_degree UNIQUE (degree_id, goal_code)  -- Validates uniqueness.
);


# Instructor Table -- Instructors Table: Stores information about instructors.
CREATE TABLE Instructors (
	instructor_id CHAR(8) NOT NULL, -- Unique identifier for each instructor.
    instructors_name VARCHAR(100) NOT NULL, -- Full name of the instructor.
    PRIMARY KEY (instructor_id),
    dept_code VARCHAR(2), -- Department the instructor belongs to (foreign key).
    FOREIGN KEY (dept_code) REFERENCES Departments(dept_code)
);

# Sections Table -- Sections Table: Stores information about course sections offered in different semesters.
CREATE TABLE Sections (
    semester ENUM('Spring', 'Summer', 'Fall') NOT NULL, -- Semester of the section. 
    year YEAR NOT NULL, -- Year of the section.
    sec_id CHAR(3) NOT NULL, -- Section identifier.
    course_id VARCHAR(8) NOT NULL, -- Course being offered (foreign key).
    instructor_id CHAR(8) NOT NULL, -- Instructor teaching the section (foreign key)
    num_of_students INT CHECK (num_of_students >= 0), -- Number of students in the section.
    PRIMARY KEY (semester, year, sec_id, course_id),  -- added course_id as part of primary key due to validation issues
    FOREIGN KEY (course_id) REFERENCES Courses(course_id), -- Unique identifier for a section. 
    FOREIGN KEY (instructor_id) REFERENCES Instructors(instructor_id) 
);

# Evaluations Table -- Evaluations Table: Stores evaluation details for assignments mapped to goals.
CREATE TABLE Evaluations (
    assignment VARCHAR(100), -- Name of the assignment (e.g. 'Homework', 'Quiz', 'Final Exam', etc).   
    instructor_id CHAR(8), -- Instructor associated with the evaluation (foreign key).
    sec_id CHAR(3) NOT NULL, -- Section ID where the evaluation took place.
    semester ENUM('Spring', 'Summer', 'Fall') NOT NULL, -- Semester of the evaluation.
    year YEAR NOT NULL, -- Year of the evaluation.
    course_id VARCHAR(8) NOT NULL, -- Course being evaluated (foreign key).
    goal_code VARCHAR(4), -- Goal being evaluated (foreign key)       
    Eval_txt VARCHAR(255), -- Evaluation text/feedback.       
    grades_A INT DEFAULT 0, -- Count of A grades assigned.      
    grades_B INT DEFAULT 0, -- Count of B grades assigned.       
    grades_C INT DEFAULT 0, -- Count of C grades assigned.     
    grades_F INT DEFAULT 0, -- Count of F grades assigned.      
    PRIMARY KEY (assignment, sec_id, semester, year, course_id, goal_code), -- Unique evaluation entry.
    FOREIGN KEY (semester, year, sec_id, course_id) REFERENCES Sections(semester, year, sec_id, course_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id),
    FOREIGN KEY (instructor_id) REFERENCES Instructors(instructor_id),
    FOREIGN KEY (goal_code) REFERENCES Goals(goal_code)  
);