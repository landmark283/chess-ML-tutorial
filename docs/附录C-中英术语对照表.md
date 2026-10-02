# 附录 C｜中英术语对照表

> **为什么需要它**：你查资料时，遇到的坑大多不是"不懂概念"，而是"**不知道它的英文名**"。
> 搜 `sklearn 交叉验证` 出来的多半是中文博客的二手总结；搜 `sklearn cross_val_score` 出来的是一手文档。
> **本表按课程分组，学到哪查到哪。**

---

## C.1 机器学习基础概念

| 中文 | 英文 | 一句话 | 在哪一课 |
|---|---|---|---|
| 特征 | feature | 喂给模型的输入数字 | L03 |
| 标签 / 目标 | label / target | 模型要预测的正确答案 | L03 |
| 样本 | sample / instance | 一行数据 | L03 |
| 特征矩阵 | feature matrix（`X`） | 形状 `(n_samples, n_features)` | L03 |
| 目标向量 | target vector（`y`） | 形状 `(n_samples,)` | L03 |
| 表示 / 目标 / 优化 | representation / objective / optimization | 机器学习的三个问题 | L03 |
| 参数 | parameter | 模型**学出来**的东西（如权重 `w`） | L03 |
| 超参数 | hyperparameter | **你设**的东西（如学习率、树深） | L05 |
| 训练集 / 验证集 / 测试集 | training / validation / test set | 三份数据的职责不同 | L05 |
| 泛化 | generalization | 在没见过的数据上表现好 | L03 |
| 过拟合 | overfitting | 背下了训练集 | L03 |
| 欠拟合 | underfitting | 连训练集都没学好 | L03 |
| 偏差 / 方差 | bias / variance | 系统性错 / 不稳定 | L05 |
| 正则化 | regularization | 惩罚模型复杂度 | L03 |
| L1 / L2 正则 | Lasso / Ridge | 让权重稀疏 / 让权重变小 | L03 |
| 损失函数 | loss function / cost function | "错得多离谱"的度量 | L03 |
| 梯度下降 | gradient descent | 沿最陡的下坡方向挪一步 | L03 |
| 学习率 | learning rate | 每步挪多远 | L03 |
| 收敛 | convergence | 不再明显变好 | L03 |
| 批量 / 随机 / 小批量 | batch / stochastic / mini-batch | 每次用多少数据算梯度 | L03 |
| 特征缩放 / 标准化 | feature scaling / standardization | 把不同量纲拉到一起 | L07 |
| 流水线 | pipeline | 预处理 + 模型打包 | L07 |
| 基线 | baseline | 先做个笨办法当参照 | L05 |

---

## C.2 分类与评估

| 中文 | 英文 | 一句话 | 在哪一课 |
|---|---|---|---|
| 回归 / 分类 / 聚类 | regression / classification / clustering | 预测数值 / 预测类别 / 分组 | L03 |
| 二分类 / 多分类 | binary / multiclass | 两类 / 多类 | L04 |
| 逻辑回归 | logistic regression | 名字叫回归，其实是分类器 | L04 |
| sigmoid / logistic 函数 | sigmoid | 把任意实数压到 (0, 1) | L04 |
| 对数几率 | log-odds / logit | `log(p / (1-p))` | L04 |
| 交叉熵 | cross-entropy | 分类的标准损失 | L04 |
| 决策边界 | decision boundary | 分开两类的面 | L04 |
| 阈值 | threshold | 概率大于多少算正类 | L04 |
| 混淆矩阵 | confusion matrix | TP / FP / FN / TN 四个格 | L04 |
| 准确率 | accuracy | 猜对的比例（不平衡数据会骗人） | L04 |
| 精确率 | precision | 说是正类的里面有多少真的是 | L04 |
| 召回率 | recall / sensitivity | 真的正类里抓出来多少 | L04 |
| F1 | F1 score | 精确率和召回率的调和平均 | L04 |
| 特异性 | specificity | 真负类里正确排除多少 | L04 |
| 类别不平衡 | class imbalance | 正负样本数量悬殊 | L04 |
| 上采样 / 下采样 | over-/undersampling | 调样本比例 | L04 |
| 类别权重 | class_weight | 让少数类更"值钱" | L04 |
| ROC 曲线 / AUC | ROC curve / AUC / AUROC | 各阈值下的表现 | L04 |
| PR 曲线 / 平均精度 | PR curve / average precision | 不平衡数据更该看这个 | L04 |
| 概率校准 | probability calibration | 说 0.7 就真有 70% | L04 |
| 可靠性图 | reliability diagram / calibration curve | 画校准好不好的图 | L04 |
| 布里尔分数 | Brier score | 概率预测的均方误差 | L04 |
| 群体智能？❌ | — | — | — |
| 对数损失 | log loss | 交叉熵的别名 | L04 |

---

## C.3 评估方法论

