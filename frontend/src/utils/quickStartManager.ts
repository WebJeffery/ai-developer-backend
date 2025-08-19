import { ElMessage } from 'element-plus';

// 快速链接数据类型
export interface QuickLink {
  title: string;
  description: string;
  icon: string;
  color: string;
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
        color: "#409EFF",
        href: "/system/user",
        action: "navigate"
      },
      {
        id: 'monitor',
        title: "系统监控",
        description: "监控系统状态",
        icon: "Monitor",
        color: "#909399",
        href: "/monitor",
        action: "navigate"
      },
      {
        id: 'baidu',
        title: "百度搜索",
        description: "访问百度搜索引擎",
        icon: "Search",
        color: "#3385FF",
        href: "https://www.baidu.com",
        action: "external"
      },
      {
        id: 'github',
        title: "GitHub",
        description: "访问代码托管平台",
        icon: "Monitor",
        color: "#24292e",
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
      ElMessage.error('保存快速链接失败');
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
      ElMessage.success(`已添加快速链接：${link.title}`);
    }
    
    this.saveQuickLinks(links);
  }

  // 删除快速链接
  removeQuickLink(id: string): void {
    const links = this.getQuickLinks();
    const filteredLinks = links.filter(link => link.id !== id);
    
    if (filteredLinks.length < links.length) {
      this.saveQuickLinks(filteredLinks);
      ElMessage.success('已删除快速链接');
    }
  }

  // 从路由信息创建快速链接
  createQuickLinkFromRoute(route: any, customTitle?: string, customDescription?: string): QuickLink {
    // 根据路径推断图标和颜色
    const iconMap: Record<string, { icon: string; color: string }> = {
      '/dashboard': { icon: 'House', color: '#409EFF' },
      '/system': { icon: 'Setting', color: '#67C23A' },
      '/user': { icon: 'User', color: '#409EFF' },
      '/role': { icon: 'UserFilled', color: '#E6A23C' },
      '/menu': { icon: 'Menu', color: '#F56C6C' },
      '/dept': { icon: 'OfficeBuilding', color: '#909399' },
      '/monitor': { icon: 'Monitor', color: '#606266' },
      '/log': { icon: 'Document', color: '#FF6B6B' },
      '/codegen': { icon: 'Code', color: '#4ECDC4' },
      '/demo': { icon: 'DataAnalysis', color: '#3385FF' },
    };

    // 查找匹配的图标配置
    let iconConfig = { icon: 'Link', color: '#909399' }; // 默认配置
    for (const [path, config] of Object.entries(iconMap)) {
      if (route.path.includes(path)) {
        iconConfig = config;
        break;
      }
    }

    return {
      title: customTitle || route.meta?.title || route.name || '未命名页面',
      description: customDescription || `快速访问 ${route.meta?.title || route.name || '页面'}`,
      icon: iconConfig.icon,
      color: iconConfig.color,
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

