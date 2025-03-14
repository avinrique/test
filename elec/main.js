const { app, BrowserWindow, ipcMain } = require("electron");
const path = require("path");
const fs = require("fs");
const { exec } = require("child_process");
const { spawn } = require('child_process');
let mainWindow;
let pythonProcess = null; 
app.whenReady().then(() => {
  const filePath = path.join(__dirname, "usersinfo.json");

  // Check if user data exists
  if (fs.existsSync(filePath)) {
    mainWindow = new BrowserWindow({
      width: 1000,
      height: 700,
      webPreferences: {
        nodeIntegration: true,
        contextIsolation: false,
      },
    });

    mainWindow.loadFile("dashboard.html"); // Directly go to dashboard if data exists
  } else {
    mainWindow = new BrowserWindow({
      width: 1000,
      height: 700,
      webPreferences: {
        nodeIntegration: true,
        contextIsolation: false,
      },
    });

    mainWindow.loadFile("index.html");
  }
});

// Handle window navigation
ipcMain.on("navigate", (event, page) => {
  mainWindow.loadFile(page);
});

ipcMain.on('run-python', () => {
  if (!pythonProcess) {
      pythonProcess = spawn('python3', ['check2.py']); // Replace with your script

      pythonProcess.stdout.on('data', (data) => {
          console.log(`Python Output: ${data}`);
      });

      pythonProcess.stderr.on('data', (data) => {
          console.error(`Python Error: ${data}`);
      });

      pythonProcess.on('close', (code) => {
          console.log(`Python process exited with code ${code}`);
          pythonProcess = null; // Reset the reference when it stops
      });
  }
});

ipcMain.on('stop-python', () => {
  if (pythonProcess) {
      pythonProcess.kill(); // Kill the Python script
      pythonProcess = null;
  }
});
app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});
