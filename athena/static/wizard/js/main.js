var uniqueId = 1;
$("#add_column").click(function () {

    var col = $("#one_column").clone().appendTo($("#columns"));
    var columnDivId = 'column_' + uniqueId;
    col.attr('id', columnDivId);
    col.find('#column_label').val('');

    var deleteLink = $('<span class="btn btn-danger btn-xs"><i class="glyphicon glyphicon-trash"></i></span>');
    deleteLink.appendTo(col);
    deleteLink.click(function () {
        col.remove();
    });
    uniqueId++;

});
