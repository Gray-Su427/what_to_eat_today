import React, { useState, useEffect } from 'react';
import type { Dish, Canteen } from './types';
import { getCanteens, getRecommendedDishes, getTodaySuggestion } from './mock/mockApi';
import Header from './components/Header';
import RecommendCard from './components/RecommendCard';
import QuickEntry from './components/QuickEntry';
import DishList from './components/DishList';
import CanteenHeat from './components/CanteenHeat';
import AISuggestion from './components/AISuggestion';
import BottomNav from './components/BottomNav';
import SearchPage from './components/SearchPage';
import AIChat from './components/AIChat';
import './styles.css';

const App: React.FC = () => {
  // 状态管理
  const [dishes, setDishes] = useState<Dish[]>([]);
  const [canteens, setCanteens] = useState<Canteen[]>([]);
  const [suggestion, setSuggestion] = useState<string>('');
  const [highlightDish, setHighlightDish] = useState<Dish | null>(null);
  const [searchKeyword, setSearchKeyword] = useState('');
  const [loading, setLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);
  const [showSearch, setShowSearch] = useState(false);
  const [showAIChat, setShowAIChat] = useState(false);

  // 页面加载时获取数据
  useEffect(() => {
    const loadData = async () => {
      try {
        const [dishData, canteenData, suggestionData] = await Promise.all([
          getRecommendedDishes(),
          getCanteens(),
          getTodaySuggestion(),
        ]);
        setDishes(dishData);
        setCanteens(canteenData);
        setSuggestion(suggestionData.text);
        setHighlightDish(suggestionData.highlightDish ?? null);
      } catch (error) {
        console.error('加载数据失败:', error);
      } finally {
        setInitialLoading(false);
      }
    };
    loadData();
  }, []);

  // 点击"帮我推荐"
  const handleRecommend = async () => {
    setLoading(true);
    try {
      const data = await getTodaySuggestion();
      setSuggestion(data.text);
      setHighlightDish(data.highlightDish ?? null);
    } catch (error) {
      console.error('获取推荐失败:', error);
    } finally {
      setLoading(false);
    }
  };

  // 加载中状态
  if (initialLoading) {
    return (
      <div className="app-container">
        <div className="loading-screen">
          <span className="loading-emoji">🍚</span>
          <p>正在加载美味推荐...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="app-container">
      <div className="app-scroll">
        {/* 顶部区域 */}
        <Header
          searchKeyword={searchKeyword}
          onSearchChange={setSearchKeyword}
          onSearchFocus={() => setShowSearch(true)}
        />

        {/* 主推荐卡片 */}
        <RecommendCard
          suggestion={suggestion}
          highlightDish={highlightDish}
          loading={loading}
          onRecommend={handleRecommend}
        />

        {/* 快捷入口 */}
        <QuickEntry onAIClick={() => setShowAIChat(true)} />

        {/* 今日推荐（展示前 3 个） */}
        <DishList dishes={dishes.slice(0, 3)} />

        {/* 食堂热度 */}
        <CanteenHeat canteens={canteens} />

        {/* AI 场景化饮食建议 */}
        <AISuggestion onOpenChat={() => setShowAIChat(true)} />

        {/* 底部留白，避免被导航栏遮挡 */}
        <div className="bottom-spacer" />
      </div>

      {/* 底部导航栏 */}
      <BottomNav />

      {/* 搜索页面（全屏覆盖） */}
      <SearchPage visible={showSearch} onClose={() => setShowSearch(false)} />

      {/* AI 对话页面（全屏覆盖） */}
      <AIChat visible={showAIChat} onClose={() => setShowAIChat(false)} />
    </div>
  );
};

export default App;
