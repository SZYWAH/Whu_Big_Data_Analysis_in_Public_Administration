# AI学术综述

## 一、研究背景与问题界定

人工智能（AI）作为引领新一轮科技革命和产业变革的战略性技术，其发展已从实验室的理论探索，全面渗透至社会经济各领域，成为驱动新质生产力发展的核心引擎[7][39]。当前，AI研究与实践正经历从“专用智能”向“通用智能”的范式转变，其核心驱动力源于算法模型的持续演进、海量数据资源的爆炸式增长以及算力基础设施的不断突破[9][13]。在这一进程中，AI不仅重塑了传统产业的生产与服务模式，如智能制造、智慧医疗、智能交通等，更在科学研究（如AI for Science）、社会治理、文化创意等领域催生出全新的应用场景[5][8][15][23]。

然而，AI技术的迅猛发展也伴生着一系列亟待厘清与解决的关键问题。在技术层面，模型结构如何兼顾强大性能与高效推理，训练数据如何保障质量、规模与合规性，以及如何构建公正、全面的评测基准以客观衡量AI能力，是制约技术纵深发展的瓶颈[11][30]。在应用与落地层面，AI系统的安全性、鲁棒性、可解释性，以及其在垂直行业深度融合时面临的工程化挑战，构成了技术从“可用”到“好用”的关键障碍[2][26]。此外，AI的广泛部署引发了关于就业结构、伦理规范、法律权责与社会公平的深刻讨论[4][21][36][40]。因此，本综述旨在系统梳理AI技术在模型结构、训练数据、推理效率、评测基准、安全性与工程落地等方面的最新进展，分析其演进脉络、关键技术突破与实验评测比较，并探讨部署实践中的安全挑战与未来发展趋势，以期为AI技术的健康发展与负责任应用提供学术参考。

## 二、主要研究进展

### 2.1 模型与算法演进：从规模驱动到效率与智能并重

近年来，AI模型，尤其是大语言模型（LLM）和基础模型，呈现出参数规模急剧扩增的趋势，通过在海量无标注数据上进行预测练，获得了令人瞩目的泛化与涌现能力[11]。然而，单纯的规模扩展面临边际效益递减、能耗剧增和部署成本高昂等问题。因此，研究重点正逐步从“扩大规模”转向“提升效率与智能质量”。

在模型结构创新方面，动态稀疏神经网络等技术受到关注。这类方法能够在推理过程中根据输入动态激活网络的部分参数或路径，在保持模型性能的同时显著降低计算开销和内存占用，为在资源受限的边缘设备上部署大型模型提供了可能[30]。此外，针对特定领域（如无线通信）的AI模型，其对抗鲁棒性研究也日益重要。研究表明，基于AI的信道状态信息（CSI）反馈系统在面对对抗性扰动时可能表现出脆弱性，这促使研究者开发更具鲁棒性的模型结构与训练方法以保障通信系统的安全可靠[2]。

在智能范式演进上，**具身智能（Embodied AI）** 和 **Agent（智能体）** 成为前沿方向。具身智能强调智能体通过与环境进行物理交互来学习和完成任务，是实现通用人工智能（AGI）的重要路径之一，其发展对于赋能高端制造、医疗康复等实体经济领域，培育新质生产力具有关键作用[39]。而“类代理式人工智能”（如OpenClaw）则代表了AI系统从被动响应向主动规划、工具调用、多任务协作的转变，极大地扩展了AI的应用边界与自主能力[4]。同时，人智交互驱动的双元主体知识同化模型研究，探讨了人类与AI如何高效协作、相互学习和知识融合，为构建新型人机协同系统提供了理论框架[28]。

### 2.2 训练数据与评测基准：规模、质量与价值化

训练数据是AI模型性能的基石。当前，全球数据资源规模保持高速增长，为AI发展提供了丰富的燃料[9]。数据要素的市场化与价值化进程正在显著提速，高质量、结构化、领域特定的数据成为稀缺资源与核心竞争力[12]。在专业领域，例如医学影像分析、地质勘探等，AI的应用高度依赖于高质量标注数据。研究通过对比基于AI的定量CT与双能X线吸收检测在骨质疏松诊断中的效能，凸显了高质量数据与专业标注对于模型临床价值的关键作用[23]。同样，在石油地质领域，利用测井数据评价烃源岩总有机碳含量（TOC）的方法研究，也体现了领域数据与AI结合解决专业问题的潜力[1]。

