import { defineStore } from "pinia";
import type { ConfigProviderThemeVars } from "wot-design-uni";
import { useStorage } from "@uni-helper/uni-use";

// 主题色选项接口
export interface ThemeColorOption {
  name: string;
  value: string;
  primary: string;
}

// 主题类型
export type ThemeMode = "light" | "dark";

export const useThemeStore = defineStore("appTheme", () => {
  const theme = useStorage<ThemeMode>("app-theme", "dark");

  // 预定义的主题色选项
  const themeColorOptions: ThemeColorOption[] = [
    { name: "默认蓝", value: "blue", primary: "#4D7FFF" },
    { name: "活力橙", value: "orange", primary: "#FF7D00" },
    { name: "薄荷绿", value: "green", primary: "#07C160" },
    { name: "樱花粉", value: "pink", primary: "#FF69B4" },
    { name: "紫罗兰", value: "purple", primary: "#8A2BE2" },
    { name: "朱砂红", value: "red", primary: "#FF4757" },
  ];

  // 主题色
  const currentThemeColor = useStorage<ThemeColorOption>("app-theme-color", themeColorOptions[0]);

  // 主题变量（响应式对象）
  const themeVars: ConfigProviderThemeVars = reactive({
    darkBackground: "#0f0f0f",
    darkBackground2: "#1a1a1a",
    darkBackground3: "#242424",
    darkBackground4: "#2f2f2f",
    darkBackground5: "#3d3d3d",
    darkBackground6: "#4a4a4a",
    darkBackground7: "#606060",
    darkColor: "#ffffff",
    darkColor2: "#e0e0e0",
    darkColor3: "#a0a0a0",
    colorTheme: currentThemeColor.value.primary,
  });

  // 计算属性
  const isDark = computed(() => theme.value === "dark");

  // 切换主题, 指定主题模式，不传则自动切换
  const toggleTheme = (mode?: ThemeMode) => {
    theme.value = mode || (theme.value === "light" ? "dark" : "light");
    setNavigationBarColor();
  };

  // 设置导航栏颜色
  const setNavigationBarColor = () => {
    // 只在非H5环境下调用setNavigationBarColor
    if (process.env.UNI_PLATFORM !== "h5") {
      console.log("设置导航栏颜色", theme.value);
      uni.setNavigationBarColor({
        frontColor: theme.value === "light" ? "#000000" : "#ffffff",
        backgroundColor: theme.value === "light" ? "#ffffff" : "#000000",
      });
    } else {
      console.log("H5环境下跳过设置导航栏颜色");
    }
  };

  // 设置主题色
  const setCurrentThemeColor = (color: ThemeColorOption) => {
    currentThemeColor.value = color;
    themeVars.colorTheme = color.primary;
    console.log("主题色已设置:", color.name);
  };

  // 初始化主题
  const initTheme = () => {
    // 更新主题变量中的颜色
    themeVars.colorTheme = currentThemeColor.value.primary;

    // 设置导航栏颜色
    nextTick(() => {
      setNavigationBarColor();
    });
  };

  return {
    // 状态
    theme,
    currentThemeColor,
    themeVars,
    themeColorOptions,

    // 计算属性
    isDark,

    // 方法
    toggleTheme,
    setCurrentThemeColor,
    setNavigationBarColor,
    initTheme,
  };
});
