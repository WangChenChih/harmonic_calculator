# 簡介

對於樂理差勁如我的人來說，計算泛音按弦位置實在是惡夢。且樂理實在太難學，相較之下，物理還是比較平易近人。抱持著不學樂理就學物理的心態，在這裡我想要向大家介紹**泛音計算機**。這個程式使用起來直觀，我已經在檔案```harmonic_calculator.ipynb```裡寫了一個例子。只需要按照相似之用法就可以享受一秒算出泛音的快感。

注意：此程式使用numpy，在使用之前請先在執行的environment中安裝好。

# 物理原理
在這邊介紹一下物理原理。

## 自然泛音
自然泛音產生方式是用手指虛按弦上特定位置，使得「該指至千斤之距離」與「該指至琴碼的距離」成簡單整數比。今天假設「千斤至琴碼之距離」為 $L$ 且「該指至千斤之距離」為 $L'$，並假設該指與千斤之間有 $m$ 個波腹，則以下方成組必須被滿足

$$
\begin{align}
& L' = \frac{m}{2f_g} \quad ; \quad m \in \mathbb{N} \\
& L - L' = \frac{n}{2f_g} \quad ; \quad n \in \mathbb{N} \\
& L - L' = \frac{1}{2f_0}
\end{align}
$$

第一條式子要求「該指至千斤」之間有 $m$ 個波腹，並且我們欲產生之泛音頻率為 $f_g$ ；第二條式子要求「該指與千斤之間的距離」與「該指至琴碼的距離」為簡單整數比從而使駐波可以生成；第三條式子要求該指按弦處之理論實音頻率為 $f_0$ 。經過整理，可以簡化為

$$
\frac{f_g}{f_0} = n \quad ; \quad n\in\mathbb{N}
$$

因此，只需要透過迴圈尋找所有可能的按弦處使得上述兩條方程式被滿足，我們就可以找到拉出自然泛音 $f_g$ 的方法。


## 人工泛音
以二胡為例，人工泛音的產生方式通常為一指按實音，而用四指虛按某特定處。原理是因為「一指與四指之間的距離」與「四指至琴碼的距離」成簡單整數比，使得駐波可以一指與琴碼間產生，而第二指則負責為強制波節點。今天假設「千斤至琴碼之距離」為 $L$ 、「食指至千斤之距離」為 $L'$ 、「食指與第二指之間的距離」為 $l$，並假設食指與第二指之間只含有一個波腹，則需要滿足以下方成組

$$
\begin{align}
& L-L' = nl  \quad ; n\in\mathbb{N} \\
& l = \frac{1}{2f_g} \\
& L-L' = \frac{1}{2f_1} \\
& L-L'-l = \frac{1}{2f_2}
\end{align}
$$

第一條式子要求「一指與四指之間的距離」與「四指至琴碼的距離」為整數比從而使駐波可以生成；第二條式子要求產生之駐波頻率為 $f_g$ ；第三條式子要求一指按弦處之實音頻率為 $f_1$　；最後一條式子要求第二指按弦處之理論實音頻率為 $f_2$　。經過整理，我們可以得到簡化條件

$$
\begin{align}
& \frac{f_g}{f_1} = n \in \mathbb{N} \\
& \frac{f_g}{f_2} = n-1 \\
\end{align}
$$

因此，只需要透過迴圈尋找所有可能的一指與四指按弦處之組合使得上述兩條方程式被滿足，我們就可以找到拉出人工泛音 $f_g$ 的方法。

# 使用說明
在計算之前請先 import package（建議開一個Jupyter Notebook來執行，或者直接使用此 repository 中的檔案```harmonic_calculator.ipynb```）

```
from harmonic_calculator import harmonic
```

並設定空弦

```
har = harmonic(open_string_pitch="D", open_string_octave=4)
```

變數```open_string_pitch```代表空弦音高之音名，而```open_string_octave```則指其位於之八度位置。舉例：中央C的音名為C4，因此其對應的```open_string_pitch```為字串```"C"```，並且```open_string_octave```為整數```4```。至於升降則需要用 ```_sharp``` 與 ```_flat``` 來表示，例如 ♯C 應記為```C_sharp``` ，而 ♭D 應記為 ```D_flat```。

## 自然泛音
函數

```
calculate_natural_harmonic(pitch_name_goal="C", octave_goal=6)
```

將輸出虛按弦處音高（```position: ```）。其中```pitch_name_goal```為欲產生之自然泛音之音名，而```octave_goal```為其所在之八度位置。

## 人工泛音
函數

```
calculate_artificial_harmonic(pitch_name_goal, octave_goal)
```

將輸出食指按弦處之實音音高與（```forefinger: ```）四指按弦處之實音音高（```pinkie: ```）。其中```pitch_name_goal```為欲產生之人工泛音之音名，而```octave_goal```為其所在之八度位置。