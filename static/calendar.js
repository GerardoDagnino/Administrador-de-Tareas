document.addEventListener('DOMContentLoaded', function () {
    // Inicializar FullCalendar
    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        defaultView: 'month',
        editable: true,
        events: '/events'
    });

    // Configurar el formulario de tareas
    $('#add-task-btn').on('click', function () {
        const selectedDate = $('#calendar').fullCalendar('getDate').format('YYYY-MM-DD');
        const taskTitle = $('#task-title').val();

        // Enviar la tarea al servidor
        $.ajax({
            url: '/admin/add_task',
            type: 'POST',
            data: {
                date: selectedDate,
                title: taskTitle
            },
            success: function (response) {
                // Recargar eventos después de agregar la tarea
                $('#calendar').fullCalendar('refetchEvents');
                // Otros manejadores de éxito
            },
            error: function (error) {
                console.error('Error al agregar tarea:', error);
            }
        });
    });
});