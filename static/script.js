// let qrCount = 1;

// function showMessage(text, type = 'info') {
//     const msg = document.getElementById('message');
//     msg.className = `alert alert-${type}`;
//     msg.textContent = text;
//     msg.style.display = 'block';
//     setTimeout(() => msg.style.display = 'none', 4000);
// }

// async function getAccurateLocation(timeout = 10000) {
//     return new Promise((resolve, reject) => {
//         if (!navigator.geolocation) {
//             showMessage('GPS not supported.', 'warning');
//             return reject('GPS not supported');
//         }

//         const timer = setTimeout(() => {
//             showMessage('GPS timeout. Try again outdoors.', 'danger');
//             reject('Timeout');
//         }, timeout);

//         navigator.geolocation.getCurrentPosition(
//             async pos => {
//                 clearTimeout(timer);
//                 const lat = pos.coords.latitude;
//                 const lon = pos.coords.longitude;
//                 try {
//                     const response = await fetch(`https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json`, {
//                         headers: {
//                             'User-Agent': 'QR-WalkTracker-App/1.0'
//                         }
//                     });
//                     const data = await response.json();
//                     resolve({ coords: `${lat}, ${lon}`, address: data.display_name });
//                 } catch (e) {
//                     resolve({ coords: `${lat}, ${lon}`, address: `${lat}, ${lon}` });
//                 }
//             },
//             err => {
//                 clearTimeout(timer);
//                 console.error('GPS error:', err);
//                 showMessage('Unable to get GPS location.', 'danger');
//                 reject(err);
//             },
//             { enableHighAccuracy: true, timeout: timeout, maximumAge: 0 }
//         );
//     });
// }

// async function startWalk() {
//     const res = await fetch('/start', { method: 'POST' });
//     const data = await res.json();
//     if (res.ok && data.status === 'started') {
//         showMessage(`Walk started at: ${data.start_time}`, 'success');
//     } else {
//         showMessage(data.message || 'Failed to start walk.', 'danger');
//     }
// }

// async function scanQR() {
//     try {
//         const html5QrCode = new Html5Qrcode("reader");
//         document.getElementById("reader").style.display = "block";

//         await html5QrCode.start(
//             { facingMode: "environment" },
//             { fps: 10, qrbox: 250 },
//             async (decodedText) => {
//                 await html5QrCode.stop();
//                 document.getElementById("reader").style.display = "none";

//                 const { coords, address } = await getAccurateLocation();
//                 const scan_time = new Date().toLocaleString();

//                 const response = await fetch('/scan', {
//                     method: 'POST',
//                     headers: { 'Content-Type': 'application/json' },
//                     body: JSON.stringify({
//                         scan_time,
//                         gps: coords,
//                         address,
//                         qr_text: decodedText
//                     })
//                 });

//                 const result = await response.json();
//                 if (response.ok && result.status === 'success') {
//                     showMessage(`QR ${qrCount++} scanned.`, 'success');
//                 } else {
//                     showMessage('Failed to save scan.', 'danger');
//                 }
//             }
//         );
//     } catch (err) {
//         console.error('QR scan failed:', err);
//         showMessage('Error during QR scan.', 'danger');
//     }
// }

// async function submitWalk() {
//     const res = await fetch('/submit', { method: 'POST' });
//     const data = await res.json();
//     if (res.ok && data.status === 'submitted') {
//         showMessage('Walk submitted and emailed.', 'success');
//         qrCount = 1;
//     } else {
//         showMessage('Submission failed.', 'danger');
//     }
// }
///---------------------------------NEW VERSION -----------------------------------------------

// let qrCount = 1;

