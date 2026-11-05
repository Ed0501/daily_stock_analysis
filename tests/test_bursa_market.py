
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

def test_bursa_trading_calendar_config():
    from src.core.trading_calendar import (
        MARKET_EXCHANGE,
        MARKET_TIMEZONE,
        get_market_for_stock,
    )

    assert MARKET_EXCHANGE["my"] == "XKLS"
    assert MARKET_TIMEZONE["my"] == "Asia/Kuala_Lumpur"

    for symbol in ("4456.KL", "5323.KL", "8524.KL"):
        assert get_market_for_stock(symbol) == "my"


def test_bursa_lunch_break():
    from datetime import datetime
    from zoneinfo import ZoneInfo
    from src.core.trading_calendar import (
        infer_market_phase,
        MarketPhase,
    )

    lunchtime = datetime(
        2026, 11, 5, 13, 0,
        tzinfo=ZoneInfo("Asia/Kuala_Lumpur"),
    )

    assert infer_market_phase(
        "my", current_time=lunchtime
    ) == MarketPhase.LUNCH_BREAK
    
def test_bursa_full_trading_session():
    from datetime import datetime
    from zoneinfo import ZoneInfo
    from src.core.trading_calendar import (
        infer_market_phase,
        MarketPhase,
    )

    tz = ZoneInfo("Asia/Kuala_Lumpur")

    cases = [
        (8, 0, MarketPhase.PREMARKET),
        (11, 0, MarketPhase.INTRADAY),
        (13, 0, MarketPhase.LUNCH_BREAK),
        (15, 0, MarketPhase.INTRADAY),
        (17, 30, MarketPhase.POSTMARKET),
    ]

    for hour, minute, expected in cases:
        now = datetime(
            2026, 11, 5, hour, minute,
            tzinfo=tz,
        )

        actual = infer_market_phase(
            "my", current_time=now
        )

        assert actual == expected, (
            f"{hour:02d}:{minute:02d}: "
            f"expected {expected}, got {actual}"
        )

def test_bursa_weekend_closed():
    from datetime import datetime
    from zoneinfo import ZoneInfo
    from src.core.trading_calendar import (
        infer_market_phase,
        MarketPhase,
    )

    tz = ZoneInfo("Asia/Kuala_Lumpur")

    for day in (7, 8):
        now = datetime(
            2026, 11, day, 11, 0,
            tzinfo=tz,
        )

        assert infer_market_phase(
            "my", current_time=now
        ) == MarketPhase.NON_TRADING

