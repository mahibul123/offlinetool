
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles


import uvicorn
import shutil
import os
import subprocess
import math
import uuid

# =========================================================
# APP CONFIG
# =========================================================

app = FastAPI()
app.mount("/static", StaticFiles(directory="."), name="static")
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

# =========================================================
# HTML UI
# =========================================================

HTML = """

<!DOCTYPE html>
<html>

<head>

<title>Reelsnip.com</title>

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>

*{
margin:0;
padding:0;
box-sizing:border-box;
}

body{
background:#0f172a;
font-family:Arial;
color:white;
overflow:hidden;
}

.main{
display:flex;
height:100vh;
}

.sidebar{
width:260px;
background:#111827;
padding:20px;
overflow-y:auto;
border-right:2px solid #1e293b;
}

.logo{
font-size:32px;
font-weight:bold;
margin-bottom:30px;
color:#60a5fa;
}

.sidebar h2{
margin-bottom:20px;
font-size:18px;
}

.tool-btn{
width:100%;
padding:15px;
margin-bottom:12px;
background:#1e293b;
border:none;
color:white;
border-radius:14px;
font-size:16px;
cursor:pointer;
text-align:left;
transition:0.3s;
}

.tool-btn:hover{
background:#2563eb;
}

.content{
flex:1;
overflow-y:auto;
padding:25px;
}

.card{
background:#1e293b;
padding:22px;
border-radius:20px;
margin-bottom:25px;
}

input,
select{
width:100%;
padding:13px;
margin-top:10px;
margin-bottom:18px;
border:none;
border-radius:10px;
font-size:15px;
background:#0f172a;
color:white;
}

button.process{
width:100%;
padding:15px;
background:#2563eb;
color:white;
border:none;
border-radius:12px;
font-size:17px;
cursor:pointer;
font-weight:bold;
}

button.process:hover{
background:#1d4ed8;
}

video{
width:120px;
height:70px;
object-fit:cover;
margin-top:8px;
border-radius:10px;
background:black;
display:block;
}

#preview{
width:170px;
height:100px;
margin-top:15px;
}

.output-card video{
width:120px;
height:70px;
}

.output-card{
background:#111827;
padding:12px;
margin-top:15px;
border-radius:15px;
display:inline-block;
width:150px;
vertical-align:top;
margin-right:10px;
text-align:center;
}

.download-btn{
display:inline-block;
padding:9px 14px;
background:#10b981;
color:white;
text-decoration:none;
border-radius:10px;
margin-top:10px;
font-weight:bold;
font-size:13px;
}

.slider-label{
margin-top:-10px;
margin-bottom:15px;
font-size:13px;
color:#cbd5e1;
}

.hidden{
display:none;
}

.flex{
display:flex;
gap:15px;
}

.loader-box{
display:none;
margin-top:20px;
padding:20px;
background:#111827;
border-radius:15px;
width:260px;
text-align:center;
}

.spinner{
width:50px;
height:50px;
border:5px solid #334155;
border-top:5px solid #60a5fa;
border-radius:50%;
animation:spin 1s linear infinite;
margin:auto;
margin-bottom:15px;
}

@keyframes spin{

0%{
transform:rotate(0deg);
}

100%{
transform:rotate(360deg);
}

}

.progress-bar{
width:100%;
height:12px;
background:#1e293b;
border-radius:20px;
overflow:hidden;
margin-top:15px;
}

#progressFill{
width:0%;
height:100%;
background:#2563eb;
transition:0.3s;
}

</style>

</head>

<body>

<div class="main">

<!-- SIDEBAR -->

<div class="sidebar">

<div class="logo">

Reelsnip.com

</div>

<h2>🎬 PRO TOOLS</h2>

<button class="tool-btn" onclick="showTool('cutter')">
✂ Video Cutter
</button>

<button class="tool-btn" onclick="showTool('shorts')">
📱 Multiple Shorts
</button>

<button class="tool-btn" onclick="showTool('compress')">
⚡ Video Compress
</button>

<button class="tool-btn" onclick="showTool('reels')">
📲 Reels Resize
</button>

<button class="tool-btn" onclick="showTool('youtube')">
▶ YouTube Resize
</button>

<button class="tool-btn" onclick="showTool('mute')">
🔇 Remove Audio
</button>

<button class="tool-btn" onclick="showTool('mp3')">
🎵 Extract MP3
</button>

<button class="tool-btn" onclick="showTool('reverse')">
🔄 Reverse Video
</button>

<button class="tool-btn" onclick="showTool('speed')">
🚀 Speed Control
</button>

</div>

<!-- CONTENT -->

<div class="content">

<h1 style="
display:flex;
align-items:center;
gap:12px;
font-size:30px;
margin-bottom:20px;
">

Ultimate Offline Video Processor

<span style="
font-size:16px;
color:#60a5fa;
font-weight:normal;
">

Made by Reelsnip.com

</span>

</h1>

<input type="file" id="videoFile">

<video id="preview" controls></video>

<!-- LOADER -->

<div id="loaderBox" class="loader-box">

<div class="spinner"></div>

<div id="progressText">

Processing Video... 0%

</div>

<div class="progress-bar">

<div id="progressFill"></div>

</div>

</div>

<!-- VIDEO CUTTER -->

<div id="cutter" class="card tool-panel">

<h2>✂ Video Cutter</h2>

<label>Start Time</label>

<input type="range" id="cutStart" min="0" max="300" value="0">

<div class="slider-label" id="cutStartLabel">
0 sec
</div>

<label>End Time</label>

<input type="range" id="cutEnd" min="1" max="300" value="30">

<div class="slider-label" id="cutEndLabel">
30 sec
</div>

<select id="quality">

<option value="1080">Full HD 1080p</option>
<option value="720">HD 720p</option>
<option value="480">NON HD 480p</option>
<option value="360">LOW 360p</option>
<option value="original">Original</option>

</select>

<button class="process" onclick="processVideo('cutter')">
🚀 Process Video
</button>

</div>

<!-- MULTIPLE SHORTS -->

<div id="shorts" class="card tool-panel hidden">

<h2>📱 Multiple Shorts</h2>

<select id="shortDuration">

<option value="15">15 Seconds</option>
<option value="30">30 Seconds</option>
<option value="60">60 Seconds</option>

</select>

<select id="shortQuality">

<option value="1080">Full HD 1080p</option>
<option value="720" selected>HD 720p (Medium)</option>
<option value="480">NON HD 480p</option>
<option value="360">LOW 360p</option>
<option value="original">Original</option>

</select>

<button class="process" onclick="processVideo('shorts')">
🚀 Create Shorts
</button>

</div>

<!-- COMPRESS -->

<div id="compress" class="card tool-panel hidden">

<h2>⚡ Video Compress</h2>

<select id="compressLevel">

<option value="23">Low Compression</option>
<option value="30">Medium Compression</option>
<option value="38">High Compression</option>

</select>

<button class="process" onclick="processVideo('compress')">
🚀 Compress Video
</button>

</div>

<!-- REELS -->

<div id="reels" class="card tool-panel hidden">

<h2>📲 Reels Resize 9:16</h2>

<button class="process" onclick="processVideo('reels')">
🚀 Convert Reels
</button>

</div>

<!-- YOUTUBE -->

<div id="youtube" class="card tool-panel hidden">

<h2>▶ YouTube Resize 16:9</h2>

<button class="process" onclick="processVideo('youtube')">
🚀 Convert YouTube
</button>

</div>

<!-- REMOVE AUDIO -->

<div id="mute" class="card tool-panel hidden">

<h2>🔇 Remove Audio</h2>

<button class="process" onclick="processVideo('mute')">
🚀 Remove Audio
</button>

</div>

<!-- MP3 -->

<div id="mp3" class="card tool-panel hidden">

<h2>🎵 Extract MP3</h2>

<button class="process" onclick="processVideo('mp3')">
🚀 Extract MP3
</button>

</div>

<!-- REVERSE -->

<div id="reverse" class="card tool-panel hidden">

<h2>🔄 Reverse Video</h2>

<button class="process" onclick="processVideo('reverse')">
🚀 Reverse Video
</button>

</div>

<!-- SPEED -->

<div id="speed" class="card tool-panel hidden">

<h2>🚀 Speed Control</h2>

<select id="speedValue">

<option value="0.5">0.5x Slow</option>
<option value="1">1x Normal</option>
<option value="2">2x Fast</option>

</select>

<button class="process" onclick="processVideo('speed')">
🚀 Change Speed
</button>

</div>

<!-- RESULTS -->

<div id="results"></div>

</div>

</div>

<script>

const preview = document.getElementById("preview")
const videoInput = document.getElementById("videoFile")

videoInput.onchange = () => {

const file = videoInput.files[0]

preview.src = URL.createObjectURL(file)

}

function showTool(toolId){

document.querySelectorAll(".tool-panel").forEach(panel=>{

panel.classList.add("hidden")

})

document.getElementById(toolId).classList.remove("hidden")

}

document.getElementById("cutStart").oninput = function(){

document.getElementById("cutStartLabel").innerText =
this.value + " sec"

}

document.getElementById("cutEnd").oninput = function(){

document.getElementById("cutEndLabel").innerText =
this.value + " sec"

}

async function processVideo(tool){

const file = videoInput.files[0]

if(!file){

alert("Select Video First")

return

}

const loaderBox =
document.getElementById("loaderBox")

loaderBox.style.display = "block"

const progressFill =
document.getElementById("progressFill")

const progressText =
document.getElementById("progressText")

let progress = 0

const interval = setInterval(()=>{

if(progress < 90){

progress += 10

progressFill.style.width =
progress + "%"

progressText.innerText =
"Processing Video... " + progress + "%"

}

},500)

const formData = new FormData()

formData.append("video", file)
formData.append("tool", tool)

formData.append("start",
document.getElementById("cutStart")?.value || 0)

formData.append("end",
document.getElementById("cutEnd")?.value || 30)

formData.append("quality",
document.getElementById("quality")?.value || "720")

formData.append("short_duration",
document.getElementById("shortDuration")?.value || "30")

formData.append("short_quality",
document.getElementById("shortQuality")?.value || "720")

formData.append("compress_level",
document.getElementById("compressLevel")?.value || "30")

formData.append("speed",
document.getElementById("speedValue")?.value || "1")

const response = await fetch("/process", {

method:"POST",
body:formData

})

const data = await response.json()

clearInterval(interval)

progressFill.style.width = "100%"

progressText.innerText =
"Processing Complete 100%"

setTimeout(()=>{

loaderBox.style.display = "none"

},1000)

const results = document.getElementById("results")

results.innerHTML = ""

data.files.forEach(file=>{

results.innerHTML += `

<div class="output-card">

<h4>${file.name}</h4>

${file.url.endsWith(".mp3")
? `<audio controls src="${file.url}"></audio>`
: `<video controls src="${file.url}"></video>`}

<br>

<a class="download-btn"
href="${file.url}" download>

⬇ Download

</a>

</div>

`

})

}

</script>

</body>

</html>

"""

