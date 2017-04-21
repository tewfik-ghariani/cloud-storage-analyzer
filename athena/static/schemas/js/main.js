// Handle radio buttons on config page
$('.xtra').click(function () {
    if (this.value == 'xtra') {
        $('#which1')[0].disabled = false;
        $('#which2')[0].disabled = false;
    }
    else {
        $('#which1')[0].disabled = true;
        $('#which2')[0].disabled = true;
    }
});

