// Load attendance records when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadAttendance();
    loadStudentsForDropdown();
    loadClassesForDropdown();
    setTodayDate();
});

// Set today's date as default
function setTodayDate() {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date').value = today;
}

// Load all attendance records
async function loadAttendance() {
    try {
        const response = await fetch('/api/attendance');
        const records = await response.json();
        displayAttendance(records);
    } catch (error) {
        console.error('Error loading attendance:', error);
        alert('Error loading attendance records');
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

// Display attendance in table
function displayAttendance(records) {
    const tbody = document.getElementById('attendanceTableBody');
    tbody.innerHTML = '';

    records.forEach(record => {
        const row = tbody.insertRow();
        const statusClass = record.status === 'Present' ? 'status-present' :
                          record.status === 'Absent' ? 'status-absent' : 'status-late';

        row.innerHTML = `
            <td>${record.id}</td>
            <td>${record.student_name || '-'}</td>
            <td>${record.class_name || '-'}</td>
            <td>${record.date}</td>
            <td><span class="${statusClass}">${record.status}</span></td>
            <td class="action-buttons">
                <button class="btn btn-danger" onclick="deleteAttendance(${record.id})">Delete</button>
            </td>
        `;
    });
}

// Show add modal
function showAddModal() {
    document.getElementById('attendanceForm').reset();
    setTodayDate();
    document.getElementById('attendanceModal').style.display = 'block';
}

// Delete attendance record
async function deleteAttendance(id) {
    if (!confirm('Are you sure you want to delete this attendance record?')) return;

    try {
        const response = await fetch(`/api/attendance/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            loadAttendance();
            alert('Attendance record deleted successfully');
        } else {
            alert('Error deleting attendance record');
        }
    } catch (error) {
        console.error('Error deleting attendance:', error);
        alert('Error deleting attendance record');
    }
}

// Close modal
function closeModal() {
    document.getElementById('attendanceModal').style.display = 'none';
}

// Handle form submission
document.getElementById('attendanceForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const data = {
        student_id: parseInt(document.getElementById('studentId').value),
        class_id: parseInt(document.getElementById('classId').value),
        date: document.getElementById('date').value,
        status: document.getElementById('status').value
    };

    try {
        const response = await fetch('/api/attendance', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            closeModal();
            loadAttendance();
            alert('Attendance recorded successfully');
        } else {
            const error = await response.json();
            alert('Error: ' + (error.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error saving attendance:', error);
        alert('Error saving attendance');
    }
});

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('attendanceModal');
    if (event.target == modal) {
        closeModal();
    }
}