# =========================================================
# HOME
# =========================================================

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML

# =========================================================
# PROCESS VIDEO
# =========================================================

@app.post("/process")
async def process_video(
    video: UploadFile = File(...),
    tool: str = Form(...),
    start: int = Form(0),
    end: int = Form(30),
    quality: str = Form("720"),
    short_duration: int = Form(30),
    short_quality: str = Form("720"),
    compress_level: int = Form(30),
    speed: float = Form(1)
):

    uid = str(uuid.uuid4())

    input_path = f"{UPLOAD_FOLDER}/{uid}_{video.filename}"

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    output_files = []

    def add_output(name):
        output_files.append({
            "name": name,
            "url": f"/outputs/{name}"
        })

    # VIDEO CUTTER

    if tool == "cutter":

        output_name = f"{uid}_cut.mp4"

        subprocess.run([
            "ffmpeg","-i",input_path,
            "-ss",str(start),
            "-to",str(end),
            "-preset","ultrafast",
            f"{OUTPUT_FOLDER}/{output_name}",
            "-y"
        ])

        add_output(output_name)

    # MULTIPLE SHORTS

    elif tool == "shorts":

        total_duration = 180

        parts = math.ceil(
            total_duration / short_duration
        )

        for i in range(parts):

            ss = i * short_duration

            output_name = f"{uid}_short_{i+1}.mp4"

            subprocess.run([
                "ffmpeg","-i",input_path,
                "-ss",str(ss),
                "-t",str(short_duration),
                "-preset","ultrafast",
                f"{OUTPUT_FOLDER}/{output_name}",
                "-y"
            ])

            add_output(output_name)

    # VIDEO COMPRESS

    elif tool == "compress":

        output_name = f"{uid}_compress.mp4"

        subprocess.run([
            "ffmpeg","-i",input_path,
            "-vcodec","libx264",
            "-crf",str(compress_level),
            f"{OUTPUT_FOLDER}/{output_name}",
            "-y"
        ])

        add_output(output_name)

    # REELS

    elif tool == "reels":

        output_name = f"{uid}_reels.mp4"

        subprocess.run([
            "ffmpeg","-i",input_path,
            "-vf","scale=1080:1920",
            f"{OUTPUT_FOLDER}/{output_name}",
            "-y"
        ])

        add_output(output_name)

    # YOUTUBE

    elif tool == "youtube":

        output_name = f"{uid}_youtube.mp4"

        subprocess.run([
            "ffmpeg","-i",input_path,
            "-vf","scale=1920:1080",
            f"{OUTPUT_FOLDER}/{output_name}",
            "-y"
        ])

        add_output(output_name)

    # REMOVE AUDIO

    elif tool == "mute":

        output_name = f"{uid}_mute.mp4"

        subprocess.run([
            "ffmpeg","-i",input_path,
            "-an",
            f"{OUTPUT_FOLDER}/{output_name}",
            "-y"
        ])

        add_output(output_name)

    # MP3

    elif tool == "mp3":

        output_name = f"{uid}.mp3"

        subprocess.run([
            "ffmpeg","-i",input_path,
            "-q:a","0",
            "-map","a",
            f"{OUTPUT_FOLDER}/{output_name}",
            "-y"
        ])

        add_output(output_name)

    # REVERSE

    elif tool == "reverse":

        output_name = f"{uid}_reverse.mp4"

        subprocess.run([
            "ffmpeg","-i",input_path,
            "-vf","reverse",
            "-af","areverse",
            f"{OUTPUT_FOLDER}/{output_name}",
            "-y"
        ])

        add_output(output_name)

    # SPEED

    elif tool == "speed":

        output_name = f"{uid}_speed.mp4"

        pts = 1 / speed

        subprocess.run([
            "ffmpeg","-i",input_path,
            "-filter:v",f"setpts={pts}*PTS",
            f"{OUTPUT_FOLDER}/{output_name}",
            "-y"
        ])

        add_output(output_name)

    return JSONResponse({
        "files": output_files
    })

# =========================================================
# RUN APP
# =========================================================

if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8000)