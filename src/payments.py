def min_installment_value(installments):
    if installments < 1 or installments > 12:
        raise ValueError("installments must be between 1 and 12")
    if installments == 1:
        return 0
    elif installments <= 3:
        return 50
    elif installments <= 6:
        return 80
    else:
        return 100

PIX_DISCOUNT = 0.05

def get_pix_price(price_brl):
    return round(price_brl * (1 - PIX_DISCOUNT), 2)


def get_max_installments(price_brl):
    for installments in range(12, 0, -1):
        if price_brl / installments >= min_installment_value(installments):
            return installments


def get_payment_options(price_brl):
    max_installments = get_max_installments(price_brl)
    return {
        "price_brl": price_brl,
        "pix_price_brl": get_pix_price(price_brl),
        "max_installments": max_installments,
        "installment_value_brl": round(price_brl / max_installments, 2),
    }