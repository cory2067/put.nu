function read_file (f) {
    if (!f.length) {
        return;
    }

    var formData = new FormData();
    formData.append("file", f[0], f[0].name);
    formData.append("duration", "a LONG time"); //testing
    $('.text-container').hide();

    $.ajax({
        url: '/upload',
        data: formData,
        type: 'POST',
        contentType: false,
        processData: false,
        success: function(resp) {
            $("main").html(resp);
        },
        xhr: function(resp) {
            var xhr = $.ajaxSettings.xhr();
            xhr.upload.onprogress = function (e) {
                // upload progress
                if (e.lengthComputable) {
                    var percent = 100 * e.loaded / e.total;
                    $('#progress').css('width', percent + '%');
                    console.log(percent);
                }
            };
       return xhr;
        }
    });
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
    });

    $("#login-submit").click(function() {
        $("#login-user").removeClass("is-invalid");
        $("#login-password").removeClass("is-invalid");

        var login = {
            username: $("#login-user").val(),
            password: $("#login-password").val()
        };

        $.post("/login", login, function (resp) {
            if (resp.success) {
                $("#login-modal").modal("hide");
                $("#guest-controls").hide();
                $("#user-controls").fadeIn();
            } else {
                $(resp.error).addClass("is-invalid");
            }
        });
    });

    $("#register-start").click(function() {
        $("#login-modal").modal("hide");
        $("#register-modal").modal("show");
    });

    $("#register-submit").click(function() {
        $("#register-user").removeClass("is-invalid");
        $("#register-password").removeClass("is-invalid");
        $("#register-confirm").removeClass("is-invalid");

        if ($("#register-password").val() !== $("#register-confirm").val()) {
            $("#register-confirm").addClass("is-invalid");
            return; // Passwords don't match
        }

        var login = {
            username: $("#register-user").val(),
            password: $("#register-password").val()
        };

        $.post("/create_account", login, function (resp) {
            if (resp.success) {
                $("#register-modal").modal("hide");
                $("#guest-controls").hide();
                $("#user-controls").fadeIn();
            } else {
                $(resp.error).addClass("is-invalid");
            }
        });
    });

    setTimeout(function() {
        $('.flash-msg').slideUp();
    }, 1250);
});