// // ✅ Updated QR-specific checklist questions with some pairs
// const allowedQRs = {
//     "BPCL Admin Building": [
//         ["Oil Leakage", "Encroachment"],
//         ["Fire Incident", "Missing of Boundary pillars"],
//         ["Wastages/Plastic bins", "Grass Cutting"],
//         ["Removal of trees/branches", "Filling of earth hole"],
//         ["Replacement/Repairing of Warning boards"],
//         ["Checking of Cattles", "TLP Box"]
//     ],
//     "BPCL Entry Gate": [
//         ["Oil Leakage", "Encroachment"],
//         ["Dumping of Rail Sleepers, M/Sand Metal etc."],
//         ["Removal of trees/branches", "Grass Cutting"],
//         ["Pipeline protection net, Door & lock"]
//     ],
//     "BPCL Admin Annex Building": [
//         ["Oil Leakage", "Encroachment"],
//         ["Removal of 03 X boundary pillars named 'SR' placed by the Railway"],
//         ["Visibility of boundary pillars", "Grass Cutting"],
//         ["Wastages/Plastic bins", "Missing of Boundary pillars"],
//         ["Cultivation of Banana trees/vegetables etc."],
//         ["Repair/replacement of warning boards", "TLP Box"],
//         ["Pipeline protection net, Door & lock at Canal Crossing No 1, Error"]
//     ],
//     "T p r Business plaza": [
//         ["Oil Leakage", "Encroachment"],
//         ["Dumping of house construction materials."],
//         ["Wastages/Plastic bins", "Fire Incident"],
//         ["TLP Box", "Repair / Replacement of Warning boards"],
//         ["Cultivation of Banana trees/vegetables etc."],
//         ["Removal of trees branches", "Missing of Boundary pillars"],
//         ["Pipeline protection net, Door & lock at Kaniyampuzha"],
//         ["Removal of concrete pipe dumped on the pipeline"]
//     ]
// };

// let currentQRCode = "";

// function showMessage(text, type = 'info') {
//     const msg = document.getElementById('message');
//     msg.className = `alert alert-${type}`;
//     msg.textContent = text;
//     msg.style.display = 'block';
//     setTimeout(() => msg.style.display = 'none', 4000);
// }

// async function getAccurateLocation(timeout = 10000) {
//     return new Promise((resolve, reject) => {
//         if (!navigator.geolocation) {
//             showMessage('GPS not supported.', 'warning');
//             return reject('GPS not supported');
//         }

//         const timer = setTimeout(() => {
//             showMessage('GPS timeout. Try again outdoors.', 'danger');
//             reject('Timeout');
//         }, timeout);

//         navigator.geolocation.getCurrentPosition(
//             async pos => {
//                 clearTimeout(timer);
//                 const lat = pos.coords.latitude;
//                 const lon = pos.coords.longitude;
//                 try {
//                     const response = await fetch(`https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json`, {
//                         headers: {
//                             'User-Agent': 'QR-WalkTracker-App/1.0'
//                         }
//                     });
//                     const data = await response.json();
//                     resolve({ coords: `${lat}, ${lon}`, address: data.display_name });
//                 } catch (e) {
//                     resolve({ coords: `${lat}, ${lon}`, address: `${lat}, ${lon}` });
//                 }
//             },
//             err => {
//                 clearTimeout(timer);
//                 console.error('GPS error:', err);
//                 showMessage('Unable to get GPS location.', 'danger');
//                 reject(err);
//             },
//             { enableHighAccuracy: true, timeout: timeout, maximumAge: 0 }
//         );
//     });
// }

// async function startWalk() {
//     const res = await fetch('/start', { method: 'POST' });
//     const data = await res.json();
//     if (res.ok && data.status === 'started') {
//         showMessage(`Walk started at: ${data.start_time}`, 'success');
//     } else {
//         showMessage(data.message || 'Failed to start walk.', 'danger');
//     }
// }

// async function scanQR() {
//     try {
//         const html5QrCode = new Html5Qrcode("reader");
//         document.getElementById("reader").style.display = "block";

//         await html5QrCode.start(
//             { facingMode: "environment" },
//             { fps: 10, qrbox: 250 },
//             async (decodedText) => {
//                 await html5QrCode.stop();
//                 document.getElementById("reader").style.display = "none";

//                 const { coords, address } = await getAccurateLocation();
//                 const scan_time = new Date().toLocaleString();

//                 const response = await fetch('/scan', {
//                     method: 'POST',
//                     headers: { 'Content-Type': 'application/json' },
//                     body: JSON.stringify({
//                         scan_time,
//                         gps: coords,
//                         address,
//                         qr_text: decodedText
//                     })
//                 });

//                 const result = await response.json();
//                 if (response.ok && result.status === 'success') {
//                     showMessage(`QR ${qrCount++} scanned.`, 'success');
//                     showChecklist(decodedText);
//                 } else {
//                     showMessage('Failed to save scan.', 'danger');
//                 }
//             }
//         );
//     } catch (err) {
//         console.error('QR scan failed:', err);
//         showMessage('Error during QR scan.', 'danger');
//     }
// }

// function showChecklist(qrData) {
//     const questions = allowedQRs[qrData];

//     if (!questions) {
//         showMessage("Unknown QR Code: " + qrData, "warning");
//         return;
//     }

