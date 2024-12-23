# University Database Management System

![University System Screenshot]('../../Assets/uni.png')

## Overview  
The **University Database Management System** is a comprehensive web-based application designed to assist university departments in the review and evaluation of their academic programs. The system supports the collection, storage, and analysis of data related to degrees, courses, instructors, and student performance.  

The primary objective of this system is to streamline the evaluation process by enabling administrators and instructors to manage program goals, assess student achievements, and gather feedback for continuous improvement. This system ensures that program evaluations are data-driven, organized, and accessible.

### Key Objectives  
1. **Centralized Data Management**: Provide a unified platform to store and manage information about degrees, courses, instructors, and evaluations.  
2. **Streamlined Evaluation**: Allow instructors to input evaluation data for each course, focusing on student performance and program goals.  
3. **Actionable Insights**: Support detailed querying to identify areas of success and opportunities for improvement within academic programs.  
4. **User-Friendly Interface**: Offer an intuitive frontend for instructors and administrators to interact with the system.  

## Features  

### Data Entry  
The system allows users to manage and input essential program-related information, including:  
- **Degrees**: Enter degree names, levels (BA, BS, MS, PhD, etc.), and associate them with courses and goals.  
- **Courses**: Manage course details, including course numbers, names, and their associations with degrees.  
- **Instructors**: Store instructor information, including unique IDs and names.  
- **Sections**: Define specific sections for courses offered in different semesters and track enrollment numbers.  
- **Goals**: Create program-specific goals, including unique codes and detailed descriptions.  

### Evaluation Process  
Instructors can enter and manage evaluation data for each course section, which includes:  
- **Evaluation Methods**: Record methods used to assess program goals, such as Homework, Projects, Quizzes, Oral Presentations, and Exams.  
- **Performance Data**: Input the number of students achieving each grade (A, B, C, F) for each goal.  
- **Feedback**: Add optional narrative feedback to suggest improvements for future semesters.  

The system also provides tools for duplicating evaluations for courses associated with multiple degrees, ensuring consistency and reducing data entry effort.  

### Querying and Reporting  
Users can generate detailed reports and insights, including:  
- **Degree Reports**: List all courses, core courses, offered sections (chronologically), program goals, and course-goal associations.  
- **Course Reports**: Display all sections of a course for a specific time range.  
- **Instructor Reports**: Show all sections taught by an instructor in a defined period.  
- **Evaluation Reports**: Identify missing or incomplete evaluation data, and highlight sections meeting specific performance criteria.  

## Technology Stack  

This project utilizes the following technologies:  
- **Backend**: Python with Flask framework for managing the server-side logic, RESTful APIs, and database interactions.  
- **Frontend**:  
  - HTML for structuring the web interface.  
  - CSS for styling the application (optional).  
  - JavaScript for interactive and dynamic user experience.  
- **Database**: MySQL for relational data storage, with the schema designed using MySQL Workbench.  
- **Development Environment**: Flask's built-in development server for testing and debugging.  
