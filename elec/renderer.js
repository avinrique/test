// const { ipcRenderer } = require("electron");
// const fs = require("fs");
// const path = require("path");

// const categoryQuestions = {
//     kid: [  "What’s your name? 😊",
//         "How old are you? 🎂",
//         "What do you like to do for fun? (Games, drawing, stories, cartoons, etc.) 🎮🎨📖",
//         "Do you want me to tell stories, jokes, or help with homework? 🤖📚",
//         "What’s your favorite cartoon or superhero? 🦸‍♂️🦸‍♀️",
//         "Do you want to learn something new? (Science, space, math, fun facts?) 🚀🔬",
//         "Should I call you by your name or a fun nickname? 😃",
//         "Do you like short answers or detailed stories? ✨",
//         "What’s your favorite color and animal? 🎨🐼",
//         "Do you want me to remind you about homework or bedtime? ⏰"],
//     senior: ["What’s your name? 😊",
//             "Would you like me to call you by your first name or something else? 🤗",
//             "What do you enjoy talking about? (Family, news, history, hobbies, music?) 📻📜🎵",
//             "Do you want help remembering things like medication or events? 💊📅",
//             "Would you like daily stories, jokes, or uplifting messages? 🌞📖",
//             "Are you interested in learning something new? (Tech, language, history?) 🧠📚",
//             "Do you prefer short, simple replies or more detailed conversations? 🗣️",
//             "Would you like to talk about old memories and life experiences? 💭",
//             "Do you need help with using technology? (Phones, emails, internet?) 📱💻",
//             "Should I remind you to drink water and go for a walk? 🚶‍♂️💧"],
//     techie: ["What’s your name or alias? (Optional) 😎",
//             "What’s your main area of interest? (Coding, AI, cybersecurity, robotics, etc.) 🤖🔍",
//             "What tech stack do you work with? (Python, Linux, Docker, etc.) 💻🐍",
//             "Do you want detailed explanations or quick answers? ⏳",
//             "Are you working on any projects I can assist with? 🛠️",
//             "Do you prefer step-by-step debugging help or just suggestions? 🐞",
//             "Would you like updates on new tech trends, frameworks, or security news? 📰",
//             "How deep should I go into technical topics? (Beginner, intermediate, expert) ⚙️",
//             "Would you like productivity reminders (stand-up breaks, task tracking)? ⏰",
//             "Do you want occasional jokes or memes to lighten the mood? 😆"]
// };

// document.getElementById("categorySelect").addEventListener("change", function() {
//     const category = this.value;
//     const questionsContainer = document.getElementById("questionsContainer");
//     questionsContainer.innerHTML = "";

//     if (category) {
//         categoryQuestions[category].forEach((question, index) => {
//             const label = document.createElement("label");
//             label.innerText = question;

//             const input = document.createElement("input");
//             input.type = "text";
//             input.id = `q${index}`;

//             questionsContainer.appendChild(label);
//             questionsContainer.appendChild(input);
//             questionsContainer.appendChild(document.createElement("br"));
//         });
//     }
// });

// document.getElementById("submitBtn").addEventListener("click", function() {







//     ipcRenderer.send("navigate", "dashboard.html");
// });

const { ipcRenderer } = require("electron");
const fs = require("fs");
const path = require("path");

// Define questions for each category