//     currentQRCode = qrData;
//     document.getElementById("qr-label").innerText = qrData;

//     const container = document.getElementById("checklist-questions");
//     container.innerHTML = "";

//     questions.forEach((q, i) => {
//         if (Array.isArray(q)) {
//             // Row with two side-by-side checkboxes
//             container.innerHTML += `
//                 <div class="row mb-2">
//                     <div class="col-md-6">
//                         <div class="form-check text-start">
//                             <input class="form-check-input" type="checkbox" id="q${i}_1" name="questions" value="${q[0]}">
//                             <label class="form-check-label" for="q${i}_1">${q[0]}</label>
//                         </div>
//                     </div>
//                     ${q[1] ? `
//                     <div class="col-md-6">
//                         <div class="form-check text-start">
//                             <input class="form-check-input" type="checkbox" id="q${i}_2" name="questions" value="${q[1]}">
//                             <label class="form-check-label" for="q${i}_2">${q[1]}</label>
//                         </div>
//                     </div>` : ""}
//                 </div>
//             `;
//         } else {
//             // Single checklist item
//             container.innerHTML += `
//                 <div class="form-check text-start mb-2">
//                     <input class="form-check-input" type="checkbox" id="q${i}" name="questions" value="${q}">
//                     <label class="form-check-label" for="q${i}">${q}</label>
//                 </div>
//             `;
//         }
//     });

//     document.getElementById("checklist-section").style.display = "block";
// }

// document.getElementById("checklist-form").addEventListener("submit", function (e) {
//     e.preventDefault();
//     const rows = [];
//     const formGroups = document.querySelectorAll('#checklist-questions .row, #checklist-questions .form-check:not(.row *)');

//     formGroups.forEach(group => {
//         const checkboxes = group.querySelectorAll('input[type="checkbox"]:checked');
//         if (checkboxes.length === 1) {
//             rows.push(`- ${checkboxes[0].value}`);
//         } else if (checkboxes.length === 2) {
//             const left = `- ${checkboxes[0].value}`.padEnd(35);
//             const right = `- ${checkboxes[1].value}`;
//             rows.push(`${left}${right}`);
//         }
//     });

//     const formattedChecklist = rows.join("\n");
//     const qrCode = currentQRCode;

//     fetch("/submit-checklist", {
//         method: "POST",
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ qr_code: qrCode, checklist: formattedChecklist })
//     })
//     .then(res => res.json())
//     .then(data => {
//         showMessage("Checklist submitted successfully!", "success");
//         document.getElementById("checklist-section").style.display = "none";
//     })
//     .catch(err => {
//         console.error("Checklist error:", err);
//         showMessage("Error submitting checklist.", "danger");
//     });
// });

// async function submitWalk() {
//     try {
//         const res = await fetch('/submit', { method: 'POST' });
//         const data = await res.json();
//         if (res.ok && data.status === 'submitted') {
//             showMessage('Walk submitted and emailed.', 'success');
//             qrCount = 1;
//         } else {
//             console.error('Backend error:', data.message);  // Show the real backend error
//             showMessage(`Submission failed: ${data.message}`, 'danger');
//         }
//     } catch (err) {
//         console.error('Fetch error:', err);
//         showMessage(`Submission failed: ${err.message}`, 'danger');
//     }
// }

//---------------------GPS VERSION-----------------------------------------------------
let watchId = null;
let messageTimeout = null;
let hasStarted = false;
let qrCount = 1;
// ✅ Updated QR-specific checklist questions with some pairs
const allowedQRs = {
    "BPCL Admin Building": [
        ["Oil Leakage", "Encroachment"],
        ["Fire Incident", "Missing of Boundary pillars"],
        ["Wastages/Plastic bins", "Grass Cutting"],
        ["Removal of trees/branches", "Filling of earth hole"],
        ["Replacement/Repairing of Warning boards"],
        ["Checking of Cattles", "TLP Box"]
    ],
    "BPCL Entry Gate": [
        ["Oil Leakage", "Encroachment"],
        ["Dumping of Rail Sleepers, M/Sand Metal etc."],
        ["Removal of trees/branches", "Grass Cutting"],
        ["Pipeline protection net, Door & lock"]
    ],
    "BPCL Admin Annex Building": [
        ["Oil Leakage", "Encroachment"],
        ["Removal of 03 X boundary pillars named 'SR' placed by the Railway"],
        ["Visibility of boundary pillars", "Grass Cutting"],
        ["Wastages/Plastic bins", "Missing of Boundary pillars"],
        ["Cultivation of Banana trees/vegetables etc."],
        ["Repair/replacement of warning boards", "TLP Box"],
        ["Pipeline protection net, Door & lock at Canal Crossing No 1, Error"]
    ],
    "T p r Business plaza": [
        ["Oil Leakage", "Encroachment"],
        ["Dumping of house construction materials."],
        ["Wastages/Plastic bins", "Fire Incident"],
        ["TLP Box", "Repair / Replacement of Warning boards"],
        ["Cultivation of Banana trees/vegetables etc."],
        ["Removal of trees branches", "Missing of Boundary pillars"],
        ["Pipeline protection net, Door & lock at Kaniyampuzha"],
        ["Removal of concrete pipe dumped on the pipeline"]
    ]
};
let currentQRCode = "";

