# 使用方法

先 make 好，cd 到 main 在的資料夾，執行

```
python <path_to_judge.py> 1 2 3
```

## Subtask 1

只有 SIGALRM，沒有 SIGTSTP。

沒有 max_subarray(async_read)

## Subtask 2

有 SIGALRM，有 SIGTSTP。

沒有 max_subarray(async_read)

## Subtask 3

有 SIGALRM，有 SIGTSTP。

有 max_subarray(async_read)

如果只要測 subtask 1,2 可以:

```
python <path_to_judge.py> 1 2
```

## Output

結果會出現在 test_result 這個資料夾中，.out 為你的輸出，.ans 為正確答案。