随着模型能力的多元化，构建全面、公正、具有挑战性的评测基准变得至关重要。评测不仅关注传统的准确率、召回率等指标，更扩展到模型的多模态理解、复杂推理、代码生成、安全对齐、长上下文处理以及专业领域知识掌握等多个维度。例如，在创造性问题解决领域，研究探讨了不同搜索空间限制下人类与AI的认知机制，这为设计评测AI创造性思维能力的基准提供了心理学依据[22]。同时，针对专利文本、学术论文等专业文献的自动分类与知识挖掘，也需要构建领域特定的评测体系[33]。

### 2.3 推理效率与工程落地：从云端到边缘与垂直整合

为了实现AI技术的广泛应用，推理效率的提升和工程化落地是关键。除了前述模型结构上的优化（如动态稀疏化），模型压缩（剪枝、量化、知识蒸馏）、硬件适配（专用AI芯片）、编译器优化以及推理框架创新等技术，共同推动了AI模型在云端、边缘端和终端设备上的高效部署[14][30]。上海等地区致力于打造“AI之城”，其核心举措之一便是推动“模力”（算法模型）与“芯动”（算力芯片）的协同发展，构建从底层算力到上层应用的完整产业生态[14]。

在垂直行业落地方面，AI呈现出深度赋能的特点。在**智慧医疗**领域，AI已广泛应用于疾病筛查（如宫颈癌AI辅助诊断）、医学影像分析、心电监测预警（如急性心肌梗死）以及中医药现代化研究（如虚拟细胞技术）中，显著提升了诊疗的效率和精准度[5][23][31][32]。在**智慧教育**领域，AI驱动学情诊断与个性化任务适配，正在推动初中英语分层教学、历史“教、学、评”一体化等教学模式的智能化升级[19][20]。同时，AI也被应用于“智慧耕读教育”等新型教育体系的构建中[24]。在**社会治理**领域，AI赋能监狱管理、智慧税务、灾害响应（如结合众源地理信息与跨视角地理定位技术）、城市地理学教学改革等，提升了公共服务的智能化水平和应急管理能力[3][6][27][37]。此外，AI在推动艺科融合、网络文明建设、绿色设计推广等方面也展现出独特价值[8][10][15][17]。

### 2.4 安全、伦理与治理挑战

随着AI能力的增强和应用范围的扩大，其安全与伦理问题日益凸显，治理框架的构建迫在眉睫。

**安全性**涵盖多个层面：一是对抗安全性，即模型抵御恶意输入攻击的能力，这在自动驾驶、金融风控等高风险场景中至关重要[2]。二是内容安全性，防止AI生成有害、偏见或虚假信息，维护网络空间清朗[17][26]。三是系统安全性，保障AI基础设施和供应链的安全可靠。

**伦理与法律**挑战集中体现在：**知识产权方面**，生成式AI输出内容的著作权归属与侵权责任认定成为法律界热议的焦点，需要平衡技术创新与权利保护[21]。**学术诚信方面**，AI参与学位论文创作的边界与合规性规则亟待明确，以维护学术研究的严肃性[36]。**就业影响方面**，AI对劳动力市场的冲击引发广泛关注，实证分析其对不同技能水平就业者的差异化影响，对于制定合理的劳动力市场政策具有重要意义[40]。**文化安全方面**，AI技术可能带来的文化同质化、意识形态渗透等风险，也需要从国家文化安全战略高度进行审视和应对[26]。

在**治理与规则**层面，全球范围内正在加快构建AI治理体系。这包括技术标准制定（如模型透明度、可解释性标准）、法律法规完善（如数据安全法、个人信息保护法、AI专门立法）、伦理准则确立以及行业自律机制的建立。例如，在智慧税务系统中，如何在提升征管效率的同时保护纳税人权利，就是技术应用必须面对的法治命题[37]。

## 三、挑战与发展趋势

### 3.1 面临的主要挑战

