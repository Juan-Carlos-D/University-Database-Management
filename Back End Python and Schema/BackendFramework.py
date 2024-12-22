import re
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config.from_pyfile('config.py')
mysql = MySQL(app)

# GET Degrees
@app.route('/degrees', methods=['GET'])
def get_degrees():
    cursor = mysql.connection.cursor()
    query =  """
        SELECT *
        FROM degrees
    """
    cursor.execute(query)
    degrees = cursor.fetchall()

    degrees_list = []
    for degree in degrees:
        degrees_dict = {
            'degree_id': degree[0],
            'level': degree[1],
            'degree_Name': degree[2],
            'dept_code': degree[3]
        }
        degrees_list.append(degrees_dict)

    cursor.close()
    return jsonify(degrees_list)

# GET Goals
@app.route('/goals', methods=['GET'])
def get_goals():
    cursor = mysql.connection.cursor()
    query =  """
        SELECT *
        FROM goals
    """
    cursor.execute(query)
    goals = cursor.fetchall()

    goals_list = []
    for goal in goals:
        goals_dict = {
            'goal_code': goal[0],
            'goal_desc': goal[1]
        }
        goals_list.append(goals_dict)

    cursor.close()
    return jsonify(goals_list)

# GET departments
@app.route('/departments', methods=['GET'])
def get_departments():
    cursor = mysql.connection.cursor()
    query =  """
        SELECT *
        FROM departments
    """
    cursor.execute(query)
    departments = cursor.fetchall()

    departments_list = []
    for department in departments:
        dept_dict = {
            'dept_code': department[0],
            'dept_name': department[1]
        }
        departments_list.append(dept_dict)

    cursor.close()
    return jsonify(departments_list)

# GET courses
@app.route('/courses', methods=['GET'])
def get_courses():
    cursor = mysql.connection.cursor()
    query =  """
        SELECT *
        FROM courses
    """
    cursor.execute(query)
    courses = cursor.fetchall()

    courses_list = []
    for course in courses:
        courses_dict = {
            'course_id': course[0],
            'course_name': course[1],
            'core_class': course[2],
            'dept_code': course[3]
        }
        courses_list.append(courses_dict)

    cursor.close()
    return jsonify(courses_list)

# GET instructors
@app.route('/instructors', methods=['GET'])
def get_instructors():
    cursor = mysql.connection.cursor()
    query =  """
        SELECT *
        FROM instructors
    """
    cursor.execute(query)
    instructors = cursor.fetchall()

    instructors_list = []
    for instructor in instructors:
        instructors_dict = {
            'instructor_id': instructor[0],
            'instructors_name': instructor[1]
        }
        instructors_list.append(instructors_dict)

    cursor.close()
    return jsonify(instructors_list)

# GET sections
@app.route('/sections', methods=['GET'])
def get_sections():
    cursor = mysql.connection.cursor()
    query =  """
        SELECT *
        FROM sections
    """
    cursor.execute(query)
    sections = cursor.fetchall()

    sections_list = []
    for section in sections:
        sections_dict = {
            'semester': section[0],
            'year': section[1],
            'sec_id': section[2],
            'course_id': section[3],
            'instructor_id': section[4],
            'num_of_students': section[5]
        }
        sections_list.append(sections_dict)

    cursor.close()
    return jsonify(sections_list)

@app.route('/goalcourses', methods=['GET'])
def get_goalCourses():
    cursor = mysql.connection.cursor()
    query =  """
        SELECT *
        FROM goal_courses
    """
    cursor.execute(query)
    goal_courses = cursor.fetchall()

    goal_courses_list = []
    for goal_course in goal_courses:
        goal_course_dict = {
            'goal_code': goal_course[0],
            'course_id': goal_course[1]
        }
        goal_courses_list.append(goal_course_dict)

    cursor.close()
    return jsonify(goal_courses_list)


