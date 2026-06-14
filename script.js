const uploadBtn = document.getElementById("videoUpload");

uploadBtn.addEventListener("change", function () {
    const file = this.files[0];

    if (file) {
        alert("Video Uploaded: " + file.name);

        const video = document.createElement("video");
        video.src = URL.createObjectURL(file);
        video.controls = true;
        video.width = 400;

        document.body.appendChild(video);
    }
});