尽管AI发展取得显著进展，但仍面临一系列严峻挑战：**技术层面**，追求更高性能与更低能耗、更小模型体积之间的平衡仍是长期课题；复杂场景下的鲁棒性、可解释性与因果推理能力尚未根本解决；高质量、多模态、合规训练数据的获取与清洗成本高昂。**工程落地层面**，AI与行业知识的深度融合存在壁垒，定制化解决方案的开发和维护复杂度高；在医疗、司法等高可靠性要求的领域，AI系统的责任认定与可靠性验证标准缺失。**安全与治理层面**，对抗攻击手段不断演进，防御技术需持续迭代；全球AI治理规则碎片化，国际合作与协调难度大；算法偏见难以根除，可能加剧社会不平等。**社会与经济层面**，AI对就业结构的冲击可能引发结构性失业问题，需配套的社会保障与再就业培训体系[40]；AI技术的“数字鸿沟”可能扩大地区间、群体间的发展差距。

### 3.2 未来发展趋势

展望未来，AI技术与发展将呈现以下趋势：

1.  **模型发展走向高效化与专业化**：模型演进将继续朝着“大模型”与“小模型”并存、云端协同的方向发展。一方面，通过稀疏化、模块化、蒸馏等技术持续优化大模型的推理效率；另一方面，针对特定垂直场景（如工业质检、科学计算）开发轻量化、高精度的专业模型将成为主流[30][38]。**自主智能**与**人机融合智能**是长期方向，AI系统将具备更强的环境感知、自主规划与决策能力，并与人类形成深度协作的伙伴关系[28][38]。

2.  **数据与评测走向高质量与生态化**：数据建设将从重“规模”转向重“质量”与“价值”，领域知识库、高质量合成数据、隐私计算等技术将助力解决数据瓶颈[12]。评测基准将更加体系化、场景化和动态化，不仅评估模型静态能力，更关注其在复杂、开放环境中的持续学习与适应表现。

3.  **应用落地走向深水区与普惠化**：AI将进一步与实体经济深度融合，特别是在智能制造、生物医药、能源材料、现代农业等关乎国计民生的领域，催生颠覆性创新[5][7][24][39]。同时，通过开源模型、低代码平台、AI即服务（AIaaS）等方式，降低AI使用门槛，推动技术普惠，让更多中小企业和个人开发者受益[11][16]。

4.  **安全治理走向体系化与全球化**：可解释AI（XAI）、AI对齐（AI Alignment）、持续监控与审计等技术将得到大力发展，以增强AI系统的可靠性与可控性[2][4]。全球主要国家和地区将加速AI立法进程，在促进创新与防范风险之间寻求动态平衡。跨国合作将在AI安全标准、伦理准则、危机应对等方面变得更为重要[21][26][36][37]。

5.  **学科交叉与产业融合加速**：AI将与物理学、生命科学、材料科学、社会科学等学科产生更深刻的交叉，推动“AI for Science”范式变革[5][38]。同时，AI产业将与芯片、机器人、物联网、元宇宙等产业紧密融合，共同塑造未来数字社会的形态[14][39]。中国作为数据大国和AI应用活跃的市场，正通过政策引导、产业集聚和人才培养，加速向“数字强国”和“AI创新高地”迈进[13][14][34][35]。

总之，人工智能正处于从技术突破走向大规模产业化、社会化的关键阶段。未来的发展需要在持续推进技术创新的同时，高度重视其带来的安全、伦理与社会影响，通过技术、法律、市场与社会多元共治，引导人工智能朝着赋能人类、造福社会的方向健康发展。

