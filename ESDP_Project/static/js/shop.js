$(document).ready(function() {
    $('.carousel-control-next').on('click', function() {
        $('.carousel').carousel('pause');
    });

    $('.carousel-control-prev').on('click', function() {
        $('.carousel').carousel('pause');
    });

    let deleteForm;

    $('.delete-btn').click(function() {
        deleteForm = $(this).closest('form');
        $('#deleteConfirmModal').modal('show');
    });

    $('#confirmDelete').click(function() {
        deleteForm.submit();
    });
});
