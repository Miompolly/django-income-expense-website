const searchField=document.querySelector("#searchField")


searchField.addEventListener('keyup',e=>{
    const searchValue=e.target.value
    if(searchValue.length>0){
        console.log(searchValue)

        fetch("/authentication/validate-email", {
            body: JSON.stringify({ email: emailVal }),
            method: "POST",
           
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