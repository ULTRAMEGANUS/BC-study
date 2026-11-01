# Appendix D — Calculation Cheat Sheet｜附录 D　计算速查

## D-1　Significant Figures｜有效数字

**Counting rules｜计位规则**
1. Non-zero digits count｜非零数字都算。
2. Captive and trailing zeros after a decimal count｜小数中的 0 与小数末尾的 0 都算（1.005 → 4；2.50 → 3）。
3. Leading zeros never count｜前导零不算（0.0025 → 2）。
4. Exact/counted numbers and defined factors have unlimited s.f.｜精确数与定义量无限位（2 mol、100 cm ≡ 1 m）。

**Rounding rules｜运算规则**
- × ÷ → fewest s.f.｜乘除看位数
- + − → fewest decimal places｜加减看小数位
- carry 4–5 s.f. inside the chain, round **once** at the end｜链中保 4–5 位，最后只舍一次

```
0.0120 mol ÷ 25.00 mL → convert first: 0.02500 L
0.0120 / 0.02500 = 0.480 mol/L   (3 s.f. — limited by 0.0120)
```

## D-2　Dimensional Analysis: The Universal Five｜量纲分析万能五步

1. Write the **known** with its unit｜写出已知量（带单位）。
2. State the **wanted** unit｜写明目标单位。
3. Chain conversion factors that equal 1｜串"等于 1"的转换因子。
4. Cancel units diagonally on paper｜在纸上斜向约单位。
5. Round once, attach unit, sanity-check size｜只舍一次、带单位、量级自检。

```
wanted: molecules in 5.0 g H₂O
5.0 g × (1 mol/18.02 g) × (6.02×10²³/1 mol) = 1.7×10²³ molecules
        g cancels ✔            mol cancels ✔       2 s.f. ✔
```

## D-3　The Bridges: Dry and Solution Versions｜三桥与四桥

**Dry (Ch.8)｜摩尔三桥**

```
particles ⇄ (×/÷ 6.02×10²³) ⇄ mol ⇄ (×/÷ molar mass) ⇄ mass
```

**Solution (Ch.13)｜溶液版四桥**

```
mass ⇄ (÷M_mass) ⇄ mol ⇄ (×/÷ C) ⇄ volume(L)      C = mol/L
                                    dilution: C₁V₁ = C₂V₂ (units match, mL ok)
```

See Fig. 8-1 and Fig. 13-1 in the chapters for the drawn maps.｜图见正文 Fig. 8-1 与 Fig. 13-1。

## D-4　Stoichiometry: Four Steps + Limiting Methods｜计量四步与限量两法

**Mass–mass four steps｜质量对质量四步**

```
① balance  ② mass A ÷ M_A = mol A  ③ × ratio = mol B  ④ × M_B = mass B
```

**Limiting reagent｜限量试剂**
- Method 1 双假设: product from each reactant → smaller wins｜各自算产物，取小
- Method 2 系数比: mol ÷ coefficient → smaller wins｜除以系数，取小
- yield: use the **limiting** reagent only｜产量只用限量试剂

**Percentages｜三个百分比**

```
% yield  = actual / theoretical × 100%      (actual from lab; never >100% for pure dry product)
% purity = pure mass / sample mass × 100%   (apply BEFORE the mole bridge)
```

## D-5　Concentration, Dilution, Titration Card｜浓度·稀释·滴定卡

| Situation｜场景 | Formula｜公式 | Watch｜注意 |
|---|---|---|
| molarity 摩尔浓度 | M = mol ÷ V(L) | V must be litres｜体积必须升 |
| moles from solution 溶液取摩尔 | mol = M × V(L) | mL → ÷1000 first｜先换算 |
| dilution 稀释 | C₁V₁ = C₂V₂ | units match, not necessarily L｜单位一致即可 |
| titration 滴定 | mol titre × ratio = mol unknown | end point ≈ equivalence｜终点≈等当点 |
| gravimetry 重量分析 | mol ppt (1:1 typical) → mol target → mass | constant mass required｜必须恒重 |

**Final check ritual｜交卷三查**
1. 单位 Units — every line, all cancelling on paper｜每行带单位、纸上约尽。
2. 位数 s.f. — one rounding, matching the weakest input｜只舍一次、随最弱输入。
3. 守恒 Conservation — atoms both sides; charge sums equal｜原子左右等、电荷总和等。
