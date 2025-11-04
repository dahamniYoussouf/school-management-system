// Load classes and teachers when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadClasses();
    loadTeachersForDropdown();
});

// Load all classes
async function loadClasses() {
    try {
        const response = await fetch('/api/classes');
        const classes = await response.json();
        displayClasses(classes);
    } catch (error) {
        console.error('Error loading classes:', error);
        alert('Error loading classes');
    }
}

// Load teachers for dropdown
async function loadTeachersForDropdown() {
    try {
        const response = await fetch('/api/teachers');
        const teachers = await response.json();

        const select = document.getElementById('teacherId');
        select.innerHTML = '<option value="">Select Teacher</option>';

        teachers.forEach(teacher => {
            const option = document.createElement('option');
            option.value = teacher.id;
            option.textContent = `${teacher.first_name} ${teacher.last_name}`;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading teachers:', error);
    }
}

// Display classes in table
function displayClasses(classes) {
    const tbody = document.getElementById('classesTableBody');
    tbody.innerHTML = '';

    classes.forEach(cls => {
        const row = tbody.insertRow();
        row.innerHTML = `
            <td>${cls.id}</td>
            <td>${cls.name}</td>
            <td>${cls.subject}</td>
            <td>${cls.teacher_name || '-'}</td>
            <td>${cls.schedule || '-'}</td>
            <td>${cls.room || '-'}</td>
            <td class="action-buttons">
                <button class="btn btn-edit" onclick="editClass(${cls.id})">Edit</button>
                <button class="btn btn-danger" onclick="deleteClass(${cls.id})">Delete</button>
            </td>
        `;
    });
}

// Show add modal
function showAddModal() {
    document.getElementById('modalTitle').textContent = 'Add Class';
    document.getElementById('classForm').reset();
    document.getElementById('classId').value = '';
    document.getElementById('classModal').style.display = 'block';
}

// Edit class
async function editClass(id) {
    try {
        const response = await fetch(`/api/classes/${id}`);
        const cls = await response.json();

        document.getElementById('modalTitle').textContent = 'Edit Class';
        document.getElementById('classId').value = cls.id;
        document.getElementById('className').value = cls.name;
        document.getElementById('subject').value = cls.subject;
        document.getElementById('teacherId').value = cls.teacher_id;
        document.getElementById('schedule').value = cls.schedule || '';
        document.getElementById('room').value = cls.room || '';

        document.getElementById('classModal').style.display = 'block';
    } catch (error) {
        console.error('Error loading class:', error);
        alert('Error loading class');
    }
}

// Delete class
async function deleteClass(id) {
    if (!confirm('Are you sure you want to delete this class?')) return;

    try {
        const response = await fetch(`/api/classes/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            loadClasses();
            alert('Class deleted successfully');
        } else {
            alert('Error deleting class');
        }
    } catch (error) {
        console.error('Error deleting class:', error);
        alert('Error deleting class');
    }
}

// Close modal
function closeModal() {
    document.getElementById('classModal').style.display = 'none';
}

// Handle form submission
document.getElementById('classForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const classId = document.getElementById('classId').value;
    const data = {
        name: document.getElementById('className').value,
        subject: document.getElementById('subject').value,
        teacher_id: parseInt(document.getElementById('teacherId').value),
        schedule: document.getElementById('schedule').value,
        room: document.getElementById('room').value
    };

    try {
        const url = classId ? `/api/classes/${classId}` : '/api/classes';
        const method = classId ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            closeModal();
            loadClasses();
            alert(classId ? 'Class updated successfully' : 'Class added successfully');
        } else {
            const error = await response.json();
            alert('Error: ' + (error.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error saving class:', error);
        alert('Error saving class');
    }
});

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('classModal');
    if (event.target == modal) {
        closeModal();
    }
}
