import React, { useState } from 'react';
import Chat from './components/Chat';
// Раскомментируйте для использования расширенного примера:
// import VersioningExample from './examples/VersioningExample';

function App() {
  const [showAdvancedExample, setShowAdvancedExample] = useState(false);
  // ========================================
  // ЗДЕСЬ ВЫ МОЖЕТЕ ДОБАВИТЬ СВОИ ФУНКЦИИ
  // ========================================
  
  // Функция для обработки редактирования сообщения
  const handleMessageEdit = (editData) => {
    console.log('App: Сообщение отредактировано', editData);
    
    // Здесь вы можете:
    // - Сохранить версию в localStorage
    // - Отправить на сервер
    // - Обновить глобальное состояние
    // - Сохранить в базу данных
    
    // Пример сохранения в localStorage:
    const editHistory = JSON.parse(localStorage.getItem('messageEditHistory') || '[]');
    editHistory.push(editData);
    localStorage.setItem('messageEditHistory', JSON.stringify(editHistory));
  };

  // Функция для обработки отправки нового сообщения
  const handleMessageSend = (message) => {
    console.log('App: Новое сообщение', message);
    
    // Здесь вы можете:
    // - Сохранить сообщение в базу данных
    // - Отправить на сервер
    // - Добавить в историю версий
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <Chat 
        onMessageEdit={handleMessageEdit}
        onMessageSend={handleMessageSend}
      />
    </div>
  );
}

export default App;
