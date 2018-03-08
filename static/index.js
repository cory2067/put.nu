function read_file (f) {
    if (!f.length) {
        return;
    }

    //https://github.com/blueimp/jQuery-File-Upload
    console.log(f[0]);
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
        read_file(this.files);
    })

    setTimeout(function() {
        $('.flash-msg').slideUp();
    }, 1250);
});
