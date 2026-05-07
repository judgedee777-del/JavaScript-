document.addEventListener('DOMContentLoaded', async () => {
  const keywordInput = document.getElementById('keyword');
  const searchBtn = document.getElementById('searchBtn');
  const productList = document.getElementById('productList');
  const resultCount = document.getElementById('resultCount');
  const platformIndicator = document.getElementById('platformIndicator');
  const tabs = document.querySelectorAll('.tab');

  let currentPlatform = 'jd';

  // 平台配置
  const platformConfig = {
    jd: { name: '京东', color: '#e2231a' },
    tb: { name: '淘宝', color: '#ff5000' },
    pdd: { name: '拼多多', color: '#ee3d3f' }
  };

  // 切换平台
  function switchPlatform(platform) {
    currentPlatform = platform;
    const config = platformConfig[platform];

    // 更新标签状态
    tabs.forEach(tab => {
      tab.classList.toggle('active', tab.dataset.platform === platform);
    });

    // 更新平台指示器
    platformIndicator.textContent = config.name;
    platformIndicator.style.background = config.color;

    // 更新 CSS 变量
    document.documentElement.style.setProperty('--active-color', config.color);
    const glowColor = config.color.replace(')', ', 0.2)').replace('rgb', 'rgba');
    document.documentElement.style.setProperty('--active-glow', glowColor);

    // 清空结果
    resultCount.textContent = '0 个结果';
    showEmpty(`切换到${config.name}，输入关键词开始搜索`);
  }

  // 初始化平台
  switchPlatform('jd');

  // 标签点击事件
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      if (!tab.disabled) {
        switchPlatform(tab.dataset.platform);
      }
    });
  });

  // 渲染加载状态
  function showLoading() {
    productList.innerHTML = `
      <div class="loading-state">
        <div class="loading-spinner"></div>
        <p>搜索中...</p>
      </div>
    `;
  }

  // 渲染空状态
  function showEmpty(message = '未找到商品') {
    productList.innerHTML = `
      <div class="empty-state">
        <svg class="empty-state-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
        </svg>
        <p>${message}</p>
      </div>
    `;
  }

  // 渲染错误状态
  function showError(message) {
    productList.innerHTML = `
      <div class="error-state">
        <svg class="error-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
          <line x1="12" y1="8" x2="12" y2="12"/>
          <line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
        <p class="error-message">${escapeHtml(message)}</p>
      </div>
    `;
  }

  // 渲染商品列表
  function renderProducts(products) {
    if (!products || products.length === 0) {
      showEmpty();
      return;
    }

    productList.innerHTML = products.map(p => `
      <div class="product-item">
        <div class="product-image-wrapper">
          <img class="product-image"
               src="${p.imageUrl || ''}"
               alt="${escapeHtml(p.name)}"
               onerror="this.parentElement.innerHTML='<div style=\\'display:flex;align-items:center;justify-content:center;width:100%;height:100%;color:var(--color-text-muted);font-size:12px;\\'>暂无图片</div>'" />
        </div>
        <div class="product-info">
          <div class="product-name">${escapeHtml(p.name)}</div>
          <div class="product-bottom">
            <div class="product-price">${p.price}</div>
            <div class="product-meta">
              <span>🏪 ${escapeHtml(p.shop || '未知店铺')}</span>
              <span>📦 ${formatSales(p.sales)}</span>
            </div>
          </div>
        </div>
      </div>
    `).join('');
  }

  // HTML转义
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // 格式化销量
  function formatSales(sales) {
    if (!sales && sales !== 0) return '暂无';
    if (sales >= 10000) {
      return (sales / 10000).toFixed(1) + '万+';
    }
    return sales.toString();
  }

  // 搜索
  async function doSearch() {
    const keyword = keywordInput.value.trim();
    if (!keyword) {
      showEmpty('请输入搜索关键词');
      return;
    }

    searchBtn.disabled = true;
    searchBtn.textContent = '搜索中...';
    showLoading();

    try {
      const result = await window.api.search(keyword, currentPlatform);

      if (result.code !== 0) {
        showError(result.message || '搜索失败');
        return;
      }

      // 根据不同平台解析响应
      let products = [];
      let total = 0;

      switch (currentPlatform) {
        case 'jd':
          // JD 返回结构: { code, message, data: { resultCount, wareList: [...] }, extracted: [...] }
          const jdData = result.data || {};
          products = (jdData.wareList || result.extracted || []).map(item => ({
            name: item.wareName || item.name || '未知商品',
            price: item.realPrice || item.dPrice || '暂无',
            shop: item.shopName || '未知店铺',
            sales: item.totalSales || item.yuYueNum || 0,
            imageUrl: item.imageurl ? 'https://img14.360buyimg.com/n1/' + item.imageurl : ''
          }));
          total = jdData.resultCount || products.length;
          break;

        case 'tb':
          // TB 返回结构: { code, data: {...}, products: [...] }
          const tbData = result.data || {};
          products = (tbData.itemsArray || result.products || []).map(item => ({
            name: item.title || '未知商品',
            price: item.price || '暂无',
            shop: item.procity || '未知店铺',
            sales: item.realSales || 0,
            imageUrl: item.pic_path || ''
          }));
          total = products.length;
          break;

        case 'pdd':
          // PDD 返回结构: { goods_list: [...] }
          products = (result.data?.goods_list || result.goods_list || []).map(item => ({
            name: item.goods_name || '未知商品',
            price: item.price || '暂无',
            shop: item.mall_name || '未知店铺',
            sales: item.sales || 0,
            imageUrl: item.image_url || ''
          }));
          total = result.data?.total || products.length;
          break;
      }

      resultCount.textContent = `${total} 个结果`;
      renderProducts(products);

    } catch (err) {
      showError(`搜索出错: ${err.message}`);
    } finally {
      searchBtn.disabled = false;
      searchBtn.textContent = '搜索';
    }
  }

  // 事件绑定
  searchBtn.addEventListener('click', doSearch);
  keywordInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') doSearch();
  });
});
