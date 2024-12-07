let currentInput = ""; // This holds the current input from the user

// Function to handle button clicks
function press(value) {
    currentInput += value;  // Append the clicked value to the current input
    document.getElementById("calc-screen").value = currentInput; // Display the current input
}

// Function to clear the calculator screen
function clearCalc() {
    currentInput = "";  // Clear the current input
    document.getElementById("calc-screen").value = currentInput;  // Update the screen
}

// Function to calculate the result
function calculate() {
    try {
        currentInput = eval(currentInput).toString();  // Use eval to compute the expression
        document.getElementById("calc-screen").value = currentInput;  // Display the result
    } catch (error) {
        document.getElementById("calc-screen").value = "Error";  // If there's an error, display 'Error'
    }
}