# GET Evaluations for loading previous evaluations if necessary
@app.route('/evaluations', methods=['POST'])
def get_evaluations():
    cursor = mysql.connection.cursor()
    assignment = request.json['assignment']
    sec_id = request.json['sec_id']
    semester = request.json['semester']
    year = request.json['year']
    course_id = request.json['course_id']
    goal_code = request.json['goal_code']

    query =  """
        SELECT Eval_txt, grades_A, grades_B, grades_C, grades_F
        FROM evaluations
        WHERE assignment = %s
            AND sec_id = %s
            AND semester = %s
            AND year = %s
            AND course_id = %s
            AND goal_code = %s
    """
    cursor.execute(query, (assignment, sec_id, semester, year, course_id, goal_code))
    evaluations = cursor.fetchall()

    evaluations_list = []
    for evaluation in evaluations:
        evaluations_dict = {
            'Eval_txt': evaluation[0],
            'grades_A': evaluation[1],
            'grades_B': evaluation[2],
            'grades_C': evaluation[3],
            'grades_F': evaluation[4]
        }
        evaluations_list.append(evaluations_dict)

    cursor.close()
    return jsonify(evaluations_list)


########## Queries from Juan ###########
# GET courses from degree_id
@app.route('/degreeCourses', methods=['POST'])
def get_degree_courses():
    degree_id = request.json.get('degree_id')
    cursor = mysql.connection.cursor()
    query =  """
    SELECT c.course_id, c.course_name, c.core_class
    FROM Courses c
    JOIN Goal_Courses gc ON gc.course_id = c.course_id
    JOIN Goals g ON g.goal_code = gc.goal_code
    JOIN Degree_Goals dg ON dg.goal_code = g.goal_code
    WHERE dg.degree_id = %s;
    """
    cursor.execute(query, (degree_id,))
    courses = cursor.fetchall()

    courses_list = []
    for course in courses:
        courses_dict = {
            'course_id': course[0],
            'course_name': course[1],
            'core_class': course[2]
        }
        courses_list.append(courses_dict)

    cursor.close()
    return jsonify(courses_list)

# GET sections from degree_id and year
@app.route('/degreeSectionsRange', methods=['POST'])
def get_degree_sections_range():
    degree_id = request.json.get('degree_id')
    start_year = request.json.get('start_year')
    end_year = request.json.get('end_year')
    cursor = mysql.connection.cursor()
    query = """
    SELECT s.semester, s.year, s.sec_id, c.course_id, c.course_name
    FROM Sections s 
    JOIN Courses c ON s.course_id = c.course_id 
    JOIN Goal_Courses gc ON gc.course_id = c.course_id
    JOIN Degree_Goals dg ON gc.goal_code = dg.goal_code
    WHERE dg.Degree_id = %s
        AND (s.year BETWEEN %s AND %s)
    ORDER BY s.year, FIELD(s.semester, 'Spring', 'Summer', 'Fall');
    """
    cursor.execute(query, (degree_id, start_year, end_year))
    sections = cursor.fetchall()

    sections_list = []
    for section in sections:
        sections_dict = {
            'semester': section[0],
            'year': section[1],
            'sec_id': section[2],
            'course_id': section[3],
            'course_name': section[4]
        }
        sections_list.append(sections_dict)

    cursor.close()
    return jsonify(sections_list)

# GET goals from degree_id
@app.route('/degreeGoals', methods=['POST'])
def get_degree_goals():
    degree_id = request.json.get('degree_id')
    cursor = mysql.connection.cursor()
    query = """
    SELECT g.goal_code, g.goal_desc
    FROM Goals g 
    JOIN Degree_goals dg ON g.goal_code = dg.goal_code
    WHERE dg.Degree_id = %s;
    """

    cursor.execute(query, (degree_id,))
    goals = cursor.fetchall()

    goals_list = []
    for goal in goals:
        goals_dict = {
            'goal_code': goal[0],
            'goal_desc': goal[1]
        }
        goals_list.append(goals_dict)

    cursor.close()
    return jsonify(goals_list)

