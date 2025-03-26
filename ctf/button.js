frappe.ready(function() {
    frappe.realtime.connect(); // TODO: obfuscate this in some random code
})


function triger_button() {
    frappe.xcall("ctf.api.stage.the_button_pressed")
}

let timeLeft = 60;
let interval;

const timerElement = document.getElementById("the_timer");
const buttonElement = document.getElementById("the_button");

function updateTimer() {
	if (timeLeft > 0) {
		timeLeft--;
		timerElement.textContent = `${timeLeft}`;
	} else {
		frappe.xcall("ctf.api.stage.the_button_not_pressed");
		buttonElement.className = `btn ${getColor(timeLeft)}`;
		clearInterval(interval);
	}
}

function getColor(time) {
	if (time >= 40) return "btn-default";
	if (time >= 10) return "btn-danger";
	return "btn-secondary";
}

function resetExperiment() {
	timeLeft = 60;
	buttonElement.disabled = false;
	buttonElement.className = "btn btn-primary";
	timerElement.textContent = `${timeLeft}`;
	clearInterval(interval);
	interval = setInterval(updateTimer, 1000);
}

interval = setInterval(updateTimer, 1000);

buttonElement.addEventListener("click", function () {
	buttonElement.className = `btn ${getColor(timeLeft)}`;
	buttonElement.disabled = true;
	setTimeout(resetExperiment, 2500);
});
