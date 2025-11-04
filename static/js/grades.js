// Load grades when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadGrades();
    loadStudentsForDropdown();
    loadClassesForDropdown();
    setTodayDate();
});

// Set today's date as default
function setTodayDate() {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date').value = today;
}

// Load all grades
async function loadGrades() {
    try {
        const response = await fetch('/api/grades');
        const grades = await response.json();
        displayGrades(grades);
    } catch (error) {
        console.error('Error loading grades:', error);
        alert('Error loading grades');
    }
}

// Load students for dropdown
async function loadStudentsForDropdown() {
    try {
        const response = await fetch('/api/students');
        const students = await response.json();

        const select = document.getElementById('studentId');
        select.innerHTML = '<option value="">Select Student</option>';

        students.forEach(student => {
            const option = document.createElement('option');
            option.value = student.id;
            option.textContent = `${student.first_name} ${student.last_name}`;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading students:', error);
    }
}

// Load classes for dropdown
async function loadClassesForDropdown() {
    try {
        const response = await fetch('/api/classes');
        const classes = await response.json();

        const select = document.getElementById('classId');
        select.innerHTML = '<option value="">Select Class</option>';

        classes.forEach(cls => {
            const option = document.createElement('option');
            option.value = cls.id;
            option.textContent = cls.name;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading classes:', error);
    }
}

// Display grades in table
function displayGrades(grades) {
    const tbody = document.getElementById('gradesTableBody');
    tbody.innerHTML = '';

    grades.forEach(grade => {
        const row = tbody.insertRow();
        row.innerHTML = `
            <td>${grade.id}</td>
            <td>${grade.student_name || '-'}</td>
            <td>${grade.class_name || '-'}</td>
            <td>${grade.assignment_name}</td>
            <td>${grade.grade}</td>
            <td>${grade.date}</td>
            <td class="action-buttons">
                <button class="btn btn-edit" onclick="editGrade(${grade.id})">Edit</button>
                <button class="btn btn-danger" onclick="deleteGrade(${grade.id})">Delete</button>
            </td>
        `;
    });
}

// Show add modal
function showAddModal() {
    document.getElementById('modalTitle').textContent = 'Add Grade';
    document.getElementById('gradeForm').reset();
    document.getElementById('gradeId').value = '';
    setTodayDate();
    document.getElementById('gradeModal').style.display = 'block';
}

// Edit grade
async function editGrade(id) {
    try {
        const response = await fetch(`/api/grades/${id}`);
        const grade = await response.json();

        document.getElementById('modalTitle').textContent = 'Edit Grade';
        document.getElementById('gradeId').value = grade.id;
        document.getElementById('studentId').value = grade.student_id;
        document.getElementById('classId').value = grade.class_id;
        document.getElementById('assignmentName').value = grade.assignment_name;
        document.getElementById('grade').value = grade.grade;
        document.getElementById('date').value = grade.date;

        document.getElementById('gradeModal').style.display = 'block';
    } catch (error) {
        console.error('Error loading grade:', error);
        alert('Error loading grade');
    }
}

// Delete grade
async function deleteGrade(id) {
    if (!confirm('Are you sure you want to delete this grade?')) return;

    try {
        const response = await fetch(`/api/grades/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            loadGrades();
            alert('Grade deleted successfully');
        } else {
            alert('Error deleting grade');
        }
    } catch (error) {
        console.error('Error deleting grade:', error);
        alert('Error deleting grade');
    }
}

// Close modal
function closeModal() {
    document.getElementById('gradeModal').style.display = 'none';
}

// Handle form submission
document.getElementById('gradeForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const gradeId = document.getElementById('gradeId').value;
    const data = {
        student_id: parseInt(document.getElementById('studentId').value),
        class_id: parseInt(document.getElementById('classId').value),
        assignment_name: document.getElementById('assignmentName').value,
        grade: parseFloat(document.getElementById('grade').value),
        date: document.getElementById('date').value
    };

    try {
        const url = gradeId ? `/api/grades/${gradeId}` : '/api/grades';
        const method = gradeId ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            closeModal();
            loadGrades();
            alert(gradeId ? 'Grade updated successfully' : 'Grade added successfully');
        } else {
            const error = await response.json();
            alert('Error: ' + (error.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error saving grade:', error);
        alert('Error saving grade');
    }
});

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('gradeModal');
    if (event.target == modal) {
        closeModal();
    }
}
