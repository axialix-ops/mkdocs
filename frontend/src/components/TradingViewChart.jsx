import React, { useEffect, useRef } from 'react';
import { createChart } from 'lightweight-charts';

const TradingViewChart = () => {
    const chartContainerRef = useRef();
    const candleSeriesRef = useRef();

    useEffect(() => {
        const chart = createChart(chartContainerRef.current, {
            width: 900,
            height: 500,
            layout: {
                backgroundColor: '#131722',
                textColor: 'rgba(255, 255, 255, 0.9)',
            },
            grid: {
                vertLines: {
                    color: 'rgba(197, 203, 206, 0.5)',
                },
                horzLines: {
                    color: 'rgba(197, 203, 206, 0.5)',
                },
            },
            crosshair: {
                mode: 'normal',
            },
            rightPriceScale: {
                borderColor: 'rgba(197, 203, 206, 0.8)',
            },
            timeScale: {
                borderColor: 'rgba(197, 203, 206, 0.8)',
                timeVisible: true,
                secondsVisible: false,
            },
        });

        candleSeriesRef.current = chart.addCandlestickSeries({
            upColor: '#26a69a',
            downColor: '#ef5350',
            borderDownColor: '#ef5350',
            borderUpColor: '#26a69a',
            wickDownColor: '#ef5350',
            wickUpColor: '#26a69a',
        });

        const ws = new WebSocket(`ws://${window.location.host.replace('3000', '8000')}/ws/prices`);

        ws.onopen = () => {
            console.log("WebSocket connection opened");
        };

        ws.onmessage = (event) => {
            const candleData = JSON.parse(event.data);
            // Преобразуем время из ISO-строки в Unix-таймстемп
            candleData.time = new Date(candleData.time).getTime() / 1000;
            candleSeriesRef.current.update(candleData);
        };

        ws.onclose = () => {
            console.log("WebSocket connection closed");
        };

        ws.onerror = (error) => {
            console.error("WebSocket error:", error);
        };


        return () => {
            ws.close();
            chart.remove();
        };
    }, []);

    return <div ref={chartContainerRef} />;
};

export default TradingViewChart;
