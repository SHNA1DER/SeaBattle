import pytest
from unittest import mock


# Импортируем функцию draw_point
from ..src.SeaBattle import draw_point

@mock.patch('..src.SeaBattle.canvas')
def test_draw_point_zero(mock_canvas):
    # Создаем mock для enemy_ships1
    enemy_ships1 = [[0]]
    
    # Вызываем функцию
    draw_point(0, 0)
    
    # Проверяем, что create_text был вызван с правильными параметрами
    mock_canvas.create_text.assert_called_once_with(
        10,  # Примерное значение координаты X
        20,  # Примерное значение координаты Y
        text='💦',
        font=(60, 60),
        fill="lightcyan",
    )

@mock.patch('..src.SeaBattle.canvas')
def test_draw_point_greater_than_zero(mock_canvas):
    # Создаем mock для enemy_ships1
    enemy_ships1 = [[1]]
    
    # Вызываем функцию
    draw_point(0, 0)
    
    # Проверяем, что create_text был вызван три раза с правильными параметрами
    assert mock_canvas.create_text.call_count == 3
    calls = [
        mock.call(10, 20, text='💥', font=(80, 80), fill="white"),  # Примерные значения координат
        mock.call(10, 20, text='💥', font=(60, 60), fill="orange"),
        mock.call(10, 20, text='💥', font=(35, 35), fill="red")
    ]
    mock_canvas.create_text.assert_has_calls(calls)