# GET courses for a goal
@app.route('/goalCourses', methods=['POST'])
def get_goal_courses():
    degree_id = request.json.get('degree_id')
    goal_code = request.json.get('goal_code')
    cursor = mysql.connection.cursor()
    query = """
    SELECT c.course_id, c.course_name
    FROM Courses c 
    JOIN Goal_Courses gc ON c.course_id = gc.course_id 
    JOIN Degree_Goals dg ON dg.goal_code = gc.goal_code
    WHERE dg.degree_id = %s
        AND gc.goal_code = %s;
    """
    cursor.execute(query, (degree_id, goal_code))
    goalCourses = cursor.fetchall()

    goalCourses_list = []
    for goalCourse in goalCourses:
        goalCourses_dict = {
            'course_id': goalCourse[0],
            'course_name': goalCourse[1]
        }
        goalCourses_list.append(goalCourses_dict)

    cursor.close()
    return jsonify(goalCourses_list)

# GET sections for a course (specified range of semesters)
@app.route('/courseSections', methods=['POST'])
def get_course_sections():
    course_id = request.json.get('course_id')
    start_year = request.json.get('start_year')
    end_year = request.json.get('end_year')
    cursor = mysql.connection.cursor()
    query = """
    SELECT s.semester, s.year, s.sec_id, i.instructors_name AS instructor_name 
    FROM Sections s 
    JOIN Instructors i ON s.instructor_id = i.instructor_id 
    WHERE s.course_id = %s
        AND (s.year BETWEEN %s AND %s)
    ORDER BY s.year, FIELD(s.semester, 'Spring', 'Summer', 'Fall');
    """
    cursor.execute(query, (course_id, start_year, end_year))
    courseSections = cursor.fetchall()

    courseSections_list = []
    for courseSection in courseSections:
        courseSections_dict = {
            'semester': courseSection[0],
            'year': courseSection[1],
            'sec_id': courseSection[2],
            'instructor_name': courseSection[3]
        }
        courseSections_list.append(courseSections_dict)

    cursor.close()
    return jsonify(courseSections_list)

# GET Sections for an Instructor
@app.route('/instSections', methods=['POST'])
def get_inst_sections():
    instructor_id = request.json.get('instructor_id')
    start_year = request.json.get('start_year')
    end_year = request.json.get('end_year')
    cursor = mysql.connection.cursor()
    query = """
    SELECT s.semester, s.year, s.sec_id, c.course_id, c.course_name
    FROM Sections s 
    JOIN Courses c ON s.course_id = c.course_id
    WHERE s.instructor_id = %s
        AND (s.year BETWEEN %s AND %s)
    ORDER BY s.year, FIELD(s.semester, 'Spring', 'Summer', 'Fall');
    """
    cursor.execute(query, (instructor_id, start_year, end_year))
    instSections = cursor.fetchall()

    instSections_list = []
    for instSection in instSections:
        instSections_dict = {
            'semester': instSection[0],
            'year': instSection[1],
            'sec_id': instSection[2],
            'course_id': instSection[3],
            'course_name': instSection[4]
        }
        instSections_list.append(instSections_dict)

    cursor.close()
    return jsonify(instSections_list)

