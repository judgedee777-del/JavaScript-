const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Python 解释器路径
const PYTHON = 'python';

// 源文件路径配置
const SOURCE_PATHS = {
  jd: path.join(__dirname, '../../sources/jd/jd_search.py'),
  tb: path.join(__dirname, '../../sources/tb/tb_search.py'),
  pdd: path.join(__dirname, '../../sources/pdd/pdd_search.py')
};

// 搜索
async function search(keyword, platform = 'jd', page = 1) {
  if (!keyword) {
    return { code: -1, message: '关键词不能为空' };
  }

  const pyFile = SOURCE_PATHS[platform];
  if (!pyFile) {
    return { code: -1, message: `不支持的平台: ${platform}` };
  }

  // 确保文件存在
  if (!fs.existsSync(pyFile)) {
    return { code: -1, message: `源文件不存在: ${pyFile}` };
  }

  return new Promise((resolve) => {
    // 根据平台调用不同的 Python 脚本
    const args = [pyFile, keyword];

    const proc = spawn(PYTHON, args, {
      cwd: path.dirname(pyFile),
      encoding: 'utf-8'
    });

    let stdout = '';
    let stderr = '';

    proc.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    proc.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    proc.on('close', (code) => {
      if (stderr) {
        console.log(`[${platform.toUpperCase()}] stderr:`, stderr.substring(0, 500));
      }

      try {
        // 尝试解析 JSON 输出
        const trimmed = stdout.trim();
        const result = JSON.parse(trimmed);
        resolve(result);
      } catch (err) {
        console.log(`[${platform.toUpperCase()}] stdout:`, stdout.substring(0, 500));
        resolve({ code: -1, message: '解析失败: ' + stdout.substring(0, 100) });
      }
    });
  });
}

module.exports = { search };
