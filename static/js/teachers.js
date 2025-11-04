// Load teachers when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadTeachers();
});

// Load all teachers
async function loadTeachers() {
    try {
        const response = await fetch('/api/teachers');
        const teachers = await response.json();
        displayTeachers(teachers);
    } catch (error) {
        console.error('Error loading teachers:', error);
        alert('Error loading teachers');
    }
}

// Display teachers in table
function displayTeachers(teachers) {
    const tbody = document.getElementById('teachersTableBody');
    tbody.innerHTML = '';

    teachers.forEach(teacher => {
        const row = tbody.insertRow();
        row.innerHTML = `
            <td>${teacher.id}</td>
            <td>${teacher.first_name}</td>
            <td>${teacher.last_name}</td>
            <td>${teacher.email}</td>
            <td>${teacher.subject || '-'}</td>
            <td>${teacher.hire_date}</td>
            <td class="action-buttons">
                <button class="btn btn-edit" onclick="editTeacher(${teacher.id})">Edit</button>
                <button class="btn btn-danger" onclick="deleteTeacher(${teacher.id})">Delete</button>
            </td>
        `;
    });
}

// Show add modal
function showAddModal() {
    document.getElementById('modalTitle').textContent = 'Add Teacher';
    document.getElementById('teacherForm').reset();
    document.getElementById('teacherId').value = '';
    document.getElementById('teacherModal').style.display = 'block';
}

// Edit teacher
async function editTeacher(id) {
    try {
        const response = await fetch(`/api/teachers/${id}`);
        const teacher = await response.json();

        document.getElementById('modalTitle').textContent = 'Edit Teacher';
        document.getElementById('teacherId').value = teacher.id;
        document.getElementById('firstName').value = teacher.first_name;
        document.getElementById('lastName').value = teacher.last_name;
        document.getElementById('email').value = teacher.email;
        document.getElementById('subject').value = teacher.subject || '';

        document.getElementById('teacherModal').style.display = 'block';
    } catch (error) {
        console.error('Error loading teacher:', error);
        alert('Error loading teacher');
    }
}

// Delete teacher
async function deleteTeacher(id) {
    if (!confirm('Are you sure you want to delete this teacher?')) return;

    try {
        const response = await fetch(`/api/teachers/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            loadTeachers();
            alert('Teacher deleted successfully');
        } else {
            alert('Error deleting teacher');
        }
    } catch (error) {
        console.error('Error deleting teacher:', error);
        alert('Error deleting teacher');
    }
}

// Close modal
function closeModal() {
    document.getElementById('teacherModal').style.display = 'none';
}

// Handle form submission
document.getElementById('teacherForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const teacherId = document.getElementById('teacherId').value;
    const data = {
        first_name: document.getElementById('firstName').value,
        last_name: document.getElementById('lastName').value,
        email: document.getElementById('email').value,
        subject: document.getElementById('subject').value
    };

    try {
        const url = teacherId ? `/api/teachers/${teacherId}` : '/api/teachers';
        const method = teacherId ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            closeModal();
            loadTeachers();
            alert(teacherId ? 'Teacher updated successfully' : 'Teacher added successfully');
        } else {
            const error = await response.json();
            alert('Error: ' + (error.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error saving teacher:', error);
        alert('Error saving teacher');
    }
});

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('teacherModal');
    if (event.target == modal) {
        closeModal();
    }
}
