import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // 백엔드 API 주소
  const API_URL = 'http://localhost:8000';

  // 데이터 로드 함수
  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_URL}/items/`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setItems(data);
    } catch (e) {
      setError(e.message);
      console.error('Fetch error:', e);
    } finally {
      setLoading(false);
    }
  };

  // 컴포넌트 마운트 시 데이터 로드
  useEffect(() => {
    fetchData();
  }, []); // 빈 배열: 처음 한 번만 실행

  return (
    <div className="App">
      <header className="App-header">
        <h1>📦 DB 아이템 목록 (Full-Stack)</h1>
        
        <button onClick={fetchData} disabled={loading}>
          {loading ? '새로고침 중...' : '새로고침'}
        </button>

        {loading && <p>데이터 로딩 중...</p>}
        
        {error && <p style={{ color: 'red' }}>에러 발생: {error}</p>}

        {!loading && !error && (
          <ul style={{ textAlign: 'left', marginTop: '20px', fontSize: '1.2rem' }}>
            {items.length === 0 ? (
              <li>
                데이터가 없습니다. 
                <a 
                  href="http://localhost:8000/docs" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  style={{ color: '#61dafb' }}
                >
                  [백엔드 API 문서]
                </a>
                에서 데이터를 추가해보세요.
              </li>
            ) : (
              items.map(item => (
                <li key={item.id}>
                  <strong>{item.name}</strong> (ID: {item.id})
                  <p style={{ margin: '5px 0', fontSize: '1rem' }}>
                    {item.description}
                  </p>
                </li>
              ))
            )}
          </ul>
        )}
      </header>
    </div>
  );
}

export default App;