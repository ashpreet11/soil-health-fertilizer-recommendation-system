# CORE LOGIC (PURE FUNCTIONS ONLY)


def generate_soil_health(nitrogen, phosphorus, potassium, ph):

    if nitrogen >= 60 and phosphorus >= 60 and potassium >= 60 and 6.0 <= ph <= 7.5:
        return "Good"

    elif nitrogen >= 40 and phosphorus >= 40 and potassium >= 40:
        return "Moderate"

    else:
        return "Poor"


def generate_reason(nitrogen, phosphorus, potassium, stage, fertilizer):

    if nitrogen < 40:
        return f"Low nitrogen detected during {stage}. {fertilizer} recommended."

    elif phosphorus < 40:
        return f"Low phosphorus detected during {stage}. {fertilizer} recommended."

    elif potassium < 40:
        return f"Low potassium detected during {stage}. {fertilizer} recommended."

    else:
        return f"Soil nutrients are balanced for {stage}. {fertilizer} recommended."


FERTILIZER_COST = {
    "Urea": 500,
    "DAP": 1200,
    "NPK": 900,
    "MOP": 850,
    "SSP": 700,
    "Zinc Sulphate": 1000,
    "Compost": 400
}


def get_cost(fertilizer):
    return FERTILIZER_COST.get(fertilizer, "Not Available")


def climate_advisor(temperature, rainfall):

    if rainfall > 200:

        return (
            "Heavy rainfall detected. "
            "Apply fertilizer carefully."
        )

    elif temperature > 35:

        return (
            "High temperature detected. "
            "Proper irrigation recommended."
        )

    else:

        return (
            "Climate conditions are suitable."
        )