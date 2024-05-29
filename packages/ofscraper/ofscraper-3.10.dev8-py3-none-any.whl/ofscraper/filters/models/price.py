import logging

import ofscraper.utils.args.read as read_args
from ofscraper.filters.models.helpers import trace_log_user


def pricePaidFreeFilterHelper(filterusername):
    log = logging.getLogger("shared")

    log.debug(f"Current price filter: {read_args.retriveArgs().current_price}")
    if read_args.retriveArgs().current_price == "paid":
        filterusername = list(
            filter(
                lambda x: x.final_current_price > 0,
                filterusername,
            )
        )
        log.debug(f"Currently paid filter username count: {len(filterusername)}")
        trace_log_user(filterusername, "currently paid filter")

    elif read_args.retriveArgs().current_price == "free":
        filterusername = list(
            filter(
                lambda x: x.final_current_price == 0,
                filterusername,
            )
        )
        log.debug(f"currently free filter username count: {len(filterusername)}")
        trace_log_user(filterusername, "currently free filter")

    log.debug(f"Account renewal price filter: {read_args.retriveArgs().renewal_price}")
    if read_args.retriveArgs().renewal_price == "paid":
        filterusername = list(
            filter(
                lambda x: x.final_renewal_price > 0,
                filterusername,
            ),
        )

        log.debug(f"Paid renewal filter username count: {len(filterusername)}")
        trace_log_user(filterusername, "paid renewal filter")

    elif read_args.retriveArgs().renewal_price == "free":
        filterusername = list(
            filter(
                lambda x: x.final_renewal_price == 0,
                filterusername,
            )
        )
        log.debug(f"Free renewal filter username count: {len(filterusername)}")
        trace_log_user(filterusername, "free renewal filter")

    log.debug(f"Regular Price filter: {read_args.retriveArgs().regular_price}")
    if read_args.retriveArgs().regular_price == "paid":
        filterusername = list(filter(lambda x: x.final_regular_price, filterusername))
        log.debug(f"Paid regular price filter username count: {len(filterusername)}")
        trace_log_user(filterusername, "paid regular price filter")

    elif read_args.retriveArgs().regular_price == "free":
        filterusername = list(
            filter(lambda x: x.final_regular_price == 0, filterusername)
        )
        log.debug(f"Free regular price filter username count: {len(filterusername)}")
        trace_log_user(filterusername, "free regular price filter")
    log.debug(f"Promo price filter: {read_args.retriveArgs().promo_price}")
    if read_args.retriveArgs().promo_price == "paid":
        filterusername = list(
            filter(
                lambda x: x.final_promo_price > 0,
                filterusername,
            )
        )

        log.debug(f"Paid promo price filter username count: {len(filterusername)}")
        trace_log_user(filterusername, "paid promo price filter")

    elif read_args.retriveArgs().promo_price == "free":
        filterusername = list(
            filter(
                lambda x: x.final_promo_price == 0,
                filterusername,
            )
        )
        log.debug(f"Free promo price filter username count: {len(filterusername)}")
        trace_log_user(filterusername, "free promo price filter")

    filterusername = priceMinMaxFilters(filterusername)

    return filterusername


def priceMinMaxFilters(filterusername):
    log = logging.getLogger("shared")
    log.debug(f"Promo price min filter: {read_args.retriveArgs().promo_price_min}")
    if read_args.retriveArgs().promo_price_min:
        filterusername = list(
            filter(
                lambda x: x.final_promo_price
                >= read_args.retriveArgs().promo_price_min,
                filterusername,
            )
        )
        log.debug(f"Promo price min filter username count: {len(filterusername)}")
        trace_log_user(filterusername, "promo price min filter")

    log.debug(f"Promo price max filter: {read_args.retriveArgs().promo_price_max}")
    if read_args.retriveArgs().promo_price_max:
        filterusername = list(
            filter(
                lambda x: x.final_promo_price
                <= read_args.retriveArgs().promo_price_max,
                filterusername,
            )
        )
        log.debug(f"Promo price max filter username count: {len(filterusername)}")
        trace_log_user(filterusername, "promo price max filter")

    log.debug(f"Regular price min filter: {read_args.retriveArgs().regular_price_min}")
    if read_args.retriveArgs().regular_price_min:
        filterusername = list(
            filter(
                lambda x: x.final_regular_price
                >= read_args.retriveArgs().regular_price_min,
                filterusername,
            )
        )
        log.debug(f"Regular price min filter username count: {len(filterusername)}")
        trace_log_user(filterusername, "regular price min filter")
    log.debug(f"Regular price max filter: {read_args.retriveArgs().regular_price_max}")
    if read_args.retriveArgs().regular_price_max:
        filterusername = list(
            filter(
                lambda x: x.final_regular_price
                <= read_args.retriveArgs().regular_price_max,
                filterusername,
            )
        )
        log.debug(f"Regular price max filter username count: {len(filterusername)}")
        trace_log_user(filterusername, "regular price max filter")

    log.debug(f"Renewal price min filter: {read_args.retriveArgs().renewal_price_min}")
    if read_args.retriveArgs().renewal_price_min:
        filterusername = list(
            filter(
                lambda x: x.final_renewal_price
                >= read_args.retriveArgs().renewal_price_min,
                filterusername,
            )
        )
        log.debug(f"Renewal price min filter username count: {len(filterusername)}")
        trace_log_user(filterusername, "renewal price min filter")
    log.debug(f"Renewal price max filter: {read_args.retriveArgs().renewal_price_max}")
    if read_args.retriveArgs().renewal_price_max:
        filterusername = list(
            filter(
                lambda x: x.final_renewal_price
                <= read_args.retriveArgs().renewal_price_max,
                filterusername,
            )
        )
        log.debug(f"Renewal price max filter username count: {len(filterusername)}")
        trace_log_user(filterusername, "renewal price max filter")

    log.debug(f"Current price min filter: {read_args.retriveArgs().current_price_min}")
    if read_args.retriveArgs().current_price_min:
        filterusername = list(
            filter(
                lambda x: x.final_current_price
                >= read_args.retriveArgs().current_price_min,
                filterusername,
            )
        )
        log.debug(f"Current price min filter username count: {len(filterusername)}")
        trace_log_user(filterusername, "current price min filter")
    log.debug(f"Current price max filter: {read_args.retriveArgs().current_price_max}")
    if read_args.retriveArgs().current_price_max:
        filterusername = list(
            filter(
                lambda x: x.final_current_price
                <= read_args.retriveArgs().current_price_max,
                filterusername,
            )
        )
        log.debug(f"current price max filter username count: {len(filterusername)}")
        trace_log_user(filterusername, "current price max filter")
    return filterusername
