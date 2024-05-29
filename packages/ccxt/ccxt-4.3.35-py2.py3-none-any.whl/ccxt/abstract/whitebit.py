from ccxt.base.types import Entry


class ImplicitAPI:
    web_get_v1_healthcheck = webGetV1Healthcheck = Entry('v1/healthcheck', 'web', 'GET', {})
    v1_public_get_markets = v1PublicGetMarkets = Entry('markets', ['v1', 'public'], 'GET', {})
    v1_public_get_tickers = v1PublicGetTickers = Entry('tickers', ['v1', 'public'], 'GET', {})
    v1_public_get_ticker = v1PublicGetTicker = Entry('ticker', ['v1', 'public'], 'GET', {})
    v1_public_get_symbols = v1PublicGetSymbols = Entry('symbols', ['v1', 'public'], 'GET', {})
    v1_public_get_depth_result = v1PublicGetDepthResult = Entry('depth/result', ['v1', 'public'], 'GET', {})
    v1_public_get_history = v1PublicGetHistory = Entry('history', ['v1', 'public'], 'GET', {})
    v1_public_get_kline = v1PublicGetKline = Entry('kline', ['v1', 'public'], 'GET', {})
    v1_private_post_account_balance = v1PrivatePostAccountBalance = Entry('account/balance', ['v1', 'private'], 'POST', {})
    v1_private_post_order_new = v1PrivatePostOrderNew = Entry('order/new', ['v1', 'private'], 'POST', {})
    v1_private_post_order_cancel = v1PrivatePostOrderCancel = Entry('order/cancel', ['v1', 'private'], 'POST', {})
    v1_private_post_orders = v1PrivatePostOrders = Entry('orders', ['v1', 'private'], 'POST', {})
    v1_private_post_account_order_history = v1PrivatePostAccountOrderHistory = Entry('account/order_history', ['v1', 'private'], 'POST', {})
    v1_private_post_account_executed_history = v1PrivatePostAccountExecutedHistory = Entry('account/executed_history', ['v1', 'private'], 'POST', {})
    v1_private_post_account_executed_history_all = v1PrivatePostAccountExecutedHistoryAll = Entry('account/executed_history/all', ['v1', 'private'], 'POST', {})
    v1_private_post_account_order = v1PrivatePostAccountOrder = Entry('account/order', ['v1', 'private'], 'POST', {})
    v2_public_get_markets = v2PublicGetMarkets = Entry('markets', ['v2', 'public'], 'GET', {})
    v2_public_get_ticker = v2PublicGetTicker = Entry('ticker', ['v2', 'public'], 'GET', {})
    v2_public_get_assets = v2PublicGetAssets = Entry('assets', ['v2', 'public'], 'GET', {})
    v2_public_get_fee = v2PublicGetFee = Entry('fee', ['v2', 'public'], 'GET', {})
    v2_public_get_depth_market = v2PublicGetDepthMarket = Entry('depth/{market}', ['v2', 'public'], 'GET', {})
    v2_public_get_trades_market = v2PublicGetTradesMarket = Entry('trades/{market}', ['v2', 'public'], 'GET', {})
    v4_public_get_assets = v4PublicGetAssets = Entry('assets', ['v4', 'public'], 'GET', {})
    v4_public_get_collateral_markets = v4PublicGetCollateralMarkets = Entry('collateral/markets', ['v4', 'public'], 'GET', {})
    v4_public_get_fee = v4PublicGetFee = Entry('fee', ['v4', 'public'], 'GET', {})
    v4_public_get_orderbook_market = v4PublicGetOrderbookMarket = Entry('orderbook/{market}', ['v4', 'public'], 'GET', {})
    v4_public_get_ticker = v4PublicGetTicker = Entry('ticker', ['v4', 'public'], 'GET', {})
    v4_public_get_trades_market = v4PublicGetTradesMarket = Entry('trades/{market}', ['v4', 'public'], 'GET', {})
    v4_public_get_time = v4PublicGetTime = Entry('time', ['v4', 'public'], 'GET', {})
    v4_public_get_ping = v4PublicGetPing = Entry('ping', ['v4', 'public'], 'GET', {})
    v4_public_get_markets = v4PublicGetMarkets = Entry('markets', ['v4', 'public'], 'GET', {})
    v4_public_get_futures = v4PublicGetFutures = Entry('futures', ['v4', 'public'], 'GET', {})
    v4_public_get_platform_status = v4PublicGetPlatformStatus = Entry('platform/status', ['v4', 'public'], 'GET', {})
    v4_private_post_collateral_account_balance = v4PrivatePostCollateralAccountBalance = Entry('collateral-account/balance', ['v4', 'private'], 'POST', {})
    v4_private_post_collateral_account_balance_summary = v4PrivatePostCollateralAccountBalanceSummary = Entry('collateral-account/balance-summary', ['v4', 'private'], 'POST', {})
    v4_private_post_collateral_account_positions_history = v4PrivatePostCollateralAccountPositionsHistory = Entry('collateral-account/positions/history', ['v4', 'private'], 'POST', {})
    v4_private_post_collateral_account_leverage = v4PrivatePostCollateralAccountLeverage = Entry('collateral-account/leverage', ['v4', 'private'], 'POST', {})
    v4_private_post_collateral_account_positions_open = v4PrivatePostCollateralAccountPositionsOpen = Entry('collateral-account/positions/open', ['v4', 'private'], 'POST', {})
    v4_private_post_collateral_account_summary = v4PrivatePostCollateralAccountSummary = Entry('collateral-account/summary', ['v4', 'private'], 'POST', {})
    v4_private_post_main_account_address = v4PrivatePostMainAccountAddress = Entry('main-account/address', ['v4', 'private'], 'POST', {})
    v4_private_post_main_account_balance = v4PrivatePostMainAccountBalance = Entry('main-account/balance', ['v4', 'private'], 'POST', {})
    v4_private_post_main_account_create_new_address = v4PrivatePostMainAccountCreateNewAddress = Entry('main-account/create-new-address', ['v4', 'private'], 'POST', {})
    v4_private_post_main_account_codes = v4PrivatePostMainAccountCodes = Entry('main-account/codes', ['v4', 'private'], 'POST', {})
    v4_private_post_main_account_codes_apply = v4PrivatePostMainAccountCodesApply = Entry('main-account/codes/apply', ['v4', 'private'], 'POST', {})
    v4_private_post_main_account_codes_my = v4PrivatePostMainAccountCodesMy = Entry('main-account/codes/my', ['v4', 'private'], 'POST', {})
    v4_private_post_main_account_codes_history = v4PrivatePostMainAccountCodesHistory = Entry('main-account/codes/history', ['v4', 'private'], 'POST', {})
    v4_private_post_main_account_fiat_deposit_url = v4PrivatePostMainAccountFiatDepositUrl = Entry('main-account/fiat-deposit-url', ['v4', 'private'], 'POST', {})
    v4_private_post_main_account_history = v4PrivatePostMainAccountHistory = Entry('main-account/history', ['v4', 'private'], 'POST', {})
    v4_private_post_main_account_withdraw = v4PrivatePostMainAccountWithdraw = Entry('main-account/withdraw', ['v4', 'private'], 'POST', {})
    v4_private_post_main_account_withdraw_pay = v4PrivatePostMainAccountWithdrawPay = Entry('main-account/withdraw-pay', ['v4', 'private'], 'POST', {})
    v4_private_post_main_account_transfer = v4PrivatePostMainAccountTransfer = Entry('main-account/transfer', ['v4', 'private'], 'POST', {})
    v4_private_post_main_account_smart_plans = v4PrivatePostMainAccountSmartPlans = Entry('main-account/smart/plans', ['v4', 'private'], 'POST', {})
    v4_private_post_main_account_smart_investment = v4PrivatePostMainAccountSmartInvestment = Entry('main-account/smart/investment', ['v4', 'private'], 'POST', {})
    v4_private_post_main_account_smart_investment_close = v4PrivatePostMainAccountSmartInvestmentClose = Entry('main-account/smart/investment/close', ['v4', 'private'], 'POST', {})
    v4_private_post_main_account_smart_investments = v4PrivatePostMainAccountSmartInvestments = Entry('main-account/smart/investments', ['v4', 'private'], 'POST', {})
    v4_private_post_main_account_fee = v4PrivatePostMainAccountFee = Entry('main-account/fee', ['v4', 'private'], 'POST', {})
    v4_private_post_main_account_smart_interest_payment_history = v4PrivatePostMainAccountSmartInterestPaymentHistory = Entry('main-account/smart/interest-payment-history', ['v4', 'private'], 'POST', {})
    v4_private_post_trade_account_balance = v4PrivatePostTradeAccountBalance = Entry('trade-account/balance', ['v4', 'private'], 'POST', {})
    v4_private_post_trade_account_executed_history = v4PrivatePostTradeAccountExecutedHistory = Entry('trade-account/executed-history', ['v4', 'private'], 'POST', {})
    v4_private_post_trade_account_order = v4PrivatePostTradeAccountOrder = Entry('trade-account/order', ['v4', 'private'], 'POST', {})
    v4_private_post_trade_account_order_history = v4PrivatePostTradeAccountOrderHistory = Entry('trade-account/order/history', ['v4', 'private'], 'POST', {})
    v4_private_post_order_collateral_limit = v4PrivatePostOrderCollateralLimit = Entry('order/collateral/limit', ['v4', 'private'], 'POST', {})
    v4_private_post_order_collateral_market = v4PrivatePostOrderCollateralMarket = Entry('order/collateral/market', ['v4', 'private'], 'POST', {})
    v4_private_post_order_collateral_stop_limit = v4PrivatePostOrderCollateralStopLimit = Entry('order/collateral/stop-limit', ['v4', 'private'], 'POST', {})
    v4_private_post_order_collateral_trigger_market = v4PrivatePostOrderCollateralTriggerMarket = Entry('order/collateral/trigger-market', ['v4', 'private'], 'POST', {})
    v4_private_post_order_new = v4PrivatePostOrderNew = Entry('order/new', ['v4', 'private'], 'POST', {})
    v4_private_post_order_market = v4PrivatePostOrderMarket = Entry('order/market', ['v4', 'private'], 'POST', {})
    v4_private_post_order_stock_market = v4PrivatePostOrderStockMarket = Entry('order/stock_market', ['v4', 'private'], 'POST', {})
    v4_private_post_order_stop_limit = v4PrivatePostOrderStopLimit = Entry('order/stop_limit', ['v4', 'private'], 'POST', {})
    v4_private_post_order_stop_market = v4PrivatePostOrderStopMarket = Entry('order/stop_market', ['v4', 'private'], 'POST', {})
    v4_private_post_order_cancel = v4PrivatePostOrderCancel = Entry('order/cancel', ['v4', 'private'], 'POST', {})
    v4_private_post_order_cancel_all = v4PrivatePostOrderCancelAll = Entry('order/cancel/all', ['v4', 'private'], 'POST', {})
    v4_private_post_order_kill_switch = v4PrivatePostOrderKillSwitch = Entry('order/kill-switch', ['v4', 'private'], 'POST', {})
    v4_private_post_order_kill_switch_status = v4PrivatePostOrderKillSwitchStatus = Entry('order/kill-switch/status', ['v4', 'private'], 'POST', {})
    v4_private_post_order_bulk = v4PrivatePostOrderBulk = Entry('order/bulk', ['v4', 'private'], 'POST', {})
    v4_private_post_order_modify = v4PrivatePostOrderModify = Entry('order/modify', ['v4', 'private'], 'POST', {})
    v4_private_post_orders = v4PrivatePostOrders = Entry('orders', ['v4', 'private'], 'POST', {})
    v4_private_post_oco_orders = v4PrivatePostOcoOrders = Entry('oco-orders', ['v4', 'private'], 'POST', {})
    v4_private_post_order_collateral_oco = v4PrivatePostOrderCollateralOco = Entry('order/collateral/oco', ['v4', 'private'], 'POST', {})
    v4_private_post_order_oco_cancel = v4PrivatePostOrderOcoCancel = Entry('order/oco-cancel', ['v4', 'private'], 'POST', {})
    v4_private_post_order_oto_cancel = v4PrivatePostOrderOtoCancel = Entry('order/oto-cancel', ['v4', 'private'], 'POST', {})
    v4_private_post_profile_websocket_token = v4PrivatePostProfileWebsocketToken = Entry('profile/websocket_token', ['v4', 'private'], 'POST', {})
    v4_private_post_convert_estimate = v4PrivatePostConvertEstimate = Entry('convert/estimate', ['v4', 'private'], 'POST', {})
    v4_private_post_convert_confirm = v4PrivatePostConvertConfirm = Entry('convert/confirm', ['v4', 'private'], 'POST', {})
    v4_private_post_convert_history = v4PrivatePostConvertHistory = Entry('convert/history', ['v4', 'private'], 'POST', {})
    v4_private_post_sub_account_create = v4PrivatePostSubAccountCreate = Entry('sub-account/create', ['v4', 'private'], 'POST', {})
    v4_private_post_sub_account_delete = v4PrivatePostSubAccountDelete = Entry('sub-account/delete', ['v4', 'private'], 'POST', {})
    v4_private_post_sub_account_edit = v4PrivatePostSubAccountEdit = Entry('sub-account/edit', ['v4', 'private'], 'POST', {})
    v4_private_post_sub_account_list = v4PrivatePostSubAccountList = Entry('sub-account/list', ['v4', 'private'], 'POST', {})
    v4_private_post_sub_account_transfer = v4PrivatePostSubAccountTransfer = Entry('sub-account/transfer', ['v4', 'private'], 'POST', {})
    v4_private_post_sub_account_block = v4PrivatePostSubAccountBlock = Entry('sub-account/block', ['v4', 'private'], 'POST', {})
    v4_private_post_sub_account_unblock = v4PrivatePostSubAccountUnblock = Entry('sub-account/unblock', ['v4', 'private'], 'POST', {})
    v4_private_post_sub_account_balances = v4PrivatePostSubAccountBalances = Entry('sub-account/balances', ['v4', 'private'], 'POST', {})
    v4_private_post_sub_account_transfer_history = v4PrivatePostSubAccountTransferHistory = Entry('sub-account/transfer/history', ['v4', 'private'], 'POST', {})
