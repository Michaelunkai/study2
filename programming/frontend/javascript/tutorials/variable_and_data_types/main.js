// a variable is container for storing data
// a variable behaves as if it was the value that it contains

// two steps:
// 1. Declaration (var, let, const)
// 2. Assignment (= assignment operator)

// let age;
// age = 21;
// or:
// let age = 21;
// age = age +1;

// string:

// let firstName = "Misha"
// let age = 21;

// boolean:


// Declare variables
let firstName = "Misha"; // strings
let age = 21; // numbers
let student = false; // booleans

// Output to console
console.log("Hello", firstName);
console.log("You Are", age, "years old");
console.log("Enrolled", student);

// Output to HTML
document.getElementById("p1").innerHTML = `Hello ${firstName}`;
document.getElementById("p2").innerHTML = `You are ${age} years old`;
document.getElementById("p3").innerHTML = `Enrolled: ${student}`;
