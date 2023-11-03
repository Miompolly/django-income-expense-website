const usernameField = document.querySelector("#usernameField");
const feedbackArea=document.querySelector(".invalid_feedback");
const emailField=document.querySelector("#emailField");
const emailfeedbackArea=document.querySelector('.emailfeedbackArea')
const usernameSuccessOutput=document.querySelector('.usernameSuccessOutput')
const showPasswordToggle=document.querySelector('.showPasswordToggle')
const passwordField=document.querySelector('#passwordField')
const submitBtn=document.querySelector('.submitBtn')




const showPasswordToggleInput=(e)=>{
    if(showPasswordToggle.textContent==="SHOW"){
        showPasswordToggle.textContent="HIDE";
        passwordField.setAttribute('type','text');
    }else{
        showPasswordToggle.textContent="SHOW";
        passwordField.setAttribute('type','password')
    }
}

showPasswordToggle.addEventListener('click',showPasswordToggleInput)


emailField.addEventListener('keyup',(e)=>{
    const emailVal = e.target.value;
    emailField.classList.remove("is-invalid");
    emailfeedbackArea.style.display="none"

    if (emailVal.length > 0) {
        fetch("/authentication/validate-email", {
            body: JSON.stringify({ email: emailVal }),
            method: "POST",
            // headers: {
            //     'Content-Type': 'application/json'
            // },
        })
        .then((res) =>res.json())
     
        .then((data) => {
            console.log("data", data);
            if (data.email_error) {
                emailField.classList.add("is-invalid");
                submitBtn.disabled=true;
                emailfeedbackArea.style.display='block';
                emailfeedbackArea.innerHTML=`<p>${data.email_error}</p>`
            }else{
                submitBtn.removeAttribute("disabled")
            }
        })
     

    }
})





usernameField.addEventListener('keyup', (e) => {
    const usernameVal = e.target.value;
    console.log(usernameVal);
    usernameField.classList.remove("is-invalid");
    feedbackArea.style.display="none";
    usernameSuccessOutput.style.display='block';
    usernameSuccessOutput.textContent=`Checking ${usernameVal}`;
    



    if (usernameVal.length > 0) {
        fetch("/authentication/validate-username", {
            body: JSON.stringify({ username: usernameVal }),
            method: "POST",
            // headers: {
            //     'Content-Type': 'application/json'
            // },
        })
        .then((res) =>res.json())
     
        .then((data) => {
            console.log("data", data);
            if (data.username_error) {
                usernameField.classList.add("is-invalid");
                submitBtn.disabled=true;
                feedbackArea.style.display='block';
                feedbackArea.innerHTML=`<p>${data.username_error}</p>`
                usernameSuccessOutput.style.display='none'
            }else{
                submitBtn.removeAttribute("disabled")
            }
        })
     

    }
});
