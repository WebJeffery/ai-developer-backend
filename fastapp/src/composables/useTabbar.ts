export interface TabbarItem {
  name: string;
  title: string;
  icon: string;
}

const tabbarItems = ref<TabbarItem[]>([
  { name: "index", title: "首页", icon: "home" },
  { name: "work", title: "工作台", icon: "app" },
  { name: "mine", title: "我的", icon: "user" },
]);

const activeTabbar = ref<string>("index");

export function useTabbar() {
  const tabbarList = computed(() => tabbarItems.value);

  const setTabbarItemActive = (name: string) => {
    activeTabbar.value = name;
  };

  return {
    tabbarList,
    activeTabbar,
    setTabbarItemActive,
  };
}