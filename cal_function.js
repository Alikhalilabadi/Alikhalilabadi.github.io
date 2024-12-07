let currentInput = "";

function press(value) {
    currentInput += value;
    document.getElementById("calc-screen").value = currentInput;
}

function clearCalc() {
    currentInput = "";
    document.getElementById("calc-screen").value = currentInput;
}

function calculate() {
    try {
        currentInput = eval(currentInput).toString();
        document.getElementById("calc-screen").value = currentInput;
    } catch (error) {
        document.getElementById("calc-screen").value = "Error";
    }
}
