const usernameField = document.querySelector("#usernameField");

usernameField.addEventListener('keyup', (e) => {
    const usernameVal = e.target.value;
    console.log(usernameVal);

    if (usernameVal.length > 0) {
        fetch("/authentication/validate-username", {
            body: JSON.stringify({ username: usernameVal }),
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then((res) => {
            if (!res.ok) {
                throw new Error('Network response was not ok');
            }
            return res.json();
        })
        .then((data) => {
            console.log("data", data);
            if (data.username_error) {
                usernameField.classList.add("is-invalid");
            }
        })
        .catch((error) => {
            console.error('Fetch error:', error);
        });
        

    }
});