# GET section evaluations
@app.route('/sectionEval', methods=['POST'])
def get_section_eval():
    semester = request.json.get('semester')
    year = request.json.get('year')
    cursor = mysql.connection.cursor()
    query = """
    SELECT e.semester, e.year, e.sec_id, e.course_id, 
	(SELECT i.instructors_name FROM instructors i WHERE i.instructor_id = e.instructor_id) AS instructor_name, 
	e.assignment,
        CASE 
            WHEN COUNT(e.assignment) = 0 THEN 'Not Entered'  -- No evaluation data at all
            WHEN SUM(e.grades_A + e.grades_B + e.grades_C + e.grades_F) = 0 AND (MAX(e.Eval_txt) IS NULL OR e.Eval_txt = '') THEN 'Not Entered'  -- No grades and no feedback (NULL values in all fields)
            WHEN SUM(e.grades_A + e.grades_B + e.grades_C + e.grades_F) = 0 AND (e.Eval_txt != '') THEN 'Feedback Entered (No Grades)'
            WHEN SUM(e.grades_A + e.grades_B + e.grades_C + e.grades_F) < 
						(SELECT s.num_of_students FROM sections s WHERE s.year = e.year AND s.semester = e.semester AND s.sec_id = e.sec_id AND s.course_id = e.course_id)
                AND (MAX(e.Eval_txt) IS NULL OR e.Eval_txt = '') THEN 'Partially Entered (No Feedback)'  -- Some grades entered, but no feedback
			WHEN SUM(e.grades_A + e.grades_B + e.grades_C + e.grades_F) < 
            			(SELECT s.num_of_students FROM sections s WHERE s.year = e.year AND s.semester = e.semester AND s.sec_id = e.sec_id AND s.course_id = e.course_id)
                AND  e.Eval_txt != '' THEN 'Partially Entered (Feedback Provided)'  -- Some grades entered, and feedback provided
            WHEN SUM(e.grades_A + e.grades_B + e.grades_C + e.grades_F) = 
            			(SELECT s.num_of_students FROM sections s WHERE s.year = e.year AND s.semester = e.semester AND s.sec_id = e.sec_id AND s.course_id = e.course_id)
                AND (MAX(e.Eval_txt) IS NULL OR e.Eval_txt = '') THEN 'Fully Entered (No Feedback Provided)'  -- Some grades entered, and feedback provided
            ELSE 'Fully Entered'  -- All grades entered and feedback provided
        END AS evaluation_status
    FROM Evaluations e
    WHERE e.semester = %s
        AND e.year = %s
    GROUP BY e.semester, e.year, e.sec_id, e.course_id, instructor_name, e.Eval_txt, e.assignment;
    """ 
    cursor.execute(query, (semester, year))
    sectionEvals = cursor.fetchall()

    sectionEvals_list = []
    for sectionEval in sectionEvals:
        instSections_dict = {
            'semester': sectionEval[0],
            'year': sectionEval[1],
            'sec_id': sectionEval[2],
            'course_id': sectionEval[3],
            'instructors_name': sectionEval[4],
            'assignment': sectionEval[5],
            'evaluation_status': sectionEval[6]
        }
        sectionEvals_list.append(instSections_dict)

    cursor.close()
    return jsonify(sectionEvals_list)