const categoryQuestions = {
    kid: [  "What’s your name? 😊",
        "How old are you? 🎂",
        "What do you like to do for fun? (Games, drawing, stories, cartoons, etc.) 🎮🎨📖",
        "Do you want me to tell stories, jokes, or help with homework? 🤖📚",
        "What’s your favorite cartoon or superhero? 🦸‍♂️🦸‍♀️",
        "Do you want to learn something new? (Science, space, math, fun facts?) 🚀🔬",
        "Should I call you by your name or a fun nickname? 😃",
        "Do you like short answers or detailed stories? ✨",
        "What’s your favorite color and animal? 🎨🐼",
        "Do you want me to remind you about homework or bedtime? ⏰"],
    senior: ["What’s your name? 😊",
            "Would you like me to call you by your first name or something else? 🤗",
            "What do you enjoy talking about? (Family, news, history, hobbies, music?) 📻📜🎵",
            "Do you want help remembering things like medication or events? 💊📅",
            "Would you like daily stories, jokes, or uplifting messages? 🌞📖",
            "Are you interested in learning something new? (Tech, language, history?) 🧠📚",
            "Do you prefer short, simple replies or more detailed conversations? 🗣️",
            "Would you like to talk about old memories and life experiences? 💭",
            "Do you need help with using technology? (Phones, emails, internet?) 📱💻",
            "Should I remind you to drink water and go for a walk? 🚶‍♂️💧"],
    techie: ["What’s your name or alias? (Optional) 😎",
            "What’s your main area of interest? (Coding, AI, cybersecurity, robotics, etc.) 🤖🔍",
            "What tech stack do you work with? (Python, Linux, Docker, etc.) 💻🐍",
            "Do you want detailed explanations or quick answers? ⏳",
            "Are you working on any projects I can assist with? 🛠️",
            "Do you prefer step-by-step debugging help or just suggestions? 🐞",
            "Would you like updates on new tech trends, frameworks, or security news? 📰",
            "How deep should I go into technical topics? (Beginner, intermediate, expert) ⚙️",
            "Would you like productivity reminders (stand-up breaks, task tracking)? ⏰",
            "Do you want occasional jokes or memes to lighten the mood? 😆"]
};
// Update questions based on category selection

document.getElementById("categorySelect").addEventListener("change", function() {
    const category = this.value;
    const questionsContainer = document.getElementById("questionsContainer");
    questionsContainer.innerHTML = ""; // Clear existing content

    if (category) {
        categoryQuestions[category].forEach((question, index) => {
            const questionDiv = document.createElement("div"); 
            questionDiv.classList.add("question-item"); // Add a class for styling

            const label = document.createElement("label");
            label.innerText = question;

            const input = document.createElement("input");
            input.type = "text";
            input.id = `q${index}`;

            questionDiv.appendChild(label);
            questionDiv.appendChild(input);
            questionsContainer.appendChild(questionDiv);
        });
    }
});

// Save user info when submit is clicked
document.getElementById("submitBtn").addEventListener("click", function() {
    const category = document.getElementById("categorySelect").value;
    if (!category) {
        alert("Please select a category.");
        return;
    }

    let userInfo = {
        category: category,
        answers: {}
    };

    categoryQuestions[category].forEach((question, index) => {
        const answer = document.getElementById(`q${index}`).value || "Not answered";
        userInfo.answers[question] = answer;
    });

    // Define the path for usersinfo.json
    const filePath = path.join(__dirname, "usersinfo.json");

    // Write data to usersinfo.json
    fs.writeFile(filePath, JSON.stringify(userInfo, null, 4), (err) => {
        if (err) {
            console.error("Error saving user info:", err);
        } else {
            console.log("User info saved successfully.");
            ipcRenderer.send("navigate", "dashboard.html");
        }
    });
});



document.addEventListener("DOMContentLoaded", async () => {
    const devicesList = document.getElementById("devices");

    async function getBluetoothDevices() {
        const devices = await ipcRenderer.invoke("getBluetoothDevices");
        devicesList.innerHTML = ""; // Clear previous list

        if (devices.length === 0) {
            devicesList.innerHTML = "<p>No Bluetooth devices found.</p>";
        } else {
            devices.forEach((device) => {
                const listItem = document.createElement("li");
                listItem.textContent = `${device.name} - ${device.mac}`;
                devicesList.appendChild(listItem);
            });
        }
    }

    document.getElementById("scanBtn").addEventListener("click", getBluetoothDevices);
});