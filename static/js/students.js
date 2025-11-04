// Load students when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadStudents();
});

// Load all students
async function loadStudents() {
    try {
        const response = await fetch('/api/students');
        const students = await response.json();
        displayStudents(students);
    } catch (error) {
        console.error('Error loading students:', error);
        alert('Error loading students');
    }
}

// Display students in table
function displayStudents(students) {
    const tbody = document.getElementById('studentsTableBody');
    tbody.innerHTML = '';

    students.forEach(student => {
        const row = tbody.insertRow();
        row.innerHTML = `
            <td>${student.id}</td>
            <td>${student.first_name}</td>
            <td>${student.last_name}</td>
            <td>${student.email}</td>
            <td>${student.date_of_birth}</td>
            <td>${student.grade_level || '-'}</td>
            <td class="action-buttons">
                <button class="btn btn-edit" onclick="editStudent(${student.id})">Edit</button>
                <button class="btn btn-danger" onclick="deleteStudent(${student.id})">Delete</button>
            </td>
        `;
    });
}

// Show add modal
function showAddModal() {
    document.getElementById('modalTitle').textContent = 'Add Student';
    document.getElementById('studentForm').reset();
    document.getElementById('studentId').value = '';
    document.getElementById('studentModal').style.display = 'block';
}

// Edit student
async function editStudent(id) {
    try {
        const response = await fetch(`/api/students/${id}`);
        const student = await response.json();

        document.getElementById('modalTitle').textContent = 'Edit Student';
        document.getElementById('studentId').value = student.id;
        document.getElementById('firstName').value = student.first_name;
        document.getElementById('lastName').value = student.last_name;
        document.getElementById('email').value = student.email;
        document.getElementById('dateOfBirth').value = student.date_of_birth;
        document.getElementById('gradeLevel').value = student.grade_level || '';

        document.getElementById('studentModal').style.display = 'block';
    } catch (error) {
        console.error('Error loading student:', error);
        alert('Error loading student');
    }
}

// Delete student
async function deleteStudent(id) {
    if (!confirm('Are you sure you want to delete this student?')) return;

    try {
        const response = await fetch(`/api/students/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            loadStudents();
            alert('Student deleted successfully');
        } else {
            alert('Error deleting student');
        }
    } catch (error) {
        console.error('Error deleting student:', error);
        alert('Error deleting student');
    }
}

// Close modal
function closeModal() {
    document.getElementById('studentModal').style.display = 'none';
}

// Handle form submission
document.getElementById('studentForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const studentId = document.getElementById('studentId').value;
    const data = {
        first_name: document.getElementById('firstName').value,
        last_name: document.getElementById('lastName').value,
        email: document.getElementById('email').value,
        date_of_birth: document.getElementById('dateOfBirth').value,
        grade_level: document.getElementById('gradeLevel').value
    };

    try {
        const url = studentId ? `/api/students/${studentId}` : '/api/students';
        const method = studentId ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            closeModal();
            loadStudents();
            alert(studentId ? 'Student updated successfully' : 'Student added successfully');
        } else {
            const error = await response.json();
            alert('Error: ' + (error.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error saving student:', error);
        alert('Error saving student');
    }
});

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('studentModal');
    if (event.target == modal) {
        closeModal();
    }
}
