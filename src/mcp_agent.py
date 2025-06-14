from typing import Dict, Any

from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm import RequestParams
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM

from mcp_agent.workflows.evaluator_optimizer.evaluator_optimizer import (
    EvaluatorOptimizerLLM,
    QualityRating,
)
from rich import print

from dotenv import load_dotenv


# 環境変数の読み込み
load_dotenv()

class MCPAgent:
    def __init__(self, config_path: str = "config.yaml"):
        """MCP Agentの初期化"""
        self.app = MCPApp(name="株投資アシスタント")
        
        self.investor_information = "投資家情報はここ"

        self.optimizer = Agent(
            name="optimizer",
            instruction="""あなたは株式投資の専門家で、特に株のスクリーニングと選択を得意としています。
                与えられた市場データ、投資家のリスク許容度、投資目的、時間的制約に基づいて、
                最適な株式を選択するタスクを遂行します。以下の要素を考慮してレスポンスをカスタマイズします:
                1. 投資家プロファイル:
                - リスク許容度 (保守的/中立的/積極的)
                - 投資期間 (短期/中期/長期)
                - 投資目的 (キャピタルゲイン/配当収入/バランス)
                2. 市場条件:
                - 現在の経済状況
                - セクター別のパフォーマンス
                - 金利環境
                3. 財務指標:
                - PBR, PER, ROEなどのバリュエーション指標
                - 成長性指標
                - 財務健全性指標
                4. テクニカル要因:
                - 価格トレンド
                - 出来高
                - サポート/レジスタンスレベル
                出力は投資家のプロファイルに合わせて最適化し、各推奨銘柄について:
                - 推奨理由
                - 期待リターン
                - 想定リスク
                - モニタリングのポイント
                を明確に示します。
            """,
            server_names=["webresearch", "fetch", "yfinance"],
        )
        self.evaluator = Agent(
            name="evaluator",
            instruction="""あなたは株式分析の専門家で、投資推奨レポートの評価を担当します。
                与えられた株式分析レポートを以下の基準で評価してください：
                1. 分析の明瞭性:
                - 財務データと分析結果が明確に示されているか
                - 専門用語が適切に説明されているか
                - 評価: EXCELLENT/GOOD/FAIR/POOR
                - 改善提案: (具体的な提案)
                2. データの具体性:
                - 具体的な財務指標が使用されているか (PBR, PER, ROEなど)
                - 業績予想の根拠が示されているか
                - 評価: EXCELLENT/GOOD/FAIR/POOR
                - 改善提案: (不足しているデータの指摘)
                3. 関連性:
                - 分析が投資家のプロファイルに合っているか
                - 無関係な情報が含まれていないか
                - 評価: EXCELLENT/GOOD/FAIR/POOR
                - 改善提案: (関連性を高めるための提案)
                4. トーンとスタイル:
                - 専門的な分析トーンが保たれているか
                - 投資判断に適した形式か
                - 評価: EXCELLENT/GOOD/FAIR/POOR
                - 改善提案: (トーン調整の提案)
                5. 説得力:
                - 推奨理由がデータで裏付けられているか
                - リスク要因が適切に考慮されているか
                - 評価: EXCELLENT/GOOD/FAIR/POOR
                - 改善提案: (説得力を高める方法)
                6. 文法と正確性:
                - 数値データに誤りがないか
                - 文法や表記が正確か
                - 評価: EXCELLENT/GOOD/FAIR/POOR
                - 改善提案: (修正が必要な点)
                7. 改善対応:
                - 以前の指摘事項が反映されているか
                - 分析の進化が見られるか
                - 評価: EXCELLENT/GOOD/FAIR/POOR
                - 改善提案: (さらなる改善点)
                評価サマリー:
                - 総合評価: (EXCELLENT/GOOD/FAIR/POOR)
                - 主な強み: (3点まで)
                - 改善が必要な領域: (3点まで)
                - 優先すべき改善点: (最も重要な1点)""",
            server_names=["webresearch", "fetch", "yfinance"],
        )
        
        self.evaluator_optimizer = EvaluatorOptimizerLLM(
            optimizer=self.optimizer,
            evaluator=self.evaluator,
            llm_factory=OpenAIAugmentedLLM,
            min_rating=QualityRating.EXCELLENT,
        )
        
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        ユーザークエリを処理
        
        Args:
            query: ユーザーからの質問
            
        Returns:
            dict: 処理結果 (回答とメタデータ)
        """
        
        # 評価と最適化
        optimize_result = self._evaluator_optimizer_call(query)
        
        return {
            'answer': optimize_result
        }

    def _evaluator_optimizer_call(self, query: str) -> Dict:
        with self.app.run() as cover_letter_app:
            context = cover_letter_app.context
            logger = cover_letter_app.logger

            logger.info("Current config:", data=context.config.model_dump())

            result = self.evaluator_optimizer.generate_str(
                message=f"ユーザの入力情報を使って、Yahoo Financeから株式リスト情報を取得し、最適な投資対象株式を5つ洗い出すします。 {query}\n\投資家情報: {self.investor_information}",
                request_params=RequestParams(model="gpt-4o"),
            )

            logger.info(f"{result}")

if __name__ == "__main__":
    # テスト用のエントリポイント
    agent = MCPAgent()
    test_query = "テストクエリ"
    print(f"処理開始: {test_query}")
    result = agent.process_query(test_query)
    print("処理結果:")
    print(result)
