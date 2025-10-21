import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Login from './components/Login';
import Register from './components/Register';
import TradingViewChart from './components/TradingViewChart';
import './App.css';

const Wallet = ({ wallets }) => (
    <div>
        <h2>Кошелек</h2>
        {wallets.map(wallet => (
            <p key={wallet.currency}>{wallet.currency}: {wallet.balance.toFixed(2)}</p>
        ))}
    </div>
);

const OrderForm = ({ token }) => {
    const [quantity, setQuantity] = useState('');
    const [side, setSide] = useState('BUY');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post('/api/trades/orders', {
                symbol: 'BTC/USD',
                side,
                order_type: 'MARKET',
                quantity: parseFloat(quantity),
            }, { headers: { Authorization: `Bearer ${token}` } });
            alert('Ордер успешно размещен!');
            setQuantity('');
        } catch (error) {
            console.error('Не удалось разместить ордер:', error);
            alert('Не удалось разместить ордер. Проверьте баланс и попробуйте снова.');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Разместить ордер</h2>
            <select value={side} onChange={e => setSide(e.target.value)}>
                <option value="BUY">Купить</option>
                <option value="SELL">Продать</option>
            </select>
            <input
                type="number"
                placeholder="Количество"
                value={quantity}
                onChange={e => setQuantity(e.target.value)}
            />
            <button type="submit">Разместить ордер</button>
        </form>
    );
};

const Positions = ({ positions }) => (
    <div>
        <h2>Позиции</h2>
        <table>
            <thead>
                <tr>
                    <th>Символ</th>
                    <th>Количество</th>
                    <th>Цена входа</th>
                    <th>P&L</th>
                </tr>
            </thead>
            <tbody>
                {positions.map(pos => (
                    <tr key={pos.id}>
                        <td>{pos.symbol}</td>
                        <td>{pos.quantity}</td>
                        <td>{pos.entry_price.toFixed(2)}</td>
                        <td>{pos.pnl.toFixed(2)}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    </div>
);


function App() {
    const [token, setToken] = useState(localStorage.getItem('token'));
    const [wallets, setWallets] = useState([]);
    const [positions, setPositions] = useState([]);
    const [symbol, setSymbol] = useState('bitcoin');

    useEffect(() => {
        if (token) {
            localStorage.setItem('token', token);
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

            const fetchUserData = async () => {
                const walletsRes = await axios.get('/api/wallet/');
                setWallets(walletsRes.data);
                const positionsRes = await axios.get('/api/trades/positions');
                setPositions(positionsRes.data);
            };

            fetchUserData();
            const interval = setInterval(fetchUserData, 5000); // Обновляем данные каждые 5 секунд
            return () => clearInterval(interval);
        } else {
            localStorage.removeItem('token');
            delete axios.defaults.headers.common['Authorization'];
        }
    }, [token]);

    const handleLogout = () => {
        setToken(null);
    };

    if (!token) {
        return (
            <div>
                <Login setToken={setToken} />
                <Register />
            </div>
        );
    }

    return (
        <div className="App">
            <header>
                <h1>Симулятор Криптобиржи</h1>
                <div>
                    <select value={symbol} onChange={e => setSymbol(e.target.value)}>
                        <option value="bitcoin">Bitcoin</option>
                        <option value="ethereum">Ethereum</option>
                        <option value="ripple">Ripple</option>
                    </select>
                    <button onClick={handleLogout}>Выйти</button>
                </div>
            </header>
            <main>
                <div className="chart-container">
                    <TradingViewChart symbol={symbol} />
                </div>
                <div className="sidebar">
                    <Wallet wallets={wallets} />
                    <OrderForm token={token} />
                    <Positions positions={positions} />
                </div>
            </main>
        </div>
    );
}

export default App;