# GET percentage of students in a section for a grade
@app.route('/percentSection', methods=['POST'])
def get_percent_section():
    semester = request.json.get('semester')
    year = request.json.get('year')
    user_percentage = request.json.get('user_percentage')
    cursor = mysql.connection.cursor()
    query = """
    SELECT e.semester, e.year, e.sec_id, e.course_id, 
	(SELECT i.instructors_name FROM instructors i WHERE i.instructor_id = e.instructor_id) AS instructor_name, 
	e.assignment,
        CASE 
            WHEN COUNT(e.assignment) = 0 THEN 'Not Entered'  -- No evaluation data at all
            WHEN SUM(e.grades_A + e.grades_B + e.grades_C + e.grades_F) = 0 AND (MAX(e.Eval_txt) IS NULL OR e.Eval_txt = '') THEN 'Not Entered'  -- No grades and no feedback (NULL values in all fields)
            WHEN SUM(e.grades_A + e.grades_B + e.grades_C + e.grades_F) = 0 AND (e.Eval_txt != '') THEN 'Feedback Entered (No Grades)'
            WHEN SUM(e.grades_A + e.grades_B + e.grades_C + e.grades_F) < 
						(SELECT s.num_of_students FROM sections s WHERE s.year = e.year AND s.semester = e.semester AND s.sec_id = e.sec_id AND s.course_id = e.course_id)
                AND (MAX(e.Eval_txt) IS NULL OR e.Eval_txt = '') THEN 'Partially Entered (No Feedback)'  -- Some grades entered, but no feedback
			WHEN SUM(e.grades_A + e.grades_B + e.grades_C + e.grades_F) < 
            			(SELECT s.num_of_students FROM sections s WHERE s.year = e.year AND s.semester = e.semester AND s.sec_id = e.sec_id AND s.course_id = e.course_id)
                AND  e.Eval_txt != '' THEN 'Partially Entered (Feedback Provided)'  -- Some grades entered, and feedback provided
            WHEN SUM(e.grades_A + e.grades_B + e.grades_C + e.grades_F) = 
            			(SELECT s.num_of_students FROM sections s WHERE s.year = e.year AND s.semester = e.semester AND s.sec_id = e.sec_id AND s.course_id = e.course_id)
                AND (MAX(e.Eval_txt) IS NULL OR e.Eval_txt = '') THEN 'Fully Entered (No Feedback Provided)'  -- Some grades entered, and feedback provided
            ELSE 'Fully Entered'  -- All grades entered and feedback provided
        END AS evaluation_status,
        -- Calculate total and non-F percentages
        (SELECT s.num_of_students FROM sections s WHERE s.year = e.year AND s.semester = e.semester AND s.sec_id = e.sec_id AND s.course_id = e.course_id) AS total_students,
        SUM(COALESCE(e.grades_A, 0) + COALESCE(e.grades_B, 0) + COALESCE(e.grades_C, 0)) AS non_F_students,
        ROUND(100 * SUM(COALESCE(e.grades_A, 0) + COALESCE(e.grades_B, 0) + COALESCE(e.grades_C, 0)) / NULLIF(SUM(COALESCE(e.grades_A, 0) + COALESCE(e.grades_B, 0) + COALESCE(e.grades_C, 0) + COALESCE(e.grades_F, 0)), 0), 2) AS non_F_percentage
    FROM Evaluations e
    WHERE e.semester = %s
        AND e.year = %s
    GROUP BY e.semester, e.year, e.sec_id, e.course_id, instructor_name, e.Eval_txt, e.assignment, total_students
    HAVING 
        non_F_percentage >= %s;
    """
    cursor.execute(query, (semester, year, user_percentage))
    percentSections = cursor.fetchall()

    percentSections_list = []
    for percentSection in percentSections:
        instSections_dict = {
            'semester': percentSection[0],
            'year': percentSection[1],
            'sec_id': percentSection[2],
            'course_id': percentSection[3],
            'instructors_name': percentSection[4],
            'assignment': percentSection[5],
            'evaluation_status': percentSection[6],
            'total_students': percentSection[7],
            'non_F_students': percentSection[8],
            'non_F_percentage': percentSection[9]
        }
        percentSections_list.append(instSections_dict)

    cursor.close()
    return jsonify(percentSections_list)

