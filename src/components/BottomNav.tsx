import React from 'react';

/** 底部导航栏 */
const BottomNav: React.FC = () => {
  const tabs = [
    { icon: '🏠', label: '首页', active: true },
    { icon: '🏫', label: '食堂', active: false },
    { icon: '⭐', label: '推荐', active: false },
    { icon: '📝', label: '评价', active: false },
    { icon: '👤', label: '我的', active: false },
  ];

  return (
    <nav className="bottom-nav">
      {tabs.map((tab) => (
        <button
          key={tab.label}
          className={`bottom-nav-item ${tab.active ? 'active' : ''}`}
        >
          <span className="bottom-nav-icon">{tab.icon}</span>
          <span className="bottom-nav-label">{tab.label}</span>
        </button>
      ))}
    </nav>
  );
};

export default BottomNav;
