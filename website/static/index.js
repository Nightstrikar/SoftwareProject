

function deleteNote(noteId) {
    fetch('/delete-note',{
        method: "POST",
        body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
        window.location.href = "/";
    });
}

function deleteTask(taskId){
    fetch('/delete-task',{
        method: "POST",
        body: JSON.stringify({ taskId: taskId }),
    }).then((_res) => {
        window.location.href = "/todo";
    });
};

function updateTask(taskId){
    fetch('/update-task',{
        method: "POST",
        body: JSON.stringify({ taskId: taskId}),
    }).then((_res) => {
        window.location.href = "/todo"
    });
}