# POST a Department
@app.route('/departments', methods=['POST'])
def add_department():
    try:
        dept_code = request.json['dept_code']
        dept_name = request.json['dept_name']
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Departments (dept_code, dept_name) VALUES (%s, %s)", (dept_code, dept_name))
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({"message": "Department added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# POST a Degree
@app.route('/degrees', methods=['POST'])
def add_degree():
    try:
        level = request.json['level']
        degree_name = request.json['degree_name']
        dept_code = request.json['dept_code']
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Degrees (level, degree_name, dept_code) VALUES (%s, %s, %s)", 
                    (level, degree_name, dept_code))
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({"message": "Degree added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# POST a Course
@app.route('/courses', methods=['POST'])
def add_course():
    try:
        course_id = request.json['course_id']
        course_name = request.json['course_name']
        core_class = request.json['core_class']
        dept_code = request.json['dept_code']
        
        if not re.match(r'^[A-Z]{2,4}[0-9]{4}$', course_id):
            return jsonify({"error": "Invalid course_id format"}), 400
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Courses (course_id, course_name, core_class, dept_code) VALUES (%s, %s, %s, %s)",
                    (course_id, course_name, core_class, dept_code))
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({"message": "Course added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# POST Goals
@app.route('/goals', methods=['POST'])
def add_goal():
    try:
        goal_code = request.json['goal_code']
        goal_desc = request.json['goal_desc']
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Goals (goal_code, goal_desc) VALUES (%s, %s)", (goal_code, goal_desc))
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({"message": "Goal added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# POST a Goal Courses
@app.route('/goal_courses', methods=['POST'])
def add_goal_course():
    try:
        goal_code = request.json['goal_code']
        course_id = request.json['course_id']
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Goal_Courses (goal_code, course_id) VALUES (%s, %s)", (goal_code, course_id))
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({"message": "Goal-Course relationship added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# POST a Degree Goal
@app.route('/degree_goals', methods=['POST'])
def add_degree_goal():
    try:
        degree_id = request.json['degree_id']
        goal_code = request.json['goal_code']
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Degree_Goals (degree_id, goal_code) VALUES (%s, %s)", (degree_id, goal_code))
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({"message": "Degree-Goal relationship added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# POST an Instructor
@app.route('/instructors', methods=['POST'])
def add_instructor():
    try:
        instructor_id = request.json['instructor_id']
        instructors_name = request.json['instructors_name']
        dept_code = request.json['dept_code']
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Instructors (instructor_id, instructors_name, dept_code) VALUES (%s, %s, %s)", 
                    (instructor_id, instructors_name, dept_code))
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({"message": "Instructor added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# POST a Section for a Course
@app.route('/sections', methods=['POST'])
def add_section():
    try:
        semester = request.json['semester']
        year = request.json['year']
        sec_id = request.json['sec_id']
        course_id = request.json['course_id']
        instructor_id = request.json['instructor_id']
        num_of_students = request.json['num_of_students']
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Sections (semester, year, sec_id, course_id, instructor_id, num_of_students) VALUES (%s, %s, %s, %s, %s, %s)", 
                    (semester, year, sec_id, course_id, instructor_id, num_of_students))
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({"message": "Section added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# POST an Evaluation
@app.route('/evaluations_Insert', methods=['POST'])
def add_evaluation():
    try:
        assignment = request.json['assignment']
        instructor_id = request.json['instructor_id']
        sec_id = request.json['sec_id']
        semester = request.json['semester']
        year = request.json['year']
        course_id = request.json['course_id']
        goal_code = request.json['goal_code']
        eval_txt = request.json['eval_txt']
        grades_A = request.json.get('grades_A', 0)
        grades_B = request.json.get('grades_B', 0)
        grades_C = request.json.get('grades_C', 0)
        grades_F = request.json.get('grades_F', 0)
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Evaluations (assignment, instructor_id, sec_id, semester, year, course_id, goal_code, Eval_txt, grades_A, grades_B, grades_C, grades_F) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                    (assignment, instructor_id, sec_id, semester, year, course_id, goal_code, eval_txt, grades_A, grades_B, grades_C, grades_F))
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({"message": "Evaluation added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/evaluations_Update', methods=['POST'])
def update_evaluation():
    try:
        assignment = request.json['assignment']
        instructor_id = request.json['instructor_id']
        sec_id = request.json['sec_id']
        semester = request.json['semester']
        year = request.json['year']
        course_id = request.json['course_id']
        goal_code = request.json['goal_code']
        eval_txt = request.json['eval_txt']
        grades_A = request.json.get('grades_A', 0)
        grades_B = request.json.get('grades_B', 0)
        grades_C = request.json.get('grades_C', 0)
        grades_F = request.json.get('grades_F', 0)

        cursor = mysql.connection.cursor()
        query = """
                UPDATE evaluations
                SET 
                    Eval_txt = %s,
                    grades_A = %s,
                    grades_B = %s,
                    grades_C = %s,
                    grades_F = %s
                WHERE 
                    assignment = %s
                    AND sec_id = %s
                    AND semester = %s
                    AND year = %s
                    AND course_id = %s
                    AND goal_code = %s
                    AND instructor_id = %s;
                """
        cursor.execute(query, (eval_txt, grades_A, grades_B, grades_C, grades_F, assignment, sec_id, semester, year, course_id, goal_code, instructor_id))
        mysql.connection.commit()
        cursor.close()

        return jsonify({"message": "Evaluation updated successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400



if __name__ == '__main__':
    app.run(debug=True)