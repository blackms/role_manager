let timers = {};

function formatRoleId(role) {
    return role.replace(/ /g, '_');
}

function startTimer(role, duration) {
    var display = $('#time_' + formatRoleId(role));
    if (display.length === 0) return;

    if (timers[role]) {
        clearInterval(timers[role]);
    }

    var timer = duration;
    timers[role] = setInterval(function () {
        var minutes = parseInt(timer / 60, 10);
        var seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.text(minutes + ":" + seconds);

        if (--timer < 0) {
            clearInterval(timers[role]);
            display.text("00:00");
            releaseRole(role);
        }
    }, 1000);
}

function releaseRole(role) {
    $.get("/release_role/" + role, function() {
        location.reload();
    });
}

function assignRole(role) {
    $.get("/assign_role/" + role, function() {
        location.reload();
    });
}
