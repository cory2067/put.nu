function read_file (f) {
    if (!f.length) {
        return;
    }

    // now do something with file
}

$(function() {
    $('[data-toggle="tooltip"]').tooltip()

    $(".bigtext, .smalltext").on("mousedown", function(e) {
        // User shouldn't interact with(accidentally select) the text
        e.preventDefault();
    });

    $("main").dblclick(function() {
        $("#file-upload").click();
    });

    $("#file-upload").change(function() {
        read_files(this.files);
    })
});
