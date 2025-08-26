import { ElMessage } from 'element-plus';

// 快速链接数据类型
export interface QuickLink {
  title: string;
  description: string;
  icon: string;
  href: string;
  action: 'navigate' | 'external';
  id?: string;
}

// 快速开始管理器类
class QuickStartManager {
  private storageKey = 'quick-start-links';
  private listeners: Array<(links: QuickLink[]) => void> = [];

  // 获取所有快速链接
  getQuickLinks(): QuickLink[] {
    try {
      const stored = localStorage.getItem(this.storageKey);
      return stored ? JSON.parse(stored) : this.getDefaultLinks();
    } catch (error) {
      console.error('Failed to load quick links:', error);
      return this.getDefaultLinks();
    }
  }

  // 获取默认链接
  private getDefaultLinks(): QuickLink[] {
    return [
      {
        id: 'user-management',
        title: "用户管理",
        description: "管理系统用户信息",
        icon: "User",
        href: "/system/user",
        action: "navigate"
      },
      {
        id: 'monitor',
        title: "系统监控",
        description: "监控系统状态",
        icon: "Monitor",
        href: "/monitor",
        action: "navigate"
      },
      {
        id: 'baidu',
        title: "百度搜索",
        description: "访问百度搜索引擎",
        icon: "Search",
        href: "https://www.baidu.com",
        action: "external"
      },
      {
        id: 'github',
        title: "GitHub",
        description: "访问代码托管平台",
        icon: "Monitor",
        href: "https://github.com",
        action: "external"
      }
    ];
  }

  // 保存快速链接
  saveQuickLinks(links: QuickLink[]): void {
    try {
      localStorage.setItem(this.storageKey, JSON.stringify(links));
      this.notifyListeners(links);
    } catch (error) {
      console.error('Failed to save quick links:', error);
    }
  }

  // 添加快速链接
  addQuickLink(link: QuickLink): void {
    const links = this.getQuickLinks();
    
    // 生成唯一ID
    link.id = link.id || `link-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    
    // 检查是否已存在相同路径的链接
    const existingIndex = links.findIndex(l => l.href === link.href);
    if (existingIndex !== -1) {
      // 更新现有链接
      links[existingIndex] = { ...links[existingIndex], ...link };
      ElMessage.success(`已更新快速链接：${link.title}`);
    } else {
      // 添加新链接
      links.push(link);
    }
    
    this.saveQuickLinks(links);
  }

  // 删除快速链接
  removeQuickLink(id: string): void {
    const links = this.getQuickLinks();
    const filteredLinks = links.filter(link => link.id !== id);
    
    if (filteredLinks.length < links.length) {
      this.saveQuickLinks(filteredLinks);
    }
  }

  // 从路由信息创建快速链接
  createQuickLinkFromRoute(route: any, customTitle?: string, customDescription?: string): QuickLink {
    // 优先使用路由配置的图标
    let routeIcon = route.meta?.icon;
    let routeColor = '#409EFF'; // 默认颜色

    // 如果路由没有配置图标，根据路径推断
    if (!routeIcon) {
      const iconMap: Record<string, { icon: string; color: string }> = {
        '/dashboard/workplace': { icon: 'House', color: '#409EFF' },
        '/dashboard/analysis': { icon: 'TrendCharts', color: '#67C23A' },
        '/dashboard': { icon: 'House', color: '#409EFF' },
        '/system/user': { icon: 'User', color: '#409EFF' },
        '/system/role': { icon: 'UserFilled', color: '#E6A23C' },
        '/system/menu': { icon: 'Menu', color: '#F56C6C' },
        '/system/dept': { icon: 'OfficeBuilding', color: '#909399' },
        '/system/position': { icon: 'Briefcase', color: '#606266' },
        '/system/dict': { icon: 'Collection', color: '#FF6B6B' },
        '/system/config': { icon: 'Setting', color: '#67C23A' },
        '/system/notice': { icon: 'Bell', color: '#E6A23C' },
        '/system/log': { icon: 'Document', color: '#FF6B6B' },
        '/system': { icon: 'Setting', color: '#67C23A' },
        '/monitor/server': { icon: 'Monitor', color: '#606266' },
        '/monitor/cache': { icon: 'Coin', color: '#F56C6C' },
        '/monitor/job': { icon: 'Timer', color: '#909399' },
        '/monitor/online': { icon: 'Connection', color: '#67C23A' },
        '/monitor': { icon: 'Monitor', color: '#606266' },
        '/codegen': { icon: 'Code', color: '#4ECDC4' },
        '/demo': { icon: 'DataAnalysis', color: '#3385FF' },
        '/profile': { icon: 'User', color: '#409EFF' },
      };

      // 查找最匹配的路径配置
      let bestMatch = { icon: 'Link', color: '#909399' }; // 默认配置
      let maxMatchLength = 0;

      for (const [path, config] of Object.entries(iconMap)) {
        if (route.path.startsWith(path) && path.length > maxMatchLength) {
          bestMatch = config;
          maxMatchLength = path.length;
        }
      }

      routeIcon = bestMatch.icon;
      routeColor = bestMatch.color;
    } else {
      // 如果有路由图标，尝试获取对应的颜色
      const colorMap: Record<string, string> = {
        'house': '#409EFF',
        'user': '#409EFF',
        'setting': '#67C23A',
        'monitor': '#606266',
        'document': '#FF6B6B',
        'bell': '#E6A23C',
        'menu': '#F56C6C',
        'office-building': '#909399',
        'data-analysis': '#3385FF',
        'trend-charts': '#67C23A',
      };

      routeColor = colorMap[routeIcon.toLowerCase()] || '#409EFF';
    }

    return {
      title: customTitle || route.meta?.title || route.name || '未命名页面',
      description: customDescription || `快速访问 ${route.meta?.title || route.name || '页面'}`,
      icon: routeIcon,
      href: route.fullPath || route.path,
      action: 'navigate',
      id: `route-${route.path.replace(/\//g, '-')}-${Date.now()}`
    };
  }

  // 添加监听器
  addListener(callback: (links: QuickLink[]) => void): void {
    this.listeners.push(callback);
  }

  // 移除监听器
  removeListener(callback: (links: QuickLink[]) => void): void {
    const index = this.listeners.indexOf(callback);
    if (index > -1) {
      this.listeners.splice(index, 1);
    }
  }

  // 通知所有监听器
  private notifyListeners(links: QuickLink[]): void {
    this.listeners.forEach(callback => {
      try {
        callback(links);
      } catch (error) {
        console.error('Error in quick start listener:', error);
      }
    });
  }

  // 检查链接是否已存在
  isLinkExists(href: string): boolean {
    const links = this.getQuickLinks();
    return links.some(link => link.href === href);
  }
}

// 创建全局实例
export const quickStartManager = new QuickStartManager();

