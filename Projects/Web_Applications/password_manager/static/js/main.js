document.getElementById('generateForm').addEventListener('submit', function (event) {
    event.preventDefault();
    let length = document.getElementById('length').value;
    
    fetch('/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `length=${length}`
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('generatedPassword').style.display = 'block';
        document.getElementById('generatedPassword').innerHTML = `<b>Generated Password:</b> ${data.password}`;
    });
});

document.getElementById('retrieveForm').addEventListener('submit', function (event) {
    event.preventDefault();
    let service = document.getElementById('serviceRetrieve').value;
    
    fetch('/retrieve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `service=${service}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.password) {
            document.getElementById('retrievedPassword').style.display = 'block';
            document.getElementById('retrievedPassword').innerHTML = `<b>Password for ${service}:</b> ${data.password}`;
        } else {
            document.getElementById('retrievedPassword').style.display = 'block';
            document.getElementById('retrievedPassword').innerHTML = data.error;
        }
    });
});