function showMessage(text, type = 'info') {
    const msg = document.getElementById('message');
    msg.className = `alert alert-${type}`;
    msg.textContent = text;
    msg.style.display = 'block';
    setTimeout(() => msg.style.display = 'none', 4000);
}

async function getAccurateLocation(timeout = 10000) {
    return new Promise((resolve, reject) => {
        if (!navigator.geolocation) {
            showMessage('GPS not supported.', 'warning');
            return reject('GPS not supported');
        }

        const timer = setTimeout(() => {
            showMessage('GPS timeout. Try again outdoors.', 'danger');
            reject('Timeout');
        }, timeout);

        navigator.geolocation.getCurrentPosition(
            async pos => {
                clearTimeout(timer);
                const lat = pos.coords.latitude;
                const lon = pos.coords.longitude;
                try {
                    const response = await fetch(`https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json`, {
                        headers: {
                            'User-Agent': 'QR-WalkTracker-App/1.0'
                        }
                    });
                    const data = await response.json();
                    resolve({ coords: `${lat}, ${lon}`, address: data.display_name });
                } catch (e) {
                    resolve({ coords: `${lat}, ${lon}`, address: `${lat}, ${lon}` });
                }
            },
            err => {
                clearTimeout(timer);
                console.error('GPS error:', err);
                showMessage('Unable to get GPS location.', 'danger');
                reject(err);
            },
            { enableHighAccuracy: true, timeout: timeout, maximumAge: 0 }
        );
    });
}

function showMessage(msg, type = "info", duration = 3000) {
    const messageDiv = document.getElementById('message');
    messageDiv.innerHTML = `<div class="alert alert-${type}">${msg}</div>`;

    if (messageTimeout) clearTimeout(messageTimeout);

    messageTimeout = setTimeout(() => {
        messageDiv.innerHTML = '';
    }, duration);
}

function startWalk() {
    if (!navigator.geolocation) {
        showMessage("❌ Geolocation is not supported by this browser.", "danger");
        return;
    }

    navigator.geolocation.getCurrentPosition(
        function (position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            const currentTime = new Date().toLocaleString();

            alert(`🚶 Walk started at: ${currentTime}`);
            
            fetch('/start_walk', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ lat: lat, lon: lon })
            })
                .then(res => res.json())
                .then(data => {
                    showMessage("✅ Walk started and tracking enabled.", "success");

                    hasStarted = true;
                    startTracking();  // ✅ Start watch-based tracking
                })
                .catch(err => {
                    console.error("Failed to start walk:", err);
                    showMessage("❌ Failed to start walk!", "danger");
                });
        },
        errorCallback,
        { enableHighAccuracy: true }
    );
}

function startTracking() {
    if (navigator.geolocation) {
        watchId = navigator.geolocation.watchPosition(
            (position) => {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;
                const Timestamp = new Date().toLocaleString();

                fetch('/save_location', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ latitude, longitude, Timestamp })
                })
                    .then(response => {
                        if (!response.ok) throw new Error('Network response not ok');
                        return response.json();
                    })
                    .then(data => {
                        console.log(`✅ Location saved: ${Timestamp}, ${latitude}, ${longitude}`);
                    })
                    .catch(error => {
                        console.error('Saving position failed:', error);
                        showMessage("❌ Failed to save location!", "danger");
                    });
            },
            errorCallback,
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }
        );
    } else {
        alert("Geolocation not supported.");
    }
}
async function scanQR() {
    try {
        const html5QrCode = new Html5Qrcode("reader");
        document.getElementById("reader").style.display = "block";

        await html5QrCode.start(
            { facingMode: "environment" },
            { fps: 10, qrbox: 250 },
            async (decodedText) => {
                await html5QrCode.stop();
                document.getElementById("reader").style.display = "none";

                // ✅ Immediately show checklist
                showChecklist(decodedText);
                showMessage(`QR ${qrCount++} scanned.`, 'success');

                // ✅ Only send QR text to /scan (no GPS, time, address)
                fetch('/scan', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        qr_text: decodedText
                    })
                })
                .then(response => response.json())
                .then(result => {
                    if (!result.status || result.status !== 'success') {
                        showMessage('⚠️ Scan saved with issues.', 'warning');
                    }
                })
                .catch(() => showMessage('❌ Failed to save scan.', 'danger'));
            }
        );
    } catch (err) {
        console.error('QR scan failed:', err);
        showMessage('Error during QR scan.', 'danger');
    }
}

