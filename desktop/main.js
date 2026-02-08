const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const isDev = !app.isPackaged;

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

  if (isDev) {
    mainWindow.loadURL('http://localhost:5173');
  } else {
    // Try multiple paths for robustness
    const possiblePaths = [
        path.join(__dirname, 'dist/index.html'),
        path.join(__dirname, 'index.html'), // If flattened
        path.join(process.resourcesPath, 'app.asar/dist/index.html')
    ];
    
    let loaded = false;
    for (const p of possiblePaths) {
        try {
            // Check if file exists (sync check for debug)
            // Actually, loadFile doesn't throw, it just fails. 
            // We'll just chain them or pick the first that looks right.
            // For now, let's stick to the most likely standard build output.
            // But let's enable the inspector so we can debug.
        } catch (e) {}
    }
    
    // Default standard Vite+Electron-Builder path
    const indexPath = path.join(__dirname, 'dist/index.html');
    console.log(`Loading UI from: ${indexPath}`);
    mainWindow.loadFile(indexPath).catch(e => console.error("UI Load Failed:", e));
    
    // DevTools disabled on start (Toggle via View menu or Cmd+Opt+I)
    // mainWindow.webContents.openDevTools({ mode: 'detach' });
  }
}

function startServer() {
  console.log('Starting Omni Core...');
  
  let corePath;
  let args = ['serve'];

  if (isDev) {
    // In Dev, assume 'omni' is in PATH or venv
    corePath = 'omni'; 
    // Or hardcode to workspace venv python if needed
  } else {
    // In Prod, it is in Resources/omni-core/omni
    // 'process.resourcesPath' points to Contents/Resources
    corePath = path.join(process.resourcesPath, 'omni-core', 'omni');
  }

  console.log(`Spawning Core: ${corePath}`);
  
  serverProcess = spawn(corePath, args, { 
    shell: isDev, // Shell needed for PATH lookup in dev
    detached: false
  });
  
  serverProcess.stdout.on('data', (data) => console.log(`[Core]: ${data}`));
  serverProcess.stderr.on('data', (data) => console.error(`[Core Error]: ${data}`));
}

app.whenReady().then(() => {
  startServer();
  // Wait a sec for server to boot?
  setTimeout(createWindow, 2000);
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
  if (serverProcess) serverProcess.kill();
});

app.on('before-quit', () => {
    if (serverProcess) serverProcess.kill();
});
