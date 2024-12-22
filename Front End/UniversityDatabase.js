$(document).ready(function () {
    onInit();
    let sectionIDMatch = [];
    $('#insertSelect').on("change", function () {
        showHideInsertgroup('#' + $('#insertSelect').val());
        $(".eval-load").prop("disabled", true);

        switch ($('#insertSelect').val()) {
            case 'Degrees':
                setupDeptSelections('#degreeDeptCode');
                break;
            case 'Courses':
                setupDeptSelections('#coursesDeptCode');
                $('#deptCodePrefix').text($('#coursesDeptCode').val())
                break;
            case 'Goal_Courses':
                setupGoalSelections('#goalCoursesGoalList');
                setupCourseSelections('#goalCoursesCourseList');
                break;
            case 'Degree_Goals':
                setupGoalSelections('#degreeGoalsGoalList');
                setupDegreeSelections('#degreeGoalsDegreeList');
                break;
            case 'Instructors':
                setupDeptSelections('#instDeptCode');
                break;
            case 'Sections':
                setupCourseSelections('#sectionsCourses');
                setupInstSelections('#sectionsInstructors');
                break;
            case 'Evaluations':
                setupSections('#evaluationSection');
                break;
            default:
                break;
        }

    });

    $('#querySelect').on("change", function () {
        showHideQuerygroup('#' + $('#querySelect').val());

        switch ($('#querySelect').val()) {
            case 'DegreeCourses':
                setupDegreeSelections('#degreeCoursesQueryList');
                break;
            case 'DegreeSectionsRange':
                setupDegreeSelections('#degreeSectionsQueryList');
                break;
            case 'DegreeAllGoalsQuery':
                setupDegreeSelections('#degreeAllGoalsQueryList');
                break;
            case 'CoursesDegreeGoalQuery':
                setupDegreeSelections('#degreesForDGCQuery');
                setupGoalSelections('#goalsForDGCQuery');
                break;
            case 'CourseSectionRange':
                setupCourseSelections('#courseSectionsQueryList');
                break;
            case 'InstructorSectionRange':
                setupInstSelections('#instSectionsQueryList');
                break;
            default:
                break;
        }

    });

    $('#degreeLevel').on("change", function () {
        if ($('#degreeLevel').val() == "Other") {
            $('#degreeOtherDiv').removeClass("d-none");
        }
        else {
            $('#degreeOtherDiv').addClass("d-none");
            $('#degreeOther').removeClass("is-invalid");
            $('#degreeOther').val("");
        }
    });

    $('#coursesDeptCode').on("change", function () {
        $('#deptCodePrefix').text($('#coursesDeptCode').val())
    });

    $('#assignment').on("change", function () {
        if ($('#assignment').val() == "Other") {
            $('#assignmentOtherDiv').removeClass("d-none");
        }
        else {
            $('#assignmentOtherDiv').addClass("d-none");
            $('#assignmentOther').removeClass("is-invalid");
            $('#assignmentOther').val("");
        }
        $(".eval-load").prop("disabled", true);
        clearEvalValues();
    });

    $('#assignmentOther').on("change", function () {
        $(".eval-load").prop("disabled", true);
        clearEvalValues();
    });

    $('#evaluationSection').on("change", function () {
        loadSectionEvalInfo(sectionIDMatch);
        $(".eval-load").prop("disabled", true);
        clearEvalValues();
    });

    $('#evalGoals').on("change", function () {
        $(".eval-load").prop("disabled", true);
        clearEvalValues();
    });

    $('#loadEval').on("click", function () {
        dataObj = {};
        checkFieldsValidity('Evaluations', function (allValid) {
            if (allValid) {
                if ($('#assignment').val() == "Other") {
                    dataObj.assignment = $('#assignmentOther').val();
                }
                else {
                    dataObj.assignment = $('#assignment').val();
                }
                idx = 0;
                for (let i = 0; i < sectionIDMatch.length; i++) {
                    if (sectionIDMatch[i].uniqueSecID == $('#evaluationSection').val()) {
                        idx = sectionIDMatch[i].Idx;
                    }
                }

                dataObj.sec_id = sectionsOptions[idx].sec_id;
                dataObj.semester = sectionsOptions[idx].semester;
                dataObj.year = sectionsOptions[idx].year;
                dataObj.course_id = sectionsOptions[idx].course_id;

                dataObj.goal_code = $('#evalGoals').val();
                postToDatabase(endpoint + 'evaluations', dataObj, function (response) {
                    console.log(response);
                    evalObj = response;
                    if (evalObj.length) {
                        $('#gradesA').val(evalObj[0].grades_A);
                        $('#gradesB').val(evalObj[0].grades_B);
                        $('#gradesC').val(evalObj[0].grades_C);
                        $('#gradesF').val(evalObj[0].grades_F);
                        $('#evalText').val(evalObj[0].Eval_txt);
                    }
                });

                $(".eval-load").prop("disabled", false);
            } else {
                showMessageModal("Please fix the errors in the Eval Load fields.", "error");
            }
        });
    });

    $('#submitData').on("click", function () {
        dataObj = {};
        switch ($('#insertSelect').val()) {
            case 'Departments':
                checkFieldsValidity('Departments', function (allValid) {
                    if (allValid) {
                        dataObj.dept_code = $('#deptCode').val();
                        dataObj.dept_name = $('#deptName').val();

                        postToDatabase(endpoint + 'departments', dataObj, function (response) {
                            console.log(response);
                            showMessageModal(response.message, "success");
                        });
                    } else {
                        showMessageModal("Please fix the errors in the Department fields.", "error");
                    }
                });
                break;
            case 'Degrees':
                checkFieldsValidity('Degrees', function (allValid) {
                    if (allValid) {
                        dataObj.degree_name = $('#degreeName').val();
                        if ($('#degreeLevel').val() == "Other") {
                            dataObj.level = $('#degreeOther').val();
                        }
                        else {
                            dataObj.level = $('#degreeLevel').val();
                        }
                        dataObj.dept_code = $('#degreeDeptCode').val();
                        postToDatabase(endpoint + 'degrees', dataObj, function (response) {
                            console.log(response);
                            showMessageModal(response.message, "success");
                        });
                    } else {
                        showMessageModal("Please fix the errors in the Degree fields.", "error");
                    }
                });
                break;
            case 'Courses':
                checkFieldsValidity('Courses', function (allValid) {
                    if (allValid) {
                        dataObj.course_id = $('#coursesDeptCode').val() + $('#courseID').val();
                        dataObj.course_name = $('#courseName').val();
                        if ($('#coreClass').prop('checked')) {
                            dataObj.core_class = 1
                        }
                        else {
                            dataObj.core_class = 0
                        }
                        dataObj.dept_code = $('#coursesDeptCode').val();
                        postToDatabase(endpoint + 'courses', dataObj, function (response) {
                            console.log(response);
                            showMessageModal(response.message, "success");
                        });
                    } else {
                        showMessageModal("Please fix the errors in the Course fields.", "error");
                    }
                });
                break;
            case 'Goals':
                checkFieldsValidity('Goals', function (allValid) {
                    if (allValid) {
                        dataObj.goal_code = $('#goalCode').val();
                        dataObj.goal_desc = $('#goalDesc').val();
                        postToDatabase(endpoint + 'goals', dataObj, function (response) {
                            console.log(response);
                            showMessageModal(response.message, "success");
                        });
                    } else {
                        showMessageModal("Please fix the errors in the Goal fields.", "error");
                    }
                });
                break;
            case 'Goal_Courses':
                dataObj.goal_code = $('#goalCoursesGoalList').val();
                dataObj.course_id = $('#goalCoursesCourseList').val();
                postToDatabase(endpoint + 'goal_courses', dataObj, function (response) {
                    console.log(response);
                    showMessageModal(response.message, "success");
                });
                break;
            case 'Degree_Goals':
                dataObj.goal_code = $('#degreeGoalsGoalList').val();
                dataObj.degree_id = $('#degreeGoalsDegreeList').val();
                postToDatabase(endpoint + 'degree_goals', dataObj, function (response) {
                    console.log(response);
                    showMessageModal(response.message, "success");
                });
                break;
            case 'Instructors':
                checkFieldsValidity('Instructors', function (allValid) {
                    if (allValid) {
                        dataObj.instructor_id = $('#instructorID').val();
                        dataObj.instructors_name = $('#instructorName').val();
                        dataObj.dept_code = $('#instDeptCode').val();
                        postToDatabase(endpoint + 'instructors', dataObj, function (response) {
                            console.log(response);
                            showMessageModal(response.message, "success");
                        });
                    } else {
                        showMessageModal("Please fix the errors in the Instructor fields.", "error");
                    }
                });
                break;
            case 'Sections':
                dataObj.semester = $('#semester').val();
                dataObj.year = $('#sectionYear').val();
                dataObj.sec_id = $('#sectionID').val();
                dataObj.course_id = $('#sectionsCourses').val();
                dataObj.instructor_id = $('#sectionsInstructors').val();
                dataObj.num_of_students = $('#numOfStudents').val();
                postToDatabase(endpoint + 'sections', dataObj, function (response) {
                    console.log(response);
                    showMessageModal(response.message, "success");
                });
                break;
            case 'Evaluations':
                checkFieldsValidity('Evaluations', function (allValid) {
                    if (allValid) {
                        if ($('#assignment').val() == "Other") {
                            dataObj.assignment = $('#assignmentOther').val();
                        }
                        else {
                            dataObj.assignment = $('#assignment').val();
                        }
                        dataObj.instructor_id = $('#evalInstID').val();

                        studentCnt = 0
                        dataObj.eval_txt = $('#evalText').val();
                        if ($('#gradesA').val() == '') {
                            dataObj.grades_A = '0'
                        }
                        else {
                            dataObj.grades_A = $('#gradesA').val();
                        }
                        if ($('#gradesB').val() == '') {
                            dataObj.grades_B = '0'
                        }
                        else {
                            dataObj.grades_B = $('#gradesB').val();
                        }
                        if ($('#gradesC').val() == '') {
                            dataObj.grades_C = '0'
                        }
                        else {
                            dataObj.grades_C = $('#gradesC').val();
                        }
                        if ($('#gradesF').val() == '') {
                            dataObj.grades_F = '0'
                        }
                        else {
                            dataObj.grades_F = $('#gradesF').val();
                        }
                        dataObj.goal_code = $('#evalGoals').val();
                        studentCnt = Number($('#gradesA').val()) + Number($('#gradesB').val()) + Number($('#gradesC').val()) + Number($('#gradesF').val())

                        idx = 0;
                        for (let i = 0; i < sectionIDMatch.length; i++) {
                            if (sectionIDMatch[i].uniqueSecID == $('#evaluationSection').val()) {
                                idx = sectionIDMatch[i].Idx;
                            }
                        }
                        dataObj.sec_id = sectionsOptions[idx].sec_id;
                        dataObj.semester = sectionsOptions[idx].semester;
                        dataObj.year = sectionsOptions[idx].year;
                        dataObj.course_id = sectionsOptions[idx].course_id;

                        if (studentCnt <= sectionsOptions[idx].num_of_students) {
                            if (evalObj.length) {
                                postToDatabase(endpoint + 'evaluations_Update', dataObj, function (response) {
                                    console.log(response);
                                    $(".eval-load").prop("disabled", true);
                                    showMessageModal(response.message, "success");
                                });
                            }
                            else {
                                postToDatabase(endpoint + 'evaluations_Insert', dataObj, function (response) {
                                    console.log(response);
                                    $(".eval-load").prop("disabled", true);
                                    showMessageModal(response.message, "success");
                                });
                            }
                        }
                        else {
                            showMessageModal("Number of Students in Grades is more Section Total Students of " + sectionsOptions[idx].num_of_students, "error");
                        }
                    } else {
                        showMessageModal("Please fix the errors in the Evaluation fields.", "error");
                    }
                });
                break;
            default:
                break;
        }
    });

    $(".numeric-input").on("keypress", function (event) {
        var key = event.which || event.keyCode;
        // Allow numbers (48-57), backspace (8)
        if (!((key >= 48 && key <= 57) || key === 8)) {
            event.preventDefault();  // Prevent non-numeric
        }
    });

    $(".text-input-insert").blur(async function () {
        const inputField = $(this);
        const fieldValue = inputField.val().trim();

        if (!sanitizeInput(fieldValue)) {
            $(this).addClass('is-invalid');

            $(this).focus();
        } else {
            $(this).removeClass('is-invalid');
        }

    });

    let text_max = 255;
    $('#count_message').html('0 / ' + text_max);

    $('#evalText').keyup(function () {
        let text_length = $('#evalText').val().length;

        $('#count_message').html(text_length + ' / ' + text_max);
    });

    $('#loadQuery').on("click", function () {
        returnObj = [];
        dataObj = {};
        switch ($('#querySelect').val()) {
            case 'DegreeCourses':
                dataObj.degree_id = $('#degreeCoursesQueryList').val();
                postToDatabase(endpoint + 'degreeCourses', dataObj, function (response) {
                    console.log(response);
                    loadQueryTable(response);
                });
                break;
            case 'DegreeSectionsRange':
                dataObj.degree_id = $('#degreeSectionsQueryList').val();
                dataObj.start_year = $('#degreeSectionsStartYear').val();
                dataObj.end_year = $('#degreeSectionsEndYear').val();
                postToDatabase(endpoint + 'degreeSectionsRange', dataObj, function (response) {
                    console.log(response);
                    loadQueryTable(response);
                });
                break;
            case 'DegreeAllGoalsQuery':
                dataObj.degree_id = $('#degreeAllGoalsQueryList').val();
                postToDatabase(endpoint + 'degreeGoals', dataObj, function (response) {
                    console.log(response);
                    loadQueryTable(response);
                });
                break;
            case 'CoursesDegreeGoalQuery':
                dataObj.goal_code = $('#goalsForDGCQuery').val();
                dataObj.degree_id = $('#degreesForDGCQuery').val();
                postToDatabase(endpoint + 'goalCourses', dataObj, function (response) {
                    console.log(response);
                    loadQueryTable(response);
                });
                break;
            case 'CourseSectionRange':
                dataObj.course_id = $('#courseSectionsQueryList').val();
                //dataObj.semester = $('#courseSectionsSemester').val();
                dataObj.start_year = $('#courseSectionsStartYear').val();
                dataObj.end_year = $('#courseSectionsEndYear').val();
                postToDatabase(endpoint + 'courseSections', dataObj, function (response) {
                    console.log(response);
                    loadQueryTable(response);
                });
                break;
            case 'InstructorSectionRange':
                dataObj.instructor_id = $('#instSectionsQueryList').val();
                //dataObj.semester = $('#instSectionsSemester').val();
                dataObj.start_year = $('#instSectionsStartYear').val();
                dataObj.end_year = $('#instSectionsEndYear').val();
                postToDatabase(endpoint + 'instSections', dataObj, function (response) {
                    console.log(response);
                    loadQueryTable(response);
                });
                break;
            case 'SemesterSectionsEval':
                dataObj.semester = $('#semesterForSSEQuery').val();
                dataObj.year = $('#yearForSSEQuery').val();
                postToDatabase(endpoint + 'sectionEval', dataObj, function (response) {
                    console.log(response);
                    loadQueryTable(response);
                });
                break;
            case 'SemesterPassingPercentage':
                dataObj.semester = $('#semesterForPassing').val();
                dataObj.year = $('#yearForPassing').val();
                dataObj.user_percentage = $('#percentageForPassing').val();
                postToDatabase(endpoint + 'percentSection', dataObj, function (response) {
                    console.log(response);
                    loadQueryTable(response);
                });
                break;
            default:
                break;
        }
    });

    $('.date-own').datepicker({
        minViewMode: 2,
        format: 'yyyy'
    });

    $('.date-own').on("keypress", function (event) {
        event.preventDefault();  // Prevent non-numeric
    });

    $('#closeModal').on("click", function () {
        $('#messageModal').modal('hide');
    });

    function postToDatabase(url, data, callback) {
        $.ajax({
            type: 'post',
            url: url,
            contentType: "application/json;",
            data: JSON.stringify(data),
            success: function (response) {
                callback(response);
            },
            error: function (error) {
                console.error(error);
                showMessageModal(error.responseJSON.error, "error");
            }
        });
    }

    function getInitialData(url, callback) {
        $.ajax({
            type: 'get',
            url: url,
            success: function (response) {
                callback(response);
            },
            error: function (error) {
                console.error(error);
            }
        });
    }

    function loadSectionEvalInfo(sectionArray) {
        if (!sectionArray || sectionArray.length === 0) {
            console.error("sectionArray is empty or undefined!");
            return;
        }

        let idx = 0;
        let currentSelect = $('#evaluationSection').val();

        for (let i = 0; i < sectionArray.length; i++) {
            if (currentSelect == sectionArray[i].uniqueSecID) {
                idx = sectionArray[i].Idx;
            }
        }

        $('#evalInstID').val(sectionsOptions[idx].instructor_id);

        $('#evalGoals').empty();
        courseSelected = sectionsOptions[idx].course_id;
        for (let i = 0; i < goalCoursesOptions.length; i++) {
            if (goalCoursesOptions[i].course_id == courseSelected) {
                for (let j = 0; j < goalOptions.length; j++) {
                    if (goalOptions[j].goal_code == goalCoursesOptions[i].goal_code) {
                        const goalOption = goalOptions[i];
                        const option = $("<option></option>").val(goalOption.goal_code).text(goalOption.goal_desc);
                        $('#evalGoals').append(option);
                    }
                }
            }
        }
    }

    function loadQueryTable(returnObj) {
        $('#queryTableDiv').empty();
        let htmlStr = '';
        if (!returnObj || returnObj.length === 0) {
            console.error("return for " + $('#querySelect').val() + " is empty or undefined!");
            htmlStr += "<span>The Query is Empty</span>";
            $('#queryTableDiv').append(htmlStr);

            return;
        }
        else {
            const keys = Object.keys(returnObj[0]);

            htmlStr += '<table class="table"><thead><tr>';
            for (let i = 0; i < keys.length; i++) {
                htmlStr += '<th scope="col">' + keys[i] + '</th>';
            }
            htmlStr += '</tr></thead><tbody>';

            for (let i = 0; i < returnObj.length; i++) {
                const objRow = returnObj[i];
                htmlStr += '<tr>';
                for (let j in objRow) {
                    htmlStr += '<td>' + objRow[j] + '</td>';
                }
                htmlStr += '</tr>';
            }
            htmlStr += '</tbody></table>';

            $('#queryTableDiv').append(htmlStr);
        }
    }

    function showHideInsertgroup(elementID) {
        $(".insert-group").each(function () {
            $(this).addClass("d-none");
        });
        $(elementID).removeClass("d-none");
    }

    function showHideQuerygroup(elementID) {
        $(".query-group").each(function () {
            $(this).addClass("d-none");
        });
        $(elementID).removeClass("d-none");
    }

    function setupDeptSelections(elementID) {
        $(elementID).empty()
        for (let i = 0; i < deptOptions.length; i++) {
            const deptOption = deptOptions[i];
            const option = $("<option></option>").val(deptOption.dept_code).text(deptOption.dept_name);
            $(elementID).append(option);
        }
    }

    function setupGoalSelections(elementID) {
        $(elementID).empty()
        for (let i = 0; i < goalOptions.length; i++) {
            const goalOption = goalOptions[i];
            const option = $("<option></option>").val(goalOption.goal_code).text(goalOption.goal_desc);
            $(elementID).append(option);
        }
    }

    function setupCourseSelections(elementID) {
        $(elementID).empty()
        for (let i = 0; i < coursesOptions.length; i++) {
            const courseOption = coursesOptions[i];
            const option = $("<option></option>").val(courseOption.course_id).text(courseOption.course_name);
            $(elementID).append(option);
        }
    }

    function setupDegreeSelections(elementID) {
        $(elementID).empty()
        for (let i = 0; i < degreeOptions.length; i++) {
            const degreeOption = degreeOptions[i];
            const option = $("<option></option>").val(degreeOption.degree_id).text(degreeOption.level + ' ' + degreeOption.degree_Name);
            $(elementID).append(option);
        }
    }

    function setupInstSelections(elementID) {
        $(elementID).empty()
        for (let i = 0; i < instructorOptions.length; i++) {
            const instOption = instructorOptions[i];
            const option = $("<option></option>").val(instOption.instructor_id).text(instOption.instructors_name);
            $(elementID).append(option);
        }
    }

    function setupSections(elementID) {
        sectionIDMatch.splice(0, sectionIDMatch.length);
        $(elementID).empty()
        for (let i = 0; i < sectionsOptions.length; i++) {
            const sectionOption = sectionsOptions[i];
            let uniqueSecID = sectionOption.semester + sectionOption.year.toString() + sectionOption.sec_id + sectionOption.course_id;
            let secObj = {};
            secObj.uniqueSecID = uniqueSecID;
            secObj.Idx = i;
            sectionIDMatch.push(secObj);
            const option = $("<option></option>").val(uniqueSecID).text(sectionOption.semester + ' ' + sectionOption.year.toString() + ' ' + sectionOption.course_id + '-' + sectionOption.sec_id);
            $(elementID).append(option);
        }
        loadSectionEvalInfo(sectionIDMatch);
    }

    function showMessageModal(message, type = 'info') {
        let title = '';
        let content = message;
        let modalClass = '';

        if (type === 'success') {
            title = 'Success';
            modalClass = 'text-success';
            onInit();
        } else if (type === 'error') {
            title = 'Error';
            modalClass = 'text-danger';
        }

        document.getElementById('messageModalLabel').textContent = title;
        document.getElementById('modalMessageContent').textContent = content;
        document.getElementById('modalMessageContent').className = modalClass;

        $('#messageModal').modal('show');
    }

    function clearEvalValues() {
        $('#gradesA').val('');
        $('#gradesB').val('');
        $('#gradesC').val('');
        $('#gradesF').val('');
        $('#evalText').val('');
    }

    function sanitizeInput(input) {
        const sqlKeys = [
            "SELECT", "DROP", "DELETE", "INSERT", "UPDATE", "UNION",
            "DROP DATABASE", "ALTER", "CREATE", "TRUNCATE", "EXEC", "UNLOAD",
            "DECLARE", "FETCH", "CAST", "XP_", "SHUTDOWN", "SLEEP", "--", ";",
            "'", '"', "/*", "*/"
        ];

        let sanitizedInput = input.toUpperCase();

        for (let key of sqlKeys) {
            if (sanitizedInput.includes(key)) {
                return false;
            }
        }

        if (sanitizedInput.includes("'") || sanitizedInput.includes('"') || sanitizedInput.includes(";")) {
            return false;
        }

        return true;
    }

    function checkFieldsValidity(divId, callback) {
        var validFields = true;

        $('#' + divId + ' input, #' + divId + ' textarea').each(function () {
            sanitizeInput($(this).val());

            if ($(this).hasClass('is-invalid')) {
                validFields = false;
                return false;
            }
        });

        callback(validFields);
    }

    function onInit() {
        getInitialData(endpoint + 'degrees', function (response) {
            degreeOptions = response;
        });
        getInitialData(endpoint + 'goals', function (response) {
            goalOptions = response;
        });
        getInitialData(endpoint + 'departments', function (response) {
            deptOptions = response;
        });
        getInitialData(endpoint + 'courses', function (response) {
            coursesOptions = response;
        });
        getInitialData(endpoint + 'instructors', function (response) {
            instructorOptions = response;
        });
        getInitialData(endpoint + 'sections', function (response) {
            sectionsOptions = response;
        });
        getInitialData(endpoint + 'goalcourses', function (response) {
            goalCoursesOptions = response;
        });
    }
});