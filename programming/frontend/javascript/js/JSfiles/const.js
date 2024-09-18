//  const is a keyword used to declare constants,
// which are variables whose values cannot be reassigned.
// Understanding how const works is crucial for writing robust and maintainable code.
// In this comprehensive tutorial,
// we will explore the nuances of const and learn how to use it effectively in various scenarios.

// const is used to declare variables in JavaScript that are constant,
// meaning their values cannot be reassigned once they are initialized.
// However, it's essential to understand that const does
// not make the variable's value immutable. It only prevents reassignment of the variable itself.

const PI = 3.14;
// PI = 3.14159; // This will throw an error

// Similar to `let`, variables declared with `const` are block-scoped,
// meaning they are only accessible within the block they are defined in.

{
    const message = "Hello";
    console.log(message); // output: hello
}

// console.log(message); // Error: message is not defined

// constant objects and arrays
// when declaring a constant object or array using 'const' ,  the variable
// cannot be reassigned to a new object or array. However, the properties
// or elements of the object or array can be modified.

const person = {
    name: "John",
    age: 30
};

person,age = 31; // Valid, as it modifies the property of the object
// person = { name: "Jane", age: 25 }; // Error: Assignment to constant variable

const numbers = [1, 2, 3];
numbers.push(4); //valid, as it modifies the array
// numbers = [1, 2, 3, 4]; // Error: Assignment to constant variable

// Step 5: Best Practices
// - Use `const` for values that should not be reassigned.
// - When dealing with objects or arrays, consider whether the properties
//   or elements will need to be reassigned. If not, use `const`.
// - Avoid using `const` for primitive values if you anticipate reassigning
//   them, as it might lead to confusion.

// Step 6: Conclusion
// In JavaScript, `const` provides a way to declare constants, ensuring
// that values remain unchanged throughout the program. By understanding
// its behavior and best practices, you can write more reliable and
// maintainable code.
