import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.models as models
from biogeme.expressions import Beta
import biogeme.results as res
import os


def apply_most_recent_model_to_microcensus(data_file_directory_for_simulation, data_file_name_for_simulation,
                                           output_directory_for_simulation, output_file_name,
                                           path_to_estimated_betas, estimated_betas_name, betas=None):
    """
    :author: Antonin Danalet, based on the example '01logit_simul.py' by Michel Bierlaire, EPFL, on biogeme.epfl.ch

    Simulation with a binary logit model. Two alternatives: work from home at least some times, or not."""

    # Read the data
    df_persons = pd.read_csv(data_file_directory_for_simulation / data_file_name_for_simulation, sep=';')
    database = db.Database('persons', df_persons)

    # The following statement allows you to use the names of the variable as Python variable.
    globals().update(database.variables)

    # Parameters to be estimated
    alternative_specific_constant = Beta('alternative_specific_constant', 0, None, None, 0)

    b_no_post_school_education = Beta('b_no_post_school_education', 0, None, None, 0)
    b_secondary_education = Beta('b_secondary_education', 0, None, None, 0)
    b_tertiary_education = Beta('b_tertiary_education', 0, None, None, 0)

    b_couple_without_children_2020 = Beta('b_couple_without_children_2020', 0, None, None, 0)

    b_intermediate_work_2020 = Beta('b_intermediate_work_2020', 0, None, None, 0)

    b_home_work_distance = Beta('b_home_work_distance', 0, None, None, 0)
    b_home_work_distance_zero = Beta('b_home_work_distance_zero', 0, None, None, 0)

    b_business_sector_production = Beta('b_business_sector_production', 0, None, None, 0)
    b_business_sector_wholesale = Beta('b_business_sector_wholesale', 0, None, None, 0)
    b_business_sector_retail = Beta('b_business_sector_retail', 0, None, None, 0)
    b_business_sector_gastronomy = Beta('b_business_sector_gastronomy', 0, None, None, 0)
    b_business_sector_finance = Beta('b_business_sector_finance', 0, None, None, 0)
    b_business_sector_other_services = Beta('b_business_sector_other_services', 0, None, None, 0)
    b_business_sector_others = Beta('b_business_sector_others', 0, None, None, 0)
    b_business_sector_non_movers = Beta('b_business_sector_non_movers', 0, None, None, 0)
    b_executives = Beta('b_executives', 0, None, None, 0)
    b_german = Beta('b_german', 0, None, None, 0)
    b_hh_income_8000_or_less = Beta('b_hh_income_8000_or_less', 0, None, None, 0)

    b_owning_a_general_abo = Beta('b_owning_a_general_abo', 0, None, None, 0)

    b_mobility_resource_car_half_fare_abo = Beta('b_mobility_resource_car_half_fare_abo', 0, None, None, 0)
    b_mobility_resource_general_abo_no_car_2020 = Beta('b_mobility_resource_general_no_car_abo_2020', 0, None, None, 0)

    ''' Definition of new variables '''
    # male = (sex == 1)

    # single_household = (hh_type == 10)
    couple_without_children = (hh_type == 210)
    # couple_with_children = (hh_type == 220)
    # single_parent_with_children = (hh_type == 230)
    # not_family_household = (hh_type == 30)

    # public_transport_connection_quality_ARE_A_home = (public_transport_connection_quality_ARE_home == 1)
    # public_transport_connection_quality_ARE_B_home = (public_transport_connection_quality_ARE_home == 2)
    # public_transport_connection_quality_ARE_C_home = (public_transport_connection_quality_ARE_home == 3)
    # public_transport_connection_quality_ARE_D_home = (public_transport_connection_quality_ARE_home == 4)
    public_transport_connection_quality_ARE_NA_home = (public_transport_connection_quality_ARE_home == 5)

    # public_transport_connection_quality_ARE_A_work = (public_transport_connection_quality_ARE_work == 1)
    # public_transport_connection_quality_ARE_B_work = (public_transport_connection_quality_ARE_work == 2)
    # public_transport_connection_quality_ARE_C_work = (public_transport_connection_quality_ARE_work == 3)
    # public_transport_connection_quality_ARE_D_work = (public_transport_connection_quality_ARE_work == 4)
    # public_transport_connection_quality_ARE_NA_work = (public_transport_connection_quality_ARE_work == 5)

    # urban_home = (urban_typology_home == 1)
    # rural_home = (urban_typology_work == 3)
    # intermediate_home = (urban_typology_home == 2)

    # urban_work = (urban_typology_work == 1)
    # rural_work = (urban_typology_work == 3)
    intermediate_work = (urban_typology_work == 2)

    home_work_distance = (home_work_crow_fly_distance * (home_work_crow_fly_distance >= 0.0) / 100000.0)
    home_work_distance_zero = home_work_crow_fly_distance == 0.0

    # employees = work_position == 2
    executives = work_position == 1

    german = language == 1

    hh_income_less_than_2000 = hh_income == 1
    hh_income_2000_to_4000 = hh_income == 2
    hh_income_4001_to_6000 = hh_income == 3
    hh_income_6001_to_8000 = hh_income == 4

    owning_a_general_abo = GA_ticket == 1

    mobility_resource_car_half_fare_abo = mobility_resources == 2
    mobility_resource_general_abo_no_car = mobility_resources == 4

    #  Utility
    U = alternative_specific_constant + \
        b_executives * executives + \
        b_no_post_school_education * no_post_school_educ + \
        b_secondary_education * secondary_education + \
        b_tertiary_education * tertiary_education + \
        b_couple_without_children_2020 * couple_without_children + \
        b_home_work_distance * home_work_distance + \
        b_home_work_distance_zero * home_work_distance_zero + \
        models.piecewiseFormula(age, [15, 19, 31, 79, 85]) + \
        b_business_sector_retail * business_sector_retail + \
        b_business_sector_gastronomy * business_sector_gastronomy + \
        b_business_sector_finance * business_sector_finance + \
        b_business_sector_production * business_sector_production + \
        b_business_sector_wholesale * business_sector_wholesale + \
        b_business_sector_other_services * business_sector_other_services + \
        b_business_sector_others * business_sector_others + \
        b_business_sector_non_movers * business_sector_non_movers + \
        b_german * german + \
        models.piecewiseFormula(work_percentage, [0, 90, 101]) + \
        b_hh_income_8000_or_less * hh_income_less_than_2000 + \
        b_hh_income_8000_or_less * hh_income_2000_to_4000 + \
        b_hh_income_8000_or_less * hh_income_4001_to_6000 + \
        b_hh_income_8000_or_less * hh_income_6001_to_8000 + \
        b_owning_a_general_abo * owning_a_general_abo + \
        b_mobility_resource_car_half_fare_abo * mobility_resource_car_half_fare_abo + \
        b_intermediate_work_2020 * intermediate_work + \
        b_mobility_resource_general_abo_no_car_2020 * mobility_resource_general_abo_no_car
    U_no_telecommuting = 0

    # Associate utility functions with the numbering of alternatives
    V = {1: U,  # Yes or sometimes
         0: U_no_telecommuting}  # No

    av = {1: 1,
          0: 1}

    # The choice model is a logit, with availability conditions
    prob_telecommuting = models.logit(V, av, 1)
    prob_no_telecommuting = models.logit(V, av, 0)

    simulate = {'Prob. telecommuting': prob_telecommuting,
                'Prob. no telecommuting': prob_no_telecommuting}

    # Create the Biogeme object
    biogeme = bio.BIOGEME(database, simulate)
    biogeme.modelName = 'logit_telecommuting_simul'
    # Get the betas from the estimation
    if betas is None:
        if os.path.isfile(path_to_estimated_betas / (estimated_betas_name + '~00.pickle')):
            print('WARNING: There are several model outputs!')
        results = res.bioResults(pickleFile=path_to_estimated_betas / (estimated_betas_name + '.pickle'))
        betas = results.getBetaValues()

    # Change the working directory, so that biogeme writes in the correct folder, i.e., where this file is
    # standard_directory = os.getcwd()
    # os.chdir(output_directory_for_simulation)

    results = biogeme.simulate(theBetaValues=betas)
    # print(results.describe())
    df_persons = pd.concat([df_persons, results], axis=1)

    # Go back to the normal working directory
    # os.chdir(standard_directory)

    ''' Save the file '''
    df_persons.to_csv(output_directory_for_simulation / output_file_name, sep=',', index=False)


