document.addEventListener("DOMContentLoaded", function (event) {
    function OTPInput() {
        const inputs = document.querySelectorAll('#otp > input[type=number]');
        for (let i = 0; i < inputs.length; i++) {
            inputs[i].addEventListener('keydown', function (event) {
                if (event.key === "Backspace") {
                    inputs[i].value = '';
                    if (i !== 0) inputs[i - 1].focus();
                }
                else {
                    if (i <= inputs.length - 1 && i >= 0) {
                        inputs[i].value = event.key;
                        if (i !== inputs.length - 1)
                            inputs[i + 1].focus();
                        event.preventDefault();
                    }
                }
            });
        }
    } OTPInput();
});
function countdown(sec=30) {
    $('#resend').addClass('disabled');
    var seconds = parseInt(sec);
    function tick() {
        var counter = document.getElementById("counter");
        seconds--;
        counter.innerHTML =
            "0:" + (seconds < 10 ? "0" : "") + String(seconds);
        if (seconds > 0) {
            setTimeout(tick, 1000);
        }
        else {
            $('#resend').removeClass('disabled')
        }
    }
    tick();
}
countdown();