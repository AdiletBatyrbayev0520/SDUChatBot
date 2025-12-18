import React, { useState, useEffect, useRef } from 'react';

// ========= Константы =========
const CHAT_CONFIG = {
    BOT_RESPONSE_DELAY: 30, // задержка ответа бота в мс
    INITIAL_NODE_ID: Date.now(),
    BOT_SENDER: 'Бот',
    DEFAULT_USER: 'Пользователь'
};

// ========= Модели =========

// ResponseNode = ответ ассистента
// { id, parentEdgeId?, text, createdAt, childrenEdgeIds: [], lastVisitedLeaf: nodeId }
  
// MessageEdge = наше сообщение
// { id, fromNodeId, toNodeId?, text, kind, createdAt, editOfEdgeId? }

const Chat = ({ onMessageEdit, onMessageSend }) => {
    // Хранилище узлов и рёбер
    const [nodes, setNodes] = useState(() => {
        // Корневой узел
        const rootNode = {
            id: CHAT_CONFIG.INITIAL_NODE_ID,
            parentEdgeId: null,
            text: 'Начало диалога',
            createdAt: new Date().toISOString(),
            childrenEdgeIds: [],
            lastVisitedLeaf: CHAT_CONFIG.INITIAL_NODE_ID
        };
        return { [rootNode.id]: rootNode };
    });
    
    const [edges, setEdges] = useState({});
    
    // Курсор хранит только текущий узел
    const [cursor, setCursor] = useState({
        currentNodeId: CHAT_CONFIG.INITIAL_NODE_ID
    });
    
    // Состояние ввода сообщения
    const [inputValue, setInputValue] = useState('');
    // Для редактирования
    const [editingEdgeId, setEditingEdgeId] = useState(null);
    const [editingText, setEditingText] = useState('');
    
    const messagesEndRef = useRef(null);
    
    // Прокрутка вниз при добавлении нового ответа
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
        console.log('Cursor updated:', cursor);
        console.log('Current Node:', nodes[cursor.currentNodeId]);
        console.log('Edges:', edges);
        console.log('Nodes:', nodes);
    }, [cursor, edges, nodes]);
    
    // ========= Утилиты генерации ID =========
    const generateId = () => Date.now() + Math.floor(Math.random() * 1000);
    
    // ========= Операции =========
    
    // Отправка нового сообщения (создаёт ребро, затем эмулирует ответ)
    const sendMessage = (text) => {
        if (!text.trim()) return;
        const fromNodeId = cursor.currentNodeId;
        const newEdgeId = generateId();
        const newEdge = {
            id: newEdgeId,
            fromNodeId,
            // toNodeId будет заполнено после ответа бота
            text,
            kind: 'user',
            createdAt: new Date().toISOString()
        };
        
        setEdges(prev => ({ ...prev, [newEdgeId]: newEdge }));
        
        if (onMessageSend && typeof onMessageSend === 'function') {
            onMessageSend(newEdge);
        }
        
        // Добавляем ребро в дочерние узлы родительского node
        setNodes(prev => {
            const fromNode = prev[fromNodeId];
            const updatedNode = {
                ...fromNode,
                childrenEdgeIds: [...(fromNode.childrenEdgeIds || []), newEdgeId]
            };
            return { ...prev, [fromNodeId]: updatedNode };
        });
        
        // Эмулируем ответ бота через задержку
        setTimeout(() => {
            receiveResponse(newEdgeId, text);
        }, CHAT_CONFIG.BOT_RESPONSE_DELAY);
    };
    
    // Получение ответа от бота (создаёт узел и связывает его с ребром)
    const receiveResponse = (edgeId, requestText) => {
        const newNodeId = generateId();
        const responseText = `Эхо: ${requestText}`;
        const newNode = {
            id: newNodeId,
            parentEdgeId: edgeId,
            text: responseText,
            createdAt: new Date().toISOString(),
            childrenEdgeIds: [],
            lastVisitedLeaf: null
        };
        
        setNodes(prev => ({ ...prev, [newNodeId]: newNode }));
        
        setEdges(prev => {
            const updatedEdge = { ...prev[edgeId], toNodeId: newNodeId };
            return { ...prev, [edgeId]: updatedEdge };
        });
        
        setCursor({ currentNodeId: newNodeId });
    };
    
    // Редактирование сообщения: создаёт новое ребро, образуя новую ветку
    const editMessage = (originalEdgeId, newText) => {
        if (!newText.trim()) return;
        const originalEdge = edges[originalEdgeId];
        if (!originalEdge) return;
        
        const fromNodeId = originalEdge.fromNodeId;
        const newEdgeId = generateId();
        const newEdge = {
            id: newEdgeId,
            fromNodeId,
            text: newText,
            kind: 'user',
            createdAt: new Date().toISOString(),
            editOfEdgeId: originalEdgeId
        };
        
        setEdges(prev => ({ ...prev, [newEdgeId]: newEdge }));
        
        
        // Обновляем lastVisitedLeaf для предков текущей ветки перед переключением
        const updateLastVisitedLeaf = (nodeId) => {
            let current = nodes[nodeId];
            const leaf = nodeId;
            const updates = {};
            
            while (current) {
                updates[current.id] = {
                    ...current,
                    lastVisitedLeaf: leaf
                };
                
                if (!current.parentEdgeId) break;
                const parentEdge = edges[current.parentEdgeId];
                if (!parentEdge) break;
                current = nodes[parentEdge.fromNodeId];
            }
            
            setNodes(prev => ({
                ...prev,
                ...updates
            }));
        };

        updateLastVisitedLeaf(cursor.currentNodeId);

        setNodes(prev => {
            const parentNode = prev[fromNodeId];
            const updatedNode = {
                ...parentNode,
                childrenEdgeIds: [...(parentNode.childrenEdgeIds || []), newEdgeId]
            };
            return { ...prev, [fromNodeId]: updatedNode };
        });

        // Эмулируем ответ бота для нового ребра
        setTimeout(() => {
            receiveResponse(newEdgeId, newText);
        }, CHAT_CONFIG.BOT_RESPONSE_DELAY);
        
        if (onMessageEdit && typeof onMessageEdit === 'function') {
            onMessageEdit({
                originalEdgeId,
                newEdgeId,
                newText,
                editedAt: new Date().toISOString()
            });
        }
    };
    
    // Переключение ветки для конкретного сообщения.
    // selectedEdgeId – ребро, которое выбрали для переключения.
    const switchBranch = (selectedEdgeId) => {
        const edge = edges[selectedEdgeId];
        if (!edge) return;
        
        const targetNode = nodes[edge.toNodeId];
        if (!targetNode) return;

        // Обновляем lastVisitedLeaf для всех предков текущего узла перед переключением
        const updateLastVisitedLeaf = (nodeId) => {
            let current = nodes[nodeId];
            const leaf = nodeId;
            const updates = {};
            
            while (current) {
                updates[current.id] = {
                    ...current,
                    lastVisitedLeaf: leaf
                };
                
                if (!current.parentEdgeId) break;
                const parentEdge = edges[current.parentEdgeId];
                if (!parentEdge) break;
                current = nodes[parentEdge.fromNodeId];
            }
            
            setNodes(prev => ({
                ...prev,
                ...updates
            }));
        };

        // Обновляем lastVisitedLeaf перед переключением
        updateLastVisitedLeaf(cursor.currentNodeId);
        
        // Переходим к последнему посещенному листу в целевом поддереве
        const leafNodeId = targetNode.lastVisitedLeaf || targetNode.id;
        setCursor({ currentNodeId: leafNodeId });
    };
    
    // Для отображения «линейного» диалога получаем последовательность пар: сообщение -> ответ
    const getConversationPath = () => {
        const conversation = [];
        let current = nodes[cursor.currentNodeId];
        
        // Собираем путь от текущего узла до корня
        while (current && current.parentEdgeId) {
            const edge = edges[current.parentEdgeId];
            if (!edge) break;
            
            // Добавляем пару сообщение-ответ в конец массива
            conversation.push({ edge, node: current });
            
            // Переходим к следующему узлу
            current = nodes[edge.fromNodeId];
        }
        
        // Разворачиваем массив один раз в конце
        return conversation.reverse();
    };
    
    // ========= Обработчики UI =========
    
    const handleSend = (e) => {
        e.preventDefault();
        sendMessage(inputValue);
        setInputValue('');
    };
    
    const startEditing = (edgeId, text) => {
        setEditingEdgeId(edgeId);
        setEditingText(text);
    };
    
    const cancelEditing = () => {
        setEditingEdgeId(null);
        setEditingText('');
    };
    
    const saveEdit = (edgeId) => {
        editMessage(edgeId, editingText);
        cancelEditing();
    };
    
    const conversation = getConversationPath();
    
    return (
        <div className="flex flex-col h-screen max-w-4xl mx-auto bg-white shadow-lg">
            {/* Заголовок */}
            <div className="bg-gradient-to-r from-blue-500 to-blue-600 text-white p-4 shadow-md">
                <h1 className="text-2xl font-bold">Чат с версионированием (дерево)</h1>
                <p className="text-sm opacity-90">Сообщения хранятся как дерево: ребро — ваше сообщение, узел — ответ ассистента.</p>
            </div>
            
            {/* Область диалога */}
            <div className="flex-1 overflow-y-auto p-4 space-y-3">
                {conversation.length === 0 && (
                    <p className="text-gray-600">Начните диалог, отправив сообщение...</p>
                )}
                {conversation.map(({ edge, node }, idx) => {
                    // Определяем родительский узел, чтобы отобразить переключатель для веток,
                    // если у него более одного дочернего ребра
                    const parentNode = nodes[edge.fromNodeId];
                    const showSwitcher = parentNode && parentNode.childrenEdgeIds && parentNode.childrenEdgeIds.length > 1;
                    return (
                        <div key={edge.id} className="flex flex-col">
                            <div className="flex justify-end">
                                <div className="bg-blue-500 text-white rounded-lg px-4 py-2">
                                    {editingEdgeId === edge.id ? (
                                        <div>
                                            <textarea
                                                rows="2"
                                                value={editingText}
                                                onChange={(e) => setEditingText(e.target.value)}
                                                className="w-full p-2 text-sm text-gray-800 rounded border border-gray-300"
                                            />
                                            <div className="flex gap-2 mt-1">
                                                <button onClick={() => saveEdit(edge.id)} className="px-3 py-1 text-xs bg-green-500 text-white rounded hover:bg-green-600">Сохранить</button>
                                                <button onClick={cancelEditing} className="px-3 py-1 text-xs bg-gray-500 text-white rounded hover:bg-gray-600">Отмена</button>
                                            </div>
                                        </div>
                                    ) : (
                                        <div className="flex items-center">
                                            <span>{edge.text}</span>
                                            <button 
                                                onClick={() => startEditing(edge.id, edge.text)}
                                                className="ml-2 px-2 py-0.5 text-xs bg-white bg-opacity-20 rounded hover:bg-opacity-30"
                                            >
                                                ✏️
                                            </button>
                                        </div>
                                    )}
                                    <div className="text-xs opacity-70 mt-1">
                                        {new Date(edge.createdAt).toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })}
                                        {edge.editOfEdgeId && <span> (изменено)</span>}
                                    </div>
                                </div>
                            </div>
                            {showSwitcher && (
                                <div className="flex justify-center items-center py-1">
                                    {parentNode.childrenEdgeIds.map((childEdgeId, i) => {
                                        // Активной считается та ветка, чей ребро совпадает с текущим edge
                                        const isActive = childEdgeId === edge.id;
                                        return (
                                            <button
                                                key={childEdgeId}
                                                onClick={() => switchBranch(childEdgeId)}
                                                className={`mx-1 px-2 py-1 border rounded ${isActive ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'}`}
                                            >
                                                {i + 1}
                                            </button>
                                        );
                                    })}
                                </div>
                            )}
                            {node && (
                                <div className="flex justify-start mt-2">
                                    <div className="bg-green-100 text-gray-800 rounded-lg px-4 py-2">
                                        <div className="text-sm">{node.text}</div>
                                        <div className="text-xs opacity-70 mt-1">
                                            {new Date(node.createdAt).toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })}
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    );
                })}
                <div ref={messagesEndRef} />
            </div>
            
            {/* Поле ввода */}
            <form onSubmit={handleSend} className="p-4 bg-gray-50 border-t">
                <div className="flex gap-2">
                    <input
                        type="text"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        className="flex-1 px-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Введите сообщение..."
                    />
                    <button type="submit" className="px-6 py-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500">
                        Отправить
                    </button>
                </div>
            </form>
            
            {/* Пример навигации: возможность jump to node (для демонстрации) */}
            <div className="p-3 border-t bg-blue-50 text-center text-xs text-gray-600">
                <span onClick={() => setCursor({currentNodeId: CHAT_CONFIG.INITIAL_NODE_ID})} className="underline cursor-pointer">
                    Вернуться к началу диалога
                </span>
            </div>
        </div>
    );
};

export default Chat;