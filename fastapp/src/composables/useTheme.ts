import { useThemeStore, ThemeMode, ThemeColorOption } from "@/store";

export function useTheme() {
  const store = useThemeStore();

  /**
   * 切换暗黑模式
   * @param mode 指定主题模式，不传则自动切换
   */
  function toggleTheme(mode?: ThemeMode) {
    store.toggleTheme(mode);
  }

  /**
   * 设置主题色
   * @param option 主题色选项
   */
  function setThemeColor(option: ThemeColorOption) {
    store.setCurrentThemeColor(option);
  }

  /**
   * 初始化主题
   */
  function initTheme() {
    store.initTheme();
  }

  // 注意：全局主题管理已在App.vue中处理
  // 包括：系统主题监听、导航栏颜色同步等
  // 组件中一般不需要再调用initTheme()，除非有特殊需求

  return {
    // 状态
    theme: computed(() => store.theme),
    isDark: computed(() => store.isDark),
    currentThemeColor: computed(() => store.currentThemeColor),
    themeVars: computed(() => store.themeVars),

    // 主题选项
    themeColorOptions: computed(() => store.themeColorOptions),

    // 方法
    initTheme,
    toggleTheme,
    setThemeColor,
  };
}
