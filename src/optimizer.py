from typing import Dict, Any
import yaml
import os
from dotenv import load_dotenv

load_dotenv()

class Optimizer:
    def __init__(self, config_path: str = "config.yaml"):
        try:
            with open(config_path, encoding='utf-8') as f:
                config_content = f.read()
                config_content = os.path.expandvars(config_content)
                self.config = yaml.safe_load(config_content)
        except FileNotFoundError:
            raise FileNotFoundError(f"設定ファイル {config_path} が見つかりません")
        except UnicodeDecodeError:
            raise UnicodeDecodeError("設定ファイルの文字コードが不正です。UTF-8で保存してください")
        except yaml.YAMLError as e:
            raise ValueError(f"設定ファイルのYAML形式が不正です: {str(e)}")
        
    def optimize(self, evaluator, params: Dict, input_features: Dict, target: Any) -> Dict:
        """パラメータを最適化"""
        # TODO: 実際の最適化ロジックを実装
        optimized_params = params.copy()
        optimized_params["temperature"] = min(params["temperature"] + 0.1, 1.0)
        return optimized_params
