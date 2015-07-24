---
layout:     post
title:      "测试公式"
date:       2015-01-15 01:43:53
author:     平芜泫
category:   日记
tags:
    - 测试文章
---

公式在摘要中，通过 Pelican 标准的 render_math 插件可能不会被渲染，而我改造的插件应该能。

测试行内公式：\\(\sqrt{2}\\) 是一个无理数。

单行公式总是会被单独拆开：$$\int_{-\infty}^{\infty} e^{-\frac{x^2}{2}} \,dx$$。

在多行公式中可以使用子环境：

\\[
f(x) =
\begin{cases}
    x^2 & ,x < 1  \\\\
    \sqrt{x} & ,x \geq 1
\end{cases}
\\]

对齐多行公式使用 `array` 子环境。

$$
\begin{array}{rcl}
    S(x) &=& \int_{-\infty}^\infty \frac{cos(t x)}{\pi (1+t^2)} \,dt \\\\
         &=& e^{-t |x|}
\end{array}
$$