| 中文 | 英文 | 一句话 | 在哪一课 |
|---|---|---|---|
| 数据泄漏 | data leakage | 训练时偷看了不该看的信息 | L05 |
| 交叉验证 | cross-validation（CV） | 轮流留一份出来当验证 | L05 |
| K 折 | K-fold | 切成 K 份 | L05 |
| 分层 | stratified | 保持各类比例 | L05 |
| 分组 | grouped | 同一组的数据不能跨折 | L05 |
| 时间序列划分 | time series split | 只用过去预测未来 | L05 |
| 嵌套交叉验证 | nested CV | 调参也在 CV 里面做 | L05 |
| 学习曲线 | learning curve | 数据量 vs 分数 | L05 |
| 验证曲线 | validation curve | 超参数 vs 分数 | L05 |
| 网格搜索 | grid search | 穷举超参数组合 | L05 |
| 随机搜索 | random search | 随机采样超参数（高维更划算） | L05 |
| 贝叶斯优化 | Bayesian optimization | 用模型猜下一个该试哪里 | L05 |
| 特征重要性 | feature importance | 哪个特征有用 | L06 |
| 置换重要性 | permutation importance | 打乱某列看分数掉多少 | L06 |
| 部分依赖图 | partial dependence plot（PDP） | 某特征变化时预测怎么变 | L06 |
| 消融实验 | ablation study | 拿掉一块看掉多少 | L07 |

---

## C.4 模型

| 中文 | 英文 | 一句话 | 在哪一课 |
|---|---|---|---|
| 线性回归 | linear regression | `y = w·x + b` | L03 |
| 最小二乘 | ordinary least squares（OLS） | 平方误差最小 | L03 |
| 岭回归 | Ridge | L2 正则的线性回归 | L03 |
| 套索 | Lasso | L1 正则（会稀疏） | L03 |
| 弹性网 | ElasticNet | L1 + L2 | L03 |
| 决策树 | decision tree | 一系列 if-else | L06 |
| 基尼不纯度 | Gini impurity | 分裂时常用的不纯度 | L06 |
| 信息增益 / 熵 | information gain / entropy | 另一种分裂标准 | L06 |
| 剪枝 | pruning | 限制树的大小 | L06 |
| 随机森林 | random forest | 多棵树投票（bagging） | L06 |
| 袋装 | bagging | 有放回抽样训练多个模型 | L06 |
| 提升 | boosting | 一个接一个修正前一个的错 | L06 |
| 梯度提升 | gradient boosting | 拟合残差的 boosting | L06 |
| 直方图梯度提升 | HistGradientBoosting | sklearn 里快的那个实现 | L06 |
| XGBoost / LightGBM / CatBoost | — | 工业界三兄弟 | L06 |
| 支持向量机 | support vector machine（SVM） | 找最宽的分隔带 | 延伸 |
| 核技巧 | kernel trick | 隐式升维 | 延伸 |
| K 近邻 | k-nearest neighbors（KNN） | 看邻居是什么就猜什么 | 延伸 |
| 朴素贝叶斯 | Naive Bayes | 假装特征独立 | 延伸 |
| 集成 / 堆叠 | ensemble / stacking | 把多个模型合起来 | L06 |
| 混合 | blending | stacking 的简易版 | L06 |

---

## C.5 无监督学习（L11）

| 中文 | 英文 | 一句话 |
|---|---|---|
| K 均值 | K-means | 球状簇，要指定簇数 |
| 惯性 / 簇内平方和 | inertia / SSE | K-means 的簇紧不紧 |
| 肘部法 | elbow method | 看拐点选簇数 |
| 轮廓系数 | silhouette score | 簇分得好不好 |
| DBSCAN | — | 基于密度的聚类，能标噪声 |
| HDBSCAN | — | DBSCAN 的自适应版，不用指定簇数 |
| 主成分分析 | principal component analysis（PCA） | 线性降维 |
| 截断 SVD | truncated SVD | PCA 的稀疏文本版 |
| 非负矩阵分解 | non-negative matrix factorization（NMF） | 部件式分解 |
| t-SNE | t-distributed stochastic neighbor embedding | 可视化用，别当特征 |
| UMAP | uniform manifold approximation and projection | 更快、保留更多全局结构 |
| 异常检测 | anomaly / outlier detection | 找出怪家伙 |
| 孤立森林 | Isolation Forest | 随机切分，容易孤立的算异常 |
| 局部离群因子 | local outlier factor（LOF） | 看局部密度 |
| 单类 SVM | one-class SVM | 只学"正常"长什么样 |

---

## C.6 强化学习（L09 / L10 / L12 / L14）

