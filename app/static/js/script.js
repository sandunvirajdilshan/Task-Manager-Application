document.addEventListener('DOMContentLoaded', function () {

    // DOM elements
    const loader = document.querySelector("#loading");
    const taskForm = document.getElementById('taskForm');
    const editTaskForm = document.getElementById('editTaskForm');

    // Event listeners
    taskForm.addEventListener('submit', event => handleFormSubmit(event, 'taskForm'));
    editTaskForm.addEventListener('submit', event => handleFormSubmit(event, 'editTaskForm'));

    // Functions

    // Handle form submission for adding/editing tasks
    const handleFormSubmit = (event, formId) => {
        event.preventDefault();
        const form = document.getElementById(formId);
        const formData = new FormData(form);
        form.reset();
        displayLoading();
        const url = formId === 'taskForm' ? '/addtask' : '/edittask';
        submitFormData(url, formData);
    };

    // Submit form data via fetch
    const submitFormData = (url, formData) => {
        fetch(url, {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                hideLoading();
                showMessage(data.message, data.success === 'true');
                if (data.success === 'true') {
                    const modalId = url === '/addtask' ? '#newTaskModal' : '#editTaskModal';
                    $(modalId).modal('hide');
                    fetchTasks();
                }
            })
    };

    // Fetch tasks from server
    function fetchTasks() {
        displayLoading();
        fetch('/tasks', { method: 'GET' })
            .then(response => response.json())
            .then(data => {
                hideLoading();
                if (data.success === 'false') {
                    showMessage(data.message, false);
                } else {
                    displayTasks(data.tasks);
                }
            })
    }

    // Display tasks in the UI
    function displayTasks(tasks) {
        const sortedTasks = tasks.sort((a, b) => {
            const [dateA, timeA] = a[3].split(' ');
            const [dateB, timeB] = b[3].split(' ');
            if (dateA !== dateB) {
                return dateA.localeCompare(dateB);
            }
            return timeA.localeCompare(timeB);
        });

        const taskList = document.getElementById('taskList');
        taskList.innerHTML = '';
        sortedTasks.forEach(task => {
            const card = createTaskCard(task);
            taskList.appendChild(card);
        });
    }


    // Create task card
    function createTaskCard(task) {
        const card = document.createElement('div');
        card.classList.add('card', 'm-2');
        const cardBody = document.createElement('div');
        cardBody.classList.add('card-body');

        const taskName = document.createElement('h5');
        taskName.classList.add('card-title');
        taskName.textContent = task[1]; // TaskName is at index 1 in the tuple
        cardBody.appendChild(taskName);
        card.appendChild(cardBody);

        const detailsButton = document.createElement('button');
        detailsButton.classList.add('btn', 'btn-info', 'mr-2');
        detailsButton.textContent = 'Details';
        detailsButton.addEventListener('click', () => {
            displayTaskDetailsModal(task);
        });
        cardBody.appendChild(detailsButton);

        const editButton = document.createElement('button');
        editButton.classList.add('btn', 'btn-warning', 'mr-2');
        editButton.textContent = 'Edit';
        editButton.addEventListener('click', () => {
            displayEditTaskModal(task);
        });
        cardBody.appendChild(editButton);

        const deleteButton = document.createElement('button');
        deleteButton.classList.add('btn', 'btn-danger');
        deleteButton.textContent = 'Delete';
        deleteButton.addEventListener('click', () => {
            displayDeleteTaskModal(task);
        });
        cardBody.appendChild(deleteButton);
        return card;
    }


    // Display task details modal
    function displayTaskDetailsModal(task) {
        const modalTitle = document.getElementById('taskDetailsModalTitle');
        modalTitle.textContent = task.TaskName;

        const modalBody = document.getElementById('taskDetailsModalBody');
        modalBody.innerHTML = `
            <p><strong>Description:</strong> ${task[2]}</p>
            <p><strong>Date:</strong> ${task[3]}</p>
            <p><strong>Time:</strong> ${task[4]}</p>
        `;

        $('#taskDetailsModal').modal('show');
    }

    // Display edit task modal
    function displayEditTaskModal(task) {
        const modalTitle = document.getElementById('editTaskModalLabel');
        modalTitle.textContent = 'Edit Task';

        const editForm = document.getElementById('editTaskForm');
        editForm.taskId.value = task[0];

        editForm.taskName.value = task[1];
        editForm.taskDescription.value = task[2];
        editForm.taskDate.value = task[3];
        editForm.taskTime.value = task[4];

        $('#editTaskModal').modal('show');
    }

    // Display delete task modal
    function displayDeleteTaskModal(task) {
        const modalTitle = document.getElementById('deleteTaskModalTitle');
        modalTitle.textContent = 'Confirm Deletion';

        const modalBody = document.getElementById('deleteTaskModalBody');
        modalBody.innerHTML = `
            <p>Are you sure you want to delete task "${task[1]}"?</p>
        `;

        const confirmButton = document.getElementById('confirmDeleteButton');
        confirmButton.addEventListener('click', () => {
            const formData = new FormData();
            formData.append('taskId', task[0]);
            displayLoading()
            fetch('/deletetask', {
                method: 'DELETE',
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success === 'true') {
                        hideLoading()
                        showMessage(data.message, data.success === 'true');
                    } else {
                        hideLoading()
                        showMessage(data.message, data.success === 'true');
                    }
                    setTimeout(function() {
                        location.reload();
                    }, 1000);

                })
            $('#deleteTaskModal').modal('hide');
        });

        $('#deleteTaskModal').modal('show');
    }

    // Show messages in modal
    function showMessage(message, isSuccess) {
        var modalBody = document.getElementById("messageModalBody");
        var modalTitle = document.getElementById("messageModalTitle");

        modalBody.innerHTML = `<p class="${isSuccess ? 'text-success' : 'text-danger'}">${message}</p>`;
        modalTitle.innerHTML = isSuccess ? 'Success' : 'Error';

        $('#messageModal').modal('show');
    }

    // Display loading spinner
    function displayLoading() {
        loader.classList.add("display");
    }

    // Hide loading spinner
    function hideLoading() {
        loader.classList.remove("display");
    }

    // Initial fetch of tasks when the page loads
    fetchTasks();

});
