# Snake-AI manual

## SnakeEnv 可調用的member function & variable
*  `__init__(game_board_size, snake_color, fruit_color, gui)`：初始化遊戲介面


| 參數名稱          | 格式                                           |
|:----------------- |:---------------------------------------------- |
| `game_baord_size` | int, 建構邊長為為`game_baord_size`的正方形地圖 |
| `snake_color`     | (R, G, B), 指定蛇的顏色                        |
| `fruit_color`     | (R, G, B), 指定水果的顏色                      |
| `gui`             | True/False, 是否開啟圖形化介面                 |

*  `reset()`：將遊戲重新設為初始值
*  `new_fruit()`：將原有的水果刪除，新增另一個水果
*  `change_snake_dir(new_dir)`：更改蛇的方向，輸入須為編碼後的結果

| 方向  | 編碼 |
| ----- |:---------------- |
| `up`    | `(1, 0, 0, 0)`     |
| `down`  | `(0, 1, 0, 0)`     |
| `left`  | `(0, 0, 1, 0)`     |
| `right` | `(0, 0, 0, 1)`     |

*  `step()`:以當前蛇的方向移動一格，回傳蛇的狀態

| 回傳值 | 蛇的狀態            |
| ------ | ------------------- |
| `1`      | 蛇吃到分數          |
| `0`      | 蛇走到空的一格      |
| `-1`     | 蛇發生碰撞 遊戲結束 |
* `render()`:渲染當前畫面
* `keyboard_control()`：使用鍵盤控制蛇

