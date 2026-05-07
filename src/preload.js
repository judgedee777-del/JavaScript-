const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  search: (keyword, platform, page) => ipcRenderer.invoke('search', keyword, platform, page)
});
