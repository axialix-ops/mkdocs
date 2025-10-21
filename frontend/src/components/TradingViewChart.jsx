import React, { useEffect, useRef, useState } from 'react';
import { createChart } from 'lightweight-charts';

const TradingViewChart = ({ symbol = 'bitcoin' }) => {
    const chartContainerRef = useRef();
    const candleSeriesRef = useRef();
    const chartRef = useRef();
    const resizeObserverRef = useRef();

    useEffect(() => {
        chartRef.current = createChart(chartContainerRef.current, {
            width: chartContainerRef.current.clientWidth,
            height: chartContainerRef.current.clientHeight,
            layout: {
                backgroundColor: '#000000',
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

        const ws = new WebSocket(`ws://${window.location.host.replace('3000', '8000')}/ws/prices/${symbol}`);

        ws.onopen = () => {
            console.log(`WebSocket connection opened for ${symbol}`);
        };

        ws.onmessage = (event) => {
            const candleData = JSON.parse(event.data);
            if (candleData.symbol === symbol) {
                candleSeriesRef.current.update(candleData);
            }
        };

        ws.onclose = () => {
            console.log("WebSocket connection closed");
        };

        ws.onerror = (error) => {
            console.error("WebSocket error:", error);
        };


        return () => {
            ws.close();
            if (resizeObserverRef.current) {
                resizeObserverRef.current.disconnect();
            }
            if (chartRef.current) {
                chartRef.current.remove();
            }
        };
    }, [symbol]);

    useEffect(() => {
        resizeObserverRef.current = new ResizeObserver(entries => {
            const { width, height } = entries[0].contentRect;
            if (chartRef.current) {
                chartRef.current.applyOptions({ width, height });
            }
        });

        if (chartContainerRef.current) {
            resizeObserverRef.current.observe(chartContainerRef.current);
        }

        return () => {
            if (resizeObserverRef.current) {
                resizeObserverRef.current.disconnect();
            }
        };
    }, []);

    return <div ref={chartContainerRef} style={{ width: '100%', height: '100vh' }} />;
};

export default TradingViewChart;
