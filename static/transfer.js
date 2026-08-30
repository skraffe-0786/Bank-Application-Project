let btn= document.getElementById("search")
console.log(btn)
btn.onclick=e=>{
    let acc1=document.getElementById("too_account").value
    console.log("Entered account:",acc1)
    if(acc1 == ""){
        alert("Please enter acccount number");
        return;
    }
    fetch('recv_acc',{
        method:"POST",
        body:JSON.stringify({
            accountnumber:acc1
        })
    })
    .then(res =>{
        console.log("Response status:",res.status);
        return res.json();
    })
    .then(data => {
        console.log(data);
        if (data.success){
            document.getElementById("receiver_name").innerText
             
            "Account Holder:" +data.username.Current_Balance;
        }
        else{
            document.getElementById("receiver_name").innerText

            "Account not found";
        }
    })
    .catch(error => console.log("Error",error))
}
