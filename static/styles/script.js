const video = document.querySelector("video");
if (window.matchMedia('(prefers-reduced-motion)').matches) {
  video.removeAttribute("autoplay");
  video.pause();
}


function addNumber() {

    link = "https://jordans-jams.herokuapp.com/addFromWeb/"

    var phoneNumber = document.getElementById('phone').value
    var fullNum = "+1" + phoneNumber

    link += String(fullNum)

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", link, true);
    xhttp.send();

    document.getElementById('phone').value = " "
    alert("Thank's for signing up for Jordan's Jams. Hope you enjoy!")
}