| 中文 | 英文 | 一句话 |
|---|---|---|
| 智能体 / 环境 | agent / environment | 做决定的 / 被互动的 |
| 状态 / 动作 / 奖励 | state / action / reward | `s` / `a` / `r` |
| 策略 | policy（`π`） | 状态下选动作的规则 |
| 回报 | return（`G`） | 折扣后的累计奖励 |
| 折扣因子 | discount factor（`γ`） | 未来奖励打几折 |
| 幕 | episode | 从开始到结束的一局 |
| 值函数 | value function（`V(s)`） | 这状态值多少 |
| 动作价值 | action-value（`Q(s,a)`） | 这状态做这动作值多少 |
| 贝尔曼方程 | Bellman equation | 值函数的递归定义 |
| 时序差分 | temporal difference（TD） | 用估计更新估计 |
| TD 误差 | TD error（`δ`） | `r + γV(s') − V(s)` |
| 自举 | bootstrapping | 用还没学对的估计去更新另一个 |
| 资格迹 | eligibility trace | 记住"最近走过哪" |
| 探索 / 利用 | exploration / exploitation | 试新的 / 用已知最好的 |
| ε-贪心 | ε-greedy | 以 ε 概率随机 |
| 蒙特卡洛 | Monte Carlo（MC） | 跑到终局再回头更新 |
| 同策略 / 异策略 | on-policy / off-policy | 学的策略和走的策略是不是同一个 |
| 自对弈 | self-play | 自己跟自己下 |
| 经验回放 | experience replay | 把旧数据存起来反复用 |
| 回放缓冲区 | replay buffer | 存旧数据的地方 |
| 策略梯度 | policy gradient | 直接优化策略 |
| 演员-评论家 | actor-critic | 策略 + 值函数一起学 |
| 策略头 / 价值头 | policy head / value head | 一个网络两个输出 |
| 门控 | gating | 新模型要过关才替换旧的 |
| 温度 | temperature | 控制采样随机程度 |
| 狄利克雷噪声 | Dirichlet noise | 给根节点加探索噪声 |
| 平台期 | plateau | 怎么练都不涨 |

---

## C.7 棋类 AI 与搜索

| 中文 | 英文 | 一句话 |
|---|---|---|
| 博弈树 | game tree | 所有可能的走法构成的树 |
| 分支因子 | branching factor（`b`） | 平均每步有几个选择 |
| 深度 | depth（`d`） | 往前看几层 |
| 极小化极大 | minimax | 你取最大、对手取最小 |
| 负极大值 | negamax | minimax 的等价简写 |
| Alpha-Beta 剪枝 | alpha-beta pruning | 剪掉不影响结果的分支 |
| α / β | alpha / beta | 已知的下界 / 上界 |
| 窗口 | window | `(α, β)` 这个区间 |
| 主变例搜索 | principal variation search（PVS） | 假设第一个最好 |
| 迭代加深 | iterative deepening | 先搜 1 层，再 2 层…… |
| 走法排序 | move ordering | 好走法先搜 |
| 置换表 | transposition table | 缓存算过的局面 |
| 佐布里斯特哈希 | Zobrist hashing | 棋盘状态的增量哈希 |
| 静态搜索 | quiescence search | 在"安静"的局面才停 |
| 地平线效应 | horizon effect | 深度刚好看不见灾难 |
| 杀手走法 | killer move | 上次在这层引起剪枝的走法 |
| 历史启发 | history heuristic | 常引起剪枝的走法加分 |
| 空着裁剪 | null-move pruning | 让对手白走一步试试 |
| 后期走法削减 | late move reduction（LMR） | 靠后的走法少搜一点 |
| 蒙特卡洛树搜索 | Monte Carlo tree search（MCTS） | 靠随机模拟评估 |
| 选择 / 扩展 / 模拟 / 回传 | selection / expansion / simulation / backpropagation | MCTS 四步 |
| 上限置信区间 | upper confidence bound（UCB） | 探索与利用的平衡 |
| UCT | UCT | 把 UCB1 装进树里 |
| 树内策略 / 树外策略 | tree policy / default policy | 树里怎么走 / 树外怎么模拟 |
| 先验概率 | prior（`P`） | 网络给的"这步看着不错" |
| PUCT | PUCT | 带先验的 UCT |
| 访问次数 | visit count（`N`） | 这个节点被考虑过几次 |
| 神经网络评估 | neural network evaluation | 用网络代替手工评估 |
| 自对弈训练 | self-play training | AlphaZero 那一套 |
| 局势评估 | position evaluation | 这局面好不好 |
| 和棋 / 必胜 / 必败 | draw / win / loss | 三种理论结果 |
| 求解（棋类） | solved | 已经算出完整答案 |
| 残局库 | endgame tablebase | 存好了残局答案 |
| 等级分 | Elo rating | 棋力的数字表示 |
| 置信区间 | confidence interval | 这个数字有多不准 |
| 局面（记谱） | position / FEN | 一个棋盘状态 |

---

## C.8 搜资料时的关键词模板

| 你想知道 | 搜什么 |
|---|---|
| 这个函数怎么用 | `sklearn <函数名> example` |
| 这个报错什么意思 | 直接复制报错原文（英文） |
| 这个算法怎么实现 | `<algorithm> python implementation` |
| 概念讲解 | `<concept> explained intuitively` |
| 怎么调参 | `<model> hyperparameter tuning guide` |
| 棋类具体做法 | `chess engine <技术名>` 或 `gomoku ai <技术名>` |
| 看权威定义 | `site:scikit-learn.org <关键词>` |
| 看论文 | `arxiv <关键词>` |

**优先级**：官方文档 > 论文 > Stack Overflow > 博客 > 知乎/CSDN。
（中文博客不是不能用，但**先看官方文档再看博客**，能省下大量被二手错误误导的时间。）