## 参考文献
[1] 川东地区二叠系大隆组TOC测井评价方法. 知网, 2026-04-30 08:56. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1pRBL2ysbrxijOXePfMTT6XX9TS7pzlbP9MIkeOKvrsKdZNymgMsqgcu00hiOjFgJ_TpPWivJo9C-wrBFSNrWAhyJQ_4m4JtNagJEv1gr6aKHLsJ7lihAXiGp1OQgu4R9iXY-CSDToluytJ7S9Ksj2SYu5XdnK4qTTPCeqfeMiSlQ==&uniplatform=NZKPT&language=CHS
[2] On the adversarial robustness of AI-based CSI feedback systems. 知网, 2026-04-30 08:51. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1pTfbcpgEiwBZOl1Axwr5fyXEb9gyf8SWICr6QNo31GbocMRh3h0MBoo4RQXHmlp-jn0uNIdSSAMudJ1yJCbnl8zyDcg0usPJVi-I2cmuy99fiZeu8yIFX-ZrSXi8mt7HLC6cxU2yDPbHqrwya9X1AYJ1Q3QggCequ4yUwvNdb9QA==&uniplatform=NZKPT&language=CHS
[3] 灾害响应中众源地理信息与跨视角地理定位的协同应用研究进展. 知网, 2026-04-30 08:41. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1pTfbcpgEiwBZOl1Axwr5fyXEb9gyf8SWIR-OnTB8yg0dSAw9KAsWruLMSRH_YCzFQ2Ew8cBu-7VfU3BWLtZSMhTrfz8tNlSnBMsgEMG7N-K4W8vHqJOrbnUT0nN-_STZLev1ryzfBxRX0LW-VgxU4g2gCId0PTjCEnzHVe0VX-xg==&uniplatform=NZKPT&language=CHS
[4] “龙虾”OpenClaw类代理式人工智能的应用价值、风险挑战与应对策略. 知网, 2026-04-30 07:05. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1pPdHfCc3MQOLj70uLxUpKc-AEmmxEss-MfAydyFwKa4-cC1TiWBupslQJdMmGTKrIs_wJcDx4UJNgrh0LRYSvcmiGLC0cvZ4sGF1l5mXH9Gic0mVMl7RFx1BJoUYlReXGMxbsvMQjimxBlsVCMHWO0Fyi_qHN9MJTeyCAcozW1lw==&uniplatform=NZKPT&language=CHS
[5] 人工智能虚拟细胞技术赋能中医药现代化研究. 知网, 2026-04-30 07:04. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1pPdHfCc3MQOLj70uLxUpKc-AEmmxEss-PrMBhhMElCEr_E02BKvyr7WI8pu9RZXo7DOGV056uLbOsl1TCy6OARFY1Kkamy1wmSF-KuHzf5qJ7ib5b4CbBGWfTKrgOGWKXOM6c9gkWIg6bJCsdLAqW_In-Pln9SLIwKPRxRa9iuSQ==&uniplatform=NZKPT&language=CHS
[6] AI赋能监狱工作高质量发展的应用探讨. 知网, 2026-04-30. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1ojjLBgdtv11lmPLb9l84cZiFcvT3WxkkhZ45fMwRCDqEYULeb1bQ9jA6KToOf283sHh0daGYTgJ31NS0cbijaXXgHsZHSkH70_bdEHNYbqq3Sf7KqQiyhIsimHCI56j-BA-dt9vVkNqMCv_VT5jpBwHICz-0pMcqkuRA62igFNOA==&uniplatform=NZKPT&language=CHS
[7] 读懂“十五五”中国经济发展亮点. 知网, 2026-04-30. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1ojjLBgdtv11lmPLb9l84cZmFIBErfpkpEiazppwIeFAP_7G1vl_t7Bxk0zk2UlUAs5yRD-fIvJZMBqu0Q8U3W_bQKYpsBiIVf8GwQkwsI2x0y82ZF788UJeFdaL_hhS6QRddCReBpx_IBvwAXJrr2vbkf9Evy23D9sHUcO4ldbCqjPs3aGS6lD&uniplatform=NZKPT&language=CHS
[8] 文艺不妨多些科技思维. 知网, 2026-04-30. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1ojjLBgdtv11lmPLb9l84cZmFIBErfpkpEy43tWsqwF1oI7nUjoROHBFrDadtGIOAe3yZ89neYW3mNg56co3KxNZI77bk0q8BFP7p9Dl6ORYpCvBgp8KtKrqyqhzKcVD-sBsHhStGtHTIxcVq2vy9JAHGFhEyIaLLy4VbCGL5EnqIgihSyfhKG-&uniplatform=NZKPT&language=CHS
[9] 我国数据资源规模保持高速增长. 知网, 2026-04-30. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1qnB0SLr3zPzVvkRrho5BUNqdtoWQBQNLFIMCJjMX16GszEDHjqIvsaVgsp06rI3I3QeR-J5qfDH2R0JaEkY3rVUpdLhU2IR9ncGrnrG_UzHNG6fHsEjAY_OpN5qGpkq5R785im8redY_14vvHWoUL6hdZkZay1KljNYabH_me2ERF8m9keATNp&uniplatform=NZKPT&language=CHS
[10] 推动绿色设计从示范引领走向全面推广. 知网, 2026-04-30. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1qnB0SLr3zPzVvkRrho5BUNqdtoWQBQNLGyhGf9sQFJYWiim14IZjO99HRdDSZH5SxXDVyXU1bP8HmWhmaMwb2XrjWnSLxpckYHKeMAI2BcXuP3_XhSDc1Y3aMIaDwb9n2bJNsHP5hNdeEGSNRX1ILIgsRFWRlahQ-Vz3B7QFKrlRysCFBz51EE&uniplatform=NZKPT&language=CHS
[11] 从“流量”到“词元” 窥见中国AI产业跃升. 知网, 2026-04-30. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1qnB0SLr3zPzVvkRrho5BUNqdtoWQBQNLFgcbUE2BUaOcN08PEdwGhlTSjLqmH6pCdkMxWoiNGsaRyalh7WPiYdbMiu53RmpQr9SwLq7uO5W87AddNX7kMaMFgUxprIYbfNkPRLrQXUttp1D7qmSA176rJXWOExbgaNBwp_N8tMUPKSz00yWziJ&uniplatform=NZKPT&language=CHS
[12] 数据要素市场化价值化进程显著提速. 知网, 2026-04-30. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1qnB0SLr3zPzVvkRrho5BUNqdtoWQBQNLEgQakjATtKzw7gX9zA1KEM2N-mghNvOKtlqfiYGXv75an-jAeCMtrY63kUoRXMlGps4k4eXBgEDMuXFxVzUccXv3qbDuhOSBSSKReHzwZ93AGqmA0-Pc1IAF2fEThInCWqckdmC3Gb30Mx_1ON_VyZ&uniplatform=NZKPT&language=CHS
[13] “数据大国”加速迈向“数字强国”. 知网, 2026-04-30. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1qnB0SLr3zPzVvkRrho5BUNqdtoWQBQNLECOMiBoe_SGNnrq4FfVJ_8D_xUm6jdDtNpp_DsgrmN3Z0edv8r0NBOl8PyaCyWWK-n5Z0FZEr7AK_RkIPCcbkKv-SPDR4vsVDHroL3k198cn_yLTpUavhYrXzHJkgjniaUEAU8TOUcXO4gWpG2pyQ6&uniplatform=NZKPT&language=CHS
[14] “模力”四射、“芯动”引擎，上海加速打造“AI之城”. 知网, 2026-04-30. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1qkX2qGGtHAmfTlKTtcusYh2oEHEnO_TgRLMF6-Ej6z6rfeoNPUrBEp0cOv-5z1U-xkXPDTbXcLRdD7DZPHYaNAoURJYTa1rwy5kkqDuyaESAQJ9v6QA_bn-pKIA4TQtaoY0-P2Vsr3JzOfFssz87-em0ZkXm7PGHxBfKxh8vy-4m4lebL1DRBv&uniplatform=NZKPT&language=CHS
[15] 推动艺科融合 共赴美好未来. 知网, 2026-04-30. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1qkX2qGGtHAmfTlKTtcusYh2oEHEnO_TgRLMF6-Ej6z6rfeoNPUrBEptbzbEiGOmO2gL4S4HY-Yh2BFxBzmJlj21RlSUDAdMuCcpsqjRBc3uFPDEQ6U4ZRgREo9GZkvIDONI5_GbtQFekRsFCvraCqMVAEwEwVAzbjQhpM99LYr7lpZjk6kXGXf&uniplatform=NZKPT&language=CHS
[16] 超九成受访职场人有“AI工作搭子”. 知网, 2026-04-30. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1qkX2qGGtHAmfTlKTtcusYh2oEHEnO_TgRhEtFANC7oIx04mJvCnciBx3fgDt2X8YjCT-zsfiakN6-QjcaYrKMGdqicRmnEFIePi48t6fwMioCKPSXuCOHhxbNOl4TvrK4p_mV2YR_LuWReGAort_l-ltIwtNQiN38ZRiDSsQPUdHR0yoMWdke-&uniplatform=NZKPT&language=CHS
[17] 共建共享，筑牢网络文明底座. 知网, 2026-04-30. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1qkX2qGGtHAmfTlKTtcusYh2oEHEnO_TgTPfuCra9EHoYuTE66SEA7ItafzH2Y_WaIRmPqzyV4DFl1xqVXcIjkul8W0E5gOJCKwGh4XyLvG_KUhKn35ViJ5aoFYizIpEITMPEYv-zO2CzWubzYpmiOvCv9yQF6PPxLxNrvsoGXM6yaQ9cyiU0AK&uniplatform=NZKPT&language=CHS
[19] 初中英语分层教学的智能化升级——AI驱动的学情诊断与个性化任务适配研究. 知网, 2026-04-30. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1qhg-Hd9pe3tDaIAfGLrX0LlvCa6WDSrtuQp9lIcqFdJ-kko1IGtTQmSOaQjP8noRegBGDz8SENm1tbIb_a7gnAbSNK1qBYKzLcBw4FwFkjvKy_gp4IhypnSrQtOkajfz0kYm8EOBkt4ataCTi-Ev9vQ3SOi0_nmojKHR6MBuxdyQ==&uniplatform=NZKPT&language=CHS
[20] AI在初中历史“教、学、评”一体化中的应用. 知网, 2026-04-30. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1qhg-Hd9pe3tDaIAfGLrX0LlvCa6WDSrtuQp9lIcqFdJ-kko1IGtTQmagGnai5C_-gBg7mqztp8wNQxl0fvqhfkqjfoJVJuAOSrQaDlqxOfHVnj1lSt5TuTjca2eH_epSODVwznValNB3FloWsSuOI4JtUn9xV8G2KCKCudS8dMOg==&uniplatform=NZKPT&language=CHS
[21] 生成式人工智能输出端著作权侵权责任研究. 知网, 2026-04-29 17:55. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1pEfGOsHpb_EMRT4A5-GARlyB0roUBnAfveFlHTKt0I9fmsmnt3Ype6OTZnXJ7yuZsiV5dsektZ0zZhfr54wRk8Ihh8BB0jM-y8tZYNWb4tTxhXUhn4cSukFqSw8M9kVGufAmhyg5956AdSyGn4qbVrFFGA7p7vlJ20okXxdtQzww==&uniplatform=NZKPT&language=CHS
[22] 不同搜索空间限制下创造性问题解决的过程性搜索机制. 知网, 2026-04-29 16:09. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1rFdvFa6GDVxg4-GtABfb6SAl1WiWZlI6oM3Lrl1_qTF1pLC5VF9vKs2yyRNV9wTplXkGVoDksB1IUQCfe106Dq2CbB33WVMOGu9cP8J_6LZI6Xhgkwf_CPGxmdn-3eIoGy0K_xUFiOw3WspEurErkG_vjrlRvhYBfu7dSDJcT5eQ==&uniplatform=NZKPT&language=CHS
[23] 基于人工智能的定量CT与双能X线吸收检测在骨质疏松诊断效能中的差异性研究. 知网, 2026-04-29 15:49. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1qlxjg_QE0lZYwETM30LasMQxXT1j_Qag_DNXXwgg9SoToED-t0-gnc8fNokHS-SdzvziE0UECoVJjn9u6yLzLvEvS_IfqE0z2IjFQIPtuCkPCLgBMRizPJ9ohOI-Kc42nNjDDRPSflFTQM-qgU8vsx_R6KwQCcT8nohUfio6625Q==&uniplatform=NZKPT&language=CHS
[24] 新质生产力视域下涉农高校“智慧耕读教育”的体系构建与实施路径. 知网, 2026-04-29 15:42. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1qlxjg_QE0lZYwETM30LasMQxXT1j_Qag93nxe3hK0KLzp0C3xvCmWdoMuCKGVqV-9kBJGIs-RBX6vXEEcg1u6UBR3yXIo_Cswe14NqcjBTQEeWUNmuvoH61Che87yHvqXL9wyPdRPbEbIH525pHibKOOv_1PiyKSu_LE7t2l55Jg==&uniplatform=NZKPT&language=CHS
[26] 人工智能技术视域下的国家文化安全问题探析. 知网, 2026-04-29 14:45. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1poFa_bchA67mEQ9MP8GZ7cZ6HTm-fDA0glrGH3esZ2jfJpvjxCHrAH34RVWIDyTUOBOOvqMGwmzpXBzgaZdyQ7pEL8qKHkURSGNsuKRiWQ8E29jivXIK0w5WC3ESlHHQXjZN_tFUkRa7NyCgQcbPzjgq3OFgyar3xC_RF7586QmA==&uniplatform=NZKPT&language=CHS
[27] 人工智能背景下城市地理学教学模式改革研究. 知网, 2026-04-29 14:43. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1oEweFkgZ_Vk8uz8mEbKBOaGyjmWcOkiwOzFiZF8DMTSj0BoDMq47pco6C7TrA8xUVFQ0jLB3w8dqCwWBSEQBTORxYIcHouOB5yw2IFJRDIJ098mwZZ_DfUWt5ZnU2mbM_FK3D3yweAy1-aX3OIgnsnWSkrn-jQj2ODHUSR4NWI1Q==&uniplatform=NZKPT&language=CHS
[28] 人智交互驱动的双元主体知识同化模型研究. 知网, 2026-04-29 14:20. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1oEweFkgZ_Vk8uz8mEbKBOaGyjmWcOkiwNlXGeIRYwlu4n1gDfJcpVH4GiPM4fNSdCcj6yqofYZpD-4vFFSa2ZQVDzy-79s6P907L7GBMpikT-bTyzrRYgUefjVLJeg605BTg_5fXULEE52i04hIgdfLxKqBEd6Vtg5ZvMNO9k_Tg==&uniplatform=NZKPT&language=CHS
[30] 动态稀疏神经网络在计算机视觉中的应用. 知网, 2026-04-29 13:56. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1rwRnBpG4VwtuTdvVnnitFghow_AgYKGNdwvPM-ofnckBCG-YaoKfQDowLu1Nzd_iTke7kMDJ2AlpuKa-YRybC4RAr1DByEir3smLnzTL3LRCosRNaYGTvHPS9Bvw5J6l_HeLw3BVoNbKjMIVcMHFrxEliW_T_FW43W7yOu2GvKrA==&uniplatform=NZKPT&language=CHS
[31] 数智化技术用于急性心肌梗死心电监测的范围综述. 知网, 2026-04-29 13:54. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1pkmicmvpg-QnlzY_3Z977siAYPEO71durYNiTEqTYFhGWhJQKV0-bpf_9-quwGMUTk6gCBooLlcHwqTZLtYAYW08KUYQn1Iv9mZ8MYoCel3W84wObmwr4Ua8pUEAcVRvA0DO9wzQWKdyiQaC04gerpV5tMOHbFDw4MG_u1k6nNxA==&uniplatform=NZKPT&language=CHS
[32] 宫颈癌筛查技术的临床效能与创新应用：多维度分析与展望. 知网, 2026-04-29 13:54. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1pkmicmvpg-QnlzY_3Z977siAYPEO71durYNiTEqTYFhGWhJQKV0-bpAw-_pm-SA0rX30BQE5gTI7Vrvthqu5JsPGLTiID16coe_y-oFGbmxv27S-db-GqyLynVv8E9Z2zOLd9OZgnGyhDYfnVrnMoLqa7M8dDS2UnYdRqYexoEAQ==&uniplatform=NZKPT&language=CHS
[33] 融合审查逻辑与知识库驱动的专利层级化自动分类研究——以人工智能领域为例. 知网, 2026-04-29 13:35. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1pAUvWuw3Qtow5VvQePh2DaX_pdIxbeq5qzeDJ8rpyS1mlNCV0cDKaGCQEqaeB_yzPAwPhfdmOspr4GBfsUbi3m1kpl26S9eJw3lTPV_PzxYN9YKGeMeu8l-aLhpiw9yUoKiWdGycrueta9n_6SXLNOEyCHIixp7CjNMOeUc_N0Ag==&uniplatform=NZKPT&language=CHS
[34] 中国人工智能产业科技创新水平测度及影响因素分析. 知网, 2026-04-29 12:08. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1pAUvWuw3Qtow5VvQePh2DaX_pdIxbeq5rO8KJfXrgOT9P9RbAxAZstiAFmFutxxdgIwfqQlBxY5D9ODZvaWwUbNos-sD0umwawxoHgtCe5vLuQIlvev-7kHhjS-8DiHz4tUPrAUL1GSfIQUkwkaUkejyt1mKI7rNU1koDi3v5SXQ==&uniplatform=NZKPT&language=CHS
[35] 数字政府建设对智能经济的影响研究——基于大数据管理机构改革的准自然实验. 知网, 2026-04-29 11:56. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1rk2JFQs_zSDpjpjLEdRK--ei3rM7ZTF9-qBy0LcGWwwulUHy8oJ7FwkOERIKDDhSN21hu6GIDad09bT0_0xUO2jAwXfdXJ3aDBh4EhtqMAaYJMuvTsC277ULGSu5XcGGE_Xyrw2e1B7e_KnotUFUVVebpzMSGrrFio2L4dlkRERA==&uniplatform=NZKPT&language=CHS
[36] 人工智能参与学位论文创作如何合规：技术与规则的路径展开. 知网, 2026-04-29 11:44. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1pO5Bj0S9J-yyw5yudrkU-LLsn-45a-ZYTBkWBsVD1Z_8YP-qF9yjWVzvbIyfovQcJ9Vp2yvo79-zPivqMTnSha1xYYv3KhErbuNXlm4DHwOFXhPDyfoN9erkJx8qN6a4et0_MgEMO_E42tHtUT6_femctHQhAWAEgS7FF9HLDTxw==&uniplatform=NZKPT&language=CHS
[37] 智慧税务视域下纳税人权利的保护. 知网, 2026-04-29 11:36. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1pO5Bj0S9J-yyw5yudrkU-LLsn-45a-ZYSQD1PqtOrCEKBarlucsYNPHzuPO-p1gANfl8m4jZozmX1mq1fHZmtYC1-3NO0QpcA1st-Koq_UKopwGwaBb4OQuo1FLwFErjpP2TkVdPaix7hFoGeYF57Buj-P_rtDjowYK95wXmVlNA==&uniplatform=NZKPT&language=CHS
[38] 电磁超材料与人工智能:从智能赋能到自主智能. 知网, 2026-04-29 11:34. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1oKqR1owpMQ9Dlc4qG5LBaA7tuS61xqGqa-13ltyME6268H-MoyKorl3egLSpV9Zgrw2f2FrxTm5sbWgKWrsBH1TsWC28G1U_UNk-lMdwGCtZed8KO5cvLei6X936CMxblcaQxbW5vSIxNhj1T62yFgfaHdZyQidX-ojoq6Z00PjQ==&uniplatform=NZKPT&language=CHS
[39] 具身智能赋能新质生产力发展的内在机理、现实困境与突破路径. 知网, 2026-04-29 11:34. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1oKqR1owpMQ9Dlc4qG5LBaA7tuS61xqGqZxIPl_dhAfylc1uCPjNSsJBafIfHK5tDbBHNXqcPz49poZ9WKf0DkSRk_wZ7_3GVC3MgtAmwUP8ftLwMMfg66NLqpM_p119imjIAJv-VSRJ0KuVdA2u8DchB_QouHu0303aNq6ToCP4w==&uniplatform=NZKPT&language=CHS
[40] 人工智能发展如何影响劳动力就业？——理论模型与实证分析. 知网, 2026-04-29 11:33. https://kns.cnki.net/kcms2/article/abstract?v=tdDAU2ZCd1oUJsRY5s4uVz8TodRn7U6lTsfj-9z0x6q_0BCnxgbz0bt4epHjiiB-cIlFwYEuZOHAIo5RiGXhRgJ7n8d_dKxUfJ4zRpr9n6AvRhMXuZpO9yoNseuLITgmvCD0sCPS6HgN1boESMhrMKw--xKdZIQgoZWmJ2FweMNPUKgKjGY77Q==&uniplatform=NZKPT&language=CHS