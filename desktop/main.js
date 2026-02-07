const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let serverProcess;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    titleBarStyle: 'hiddenInset',
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    },
    backgroundColor: '#050505',
    icon: path.join(__dirname, 'assets/icon.png')
  });

  // Load UI (For now, just a placeholder or the website)
  // In Phase 2.1, we will serve the React app here.
  mainWindow.loadURL('http://localhost:8000'); 
  // Wait! We don't have a UI served by FastAPI yet. 
  // We need the React app. For MVP, let's load a static HTML file.
  mainWindow.loadFile('index.html');
}

function startServer() {
  console.log('Starting Omni Core...');
  // This assumes 'omni' is in PATH or relative. 
  // In prod, we bundle the python binary.
  // For dev, we assume user ran `omni serve` or we spawn it.
  
  // serverProcess = spawn('omni', ['serve'], { shell: true });
  // serverProcess.stdout.on('data', (data) => console.log(`Core: ${data}`));
}

app.whenReady().then(() => {
  // startServer(); // Manual start for now
  createWindow();
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
  if (serverProcess) serverProcess.kill();
});