def apply_model_2015_to_microcensus(data_file_directory_for_simulation, data_file_name_for_simulation,
                                    output_directory_for_simulation, output_file_name,
                                    path_to_estimated_betas, estimated_betas_name, betas=None):
    """
    :author: Antonin Danalet, based on the example '01logit_simul.py' by Michel Bierlaire, EPFL, on biogeme.epfl.ch

    Simulation with a binary logit model. Two alternatives: work from home at least some times, or not."""

    # Read the data
    df_persons = pd.read_csv(data_file_directory_for_simulation / data_file_name_for_simulation, sep=';')
    database = db.Database('persons', df_persons)

    # The following statement allows you to use the names of the variable as Python variable.
    globals().update(database.variables)

    # Parameters to be estimated
    alternative_specific_constant = Beta('alternative_specific_constant', 0, None, None, 0)

    b_no_post_school_education = Beta('b_no_post_school_education', 0, None, None, 0)
    b_secondary_education = Beta('b_secondary_education', 0, None, None, 0)
    b_tertiary_education = Beta('b_tertiary_education', 0, None, None, 0)

    b_couple_without_children = Beta('b_couple_without_children', 0, None, None, 0)

    b_public_transport_connection_quality_are_na_home = Beta('b_public_transport_connection_quality_are_na_home',
                                                             0, None, None, 0)

    b_home_work_distance = Beta('b_home_work_distance', 0, None, None, 0)
    b_home_work_distance_zero = Beta('b_home_work_distance_zero', 0, None, None, 0)

    b_business_sector_production = Beta('b_business_sector_production', 0, None, None, 0)
    b_business_sector_wholesale = Beta('b_business_sector_wholesale', 0, None, None, 0)
    b_business_sector_retail = Beta('b_business_sector_retail', 0, None, None, 0)
    b_business_sector_gastronomy = Beta('b_business_sector_gastronomy', 0, None, None, 0)
    b_business_sector_finance = Beta('b_business_sector_finance', 0, None, None, 0)
    b_business_sector_other_services = Beta('b_business_sector_other_services', 0, None, None, 0)
    b_business_sector_others = Beta('b_business_sector_others', 0, None, None, 0)
    b_business_sector_non_movers = Beta('b_business_sector_non_movers', 0, None, None, 0)
    b_executives = Beta('b_executives', 0, None, None, 0)
    b_german = Beta('b_german', 0, None, None, 0)
    b_hh_income_8000_or_less = Beta('b_hh_income_8000_or_less', 0, None, None, 0)

    b_general_abo = Beta('b_general_abo', 0, None, None, 0)

    b_mobility_resource_car_half_fare_abo = Beta('b_mobility_resource_car_half_fare_abo', 0, None, None, 0)

    ''' Definition of new variables '''
    # male = (sex == 1)

    # single_household = (hh_type == 10)
    couple_without_children = (hh_type == 210)
    # couple_with_children = (hh_type == 220)
    # single_parent_with_children = (hh_type == 230)
    # not_family_household = (hh_type == 30)

    # public_transport_connection_quality_ARE_A_home = (public_transport_connection_quality_ARE_home == 1)
    # public_transport_connection_quality_ARE_B_home = (public_transport_connection_quality_ARE_home == 2)
    # public_transport_connection_quality_ARE_C_home = (public_transport_connection_quality_ARE_home == 3)
    # public_transport_connection_quality_ARE_D_home = (public_transport_connection_quality_ARE_home == 4)
    public_transport_connection_quality_ARE_NA_home = (public_transport_connection_quality_ARE_home == 5)

    # public_transport_connection_quality_ARE_A_work = (public_transport_connection_quality_ARE_work == 1)
    # public_transport_connection_quality_ARE_B_work = (public_transport_connection_quality_ARE_work == 2)
    # public_transport_connection_quality_ARE_C_work = (public_transport_connection_quality_ARE_work == 3)
    # public_transport_connection_quality_ARE_D_work = (public_transport_connection_quality_ARE_work == 4)
    # public_transport_connection_quality_ARE_NA_work = (public_transport_connection_quality_ARE_work == 5)

    # urban_home = (urban_typology_home == 1)
    # rural_home = (urban_typology_work == 3)
    # intermediate_home = (urban_typology_home == 2)

    # urban_work = (urban_typology_work == 1)
    # rural_work = (urban_typology_work == 3)
    # intermediate_work = (urban_typology_work == 2)

    home_work_distance = (home_work_crow_fly_distance * (home_work_crow_fly_distance >= 0.0) / 100000.0)
    home_work_distance_zero = home_work_crow_fly_distance == 0.0

    # employees = work_position == 2
    executives = work_position == 1

    german = language == 1

    # nationality_switzerland = nation == 8100
    # nationality_germany_austria_lichtenstein = (nation == 8207) + (nation == 8229) + (nation == 8222)
    # nationality_italy_vatican = (nation == 8218) + (nation == 8241)
    # nationality_france_monaco_san_marino = (nation == 8212) + (nation == 8226) + (nation == 8233)
    # nationality_northwestern_europe = (nation == 8204) + (nation == 8223) + (nation == 8227) + (nation == 8206) + \
    #                                   (nation == 8211) + (nation == 8215) + (nation == 8216) + (nation == 8217) + \
    #                                   (nation == 8228) + (nation == 8234)
    # nationality_south_west_europe = (nation == 8231) + (nation == 8236) + (nation == 8202)
    # nationality_southeast_europe = (nation == 8224) + (nation == 8201) + (nation == 8214) + (nation == 8256) + \
    #                                (nation == 8250) + (nation == 8251) + (nation == 8252) + (nation == 8255) + \
    #                                (nation == 8205) + (nation == 8239) + (nation == 8242) + (nation == 8248) + \
    #                                (nation == 8254)
    # nationality_eastern_europe = (nation == 8230) + (nation == 8232) + (nation == 8240) + (nation == 8243) + \
    #                              (nation == 8244) + (nation == 8263) + (nation == 8265) + (nation == 8266) + \
    #                              (nation == 8260) + (nation == 8261) + (nation == 8262)

    # several_part_time_jobs = full_part_time_job == 3

    hh_income_less_than_2000 = hh_income == 1
    hh_income_2000_to_4000 = hh_income == 2
    hh_income_4001_to_6000 = hh_income == 3
    hh_income_6001_to_8000 = hh_income == 4
    # hh_income_8001_to_10000 = hh_income == 5
    # hh_income_10001_to_12000 = hh_income == 6
    # hh_income_12001_to_14000 = hh_income == 7
    # hh_income_14001_to_16000 = hh_income == 8
    # hh_income_more_than_16000 = hh_income == 9

    general_abo = GA_ticket == 1

    mobility_resource_car_half_fare_abo = mobility_resources == 2

    #  Utility
    U = alternative_specific_constant + \
        b_executives * executives + \
        b_no_post_school_education * no_post_school_educ + \
        b_secondary_education * secondary_education + \
        b_tertiary_education * tertiary_education + \
        b_couple_without_children * couple_without_children + \
        b_public_transport_connection_quality_are_na_home * public_transport_connection_quality_ARE_NA_home + \
        b_home_work_distance * home_work_distance + \
        b_home_work_distance_zero * home_work_distance_zero + \
        models.piecewiseFormula(age, [15, 19, 31, 79, 86]) + \
        b_business_sector_retail * business_sector_retail + \
        b_business_sector_gastronomy * business_sector_gastronomy + \
        b_business_sector_finance * business_sector_finance + \
        b_business_sector_production * business_sector_production + \
        b_business_sector_wholesale * business_sector_wholesale + \
        b_business_sector_other_services * business_sector_other_services + \
        b_business_sector_others * business_sector_others + \
        b_business_sector_non_movers * business_sector_non_movers + \
        b_german * german + \
        models.piecewiseFormula(work_percentage, [0, 90, 101]) + \
        b_hh_income_8000_or_less * hh_income_less_than_2000 + \
        b_hh_income_8000_or_less * hh_income_2000_to_4000 + \
        b_hh_income_8000_or_less * hh_income_4001_to_6000 + \
        b_hh_income_8000_or_less * hh_income_6001_to_8000 + \
        b_general_abo * general_abo + \
        b_mobility_resource_car_half_fare_abo * mobility_resource_car_half_fare_abo
    U_no_telecommuting = 0

    # Associate utility functions with the numbering of alternatives
    V = {1: U,  # Yes or sometimes
         0: U_no_telecommuting}  # No

    av = {1: 1,
          0: 1}

    # The choice model is a logit, with availability conditions
    prob_telecommuting = models.logit(V, av, 1)
    prob_no_telecommuting = models.logit(V, av, 0)

    simulate = {'Prob. telecommuting': prob_telecommuting,
                'Prob. no telecommuting': prob_no_telecommuting}

    # Create the Biogeme object
    biogeme = bio.BIOGEME(database, simulate)
    biogeme.modelName = 'logit_telecommuting_simul'
    # Get the betas from the estimation
    if betas is None:
        if os.path.isfile(path_to_estimated_betas / (estimated_betas_name + '~00.pickle')):
            print('WARNING: There are several model outputs!')
        results = res.bioResults(pickleFile=path_to_estimated_betas / (estimated_betas_name + '.pickle'))
        betas = results.getBetaValues()

    # Change the working directory, so that biogeme writes in the correct folder, i.e., where this file is
    # standard_directory = os.getcwd()
    # os.chdir(output_directory_for_simulation)

    results = biogeme.simulate(theBetaValues=betas)
    # print(results.describe())
    df_persons = pd.concat([df_persons, results], axis=1)

    # Go back to the normal working directory
    # os.chdir(standard_directory)

    ''' Save the file '''
    df_persons.to_csv(output_directory_for_simulation / output_file_name, sep=',', index=False)
