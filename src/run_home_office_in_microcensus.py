from estimate_choice_model_home_office import estimate_choice_model_home_office
from validate_choice_model_home_office import validate_choice_model_home_office
from apply_model_to_synthetic_population import apply_model_to_synthetic_population


def run_home_office_in_microcensus():
    estimate_choice_model_home_office()
    validate_choice_model_home_office()
    apply_model_to_synthetic_population()


if __name__ == '__main__':
    run_home_office_in_microcensus()
