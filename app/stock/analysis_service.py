import logging
from datetime import date

from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate

from app.llm.llm_factory import LLMFactory
from app.models.stock import StockSignal
from app.stock.datastore import StockDatastore

logger = logging.getLogger(__name__)


class StockAnalysisService:
    """股票分析服务"""

    def __init__(self, datastore: StockDatastore):
        self.datastore = datastore
        self.chain = self._get_prompt() | LLMFactory.get_client("Qwen2.5-32B-Instruct")

    @classmethod
    def _get_prompt(cls):
        return ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="你是一个专业的股票分析师，请根据技术指标信号分析股票的交易机会。"
                ),
                ("user", "{message}"),
            ]
        )

    def analyze_signals(self, code: str, trade_date: date) -> None:
        """分析股票信号并生成AI评估

        Args:
            code: 股票代码
            trade_date: 交易日期
        """
        try:
            # 获取当日信号
            signal = self.datastore.get_signal(code, trade_date)
            if not signal:
                logger.warning(f"未找到股票{code}在{trade_date}的信号数据")
                return

            # 构建提示信息
            message = self._build_analysis_message(signal)
            response = self.chain.invoke(input={"message": message})
            analysis = response.content

            # 更新信号记录
            signal.ai_analysis = analysis
            signal.ai_score = self._extract_score(analysis)
            self.datastore.upsert(signal)

        except Exception as e:
            logger.exception(
                f"AI分析股票{code}在{trade_date}的信号时发生错误: {str(e)}"
            )

    @classmethod
    def _build_analysis_message(cls, signal: StockSignal) -> str:
        """构建AI分析提示"""
        message = f"""
请分析股票{signal.code} ({signal.name})在{signal.trade_date}的交易机会，技术指标信号如下：

MACD信号:
- 金叉: {signal.macd_golden_cross}
- 死叉: {signal.macd_dead_cross}

KDJ信号:
- 金叉: {signal.kdj_golden_cross}
- 死叉: {signal.kdj_dead_cross}
- 超卖: {signal.kdj_oversold}
- 超买: {signal.kdj_overbought}

RSI信号:
- 超卖: {signal.rsi_oversold}
- 超买: {signal.rsi_overbought}

布林带信号:
- 突破上轨: {signal.boll_break_up}
- 突破下轨: {signal.boll_break_down}

均线信号:
- 金叉: {signal.ma_golden_cross}
- 死叉: {signal.ma_dead_cross}

请提供详细分析和建议，并给出0-100的综合评分（0表示最不适合交易，100表示最适合交易）。
"""
        return message

    @classmethod
    def _extract_score(cls, analysis: str) -> float:
        """从AI分析文本中提取评分"""
        try:
            # 这里需要根据实际的AI响应格式来实现评分提取逻辑
            # 简单示例：假设评分在文本最后一行，格式为"评分：XX"
            lines = analysis.strip().split("\n")
            for line in reversed(lines):
                if "评分" in line:
                    score = float(line.split("：")[1].strip())
                    return min(max(score, 0), 100)
            return 50.0  # 默认评分
        except Exception:
            return 50.0
