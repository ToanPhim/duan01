function changeLink() {
    var inputLink = document.getElementById("linkInput").value;
    var modifiedLink = inputLink.replace("/lh3.googleusercontent.com/", "/1.bp.blogspot.com/")
                                 .replace("h120", "s16000");
    document.getElementById("result").innerText = modifiedLink;
}


function copylink() {
    var copyText = document.getElementById("result");
    navigator.clipboard.writeText(copyText.value);
    alert("Đã copy thành công!");
}