function showChecklist(qrData) {
    const questions = allowedQRs[qrData];

    if (!questions) {
        showMessage("Unknown QR Code: " + qrData, "warning");
        return;
    }

    currentQRCode = qrData;
    document.getElementById("qr-label").innerText = qrData;

    const container = document.getElementById("checklist-questions");
    container.innerHTML = "";

    questions.forEach((q, i) => {
        if (Array.isArray(q)) {
            // Row with two side-by-side checkboxes
            container.innerHTML += `
                <div class="row mb-2">
                    <div class="col-md-6">
                        <div class="form-check text-start">
                            <input class="form-check-input" type="checkbox" id="q${i}_1" name="questions" value="${q[0]}">
                            <label class="form-check-label" for="q${i}_1">${q[0]}</label>
                        </div>
                    </div>
                    ${q[1] ? `
                    <div class="col-md-6">
                        <div class="form-check text-start">
                            <input class="form-check-input" type="checkbox" id="q${i}_2" name="questions" value="${q[1]}">
                            <label class="form-check-label" for="q${i}_2">${q[1]}</label>
                        </div>
                    </div>` : ""}
                </div>
            `;
        } else {
            // Single checklist item
            container.innerHTML += `
                <div class="form-check text-start mb-2">
                    <input class="form-check-input" type="checkbox" id="q${i}" name="questions" value="${q}">
                    <label class="form-check-label" for="q${i}">${q}</label>
                </div>
            `;
        }
    });

    document.getElementById("checklist-section").style.display = "block";
}

document.getElementById("checklist-form").addEventListener("submit", function (e) {
    e.preventDefault();
    const rows = [];
    const formGroups = document.querySelectorAll('#checklist-questions .row, #checklist-questions .form-check:not(.row *)');

    formGroups.forEach(group => {
        const checkboxes = group.querySelectorAll('input[type="checkbox"]:checked');
        if (checkboxes.length === 1) {
            rows.push(`- ${checkboxes[0].value}`);
        } else if (checkboxes.length === 2) {
            const left = `- ${checkboxes[0].value}`.padEnd(35);
            const right = `- ${checkboxes[1].value}`;
            rows.push(`${left}${right}`);
        }
    });

    const formattedChecklist = rows.join("\n");
    const qrCode = currentQRCode;

    fetch("/submit-checklist", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ qr_code: qrCode, checklist: formattedChecklist })
    })
    .then(res => res.json())
    .then(data => {
        showMessage("Checklist submitted successfully!", "success");
        document.getElementById("checklist-section").style.display = "none";
    })
    .catch(err => {
        console.error("Checklist error:", err);
        showMessage("Error submitting checklist.", "danger");
    });
});

function stopWalk() {
    // hasStarted = false;

    if (watchId !== null) {
        navigator.geolocation.clearWatch(watchId);
        watchId = null;
        console.log("🛑 Walk tracking stopped.");
    }

    fetch('/submit_walk', { method: 'POST' })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.text();
        })
        .then(data => {
            showMessage("✅ Walk route map generated and emailed successfully!", "success");
        })
        .catch(error => {
            console.error('Generating walk map failed:', error);
            showMessage("❌ Failed to generate walk map.", "danger");
        });
}

function errorCallback(error) {
    let message = '';
    switch (error.code) {
        case error.PERMISSION_DENIED:
            message = "User denied the request for Geolocation.";
            break;
        case error.POSITION_UNAVAILABLE:
            message = "Location information is unavailable.";
            break;
        case error.TIMEOUT:
            message = "The request to get user location timed out.";
            break;
        default:
            message = "An unknown error occurred.";
            break;
    }
    showMessage(`❌ ${message}`, "danger");
}
