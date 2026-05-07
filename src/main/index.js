const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { search } = require('./search');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, '../preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  mainWindow.loadFile(path.join(__dirname, '../renderer/index.html'));
}

app.whenReady().then(() => {
  createWindow();

  // 注册 IPC 处理器
  ipcMain.handle('search', async (event, keyword, platform = 'jd', page = 1) => {
    return await search(keyword, platform, page);
  });
});

app.on('window-all-closed', () => {
  app.quit();
});
