
from src.services.market_symbol_utils import get_suffix_market
from data_provider.base import _market_tag
from data_provider.yfinance_fetcher import YfinanceFetcher


def test_bursa_symbol_detection():
    assert get_suffix_market("4456.KL") == "my"
    assert get_suffix_market("5323.KL") == "my"
    assert get_suffix_market("8524.KL") == "my"


def test_bursa_market_classification():
    assert _market_tag("4456.KL") == "my"
    assert _market_tag("5323.KL") == "my"


def test_bursa_yahoo_symbol():
    fetcher = YfinanceFetcher()
    assert fetcher._convert_stock_code("4456.KL") == "4456.KL"
    assert fetcher._convert_stock_code("5323.KL") == "5323.KL"

def test_bursa_stock_input_parser():
    from src.services.stock_list_parser import parse_analysis_target
    from src.services.stock_code_utils import normalize_code

    for symbol in ("4456.KL", "5323.KL", "8524.KL"):
        result = parse_analysis_target(symbol)

        assert result.asset_type == "stock"
        assert result.canonical_id == symbol
        assert normalize_code(symbol) == symbol
        
def test_bursa_data_source_routing():
    from types import SimpleNamespace
    from data_provider.base import DataFetcherManager, normalize_stock_code

    assert normalize_stock_code("4456.kl") == "4456.KL"

    fetchers = [
        SimpleNamespace(name="AkshareFetcher"),
        SimpleNamespace(name="TencentFetcher"),
        SimpleNamespace(name="YfinanceFetcher"),
    ]

    selected = DataFetcherManager._filter_daily_fetchers_for_market(
        fetchers, "my"
    )

    assert [fetcher.name for fetcher in selected] == [
        "YfinanceFetcher"
    ]

