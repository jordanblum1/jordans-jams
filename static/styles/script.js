const video = document.querySelector("video");
if (window.matchMedia('(prefers-reduced-motion)').matches) {
  video.removeAttribute("autoplay");
  video.pause();
}

function isValid(number) {
    var phoneRegEx = /^[2-9]\d{2}[2-9]\d{2}\d{4}$/;
    var digits = number.replace(/\D/g, "");
    return phoneRegEx.test(digits);
  }


function addNumber() {

    link = "https://jordans-jams.herokuapp.com/addFromWeb/";
    var phoneNumber = document.getElementById('phone').value;

    if(isValid(phoneNumber) && phoneNumber.length >= 10){
        number = phoneNumber.replace(/\D/g, "");

        var fullNum = "+1" + number;

        link += String(fullNum);

        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", link, true);
        xhttp.send();

        document.getElementById('phone').value = "";
        alert("You have successfully signed up for Jordan's Jams");
    }
    else{
        alert("The phone number you have entered is invalid. Please try again.");
    }
}


