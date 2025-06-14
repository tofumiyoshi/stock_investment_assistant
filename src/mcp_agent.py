from typing import Dict, Any
import httpx
from evaluator import Evaluator
from optimizer import Optimizer
import yaml
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

class MCPAgent:
    def __init__(self, config_path: str = "config.yaml"):
        """MCP Agentの初期化"""
        try:
            with open(config_path, encoding='utf-8') as f:
                config_content = f.read()
                # 環境変数を展開
                config_content = os.path.expandvars(config_content)
                self.config = yaml.safe_load(config_content)
        except FileNotFoundError:
            raise FileNotFoundError(f"設定ファイル {config_path} が見つかりません")
        except UnicodeDecodeError:
            raise UnicodeDecodeError("設定ファイルの文字コードが不正です。UTF-8で保存してください")
        except yaml.YAMLError as e:
            raise ValueError(f"設定ファイルのYAML形式が不正です: {str(e)}")
        
        # コンポーネント初期化
        self.evaluator = Evaluator(config_path)
        self.optimizer = Optimizer(config_path)
        
        # モデルパラメータ (設定ファイルから読み込み)
        self.reasoner_params = self.config['llm']['reasoner']
        self.chat_params = self.config['llm']['chat']
        
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        ユーザークエリを処理
        
        Args:
            query: ユーザーからの質問
            
        Returns:
            dict: 処理結果 (回答とメタデータ)
        """
        # 1. データ取得
        data = self._fetch_data(query)
        
        # 2. 分析実行 (deeseek reasoner使用)
        analysis_result = self._analyze_with_reasoner(query, data)
        
        # 3. 評価と最適化
        score, needs_improvement = self.evaluator.evaluate(analysis_result)
        
        if needs_improvement:
            # 最適化実行
            optimized_params = self.optimizer.optimize(
                self.evaluator,
                self.reasoner_params,
                analysis_result['input_features'],
                analysis_result['target']
            )
            # パラメータ更新
            self.reasoner_params.update(optimized_params)
            # 再分析
            analysis_result = self._analyze_with_reasoner(query, data)
        
        # 4. レポート生成 (deepseek chat使用)
        report = self._generate_report_with_chat(analysis_result)
        
        return {
            'answer': report,
            'score': score,
            'params': self.reasoner_params,
            'needed_optimization': needs_improvement
        }
    
    def _fetch_data(self, query: str) -> Dict:
        """データ取得 (実装は別モジュールに委譲)"""
        # TODO: 実際のデータ取得処理を実装
        return {}
    
    def _analyze_with_reasoner(self, query: str, data: Dict) -> Dict:
        """httpxを使用して分析実行"""
        headers = {
            "Authorization": f"Bearer {self.config['llm']['reasoner']['api_key']}",
            "Content-Type": "application/json"
        }
        payload = {
            "query": query,
            "data": data,
            "params": self.reasoner_params
        }
        # テスト用のモックレスポンス
        if os.getenv("TEST_MODE") == "true":
            return {
                "input_features": {"query": query, "data": data},
                "target": "test_response",
                "score": 0.85
            }
        
        endpoint = os.getenv("DEEPSEEK_REASONER_ENDPOINT", "https://api.example.com/reason")
        with httpx.Client() as client:
            response = client.post(
                endpoint,
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
    
    def _generate_report_with_chat(self, result: Dict) -> str:
        """httpxを使用してレポート生成"""
        # テスト用のモックレスポンス
        if os.getenv("TEST_MODE") == "true":
            return f"テストレポート: {result}"
            
        headers = {
            "Authorization": f"Bearer {self.config['llm']['chat']['api_key']}",
            "Content-Type": "application/json"
        }
        payload = {
            "analysis_result": result,
            "params": self.chat_params
        }
        endpoint = os.getenv("DEEPSEEK_CHAT_ENDPOINT", "https://api.example.com/chat")
        with httpx.Client() as client:
            response = client.post(
                endpoint,
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.text

if __name__ == "__main__":
    # テスト用のエントリポイント
    agent = MCPAgent()
    test_query = "テストクエリ"
    print(f"処理開始: {test_query}")
    result = agent.process_query(test_query)
    print("処理結果:")
    print(result)
