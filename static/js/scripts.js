function startTimer(role, duration) {
    var display = document.getElementById('time_' + role);
    if (!display) {
        console.error('Element not found for role:', role);
        return;
    }
    var timer = duration, minutes, seconds;

    var interval = setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            clearInterval(interval);
            releaseRole(role);
        }
    }, 1000);
}

function releaseRole(role) {
    $.get('/release_role/' + role.replace('_', ' '), function(data) {
        location.reload();
    });
}

function assignRole(role) {
    $.get('/assign_role/' + role.replace('_', ' '), function(data) {
        var startTime = new Date(data.assign_time);
        var now = new Date();
        var elapsed = Math.floor((now - startTime) / 1000);
        var remaining = 300 - elapsed; // 5 minutes (300 seconds)
        startTimer(role, remaining);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    var requestRoleButton = document.getElementById('request-role-button');
    var playerNameField = document.getElementById('player');

    if (requestRoleButton) {
        requestRoleButton.addEventListener('click', function(event) {
            if (!validatePlayerName()) {
                event.preventDefault();
            }
        });
    }

    if (playerNameField) {
        playerNameField.addEventListener('input', function() {
            playerNameField.classList.remove('invalid');
            document.getElementById('player-error').style.display = 'none';
        });
    }
});

function validatePlayerName() {
    var playerNameField = document.getElementById('player');
    var playerName = playerNameField.value;
    var allianceTagPattern = /^\[.+\].+$/;
    var errorMessage = document.getElementById('player-error');

    if (!allianceTagPattern.test(playerName)) {
        playerNameField.classList.add('invalid');
        errorMessage.style.display = 'block';
        return false;
    } else {
        playerNameField.classList.remove('invalid');
        errorMessage.style.display = 'none';
        return true;
    }
}
